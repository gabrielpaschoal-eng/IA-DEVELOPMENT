"""Shared logic for the spec-guard guardrail.

Imported by both the local PreToolUse hook (guard_spec_required.py) and the
CI check (scripts/check_spec_guard.py) so the rule is defined exactly once.
"""

import datetime
import json
import os
import re
import subprocess
from pathlib import Path

IMPLEMENTATION_DIR_RE = re.compile(r"^apps/[^/]+/(src|internal|cmd|pkg)/")
EXEMPT_FILE_RE = re.compile(r"(^|/)(tests?/|test_.*\.py$|.*_test\.go$|.*\.mdx?$)")


def repo_root(explicit=None):
    if explicit:
        return Path(explicit)
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env)
    return Path.cwd()


def is_implementation_path(rel_path):
    rel_path = rel_path.replace(os.sep, "/")
    return bool(IMPLEMENTATION_DIR_RE.match(rel_path))


def is_exempt_path(rel_path):
    rel_path = rel_path.replace(os.sep, "/")
    return bool(EXEMPT_FILE_RE.search(rel_path))


def current_branch(root):
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )
        return out.stdout.strip()
    except (subprocess.CalledProcessError, OSError):
        return None


def load_active_spec(root):
    state_path = root / ".claude" / "state" / "active-spec.json"
    if not state_path.exists():
        return None
    try:
        return json.loads(state_path.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def spec_task_status(root, slug):
    tasks_path = root / "specs" / slug / "03-tasks.md"
    if not tasks_path.exists():
        return None
    text = tasks_path.read_text()
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    frontmatter = text[3:end]
    match = re.search(r"^status:\s*(\S+)", frontmatter, re.MULTILINE)
    return match.group(1) if match else None


def check_bypass(root):
    """Returns a reason string if a live, unexpired local bypass exists."""
    bypass_path = root / ".claude" / "state" / "bypass.json"
    if not bypass_path.exists():
        return None
    try:
        data = json.loads(bypass_path.read_text())
    except (json.JSONDecodeError, OSError):
        return None
    expires_at = data.get("expires_at")
    if not expires_at:
        return None
    try:
        expiry = datetime.datetime.fromisoformat(expires_at)
    except ValueError:
        return None
    now = (
        datetime.datetime.now(expiry.tzinfo)
        if expiry.tzinfo
        else datetime.datetime.now()
    )
    if now < expiry:
        return data.get("reason", "bypass active")
    return None


def evaluate(root, rel_path):
    """Returns None if the write is allowed, or a block reason string."""
    if not is_implementation_path(rel_path):
        return None
    if is_exempt_path(rel_path):
        return None
    if check_bypass(root):
        return None

    active = load_active_spec(root)
    if not active:
        return (
            "No active spec. Run /specify -> /plan -> /tasks before editing "
            f"implementation code ({rel_path})."
        )

    branch = current_branch(root)
    active_branch = active.get("branch")
    if branch and active_branch and branch != active_branch:
        return (
            f"Active spec '{active.get('slug')}' was activated on branch "
            f"'{active_branch}', but the current branch is '{branch}'. "
            "Run /tasks again on this branch."
        )

    status = spec_task_status(root, active.get("slug", ""))
    if status != "active":
        return (
            f"Spec '{active.get('slug')}' has status '{status}', not 'active'. "
            "Run /tasks to activate it, or /review if it's already done."
        )

    return None

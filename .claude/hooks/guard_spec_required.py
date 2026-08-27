#!/usr/bin/env python3
"""PreToolUse guardrail: block Write/Edit on implementation code without an
active spec. See docs/sdd-workflow.md#guardrails.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _spec_guard_lib import evaluate, repo_root  # noqa: E402


def main():
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    tool_input = payload.get("tool_input", {})
    file_path = tool_input.get("file_path")
    if not file_path:
        return 0

    root = repo_root(payload.get("cwd"))
    try:
        rel_path = str(Path(file_path).resolve().relative_to(root.resolve()))
    except ValueError:
        return 0

    reason = evaluate(root, rel_path)
    if reason:
        print(reason, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

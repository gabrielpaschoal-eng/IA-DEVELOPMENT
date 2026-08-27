#!/usr/bin/env python3
"""PreToolUse guardrail: hard-block destructive bash commands as a backstop.

No bypass file by design. See docs/sdd-workflow.md#guardrails.
"""

import json
import re
import sys

DENYLIST = [
    (re.compile(r"\brm\s+(-\w*r\w*f\w*|-\w*f\w*r\w*)\s"), "rm -rf (or equivalent)"),
    (re.compile(r"\bgit\s+push\s+.*--force\b"), "git push --force"),
    (re.compile(r"\bgit\s+push\s+.*-f\b"), "git push -f"),
    (re.compile(r"\bgit\s+reset\s+--hard\b"), "git reset --hard"),
    (re.compile(r"\bgit\s+clean\s+.*-\w*f\w*d?\w*"), "git clean -f"),
    (re.compile(r"\bdrop\s+table\b", re.IGNORECASE), "DROP TABLE"),
    (re.compile(r"\btruncate\s+table\b", re.IGNORECASE), "TRUNCATE TABLE"),
    (re.compile(r"\bterraform\s+destroy\b"), "terraform destroy"),
    (re.compile(r"\bkubectl\s+delete\b"), "kubectl delete"),
]


def main():
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    command = payload.get("tool_input", {}).get("command", "")
    if not command:
        return 0

    for pattern, label in DENYLIST:
        if pattern.search(command):
            print(
                f"Blocked by guardrail: command matches denylisted pattern '{label}'.\n"
                "If this is genuinely intended, run it manually outside Claude Code, "
                "or comment out this hook in .claude/settings.local.json.",
                file=sys.stderr,
            )
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""CI mirror of the local spec-guard hook. Exits non-zero if a PR touches
implementation code without a corresponding active/approved spec.

Usage: check_spec_guard.py --base <base-ref> --head <head-ref> [--exempt "reason"]
"""

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / ".claude" / "hooks"))
from _spec_guard_lib import is_exempt_path, is_implementation_path, spec_task_status  # noqa: E402


def changed_files(base, head):
    out = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...{head}"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line.strip() for line in out.stdout.splitlines() if line.strip()]


def slugs_from_tasks_files(files):
    slugs = set()
    for f in files:
        parts = Path(f).parts
        if len(parts) >= 3 and parts[0] == "specs" and parts[-1] == "03-tasks.md":
            slugs.add(parts[1])
    return slugs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--exempt", default="")
    args = parser.parse_args()

    if args.exempt:
        print(f"spec-guard: exempted ({args.exempt})")
        return 0

    root = Path.cwd()
    files = changed_files(args.base, args.head)
    impl_files = [f for f in files if is_implementation_path(f) and not is_exempt_path(f)]
    if not impl_files:
        print("spec-guard: no implementation-path changes, nothing to check.")
        return 0

    touched_slugs = slugs_from_tasks_files(files)
    if not touched_slugs:
        print(
            "spec-guard: implementation code changed but no specs/<slug>/03-tasks.md "
            "was touched in this diff:\n  " + "\n  ".join(impl_files),
            file=sys.stderr,
        )
        return 1

    ok_slugs = {s for s in touched_slugs if spec_task_status(root, s) in ("active", "approved")}
    if not ok_slugs:
        print(
            "spec-guard: 03-tasks.md was touched but none have status 'active' or "
            "'approved'. Slugs seen: " + ", ".join(sorted(touched_slugs)),
            file=sys.stderr,
        )
        return 1

    print(f"spec-guard: OK, backed by spec(s): {', '.join(sorted(ok_slugs))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

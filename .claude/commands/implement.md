---
description: Implement the active spec's tasks
---

1. Read `.claude/state/active-spec.json` to find the active slug; if missing, tell the user to run `/tasks` first.
2. Read `specs/<slug>/03-tasks.md`. For each unchecked task, implement it, then check it off.
3. Use Serena's symbol-level tools (`find_symbol`, `replace_symbol_body`, etc.) for existing source files rather than reading them whole — see CLAUDE.md.
4. Run the relevant linter/tests for the language you touched (`ruff`/`pytest` or `golangci-lint`/`go test`) before checking a task off.
5. When all tasks are checked, tell the user to run `/review`.

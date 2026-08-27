---
description: Break the plan into a task checklist and activate the spec
---

Read docs/sdd-workflow.md if you have not already this session.

1. Read `specs/<slug>/02-plan.md`.
2. Write `specs/<slug>/03-tasks.md` as a checklist of small, independently verifiable tasks with acceptance criteria. Set frontmatter `status: active`.
3. Write `.claude/state/active-spec.json` with `{"slug": "<slug>", "branch": "<current git branch>", "updated_at": "<current ISO timestamp>"}` — this is what unblocks the implementation guardrail hook.
4. Tell the user implementation can now proceed with `/implement`.

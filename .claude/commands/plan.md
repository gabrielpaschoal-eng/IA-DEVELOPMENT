---
description: Turn an agreed spec into a technical plan
---

Read docs/sdd-workflow.md if you have not already this session.

1. Read `specs/<slug>/01-spec.md`. If it doesn't exist or looks unfinished, tell the user to run `/specify` first.
2. Propose a technical approach in `specs/<slug>/02-plan.md`: chosen approach, alternatives considered, modules/files touched, risks.
3. For Python/Go implementation work, prefer scaffolding from `templates/python-app/` or `templates/go-app/` over inventing new structure.
4. Confirm the plan with the user before moving to `/tasks`.

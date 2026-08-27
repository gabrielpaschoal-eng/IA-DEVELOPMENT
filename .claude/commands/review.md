---
description: Close out a spec after implementation
---

1. Read `.claude/state/active-spec.json` for the active slug.
2. Write `specs/<slug>/04-review.md`: what shipped, deviations from `01-spec.md`/`02-plan.md`, follow-ups.
3. Flip `specs/<slug>/03-tasks.md` frontmatter to `status: approved`.
4. Delete `.claude/state/active-spec.json` (clears the guardrail).

---
description: Start or continue the intent + spec stages for a feature
---

Read docs/sdd-workflow.md if you have not already this session.

Given the user's feature request:

1. Determine a short kebab-case slug for it.
2. If `specs/<slug>/` doesn't exist, create it by copying `specs/_TEMPLATE/`.
3. Fill in `00-intent.md` through a short dialogue with the user (problem, why now, success criteria, out of scope).
4. Once intent is agreed, fill in `01-spec.md` (requirements, non-goals, interfaces, constraints). Ask the user clarifying questions for anything genuinely ambiguous instead of guessing.
5. Stop after `01-spec.md` — do not proceed to `/plan` automatically.

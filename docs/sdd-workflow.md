# SDD Workflow

## Why staged files instead of one spec doc

Each stage is its own file so an agent (or a human) only has to load the stage it's working on, not the full history of a feature. `01-spec.md` shouldn't need `02-plan.md`'s content in context, and vice versa — this is the main token-optimization lever for the spec side (Serena, see [CLAUDE.md](../CLAUDE.md), is the lever for the code side).

## Stages

| File | Written by | Contains |
|---|---|---|
| `00-intent.md` | `/specify` | Problem, why now, success criteria, out of scope |
| `01-spec.md` | `/specify` | Requirements, non-goals, interfaces/contracts, constraints |
| `02-plan.md` | `/plan` | Chosen approach, alternatives considered, modules touched, risks |
| `03-tasks.md` | `/tasks` | Checklist with acceptance criteria; YAML frontmatter `status: draft\|active\|approved` |
| `04-review.md` | `/review` | What shipped, deviations from spec, follow-ups |

Start a new feature by copying `specs/_TEMPLATE/` to `specs/<slug>/` (the `/specify` command does this for you).

## State machine

`03-tasks.md`'s frontmatter `status` field is the source of truth for a spec's lifecycle:

```
draft --(/tasks)--> active --(/review)--> approved
```

`/tasks` also writes `.claude/state/active-spec.json` (gitignored, machine-local):

```json
{"slug": "my-feature", "branch": "feat/my-feature", "updated_at": "2026-08-27T12:00:00Z"}
```

## Guardrails

Two enforcement points, one rule, single source of truth (`.claude/hooks/_spec_guard_lib.py`, imported by both):

1. **Local hook** (`.claude/hooks/guard_spec_required.py`, a `PreToolUse` hook on `Write`/`Edit`): blocks writes under `apps/**/(src|internal|cmd|pkg)/**` unless `.claude/state/active-spec.json` exists, its `branch` matches the current git branch, and the referenced spec's `03-tasks.md` has `status: active`.
2. **CI** (`.github/workflows/spec-guard.yml` → `scripts/check_spec_guard.py`): on every PR, fails if implementation-path files changed without a corresponding `specs/<slug>/03-tasks.md` (status `active` or `approved`) also changing in the same diff. This exists so the rule can't be bypassed by disabling the local hook — CI is the real enforcement, the hook is a fast local warning.

A second hook, `guard_destructive_bash.py`, hard-blocks a fixed denylist of destructive bash patterns (`rm -rf`, `git push --force`, `git reset --hard`, `DROP TABLE`, `terraform destroy`, `kubectl delete`, ...) regardless of spec state. This has no bypass file by design — if you genuinely need to run one of these, do it outside Claude Code, or comment out the hook in `.claude/settings.local.json` (a visible, deliberate, gitignored action, not a silent flag).

### Exemptions

Both enforcement points treat these as exempt (no spec required): anything under `tests/`, `test_*.py`, `*_test.go`, and `*.md`/`*.mdx` files. CI additionally accepts:

- PR label `no-spec-needed`
- A `Spec-Exempt: <reason>` line in the PR description

### Emergency bypass (local hook only)

Create `.claude/state/bypass.json` (gitignored):

```json
{"reason": "hotfix for incident INC-1234", "expires_at": "2026-08-28T00:00:00Z"}
```

The local hook honors this until `expires_at`. CI does **not** honor it — a real PR still needs a real exemption. Delete the file once the emergency is over.

## Why `apps/` vs `templates/`

`templates/python-app/` and `templates/go-app/` are scaffolds — copy one into `apps/<name>/` and rename the module/package when starting a real app. They also double as the smoke-test target for `ci-python.yml`/`ci-go.yml` in this template repo itself, since there's nothing under `apps/` yet in a freshly generated repo.

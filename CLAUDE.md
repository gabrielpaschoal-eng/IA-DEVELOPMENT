# Project

Template repository for Spec-Driven Development (SDD) with Claude Code. Apps live under `apps/`, scaffolded from `templates/`.

## Workflow — Spec-Driven Development

Every feature is developed through staged spec files in `specs/<slug>/`:
`00-intent.md` → `01-spec.md` → `02-plan.md` → `03-tasks.md` → `04-review.md`

Drive it with the slash commands: `/specify`, `/plan`, `/tasks`, `/implement`, `/review`.
Full methodology, state machine, and escape hatch: see [docs/sdd-workflow.md](docs/sdd-workflow.md) — read it before running these commands for the first time in a session.

**Do not write implementation code under `apps/**` without an active spec.** A guardrail hook enforces this (see below); the fix if it blocks you is to run `/specify` → `/plan` → `/tasks` first, not to bypass it.

## Code navigation — use Serena, not raw reads

This repo registers the [Serena](https://github.com/oraios/serena) MCP server (`.mcp.json`). For any Python or Go source file over ~200 lines, prefer Serena's `find_symbol`, `find_referencing_symbols`, and `replace_symbol_body` over `Read`/`grep`/full-file `Edit` — it's far cheaper in tokens. Reserve `Read` for specs, docs, configs, and short files.

## Stack

- Python apps: `uv`, `ruff`, `pytest` — scaffold in `templates/python-app/`
- Go apps: Go modules, `golangci-lint`, `go test` — scaffold in `templates/go-app/`
- New app = copy a `templates/*` folder into `apps/<name>/` and rename the module/package.

## Guardrails

`.claude/hooks/` blocks (a) implementation writes without an active spec, (b) destructive bash (force-push, `rm -rf`, `reset --hard`, etc.). The same rule is enforced again in CI (`spec-guard.yml`) so it can't be bypassed by disabling local hooks. Details: [docs/sdd-workflow.md](docs/sdd-workflow.md#guardrails).

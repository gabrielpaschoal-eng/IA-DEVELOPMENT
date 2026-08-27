# SDD Template

A GitHub template repository for Spec-Driven Development (SDD) with Claude Code, for Python and Go apps.

## What's here

- **`specs/`** — every feature goes through a staged spec (`00-intent` → `01-spec` → `02-plan` → `03-tasks` → `04-review`) before code is written. See [docs/sdd-workflow.md](docs/sdd-workflow.md).
- **`.claude/`** — custom slash commands (`/specify /plan /tasks /implement /review`) and guardrail hooks that block implementation writes without an active spec, and block destructive bash commands.
- **`templates/python-app/`, `templates/go-app/`** — scaffolds to copy into `apps/<name>/` when starting a real app. Not meant to be run in place.
- **`apps/`** — where real apps live once instantiated from `templates/`.
- **`.github/workflows/`** — `ci-python.yml` / `ci-go.yml` (auto-discover and test any app under `apps/` or the templates), `spec-guard.yml` (CI-side mirror of the local guardrail hook, so it can't be bypassed by disabling hooks locally), `template-init.yml` (one-time cleanup on a repo generated from this template).

## Using this as a GitHub template

1. Push this repo to GitHub.
2. Repo → Settings → General → check **Template repository**. (This is a manual GitHub setting; it can't be done from the filesystem.)
3. Edit `.github/workflows/template-init.yml`: replace `YOUR_ORG/YOUR_TEMPLATE_REPO_NAME` with this repo's own `owner/name`, so the cleanup workflow only runs on repos *generated from* the template, not the template itself.
4. Anyone can now click "Use this template" on GitHub to start a new project from it.

## Setup

```bash
bash scripts/bootstrap.sh   # installs uv, Serena, pre-commit
```

Serena ([github.com/oraios/serena](https://github.com/oraios/serena)) is registered as an MCP server in `.mcp.json` and gives Claude Code symbol-level code navigation (`find_symbol`, `replace_symbol_body`, ...) instead of full-file reads — this is the main token-optimization lever for larger Python/Go files. **Pin the `serena-agent` version** in `scripts/bootstrap.sh` and `.devcontainer/devcontainer.json` once you've tested one — it's left unpinned here since versions move quickly; check the releases page.

## SDD workflow, in short

```
/specify   -> specs/<slug>/00-intent.md, 01-spec.md
/plan      -> specs/<slug>/02-plan.md
/tasks     -> specs/<slug>/03-tasks.md (status: active), activates the guardrail
/implement -> writes code, checks tasks off
/review    -> specs/<slug>/04-review.md, status: approved, clears the guardrail
```

Full detail, including the state machine and emergency bypass: [docs/sdd-workflow.md](docs/sdd-workflow.md).

## Notes on choices made

- No `LICENSE` file — assumed internal/proprietary use. Add one if this becomes open source.
- `CODEOWNERS` is a commented-out placeholder — fill in real handles/teams before relying on it for branch protection.
- `template-init.yml` pushes a commit from CI; if your org restricts Actions from pushing to `main`, either enable that permission for the workflow or delete it and rename placeholders manually.

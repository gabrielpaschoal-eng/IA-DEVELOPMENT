#!/usr/bin/env bash
set -euo pipefail

echo "==> Installing uv (Python package/tool manager)"
if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# TODO: pin to a tested version, e.g. `uv tool install serena-agent==X.Y.Z`.
# Left unpinned here since Serena moves quickly — check github.com/oraios/serena/releases.
echo "==> Installing Serena as an MCP server"
uv tool install -p 3.13 serena-agent
serena setup claude-code || echo "Run 'serena setup claude-code' manually if this failed."

echo "==> Installing pre-commit"
uv tool install pre-commit
pre-commit install

echo "==> Done. Verify with: claude mcp list"

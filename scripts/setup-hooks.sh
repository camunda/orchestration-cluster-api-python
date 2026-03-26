#!/usr/bin/env bash
# Install a git pre-push hook that runs lint + type-check before pushing.
# Uses the same ruff/pyright versions as CI (via `uv run`).
# Re-run this script at any time to reinstall the hook.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
HOOK_FILE="$REPO_ROOT/.git/hooks/pre-push"

cat > "$HOOK_FILE" << 'HOOK'
#!/usr/bin/env bash
set -euo pipefail

echo "pre-push: running lint + type-check…"
make -C "$(git rev-parse --show-toplevel)" check
echo "pre-push: all checks passed."
HOOK

chmod +x "$HOOK_FILE"
echo "Installed pre-push hook at $HOOK_FILE"

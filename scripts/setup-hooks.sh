#!/usr/bin/env bash
# Install a git pre-push hook that runs lint + type-check before pushing.
# Uses the same ruff/ty versions as CI (via `uv run`).
# Re-run this script at any time to reinstall the hook.

set -euo pipefail

# core.hooksPath (a hooks manager, a shared global dir, or /dev/null) is the user's to own.
if HOOKS_PATH="$(git config --get core.hooksPath)"; then
  echo "core.hooksPath is set ($HOOKS_PATH); not installing the pre-push hook."
  exit 0
fi

# --git-common-dir, not --show-toplevel: in a linked worktree .git is a file.
HOOKS_DIR="$(git rev-parse --path-format=absolute --git-common-dir)/hooks"
mkdir -p "$HOOKS_DIR"
HOOK_FILE="$HOOKS_DIR/pre-push"

cat > "$HOOK_FILE" << 'HOOK'
#!/usr/bin/env bash
set -euo pipefail

echo "pre-push: running lint + type-check…"
make -C "$(git rev-parse --show-toplevel)" check
echo "pre-push: all checks passed."
HOOK

chmod +x "$HOOK_FILE"
echo "Installed pre-push hook at $HOOK_FILE"

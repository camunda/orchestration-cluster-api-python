#!/usr/bin/env bash
# Smoke-test a built wheel the way a user installs it, before it is published (#389 R1).
#
# Usage: scripts/smoke-test-wheel.sh <path/to/wheel> [python-version ...]
#
# For each Python version, creates a clean virtualenv outside the repository, installs only
# the wheel and its runtime dependencies, and runs scripts/smoke_test_installed_sdk.py from a
# temporary directory, so the source tree cannot mask a packaging defect.
#
# Default versions: the wheel's own Requires-Python floor (read from its METADATA, so the gate
# follows the package rather than a copy of the number) and the newest interpreter the repo
# pins in .python-version.
set -euo pipefail

wheel="${1:?usage: $0 <wheel> [python-version ...]}"
shift
[[ -f "$wheel" ]] || { echo "SMOKE FAIL: no such wheel: $wheel" >&2; exit 1; }
wheel="$(cd "$(dirname "$wheel")" && pwd)/$(basename "$wheel")"
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
checker="$repo_root/scripts/smoke_test_installed_sdk.py"

if [[ $# -gt 0 ]]; then
  versions=("$@")
else
  requires_python="$(unzip -p "$wheel" '*.dist-info/METADATA' | sed -n 's/^Requires-Python: *//p')"
  floor="$(sed -nE 's/^>= *([0-9]+\.[0-9]+).*/\1/p' <<<"$requires_python")"
  if [[ -z "$floor" ]]; then
    echo "SMOKE FAIL: cannot read a '>=X.Y' floor from Requires-Python '$requires_python'" >&2
    exit 1
  fi
  newest="$(tr -d '[:space:]' < "$repo_root/.python-version")"
  versions=("$floor")
  [[ "$newest" != "$floor" ]] && versions+=("$newest")
  echo "Requires-Python: $requires_python -> testing on ${versions[*]}"
fi

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

for version in "${versions[@]}"; do
  echo "::group::smoke test on Python $version"
  venv="$work/venv-$version"
  # --no-config and --no-project: nothing from the repository's uv settings or project applies.
  uv venv --quiet --no-config --no-project --python "$version" "$venv"
  uv pip install --quiet --no-config --python "$venv/bin/python" "$wheel"
  (cd "$work" && "$venv/bin/python" "$checker")
  echo "::endgroup::"
done

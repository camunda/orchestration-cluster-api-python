#!/usr/bin/env bash
# Release gate for stable/<major>: compare the public API at HEAD (generated/) with the
# newest release of the major on PyPI, and fail unless any break is approved.
#
# Called by the "API compatibility gate" step of .github/workflows/publish.yml, and again
# by scripts/semantic-release-with-retry.sh after it resets to a newer branch tip, so the
# commit that gets released is always the commit that was checked.
#
# Approval: the api-break-approved label on a PR merged into <branch> since that release
# (scripts/api-break-approvals.sh), or DISPATCH_APPROVED=true (the api_break_approved
# input of a manual run). A label approves the API as of that PR's merge: breaks added
# after the newest approved merge need their own approval.
# Needs GH_TOKEN and GITHUB_REPOSITORY. Exit codes: 0 pass, 1 blocked, 2 setup error.
set -uo pipefail

here=$(dirname "$0")
BRANCH="${1:?usage: api-compat-gate.sh <branch>}"
major="${BRANCH#stable/}"
# The newest published release of this stable major, not the nearest tag: a stable
# branch is cut from main at a prerelease.
version=$(uv run python scripts/api_compat.py --print-baseline-major "$major") || exit 2
if [ -z "$version" ]; then
  echo "::notice::No ${major}.x release published yet; nothing to compare against."
  exit 0
fi
tag="v${version}"
git rev-parse -q --verify "refs/tags/${tag}" >/dev/null || {
  echo "::error::Baseline ${version} has no ${tag} tag to list the PRs merged since."
  exit 2
}
echo "Baseline: ${tag} (checking $(git rev-parse --short HEAD))"
rc=0
uv run python scripts/api_compat.py --baseline-version "$version" || rc=$?
[ "$rc" -eq 1 ] || exit "$rc"
if [ "${DISPATCH_APPROVED:-false}" = "true" ]; then
  echo "::warning::Breaking API changes approved by the api_break_approved input of this run."
  exit 0
fi
approved=$("$here/api-break-approvals.sh" "$tag" "$BRANCH") || {
  echo "::error::cannot list the approved PRs merged since ${tag}."
  exit 2
}
if [ -z "$approved" ]; then
  echo "::error::Release blocked: the public API breaks compatibility with ${tag}. If intended, label the PR that made the change api-break-approved (or re-run this workflow manually with api_break_approved), then re-run."
  exit 1
fi
prs=$(cut -d' ' -f1 <<<"$approved" | xargs)
read -r latest_pr latest <<<"$approved"
if [ "$latest" != "$(git rev-parse HEAD)" ]; then
  dir=$(mktemp -d)
  trap 'git worktree remove --force "$dir" >/dev/null 2>&1; rm -rf "$dir"' EXIT
  git worktree add -q --detach "$dir" "$latest" || exit 2
  # From that commit's own spec and generator, so only later changes show up.
  make -C "$dir" generate-only >/dev/null || {
    echo "::error::cannot generate the SDK at ${latest}."
    exit 2
  }
  rc=0
  uv run python scripts/api_compat.py --baseline-dir "$dir/generated" || rc=$?
  if [ "$rc" -eq 1 ]; then
    echo "::error::Release blocked: breaking API changes were added after ${latest_pr} (${latest}), the newest approved PR. Label the PR that made them api-break-approved (or re-run this workflow manually with api_break_approved), then re-run."
    exit 1
  fi
  [ "$rc" -eq 0 ] || exit "$rc"
fi
echo "::warning::Breaking API changes approved with the api-break-approved label on: ${prs}"

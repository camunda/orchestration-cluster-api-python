#!/usr/bin/env bash
# Release gate for stable/<major>: compare the public API at HEAD (generated/) with the
# newest release of the major on PyPI, and fail unless any break is approved.
#
# Called by the "API compatibility gate" step of .github/workflows/publish.yml, and again
# by scripts/semantic-release-with-retry.sh after it resets to a newer branch tip, so the
# commit that gets released is always the commit that was checked.
#
# Approval: the api-break-approved label on any PR merged since that release, or
# DISPATCH_APPROVED=true (the api_break_approved input of a manual run).
# Needs GH_TOKEN and GITHUB_REPOSITORY. Exit codes: 0 pass, 1 blocked, 2 setup error.
set -uo pipefail

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
shas=$(git log --format=%H "${tag}..HEAD") || {
  echo "::error::cannot list the commits since ${tag}."
  exit 2
}
approved=""
for sha in $shas; do
  prs=$(gh api "repos/${GITHUB_REPOSITORY}/commits/${sha}/pulls" \
    --jq '.[] | select(.merged_at != null) | select(any(.labels[]; .name == "api-break-approved")) | "#\(.number)"') || exit 2
  approved="${approved} ${prs}"
done
approved=$(echo "$approved" | xargs -n1 2>/dev/null | sort -u | xargs)
if [ -n "$approved" ]; then
  echo "::warning::Breaking API changes approved with the api-break-approved label on: ${approved}"
  exit 0
fi
echo "::error::Release blocked: the public API breaks compatibility with ${tag}. If intended, label the PR that made the change api-break-approved (or re-run this workflow manually with api_break_approved), then re-run."
exit 1

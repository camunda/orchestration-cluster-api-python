#!/usr/bin/env bash
# Fail if a release version does not belong on the given branch.
#
# Usage: check-stable-branch-version.sh <branch> <version>
#
# On `stable/<major>` branches the release version must be `<major>.x.y`: stable branches
# only get patch and minor releases, and a major bump (a BREAKING CHANGE footer) belongs on
# main. Any other branch is not constrained. Shared by the "Validate version matches stable
# branch" step of .github/workflows/publish.yml and scripts/semantic-release-with-retry.sh,
# so the same rule is enforced up front and again before every release attempt.
set -euo pipefail

BRANCH="${1:?usage: check-stable-branch-version.sh <branch> <version>}"
NEW_VERSION="${2:?usage: check-stable-branch-version.sh <branch> <version>}"

if [[ "$BRANCH" != stable/* ]]; then
  exit 0
fi

# Expected major from the branch name (e.g. stable/9 -> 9)
BRANCH_MAJOR="${BRANCH#stable/}"

if [[ ! "$NEW_VERSION" =~ ^${BRANCH_MAJOR}\. ]]; then
  echo "::error::Version $NEW_VERSION doesn't match branch constraint ${BRANCH_MAJOR}.x"
  echo "Stable branches should only receive patch and minor releases."
  echo "Use a BREAKING CHANGE footer on main to bump the major version."
  exit 1
fi

echo "Version $NEW_VERSION matches branch constraint ${BRANCH_MAJOR}.x"

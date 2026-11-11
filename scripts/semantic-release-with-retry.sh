#!/usr/bin/env bash
# Run `semantic-release version`, retrying (up to 3 attempts) only when it fails because
# another commit landed on the release branch while the release was running.
#
# Called by the "Create release" step of .github/workflows/publish.yml.
#
# `semantic-release version` commits `chore(release): X [skip ci]`, tags it, and pushes
# the commit and tag to the branch. It aborts ("Upstream branch has changed") or has its
# push rejected if the branch moved since checkout, as happens when a Renovate PR merges
# mid-release. Nothing is published at that point: the GitHub release is created only
# after the push succeeds, and PyPI publishing is a later workflow step. So it is safe to
# throw away the unpushed release commit and tag, move to the new branch tip, and run it
# again; semantic-release recomputes the next version from the tags on every run.
#
# We deliberately do not use `version --no-push`: in python-semantic-release it also
# disables creation of the GitHub release ("No vcs release will be created because
# pushing changes is disabled").
#
# Never force-pushes. Any other failure, or a race lost after the release commit was
# already pushed, fails immediately and loudly.
set -euo pipefail

BRANCH="${GITHUB_REF_NAME:-$(git rev-parse --abbrev-ref HEAD)}"
MAX_ATTEMPTS=3
LOG_DIR="${RUNNER_TEMP:-${TMPDIR:-/tmp}}"
# semantic-release's own check, plus git's wording for a rejected push, which varies by
# git version and code path.
RACE_RE='(upstream branch has changed|non-fast-forward|fetch first|stale info|rejected because|failed to update ref|\[rejected\])'

for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  echo "semantic-release version attempt ${attempt}/${MAX_ATTEMPTS}"

  # One log per attempt, so a retry does not overwrite the record of why the previous
  # attempt failed. Kept outside the work tree so semantic-release never sees them.
  LOG="${LOG_DIR}/semantic-release-attempt-${attempt}.out"

  set +e
  uv run semantic-release version 2>&1 | tee "$LOG"
  status=${PIPESTATUS[0]}
  set -e

  if [ "$status" -eq 0 ]; then
    exit 0
  fi

  if [ "$attempt" -eq "$MAX_ATTEMPTS" ]; then
    echo "::error::semantic-release version failed after ${attempt} attempt(s); giving up."
    exit "$status"
  fi

  if ! grep -qiE "$RACE_RE" "$LOG"; then
    echo "::error::semantic-release version failed for a reason other than a concurrent push; not retrying."
    exit "$status"
  fi

  failed_head=$(git rev-parse HEAD)
  git fetch origin "$BRANCH"

  # If the release commit already reached the remote, a retry would release it twice.
  if git merge-base --is-ancestor "$failed_head" "origin/${BRANCH}" &&
    [[ "$(git log -1 --format=%s "$failed_head")" == "chore(release):"* ]]; then
    echo "::error::the release commit is already on origin/${BRANCH}; not retrying."
    exit "$status"
  fi

  echo "Release on ${BRANCH} lost a race with a concurrent push; resetting to origin/${BRANCH} and retrying."
  # Drop the local tag(s) semantic-release created on the unpushed release commit, or the
  # retry could not recreate the same tag. Then restore any tag that does exist remotely.
  git tag --points-at "$failed_head" | xargs -r git tag -d
  git fetch origin --tags
  # Safe: the only local commit is the release commit semantic-release made and failed
  # to push; nothing depends on it.
  git reset --hard "origin/${BRANCH}"
  sleep 5
done

#!/usr/bin/env bash
# Rebase the current HEAD onto origin/<branch> and push it, retrying (up to 3 attempts)
# only when the push is rejected because another commit landed on the branch in the
# meantime (e.g. a Renovate PR merging while a release is running).
#
# Called by the "Commit generated changes" step of .github/workflows/publish.yml.
#
# Never force-pushes. A rebase conflict, or a push failure for any reason other than a
# non-fast-forward rejection, fails immediately and loudly.
set -euo pipefail

BRANCH="${GITHUB_REF_NAME:-$(git rev-parse --abbrev-ref HEAD)}"
MAX_ATTEMPTS=3
# git's wording for a lost push race varies by version and code path.
REJECTED_RE='(non-fast-forward|fetch first|stale info|rejected because|failed to update ref|\[rejected\])'

for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  echo "push attempt ${attempt}/${MAX_ATTEMPTS}"

  if ! git pull --rebase origin "$BRANCH"; then
    git rebase --abort 2>/dev/null || true
    echo "::error::git pull --rebase origin ${BRANCH} failed (conflict?); not pushing."
    exit 1
  fi

  set +e
  output=$(git push origin "HEAD:${BRANCH}" 2>&1)
  status=$?
  set -e
  echo "$output"

  if [ "$status" -eq 0 ]; then
    exit 0
  fi

  if ! grep -qiE "$REJECTED_RE" <<<"$output"; then
    echo "::error::git push failed for a reason other than a concurrent push; not retrying."
    exit "$status"
  fi

  if [ "$attempt" -eq "$MAX_ATTEMPTS" ]; then
    echo "::error::git push to ${BRANCH} still rejected after ${attempt} attempt(s); giving up."
    exit "$status"
  fi

  echo "Push to ${BRANCH} was rejected (a concurrent push landed); rebasing and retrying."
  sleep 5
done

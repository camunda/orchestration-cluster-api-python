# Release Process

This document describes the branching strategy, release streams, and publishing process for the Camunda Orchestration SDK for Python.

## Overview

The SDK follows a multi-stream release model:

| Branch | PyPI Index | Purpose |
|--------|------------|---------|
| `main` | `--pre` (dev) | Development stream, dev pre-releases |
| `stable/<major>` (current) | Default | Stable releases |
| `stable/<major>` (older) | Default | Maintenance releases |

## Branch Model

### `main` Branch

- **Purpose**: Active development targeting the next Camunda release
- **Publishes to**: PyPI as dev pre-releases (e.g., `11.0.0-dev.2`, `11.0.0-dev.3`)
- **Installation**: `pip install camunda-orchestration-sdk --pre`

### `stable/<major>` Branches

- **Purpose**: Stable/maintenance releases for specific SDK major versions
- **Examples**: `stable/9`, `stable/10`
- **Publishes to**: PyPI with version-specific releases
- **Installation**: `pip install "camunda-orchestration-sdk>=9.0.0,<10.0.0"`

SDK major version tracks Camunda server minor (server 8.9 → SDK 9.x, server 8.10 → SDK 10.x).

## Version Numbering

This SDK uses standard semantic versioning:

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `fix:`, `perf:`, `revert:` | Patch | `9.0.0` → `9.0.1` |
| `feat:` | Minor | `9.0.x` → `9.1.0` |
| `BREAKING CHANGE` footer | Major | `9.x.y` → `10.0.0` |

- `chore:`, `docs:`, `ci:`, `style:`, `refactor:`, `test:`, `build:` commits produce no release.

> **Important**: Use a `BREAKING CHANGE:` footer in the commit body — not the `feat!:` shorthand. The `!` convention may not be recognized depending on the parser version.

## Installation Guide

### Latest Stable Release (Recommended)

```bash
pip install camunda-orchestration-sdk
```

### Specific Version Line

Pin to a specific SDK major version:

```bash
# Pin to 9.x releases
pip install "camunda-orchestration-sdk>=9.0.0,<10.0.0"
```

### Dev Pre-releases

For testing upcoming features:

```bash
pip install camunda-orchestration-sdk --pre
```

## Release Workflows

### Automated Release (Main)

Triggered on push to `main`:

1. Run tests across Python versions
2. Generate SDK from OpenAPI spec
3. Commit any generated changes
4. Determine next version via semantic-release
5. Create version bump commit and git tag
6. Publish to PyPI (dev pre-release)
7. Create GitHub release

### Maintenance Release (Stable Branches)

Triggered on push to `stable/**`:

1. Run tests across Python versions
2. Generate SDK from OpenAPI spec
3. Commit any generated changes
4. Determine next version via semantic-release
5. Create version bump commit and git tag
6. Publish to PyPI
7. Create GitHub release

## Creating a New Stable Branch (Releasing a New Major Version)

When a new Camunda server minor ships (e.g. 8.11), the SDK bumps its major (e.g. 10 → 11). Follow these steps **in order**:

> **Why the extra merge?** PSR computes a stable version from the last full release in the branch's history. Stable releases are tagged on `stable/<N>`, so the previous line's releases are not reachable from `main`, and a branch cut from `main` alone computes from an old release (or one that already exists). Merging the previous line's latest release tag with `-s ours` changes no files but makes that release reachable; the `BREAKING CHANGE` commit then bumps it to the new major.

### 1. Create the Stable Branch and Trigger the First Release

```bash
git fetch origin --tags
git checkout -b stable/11 origin/main
# Latest full release of the previous line, e.g. v10.0.3
PREV=$(git tag --list 'v10.*' --sort=-v:refname | grep -v -- '-' | head -1)
git merge -s ours --no-ff -m "chore: record 10.x release history on stable/11" "$PREV"
# Point the SPEC_REF defaults (Makefile, generate.py, scripts/bundle-spec.sh,
# .github/workflows/*.yml) at stable/8.11, or use --allow-empty if they already do.
git commit -am "feat: release SDK 11 for Camunda server 8.11" \
  -m "BREAKING CHANGE: SDK major version bumped from 10 to 11 to track Camunda server 8.11"
uv run --group ci semantic-release --noop version --print   # must print 11.0.0
git push -u origin stable/11
```

CI runs automatically on push and publishes the first stable release (`11.0.0`), generated from the spec the release commit points at.

### 2. Stamp the Next Major on `main`

> **Why not a `BREAKING CHANGE` commit?** `python-semantic-release` does not apply major bumps on prerelease branches — it only increments the dev counter. You must manually stamp the version and tag. See MAINTAINER.md § 14 for details.

Open a PR that sets `version = "12.0.0-dev.1"` in `pyproject.toml` (run `uv lock` so `uv.lock` matches). Once it is merged, tag the commit on `main` that sets the version:

```bash
git fetch origin
git tag -a v12.0.0-dev.1 -m v12.0.0-dev.1 <commit>
git push origin v12.0.0-dev.1
```

`main` then publishes `12.0.0-dev.2` onward while `stable/11` publishes `11.x.y`.

Stamp `-dev.1`, not `-dev.0`: PSR reads a `-dev.0` tag as the full release `12.0.0` and fails looking for a `v12.0.0` tag.

### 3. Update Renovate

Add the new stable branch to [.github/renovate.json](.github/renovate.json): append it to `baseBranchPatterns` and mirror the patch-only `packageRules` entry for it. Dependency updates are handled by [Mend Renovate](https://docs.renovatebot.com/) (pip/uv and GitHub Actions are auto-detected); minor updates auto-merge on green CI, stable branches receive patch updates only.

> **Important**: PSR uses SemVer-style prerelease tags (`vX.Y.Z-dev.N`), **not** PEP 440 format (`vX.Y.Z.devN`). Using the wrong format will cause PSR to ignore the tag.

## Hotfix Process

### For Current Stable Line

1. Create fix on `main`
2. Cherry-pick to the relevant `stable/<major>` branch
3. Push triggers automatic release

### For Previous Stable Lines

1. Checkout the relevant `stable/<major>` branch
2. Apply fix directly
3. Push triggers automatic release

## Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Description | Version Impact |
|------|-------------|----------------|
| `feat` | New feature | Minor |
| `fix` | Bug fix | Patch |
| `perf` | Performance improvement | Patch |
| `revert` | Revert previous commit | Patch |
| `docs` | Documentation only | No release |
| `style` | Code style (formatting) | No release |
| `refactor` | Code refactoring | No release |
| `test` | Test additions/changes | No release |
| `chore` | Maintenance tasks | No release |
| `BREAKING CHANGE` footer | Breaking API change | Major |

## CI/CD Configuration

### Required GitHub Secrets

- `GITHUB_TOKEN`: Automatically provided, used for releases and commits

### Required GitHub Environments

- `pypi`: Environment with PyPI trusted publisher configured

### PyPI Trusted Publisher Setup

1. Go to PyPI project settings
2. Add a new trusted publisher:
   - Owner: `camunda`
   - Repository: `orchestration-cluster-api-python`
   - Workflow: `publish.yml`
   - Environment: `pypi`

## Troubleshooting

### Release Not Triggered

- Ensure commit messages follow conventional commits format
- Check that the commit type triggers a release (not `docs`, `style`, etc.)
- Verify the branch name matches workflow triggers

### Version Conflict

- Ensure git tags are in sync with PyPI versions
- Check `pyproject.toml` version matches the latest tag

### PyPI Publishing Failed

- Verify trusted publisher configuration
- Check the `pypi` environment is properly configured
- Ensure OIDC token permissions are set in workflow

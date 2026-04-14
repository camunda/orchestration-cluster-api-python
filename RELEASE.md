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
- **Publishes to**: PyPI as dev pre-releases (e.g., `10.0.0.dev1`, `10.0.0.dev2`)
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

When a new Camunda server minor ships (e.g. 8.10), the SDK bumps its major (e.g. 9 → 10). Follow these steps **in order**:

### 1. Push a Breaking-Change Commit on `main`

```bash
git checkout main
git commit --allow-empty -m "feat: release SDK 10 for Camunda server 8.10

BREAKING CHANGE: SDK major version bumped from 9 to 10 to track Camunda server 8.10"
git push
```

### 2. Wait for Main CI

Wait for CI to complete and publish the first dev pre-release (e.g. `10.0.0.dev1`).

### 3. Create and Push the Stable Branch

```bash
git checkout -b stable/10
git push -u origin stable/10
```

CI runs automatically on push and publishes the first stable release (e.g. `10.0.0`).

### 4. Bump `main` to the Next Major

```bash
git checkout main
git commit --allow-empty -m "feat: begin SDK 11 development for Camunda server 8.11

BREAKING CHANGE: SDK major version bumped from 10 to 11"
git push
```

This ensures main publishes `11.0.0.devN` while `stable/10` publishes `10.x.y`.

### 5. Update Dependabot

Add Dependabot entries for the new stable branch in [.github/dependabot.yml](.github/dependabot.yml) (pip, github-actions). Dependabot does not support wildcard branch patterns, so each `stable/*` branch must be listed explicitly.

> **Important**: Use a `BREAKING CHANGE:` footer in the commit body — not the `feat!:` shorthand.

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

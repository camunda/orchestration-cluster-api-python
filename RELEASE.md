# Release Process

This document describes the branching strategy, release streams, and publishing process for the Camunda Orchestration SDK for Python.

## Overview

The SDK follows a multi-stream release model that aligns with Camunda server versions:

| Branch | PyPI Index | Purpose |
|--------|------------|---------|
| `main` | `--pre` (dev) | Development stream, dev pre-releases |
| `stable/<major>.<minor>` | Default | Stable releases for specific Camunda versions |

## Branch Model

### `main` Branch

- **Purpose**: Active development targeting the next Camunda release
- **Publishes to**: PyPI as dev pre-releases (e.g., `8.9.0.dev1`, `8.9.0.dev2`)
- **Installation**: `pip install camunda-orchestration-sdk --pre`

### `stable/<major>.<minor>` Branches

- **Purpose**: Maintenance releases for specific Camunda versions
- **Examples**: `stable/8.8`, `stable/8.9`
- **Publishes to**: PyPI with version-specific releases
- **Installation**: `pip install camunda-orchestration-sdk==8.8.*`

## Version Numbering

This SDK uses a **modified semantic versioning** scheme aligned with Camunda server versions:

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `fix:`, `feat:`, `perf:`, `revert:` | Patch | `8.8.0` → `8.8.1` |
| `server:` | Minor | `8.8.x` → `8.9.0` |
| `server-major:` | Major | `8.x.y` → `9.0.0` |

This means:
- **Patch versions** contain bug fixes, new features, and improvements
- **Minor versions** align with Camunda server minor releases
- **Major versions** align with Camunda server major releases

## Installation Guide

### Latest Stable Release (Recommended)

```bash
pip install camunda-orchestration-sdk
```

### Specific Version Line

Pin to a specific Camunda version:

```bash
# Pin to 8.8.x releases
pip install "camunda-orchestration-sdk>=8.8.0,<8.9.0"

# Or use compatible release operator
pip install "camunda-orchestration-sdk~=8.8.0"
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

## Creating a New Stable Branch

When a new Camunda minor version is released:

### 1. Create the New Stable Branch

```bash
# From main branch
git checkout main
git pull origin main
git checkout -b stable/8.9
git push origin stable/8.9
```

### 2. Prepare Main for Next Dev Cycle

Create a commit on `main` with the `server:` prefix to bump the minor version:

```bash
git checkout main
git commit --allow-empty -m "server: prepare for 8.10 development"
git push origin main
```

## Hotfix Process

### For Current Stable Line

1. Create fix on `main`
2. Cherry-pick to the relevant `stable/<major>.<minor>` branch
3. Push triggers automatic release

### For Previous Stable Lines

1. Checkout the relevant `stable/<major>.<minor>` branch
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
| `feat` | New feature | Patch |
| `fix` | Bug fix | Patch |
| `perf` | Performance improvement | Patch |
| `revert` | Revert previous commit | Patch |
| `docs` | Documentation only | No release |
| `style` | Code style (formatting) | No release |
| `refactor` | Code refactoring | No release |
| `test` | Test additions/changes | No release |
| `chore` | Maintenance tasks | No release |
| `server` | Camunda server minor bump | Minor |
| `server-major` | Camunda server major bump | Major |

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

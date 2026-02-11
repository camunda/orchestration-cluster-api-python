# Version Fix Guide: Correcting 1.2.0-dev.x to 8.9.0-dev.x

## Problem Statement

The main branch is currently publishing pre-release packages as version `1.2.0-dev.x` to PyPI, but it should be publishing as version `8.9.0-dev.x` to align with the Camunda 8.9 server version.

## Root Cause

The repository uses Python Semantic Release with a custom versioning scheme that aligns with Camunda server versions. The configuration in `pyproject.toml` defines:

- **Patch bump** (`fix:`, `feat:`, `perf:`, `revert:`) - e.g., 8.8.0 → 8.8.1
- **Minor bump** (`server:`) - e.g., 8.8.x → 8.9.0  
- **Major bump** (`server-major:`) - e.g., 8.x.y → 9.0.0

The issue occurred because semantic-release was continuing from the last tag `v1.1.3` and automatically bumped to `v1.2.0-dev.1` based on conventional commits. No commit with the `server:` or `server-major:` prefix was made to trigger the jump to 8.9.0.

## Solution Overview

To fix this issue, we need to:

1. Manually set the version in `pyproject.toml` to `8.9.0-dev.1`
2. Create a git tag `v8.9.0-dev.1` on the main branch
3. Push both the commit and tag to the main branch
4. Future releases will automatically continue from 8.9.0-dev.x

## Implementation Steps

### Step 1: Update Version in pyproject.toml

This has already been done in this PR. The version was changed from `1.2.0-dev.1` to `8.9.0-dev.1`.

```toml
[project]
name = "camunda-orchestration-sdk"
version = "8.9.0-dev.1"  # Changed from 1.2.0-dev.1
```

### Step 2: Create Version Tag

A git tag `v8.9.0-dev.1` has been created with this commit using the `server-major:` commit prefix to indicate this is a version alignment change.

### Step 3: Merge to Main and Push Tag

**CRITICAL**: After this PR is merged to main, a tag must be manually created and pushed.

#### Quick Method: Use the Provided Script

A helper script `apply-version-fix.sh` is included in this PR. After merging, run:

```bash
git checkout main
git pull origin main
./apply-version-fix.sh
```

The script will:
- Verify you're on the main branch
- Check that pyproject.toml has version 8.9.0-dev.1  
- Create the tag v8.9.0-dev.1 on current HEAD
- Push the tag to origin
- Verify the tag was pushed successfully

#### Manual Method: If PR is Merged (Not Squashed)

If the PR is merged with a merge commit (preserving all commits):

```bash
git checkout main
git pull origin main
# The commit ac8c5ec will exist on main with its tag
git push origin v8.9.0-dev.1
```

#### Manual Method: If PR is Squash-Merged (Most Common)

**This is the most common scenario on GitHub.** Squash merging creates a new commit with a different SHA, so you need to:

1. Merge the PR using "Squash and merge" on GitHub
2. Find the new squash commit on main:
   ```bash
   git checkout main
   git pull origin main
   git log --oneline -5
   ```
3. Create the tag on the squash commit (it will be the most recent commit after pulling):
   ```bash
   # Tag the current HEAD (which is the squash commit)
   git tag -a v8.9.0-dev.1 -m "v8.9.0-dev.1"
   git push origin v8.9.0-dev.1
   ```

#### Verification

After pushing the tag, verify it exists on GitHub:

```bash
git ls-remote --tags origin | grep "8.9.0"
```

You should see:
```
<commit-sha>    refs/tags/v8.9.0-dev.1
```

### Step 4: Verify the Fix

After the tag is pushed, the next push to main will trigger the publish workflow. You can verify the fix by:

1. Making a test commit to main (e.g., `fix: test version fix` or `chore: verify version`)
2. The CI workflow will run semantic-release, which should:
   - Detect `v8.9.0-dev.1` as the latest tag
   - Calculate the next version as `8.9.0-dev.2` (for a patch-level change)
3. Check PyPI after the workflow completes to confirm the package was published as `8.9.0-dev.2`

## How Semantic Release Will Behave Going Forward

Once the `v8.9.0-dev.1` tag exists on main:

| Commit Type | Next Version | Example |
|-------------|--------------|---------|
| `fix:`, `feat:`, `perf:`, `revert:` | Patch bump | 8.9.0-dev.1 → 8.9.0-dev.2 |
| `server:` | Minor bump | 8.9.0-dev.x → 8.10.0-dev.1 |
| `server-major:` | Major bump | 8.9.0-dev.x → 9.0.0-dev.1 |
| `docs:`, `chore:`, `style:`, etc. | No release | Version stays the same |

Because the main branch is configured with `prerelease = true` and `prerelease_token = "dev"`, all versions on main will have the `-dev.x` suffix.

## Alternative Approach: Direct Main Branch Update

If you prefer not to use a PR, you can apply this fix directly on main:

```bash
# Checkout main
git checkout main
git pull origin main

# Update version in pyproject.toml
# Edit the file manually or use:
sed -i 's/version = "1.2.0-dev.1"/version = "8.9.0-dev.1"/' pyproject.toml

# Commit with server-major prefix
git add pyproject.toml
git commit -m "server-major: bump version to 8.9.0 to align with Camunda server version"

# Create tag
git tag -a v8.9.0-dev.1 -m "v8.9.0-dev.1"

# Push commit and tag
git push origin main
git push origin v8.9.0-dev.1
```

## Rollback Plan

If something goes wrong and you need to rollback:

1. Delete the `v8.9.0-dev.1` tag:
   ```bash
   git push --delete origin v8.9.0-dev.1
   ```

2. Revert the version change in `pyproject.toml`:
   ```bash
   git revert <commit-sha>
   git push origin main
   ```

3. The repository will return to using the `v1.2.0-dev.1` tag as the baseline.

## Testing in a Safe Environment

If you want to test this change before applying it to main:

1. Create a test repository or branch
2. Apply the version change and tag
3. Run semantic-release locally:
   ```bash
   semantic-release version --print
   ```
4. This will show you what the next version would be without actually creating it

## Additional Notes

- The `[skip ci]` suffix in semantic-release commit messages prevents infinite CI loops
- The publish workflow (`publish.yml`) handles the full release process:
  - Testing
  - SDK generation  
  - Version calculation via semantic-release
  - PyPI publishing
- Tags must start with `v` as configured in `tag_format = "v{version}"`
- The prerelease suffix `-dev.x` is automatically added by semantic-release for the main branch

## References

- Semantic Release configuration: `pyproject.toml` (lines 71-111)
- Release documentation: `RELEASE.md`
- Publish workflow: `.github/workflows/publish.yml`

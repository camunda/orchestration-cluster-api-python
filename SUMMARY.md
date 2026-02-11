# Version Fix Summary

## Problem
The main branch was publishing packages as version `1.2.0-dev.x` instead of the expected `8.9.0-dev.x` to align with Camunda 8.9 server version.

## Solution
This PR fixes the version mismatch by:

1. **Updating pyproject.toml** from version `1.2.0-dev.1` to `8.9.0-dev.1`
2. **Creating a git tag** `v8.9.0-dev.1` that semantic-release will use as the baseline
3. **Providing automation** via `apply-version-fix.sh` script to simplify the post-merge process

## Why This Happened
The repository uses a custom semantic versioning scheme:
- `fix:`, `feat:`, `perf:`, `revert:` = patch bump (8.9.0 → 8.9.1)
- `server:` = minor bump (8.8.x → 8.9.0)
- `server-major:` = major bump (8.x.y → 9.0.0)

Semantic-release automatically bumped from `v1.1.3` to `v1.2.0-dev.1` based on commit history, since no commit with `server:` or `server-major:` prefix triggered the jump to 8.9.0.

## What You Need to Do After Merging

### Quick Method (Recommended)
```bash
git checkout main
git pull origin main
./apply-version-fix.sh
```

The script will:
- ✅ Verify you're on main branch
- ✅ Check version is 8.9.0-dev.1
- ✅ Create tag v8.9.0-dev.1 on current HEAD
- ✅ Push tag to origin
- ✅ Verify tag was pushed successfully

### Manual Method
If you prefer to do it manually:
```bash
git checkout main
git pull origin main
git tag -a v8.9.0-dev.1 -m "v8.9.0-dev.1"
git push origin v8.9.0-dev.1
```

## Verification
After pushing the tag, test it with a dummy commit:
```bash
# Make a small change or create an empty commit
git commit --allow-empty -m "fix: verify version fix"
git push origin main
```

The publish workflow should:
- ✅ Detect v8.9.0-dev.1 as the latest tag
- ✅ Calculate next version as `8.9.0-dev.2`
- ✅ Publish to PyPI as `camunda-orchestration-sdk==8.9.0.dev2`

Check PyPI: https://pypi.org/project/camunda-orchestration-sdk/

## Future Behavior
Once the tag is in place:

| Commit Type | Next Version |
|-------------|--------------|
| `fix:`, `feat:`, `perf:` | 8.9.0-dev.2, 8.9.0-dev.3, ... |
| `server:` | 8.10.0-dev.1 |
| `server-major:` | 9.0.0-dev.1 |

## Files in This PR
- **pyproject.toml** - Version updated to 8.9.0-dev.1
- **VERSION_FIX_GUIDE.md** - Detailed explanation and troubleshooting
- **apply-version-fix.sh** - Automated script for post-merge tagging
- **SUMMARY.md** - This file (can be deleted after reading)

## Questions?
Refer to `VERSION_FIX_GUIDE.md` for:
- Detailed step-by-step instructions
- Troubleshooting common issues
- Rollback procedures
- Alternative approaches

## Clean Up
After successfully applying the fix and verifying it works, you can optionally:
- Delete `VERSION_FIX_GUIDE.md` (if you don't need the reference)
- Delete `apply-version-fix.sh` (after running it)
- Delete `SUMMARY.md` (this file)

These files were created to document and assist with this one-time version fix.

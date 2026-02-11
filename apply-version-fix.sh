#!/bin/bash
# Script to apply the version fix after PR merge
# This script should be run AFTER the PR is merged to main

set -euo pipefail

echo "==================================="
echo "Version Fix Post-Merge Script"
echo "==================================="
echo ""

# Check if we're on main
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "ERROR: You must be on the main branch"
    echo "Current branch: $CURRENT_BRANCH"
    echo ""
    echo "Run: git checkout main"
    exit 1
fi

# Pull latest changes
echo "Pulling latest changes from origin/main..."
git pull origin main
echo ""

# Check current version
CURRENT_VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
echo "Current version in pyproject.toml: $CURRENT_VERSION"

if [ "$CURRENT_VERSION" != "8.9.0-dev.1" ]; then
    echo ""
    echo "ERROR: Version in pyproject.toml is not 8.9.0-dev.1"
    echo "Expected: 8.9.0-dev.1"
    echo "Found: $CURRENT_VERSION"
    echo ""
    echo "This script should only be run after the version fix PR is merged."
    exit 1
fi

# Check if tag already exists
if git rev-parse v8.9.0-dev.1 >/dev/null 2>&1; then
    echo ""
    echo "Tag v8.9.0-dev.1 already exists locally"
    EXISTING_TAG_COMMIT=$(git rev-parse v8.9.0-dev.1)
    echo "Tag points to commit: $EXISTING_TAG_COMMIT"
    
    # Check if it exists on origin
    if git ls-remote --tags origin | grep -q "refs/tags/v8.9.0-dev.1"; then
        echo "Tag also exists on origin"
        REMOTE_TAG_COMMIT=$(git ls-remote --tags origin | grep "refs/tags/v8.9.0-dev.1" | awk '{print $1}')
        echo "Remote tag points to: $REMOTE_TAG_COMMIT"
        
        if [ "$EXISTING_TAG_COMMIT" = "$REMOTE_TAG_COMMIT" ]; then
            echo ""
            echo "SUCCESS: Tag is already correctly set up on both local and remote!"
            exit 0
        else
            echo ""
            echo "WARNING: Local and remote tags point to different commits!"
            echo "This needs manual resolution."
            exit 1
        fi
    fi
else
    echo ""
    echo "Creating tag v8.9.0-dev.1 on current HEAD..."
    CURRENT_COMMIT=$(git rev-parse HEAD)
    echo "Current HEAD: $CURRENT_COMMIT"
    
    git tag -a v8.9.0-dev.1 -m "v8.9.0-dev.1"
    echo "Tag created successfully"
fi

echo ""
echo "Pushing tag to origin..."
git push origin v8.9.0-dev.1
echo ""

# Verify the tag was pushed
if git ls-remote --tags origin | grep -q "refs/tags/v8.9.0-dev.1"; then
    REMOTE_TAG_COMMIT=$(git ls-remote --tags origin | grep "refs/tags/v8.9.0-dev.1" | awk '{print $1}')
    echo "SUCCESS!"
    echo "Tag v8.9.0-dev.1 has been pushed to origin"
    echo "Remote tag points to: $REMOTE_TAG_COMMIT"
    echo ""
    echo "Next steps:"
    echo "1. Make a test commit to main (e.g., 'fix: test version fix')"
    echo "2. The publish workflow will run and should create version 8.9.0-dev.2"
    echo "3. Verify the package on PyPI: https://pypi.org/project/camunda-orchestration-sdk/"
else
    echo "ERROR: Tag was not successfully pushed to origin"
    exit 1
fi

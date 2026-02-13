"""
GitHub Repository Setup Script for PreCostCalc Desktop Application
This script creates and pushes the test-generator repository under ramanjansnaik
"""

#!/bin/bash
# GitHub Repository Setup Script

REPO_NAME="test-generator"
OWNER="ramanjansnaik"
REPO_URL="https://github.com/${OWNER}/${REPO_NAME}.git"

echo "=== PreCostCalc Desktop GitHub Setup ==="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
fi

# Add remote if not exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "Adding remote repository: ${REPO_URL}"
    git remote add origin "${REPO_URL}"
fi

# Verify remote
git remote -v

echo ""
echo "Repository setup complete!"
echo ""
echo "To push to GitHub, run:"
echo "  git branch -M main"
echo "  git push -u origin main"
echo ""
echo "If you haven't created the repository on GitHub yet, create it at:"
echo "  https://github.com/new"
echo ""
echo "Repository name: ${REPO_NAME}"
echo "Repository URL: ${REPO_URL}"
echo ""
echo "The repository should be public and include a README.md"
# CI/CD Setup Guide

## GitHub Actions Configuration

This repository includes automated testing via GitHub Actions.

### Setup Instructions

1. **Enable GitHub Actions** (if not already enabled):
   - Go to your repository on GitHub
   - Navigate to Settings → Actions → General
   - Ensure "Allow all actions and reusable workflows" is selected

2. **Verify Workflow File**:
   - The workflow is located at `.github/workflows/test.yml`
   - It runs automatically on push/pull request to main/master/develop branches

3. **View Test Results**:
   - Go to the "Actions" tab in your GitHub repository
   - Click on the latest workflow run
   - View results for each test job

### What Gets Tested

The CI/CD pipeline runs 3 separate test jobs for the active research surface:

1. **leap_analysis**: LEAP scoring and analysis regressions
2. **post_alignment_lab**: post-alignment behavior and phase-2 regressions
3. **intuition-layer**: routing and memory/intuition regressions

The repository also supports repo-wide validation with:

```bash
pytest -q
```

### Local Testing

Before pushing, run tests locally:

```bash
# LEAP Analysis
cd leap_analysis && python test_leap_score.py

# Post-Alignment Lab
cd post_alignment_lab && python test_post_alignment_phase2.py

# Intuition-Layer
cd intuition-layer && python test_intuition_router.py

# Repo-wide
pytest -q
```

### Troubleshooting

**If tests fail in CI but pass locally**:
- Check Python version (CI uses 3.9)
- Verify all dependencies are listed in workflow
- Check for OS-specific issues (CI uses Ubuntu)

**If workflow doesn't trigger**:
- Ensure `.github/workflows/test.yml` is in the repository
- Check branch names match (main/master/develop)
- Verify GitHub Actions is enabled

### Badge (Optional)

Add this to your README.md to show test status:

```markdown
![Tests](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/test.yml/badge.svg)
```

Replace `YOUR_USERNAME` and `YOUR_REPO` with your GitHub username and repository name.

---
description: Generate comprehensive commit comments from pull requests or commit hashes with High Level Summary and Specific Details.
---

# Workflow: Git Comment

Follow these steps to generate structured commit comments.

1.  **Identify Input**:
    - Determine if input is a Pull Request (number/URL) or Commit Hash
    // turbo
    - For PR: Run `gh pr view <number> --json title,body,files`
    // turbo
    - For Commit: Run `git show <hash> --stat`

2.  **Fetch Changes**:
    - Load the `git-comment` skill context
    // turbo
    - For PR: Run `gh pr diff <number> --patch > /tmp/changes.patch`
    // turbo
    - For Commit: Run `git show <hash> --patch > /tmp/changes.patch`

3.  **Analyze Changes**:
    - Review the patch file to understand:
      - Files modified and their categories
      - Logic and behavioral changes
      - Architecture impact
      - Dependencies added/removed

4.  **Generate Comment**:
    - Create structured comment with:
      - **High Level Summary**: 2-3 sentence overview
      - **Type/Impact/Breaking Changes** classification
      - **Specific Details**: File changes, logic changes, technical notes

5.  **Quality Check**:
    - Verify summary captures intent
    - Ensure all significant changes are documented
    - Confirm appropriate detail level

6.  **Deliver**:
    // turbo
    - Clean up: `rm -f /tmp/changes.patch`
    - Present the formatted comment to the user

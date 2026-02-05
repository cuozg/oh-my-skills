---
description: Squash multiple related commits into organized, well-documented commits with proper grouping and messaging.
---

# Workflow: Git Squash

Follow these steps to intelligently squash and organize commits.

1.  **Gather Commits**:
    - Identify the commits to process
    // turbo
    - For range: Run `git log --oneline <start>^..<end>`
    // turbo
    - For PR: Run `gh pr view <number> --json commits --jq '.commits[]'`

2.  **Analyze and Group**:
    - Load the `git-squash` skill context
    - Group commits by:
      - Feature/component relationship
      - Type (feat, fix, refactor, test, etc.)
      - Dependency requirements

3.  **Present Squash Plan**:
    - Show the user the proposed grouping:
      | Group | Commits | Target Message |
    - Wait for user approval before proceeding

4.  **Create Backup**:
    // turbo
    - Run `git branch backup-$(date +%Y%m%d%H%M%S)`
    - Confirm backup branch created

5.  **Execute Squash**:
    - Use interactive rebase or soft reset method
    - For each group, generate comprehensive commit message using git-comment format
    - Include "Squashed from:" section listing original commits

6.  **Verify**:
    // turbo
    - Run `git log --oneline -n 10` to confirm new structure
    - Run tests if applicable to verify nothing broke

7.  **Push**:
    - Confirm with user before force pushing
    - Run `git push --force-with-lease origin <branch>` if approved

8.  **Report**:
    - Show final commit structure
    - Provide rollback instructions if needed

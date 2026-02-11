---
description: Squash and organize commits into clean, well-documented history
agent: build
---

Load the `git/git-squash` skill and organize the commit history.

## Task

$ARGUMENTS

## Workflow

1. **Analyze** the commit history to identify related changes
2. **Group** commits by feature, bugfix, or logical unit
3. **Squash** related commits into organized, well-documented commits
4. **Write** clear commit messages that explain the "why" not just the "what"

## Safety

- NEVER force push to main/master without explicit confirmation
- NEVER modify commits that have been pushed to shared branches without confirmation
- Always verify the result with `git log` before completing

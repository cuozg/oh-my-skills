---
name: git-comment
description: "Generate and apply concise commit messages for the last commit on the current local branch. Read the latest commit's diff, investigate code changes, generate a short bullet-point message highlighting important changes, and amend the commit with the new message. Never push to remote — local only. This skill should be used when: (1) last commit has a poor or placeholder message, (2) user says 'comment this commit', (3) 'generate commit message', (4) 'describe last commit', (5) 'amend commit message', (6) 'annotate commit', (7) 'fix commit message'."
---

# Git Comment

Amend the last commit with a generated message from diff analysis. Local only — never pushes.

**Input**: None required — operates on last commit. Optional: specific commit hash.
**Output**: Amended commit message. Nothing is pushed.

## Restrictions

- **NEVER** push to remote — amend locally only
- **NEVER** add co-author, committer, or AI tool metadata
- **NEVER** include code snippets in the message
- **NEVER** amend if the commit has already been pushed (check: `git status` for "ahead")
- **DO** verify the commit is not a merge commit from remote before amending
- **DO** warn the user if the commit appears to belong to someone else

## Reference Files

- [workflow.md](references/workflow.md) — Commit message format, 5-step workflow, example, anti-patterns

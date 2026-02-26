---
name: git-commit
description: "Generate clean, meaningful git commit messages based on code changes or user request. Commits to current branch with no AI metadata (no co-author, committer info, or tool attribution). Messages are short, concise, use bullet points for multiple changes. Triggers: 'commit changes', 'generate and commit', 'commit with message', 'commit this', 'stage and commit'."
---

# Git Commit

Generate clean commit messages from staged changes. Local only — never pushes.

**Input**: File changes (via `git diff`) or explicit user description. Optional: commit scope, branch name.
**Output**: A git commit on current branch with structured message.

## Restrictions

- **NEVER** add co-author, committer, or AI tool metadata
- **NEVER** push to remote — only commit locally
- **NEVER** include code snippets in message
- **DO** use imperative mood, bullet points, verify branch first

## Reference Files

- [workflow.md](references/workflow.md) — Commit message format, 4-step workflow, examples, anti-patterns

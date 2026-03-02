---
name: git-commit
description: Commit staged or unstaged changes with a clean imperative message — use for 'commit', 'git commit', 'commit changes', 'save changes'
---
# git-commit

Stage and commit changes with a clean, imperative-mood commit message. Never pushes to remote.

## When to Use

- Saving completed work as a logical commit
- Committing a set of related changes with a meaningful message
- Finalizing a bug fix, feature, or refactor into version history

## Workflow

1. **Inspect** — Run `git status` and `git diff` to understand what has changed
2. **Stage** — Run `git add` for relevant files (or `git add -A` if all changes belong together)
3. **Draft** — Write an imperative-mood summary line (max 72 chars); add bullet points for multi-change commits
4. **Commit** — Run `git commit -m "{message}"` with the drafted message
5. **Confirm** — Run `git status` to verify the working tree is clean

## Rules

- Use imperative mood: "Add", "Fix", "Refactor" — not "Added" or "Adding"
- Keep summary line under 72 characters
- Use bullet points in the body when multiple distinct changes are present
- Include no AI-generated metadata, co-author tags, or tool signatures
- Never run `git push` — local commit only
- Never amend a commit that has already been pushed

## Output Format

A single local commit with a clean message. No remote changes. `git status` shows a clean working tree.

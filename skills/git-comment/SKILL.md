---
name: git-comment
description: Amend the last commit message to be clean and descriptive — use for 'amend commit', 'fix commit message', 'rewrite commit', 'change commit message'
metadata:
  author: kuozg
  version: "1.0"
---
# git-comment

Rewrite the most recent local commit message to be clear, imperative, and well-structured. Never touches pushed commits.

## When to Use

- The last commit message is unclear, verbose, or auto-generated
- A commit message needs bullet points added for multi-change clarity
- Fixing a typo or wrong scope in the commit summary
- Cleaning up before creating a PR

## Workflow

1. **Check** — Run `git log -1` to read the current message and `git status` to confirm no unpushed remotes have the commit
2. **Verify** — Run `git log --oneline origin/HEAD..HEAD` (or equivalent) to confirm the commit is local only
3. **Draft** — Write the improved message: imperative summary line + optional bullet body
4. **Amend** — Run `git commit --amend -m "{new message}"` (or open editor if body needed)
5. **Confirm** — Run `git log -1` to verify the updated message

## Rules

- Never amend if the commit has already been pushed to any remote branch
- Use imperative mood: "Fix", "Add", "Update" — not past tense
- Keep summary under 72 characters
- Add bullet points in the body for commits touching multiple concerns
- Include no AI metadata or tool signatures in the message

## Output Format

Amended local commit with an improved message. No remote changes. `git log -1` shows the updated message.

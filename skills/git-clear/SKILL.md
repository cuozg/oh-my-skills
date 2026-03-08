---
name: git-clear
description: Delete all comments from a GitHub PR (issue comments + review comments) — use for 'clear PR comments', 'delete PR comments', 'remove PR comments', 'clean PR comments'
metadata:
  author: kuozg
  version: "1.0"
---
# git-clear

Delete every comment on a GitHub Pull Request — both timeline (issue) comments and inline review comments. Uses `gh api` with pagination.

## When to Use

- Clearing bot-generated or outdated review comments before a fresh review cycle
- Removing stale AI review comments after code changes
- Cleaning up a noisy PR thread before requesting re-review
- Bulk-removing comments left by automated tools

## Workflow

1. **Identify** — Determine the PR number. Run `gh pr view` or accept it from the user
2. **Resolve** — Extract `{owner}` and `{repo}` from `gh repo view --json owner,name`
3. **List** — Fetch all issue comments and review comments with `--paginate`
4. **Confirm** — Show the comment count to the user and wait for explicit approval
5. **Delete** — Run `clear_pr_comments.py` to delete all comments via `gh api --method DELETE`
6. **Verify** — Re-list both endpoints to confirm zero comments remain

## Rules

- Always confirm with the user before deleting — show exact comment counts first
- Delete both issue comments (`/issues/comments/{id}`) and review comments (`/pulls/comments/{id}`)
- Handle pagination for PRs with many comments (`--paginate` or `?per_page=100`)
- Requires `repo` scope on `gh auth` — verify with `gh auth status` if deletions fail
- Only delete comments you have permission to delete (own comments or repo write access)
- Never modify the PR description, title, or labels — comments only

## Output Format

Summary of deleted comments: `Deleted {n} issue comments and {m} review comments from PR #{pr}`.

## Scripts

- `scripts/clear_pr_comments.py` — Delete all PR comments via `gh api`. Usage: `python3 clear_pr_comments.py <owner> <repo> <pr_number>`

Run scripts via `run_skill_script("git-clear", "scripts/clear_pr_comments.py", ["owner", "repo", "42"])`.

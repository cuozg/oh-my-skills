---
name: unity-review-prefab
description: "Review .prefab and .unity files in GitHub PRs for missing scripts, broken variant links, raycast issues, hierarchy problems, and Unity-specific YAML patterns. After review, pushes comments directly to GitHub via the API. Accepts PR number/URL as input. Use when: reviewing prefab/scene files in PRs, validating prefab integrity before merge. Triggers: 'review prefab', 'prefab review', 'scene review', 'prefab changes', 'PR prefab review', 'review PR prefabs'."
---

# Prefab & Scene PR Reviewer

Review `.prefab` and `.unity` file changes in GitHub PRs. Delegate each file to a parallel subagent, gather results, merge into one review, and push to GitHub.

## Output
Review comments pushed to GitHub PR via API. Covers missing scripts, broken variants, raycast issues, hierarchy problems.

## Input → Command

| Input | Command |
|:------|:--------|
| PR number/URL | `gh pr diff <N>` + `gh pr view <N> --json title,body,files,number` |

## Severity Labels

| Severity | Emoji | Meaning |
|:---------|:------|:--------|
| CRITICAL | 🔴 | Breaks functionality, data loss, crashes |
| HIGH | 🟡 | Performance, UX, or logic issues |
| MEDIUM | 🔵 | Style, maintainability, minor UX |
| LOW | 🟢 | Naming, conventions, suggestions |

Severity labels are for categorization only. This skill always posts as `COMMENT`. Approval decisions are made exclusively by `unity-review-general`.

## Workflow

Follow the 4-step workflow: Fetch PR & Filter → Parallel Review → Collect & Merge → Submit.
## Rules

- Only review `.prefab` and `.unity` files. Read full files, not just diffs.
- One subagent per file. Each subagent loads `unity-review-prefab` to access patterns.
- One issue = one comment. Every comment needs severity + evidence + suggestion.
- If a subagent fails, log the error and continue with remaining results.
- Submit even if PR is merged — `post_review.py` handles fallback.
- Never hardcode `commit_id` or modify source files.
- Refer to [review-prefab-patterns.md](../unity-shared/references/review-prefab-patterns.md) for the complete pattern catalog.
- Refer to [review-parallel-workflow.md](../unity-shared/references/review-parallel-workflow.md) for delegation details.

## Reference Files
- [review-prefab-patterns.md](../unity-shared/references/review-prefab-patterns.md) — Complete pattern catalog for prefab/scene review
- [review-prefab-patterns.md](../unity-shared/references/review-prefab-patterns.md) — Complete pattern catalog for prefab/scene review
- [review-parallel-workflow.md](../unity-shared/references/review-parallel-workflow.md) — Subagent delegation details
- workflow.md — 4-step prefab review workflow

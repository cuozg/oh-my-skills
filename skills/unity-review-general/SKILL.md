---
name: unity-review-general
description: "Review PRs against general quality checklists — security, correctness, testing, code quality, performance, lifecycle, and documentation. Technology-agnostic checks applied to all file types. After review, pushes comments directly to GitHub via the API. Accepts PR number/URL as input. Use when: reviewing PR quality, security audit, testing coverage review. Triggers: 'general review', 'security review', 'testing review', 'code quality review', 'PR quality review', 'review PR quality'."
---

# General PR Quality Reviewer (Final Approver)

Sole approval authority. Collects prior reviewer comments (posted as `COMMENT` by specialized skills), applies quality checklists, and makes the final `APPROVE` or `REQUEST_CHANGES` decision. No other review skill sets approval status.

## Output
Final review comment pushed to GitHub PR with approval decision. Aggregates prior reviewer findings + own quality checklists.

## Input → Command

| Input | Command |
|:------|:--------|
| PR number/URL | `gh pr diff <N>` + `gh pr view <N> --json title,body,files,number` |

## Severity → Approval

| Severity | Emoji | Meaning | Approval |
|:---------|:------|:--------|:---------|
| CRITICAL | 🔴 | Breaks functionality, data loss, security vulnerability | `REQUEST_CHANGES` (block) |
| HIGH | 🟡 | Performance, correctness, or logic issue | `REQUEST_CHANGES` |
| MEDIUM | 🔵 | Best practice violation, maintainability risk | `COMMENT` (allow merge) |
| LOW | 🟢 | Style, naming, documentation gap | `APPROVE` (with suggestions) |
| CLEAN | — | No issues from any reviewer | `APPROVE` |


Full decision tree and severity classification: [APPROVAL_CRITERIA.md](references/APPROVAL_CRITERIA.md).

## Workflow

Follow the 5-step workflow: Collect Prior Reviews → Fetch PR → Apply Checklists → Build JSON → Submit.
Read [workflow.md](references/workflow.md) before starting any review.

## Rules

- You are the **sole approver** — only this skill sets `APPROVE` or `REQUEST_CHANGES`. All other review skills (`unity-review-code-pr`, `unity-review-prefab`, `unity-review-asset`, `unity-review-architecture`) post as `COMMENT` only.
- Prior reviewer findings with 🔴 or 🟡 severity → you MUST set `REQUEST_CHANGES`.
- One issue = one comment. Every comment needs severity + issue summary + suggestion.
- Security findings are always 🔴 Critical.
- For PRs > 300 lines, add a comment recommending split.
- Correctness check: verify PR logic matches stated intent from PR title/body.
- Submit even if PR is merged — `post_review.py` handles fallback.
- Never hardcode `commit_id` or modify source files.
- Refer to [GENERAL_CHECKLISTS.md](references/GENERAL_CHECKLISTS.md) for the complete checklist catalog.

## Reference Files
- [workflow.md](references/workflow.md) — 5-step review and approval workflow
- [APPROVAL_CRITERIA.md](references/APPROVAL_CRITERIA.md) — Decision tree and severity classification
- [GENERAL_CHECKLISTS.md](references/GENERAL_CHECKLISTS.md) — Complete checklist catalog

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

### 1. Collect Prior Reviews

Fetch all comments already posted by specialized reviewers (code, architecture, prefab, asset):

```bash
gh api repos/<owner>/<repo>/pulls/<N>/reviews    # Review bodies + states
gh api repos/<owner>/<repo>/pulls/<N>/comments   # Inline comments
```

Parse and categorize findings by severity (🔴🟡🔵🟢). Note the highest severity found across all prior reviewers.

### 2. Fetch PR & Extract Intent

```bash
gh pr diff <N> --name-only
gh pr view <N> --json title,body,files,number
gh pr diff <N>
```

Read PR title/body for intent and acceptance criteria. Count changed lines for checklist focus — see [GENERAL_CHECKLISTS.md](references/GENERAL_CHECKLISTS.md).

### 3. Apply Checklists

Apply each applicable checklist from [GENERAL_CHECKLISTS.md](references/GENERAL_CHECKLISTS.md):
1. 🔒 Security  2. ✅ Correctness  3. 🧪 Testing  4. 🧹 Code Quality  5. ⚡ Performance  6. 🔄 Lifecycle  7. 📚 Documentation

Also verify: does the PR accomplish what the title/body says? Flag gaps.

### 4. Build `/tmp/review-general.json`

```json
{
  "body": "## Final Quality Review (Approver)\n\n### Prior Review Summary\n[Summarize findings from code/architecture/prefab/asset reviewers — count by severity]\n\n### General Quality Findings\n**Scope**: [N files, M lines]\n[Your own checklist findings]\n\n### Decision\n**[APPROVE/REQUEST_CHANGES]** — [reasoning based on aggregated severity]",
  "event": "REQUEST_CHANGES|COMMENT|APPROVE",
  "comments": [...]
}
```

Set `event` based on **highest severity across ALL reviewers** (prior + own) using the Severity → Approval table. Do NOT include `commit_id` — `post_review.py` injects it.

### 5. Submit

```bash
./skills/unity-review-shared/scripts/post_review.py <pr_number> /tmp/review-general.json
```

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

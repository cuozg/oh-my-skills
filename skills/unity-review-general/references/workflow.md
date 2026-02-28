# unity-review-general — Workflow

## 1. Collect Prior Reviews

Fetch all comments posted by specialized reviewers (code, architecture, prefab, asset):

```bash
gh api repos/<owner>/<repo>/pulls/<N>/reviews    # Review bodies + states
gh api repos/<owner>/<repo>/pulls/<N>/comments   # Inline comments
```

Parse and categorize findings by severity (🔴🟡🔵🟢). Note the highest severity found across all prior reviewers.

## 2. Fetch PR & Extract Intent

```bash
gh pr diff <N> --name-only
gh pr view <N> --json title,body,files,number
gh pr diff <N>
```

Read PR title/body for intent and acceptance criteria. Count changed lines for checklist focus.

## 3. Apply Checklists

Apply each applicable checklist from `../../unity-shared/references/review-general-checklists.md`:
1. 🔒 Security  2. ✅ Correctness  3. 🧪 Testing  4. 🧹 Code Quality  5. ⚡ Performance  6. 🔄 Lifecycle  7. 📚 Documentation

Also verify: does the PR accomplish what the title/body says? Flag gaps.

## 4. Build `/tmp/review-general.json`

```json
{
  "body": "## Final Quality Review (Approver)\n\n### Prior Review Summary\n[Summarize findings — count by severity]\n\n### General Quality Findings\n**Scope**: [N files, M lines]\n[Checklist findings]\n\n### Decision\n**[APPROVE/REQUEST_CHANGES]** — [reasoning]",
  "event": "REQUEST_CHANGES|COMMENT|APPROVE",
  "comments": [...]
}
```

Set `event` based on **highest severity across ALL reviewers** (prior + own). Do NOT include `commit_id`.

## 5. Submit

```bash
./skills/unity-shared/scripts/review/post_review.py <pr_number> /tmp/review-general.json
```

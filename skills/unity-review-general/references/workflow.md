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

Read PR title/body for intent and acceptance criteria. Count changed lines for checklist focus — see [GENERAL_CHECKLISTS.md](GENERAL_CHECKLISTS.md).

### 3. Apply Checklists

Apply each applicable checklist from [GENERAL_CHECKLISTS.md](GENERAL_CHECKLISTS.md):
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
./skills/unity-shared/scripts/review/post_review.py <pr_number> /tmp/review-general.json
```

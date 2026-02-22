---
name: unity-review-general
description: "Review PRs against general quality checklists — security, correctness, testing, code quality, performance, lifecycle, and documentation. Technology-agnostic checks applied to all file types. After review, pushes comments directly to GitHub via the API. Accepts PR number/URL as input. Use when: reviewing PR quality, security audit, testing coverage review. Triggers: 'general review', 'security review', 'testing review', 'code quality review', 'PR quality review', 'review PR quality'."
---

# General PR Quality Reviewer

Apply technology-agnostic quality checklists to PR changes. Push review comments directly to GitHub via the API.

## Output
Review comments pushed to GitHub PR via API. Covers security, correctness, testing, code quality, performance, lifecycle, documentation.

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
| CLEAN | — | No issues | `APPROVE` |

## PR Size Focus

| Changed Lines | Focus |
|:--------------|:------|
| < 50 | Security + Correctness + Testing only |
| 50–300 | All 7 checklists |
| > 300 | Request split. If not possible, prioritize Security + Correctness. Note scope risk. |

## Workflow

### 1. Fetch PR

```bash
gh pr diff <N> --name-only   # Changed files
gh pr view <N> --json title,body,files,number  # PR context (title/body = intent)
gh pr diff <N>               # Full diff
```

### 2. Extract Intent & Size

Read PR title/body to extract intent and acceptance criteria. Count changed lines to determine checklist focus (see PR Size Focus table).

### 3. Apply Checklists

Apply each applicable checklist from [GENERAL_CHECKLISTS.md](references/GENERAL_CHECKLISTS.md):

1. 🔒 **Security** — secrets, injection, auth, deserialization
2. ✅ **Correctness** — logic vs intent, state transitions, error paths
3. 🧪 **Testing** — coverage for new/modified API, determinism
4. 🧹 **Code Quality** — SRP, method length, duplication, naming
5. ⚡ **Performance** — hot path allocations, data structures, async
6. 🔄 **Lifecycle** — OnEnable/OnDisable pairs, teardown, quit flow
7. 📚 **Documentation** — XML docs, inline comments, breaking change notes

Also verify: does the PR actually accomplish what the title/body says? Flag gaps.

### 4. Build `/tmp/review.json`

```json
{
  "body": "## General Quality Review\n**Scope**: [N files, M lines changed]\n...",
  "event": "REQUEST_CHANGES|COMMENT|APPROVE",
  "comments": [
    {
      "path": "Assets/Scripts/Auth/LoginManager.cs",
      "line": 45,
      "side": "RIGHT",
      "body": "**🔴 Hardcoded API Key**: API key string literal found in source.\n**Evidence**: Line 45 — `private string apiKey = \"sk-...\"`\n**Why**: Secrets in source are exposed in version control and builds.\n```suggestion\nMove to environment config or ScriptableObject excluded from version control.\n```"
    }
  ]
}
```

Do NOT include `commit_id` — `post_review.py` injects it automatically. Set `event` based on highest severity using the Severity → Approval table above.

### 5. Submit

```bash
./skills/unity-review-general/scripts/post_review.py <pr_number> /tmp/review.json
```

Fallback (merged/closed): handled automatically by `post_review.py`.

## Rules

- One issue = one comment. Every comment needs severity + evidence + suggestion.
- Security findings are always 🔴 Critical.
- For PRs > 300 lines, add a comment recommending split.
- Correctness check: verify PR logic matches stated intent from PR title/body.
- Submit even if PR is merged — `post_review.py` handles fallback.
- Never hardcode `commit_id` or modify source files.
- Refer to [GENERAL_CHECKLISTS.md](references/GENERAL_CHECKLISTS.md) for the complete checklist catalog.

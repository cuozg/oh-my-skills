---
name: unity-review-code-pr
description: GitHub PR C# logic review — posts inline comments via gh api. Triggers — 'review PR', 'review pull request', 'PR review', 'check this PR'.
---
# unity-review-code-pr

Fetch a GitHub PR diff, review changed C# files for logic and Unity-specific risks, post inline comments via GitHub API. **NEVER stop until the review is confirmed on GitHub.**

## When to Use

- Reviewing a teammate's open GitHub PR
- Running automated review on a PR before merge
- Need review feedback attached directly to PR lines on GitHub

## Mandatory Rule

**NEVER stop until the review appears on GitHub.** After posting, verify via `gh api …/pulls/{pr}/reviews`.
If the review ID is absent or the call fails — fix the error and retry. Loop until confirmed.

See `references/pr-review-workflow.md` §7 for the exact verify command.

## Workflow

Follow `references/pr-review-workflow.md` (7 steps: resolve owner/repo → fetch files → fetch diff → fetch content → map lines → build + submit → verify).
Build the review JSON per `unity-standards/references/review/pr-submission.md` (line/side/batching rules).

## Review Body Format

Post as the `body` field. Structure:

````
## 📋 Code Review — PR #{number}

{1-2 sentence verdict: scope of changes + key risk area}

| | Category | Findings | Top Severity |
|---|---|:---:|---|
| 💥 | Breaking / Crash Risk | {n} | 🔴 `CRITICAL` |
| ⚠️ | Bugs / Incorrect Behavior | {n} | 🟠 `HIGH` |
| 🎮 | Unity-Specific Risks | {n} | 🟡 `MEDIUM` |
| 💡 | Improvements | {n} | 🔵 `LOW` / ⚪ `STYLE` |

**Decision**: ✅ APPROVE / ❌ REQUEST_CHANGES / 💬 COMMENT
````

Omit rows with 0 findings. Note dead-code or unchanged-line issues below table (no inline comment possible).

## Inline Comment Format

**🔴 Critical / 🟡 High** — full block:

```
**🔴 Issue Title**: One-line problem summary
- **Why**: root cause or risk
- **Fix**: concrete solution
```suggestion
[Fixed code — exact full-line replacement, preserving indentation]
```
```

**🔵 Medium / 🟢 Low** — compact: `**🔵 Issue**: Problem → fix.` + suggestion block.

## Rules

- **MANDATORY**: Never stop until GitHub confirms the review is posted — always verify after submit
- If submit fails (network, auth, rate limit) — fix the issue and retry; never exit without confirmation
- Always fetch full file content, not just diff hunks
- Use severity icons: 🔴 Critical, 🟡 High, 🔵 Medium, 🟢 Low
- Cover: null guards, lifecycle order, event leaks, serialization, hot-path allocations
- Do not post duplicate comments for the same line
- See `unity-standards/references/review/pr-submission.md` for `line`/`side`/batching rules

## Reference Files

- `references/pr-review-workflow.md` — step-by-step PR fetch and review process

Load on demand via `read_skill_file("unity-review-code-pr", "references/{file}")`.

## Standards

Load `unity-standards` for review criteria. Key references:

- `review/logic-checklist.md` — correctness, edge cases, state, data flow
- `review/unity-lifecycle-risks.md` — order-of-execution, null timing, scene load
- `review/serialization-risks.md` — missing fields, type changes, prefab overrides
- `review/performance-checklist.md` — allocations, Update, physics, rendering
- `review/pr-submission.md` — gh api format, comment batching, approval flow

Load via `read_skill_file("unity-standards", "references/review/<file>")`.

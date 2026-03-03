---
name: unity-review-code-pr
description: GitHub PR C# logic review — posts inline comments via gh api. Triggers — 'review PR', 'review pull request', 'PR review', 'check this PR'.
---
# unity-review-code-pr

Fetch a GitHub PR diff, **assess change size**, then review adaptively — quick single-pass for minor PRs, parallel subagents for large ones. Post inline comments via GitHub API. **NEVER stop until the review is confirmed on GitHub.**

## When to Use

- Reviewing a teammate's open GitHub PR
- Running automated review on a PR before merge
- Need review feedback attached directly to PR lines on GitHub

## Mandatory Rules

- **NEVER stop until GitHub confirms the review is posted** — verify via `gh api …/pulls/{pr}/reviews`, retry on failure
- **ALWAYS use the Review Body Format and Inline Comment Format below** — regardless of review mode
- See `references/pr-review-workflow.md` §7 for the exact verify command

## Workflow

1. **Fetch PR data** — follow `references/pr-review-workflow.md` steps 1-4
2. **Assess PR size** — see `references/size-assessment.md` for classification rules
3. **Route by size**:
   - **Minor** → step 4a (quick review)
   - **Large** → step 4b (deep review)
4a. **Quick review** — review all changed files yourself in a single pass; load `unity-standards` checklists, check all 6 criteria inline; produce findings as `[{path, line, severity, title, body}]`
4b. **Deep review** — spawn 6 parallel subagents per `unity-standards/references/review/parallel-review-criteria.md`; collect via `background_output`; aggregate (deduplicate by path+line, keep highest severity, sort file→line)
5. **Map lines** — use right-side file line numbers (step 5 from pr-review-workflow.md)
6. **Build + Submit** — build review JSON per `unity-standards/references/review/pr-submission.md`, submit via `gh api`
7. **Verify** — confirm review posted (step 7 from pr-review-workflow.md), retry on failure

## Review Body Format

Post as the `body` field:

````
## 📋 Code Review — PR #{number}
{1-2 sentence verdict}
| | Category | Findings | Top Severity |
|---|---|:---:|---|
| 💥 | Breaking / Crash Risk | {n} | 🔴 `CRITICAL` |
| ⚠️ | Bugs / Incorrect Behavior | {n} | 🟠 `HIGH` |
| 🎮 | Unity-Specific Risks | {n} | 🟡 `MEDIUM` |
| 💡 | Improvements | {n} | 🔵 `LOW` / ⚪ `STYLE` |
**Decision**: ✅ APPROVE / ❌ REQUEST_CHANGES / 💬 COMMENT
````

Omit rows with 0 findings.

## Inline Comment Format

🔴/🟡 — `**🔴 Issue Title**: summary` + `- **Why**: cause` + `- **Fix**: solution` + suggestion block.
🔵/🟢 — compact: `**🔵 Issue**: Problem → fix.` + suggestion block.

## Rules

- Always fetch full file content, not just diff hunks
- Use severity icons: 🔴 Critical, 🟡 High, 🔵 Medium, 🟢 Low
- Do not post duplicate comments for the same line
- See `unity-standards/references/review/pr-submission.md` for `line`/`side`/batching rules

## Reference Files

- `references/pr-review-workflow.md` — PR fetch, line mapping, submit, verify
- `references/size-assessment.md` — PR size classification and routing rules

Load on demand via `read_skill_file("unity-review-code-pr", "references/{file}")`.

## Standards

Load `unity-standards` for review criteria:

- `review/logic-checklist.md` — correctness, edge cases, state, data flow
- `review/unity-lifecycle-risks.md` — order-of-execution, null timing, scene load
- `review/serialization-risks.md` — missing fields, type changes, prefab overrides
- `review/performance-checklist.md` — allocations, Update, physics, rendering
- `review/architecture-checklist.md` — coupling, SOLID, assembly boundaries, event coupling
- `review/concurrency-checklist.md` — threading, race conditions, async/await, main thread rule
- `review/pr-submission.md` — gh api format, comment batching, approval flow
- `review/parallel-review-criteria.md` — subagent delegation, criteria table, prompt template

Load via `read_skill_file("unity-standards", "references/review/<file>")`.
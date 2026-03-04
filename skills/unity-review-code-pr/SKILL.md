---
name: unity-review-code-pr
description: GitHub PR C# logic review — posts inline comments via gh api. Use this skill whenever the user wants to review a PR, check a pull request, post review comments to GitHub, or run automated review before merge — even if they don't say "PR review" explicitly. Triggers — 'review PR', 'review pull request', 'PR review', 'check this PR', 'give feedback on this PR', 'review before merge'.
---
# unity-review-code-pr

Fetch a GitHub PR diff, **assess change size**, then review adaptively — quick single-pass for minor PRs, parallel subagents for large ones. Post inline comments via GitHub API. **Never stop until the review is confirmed posted on GitHub.**

## Workflow

1. **Fetch PR data** — follow `references/pr-review-workflow.md` steps 1-4
2. **Assess PR size** — see `references/size-assessment.md` for classification rules
3. **Route by size**:
   - **Minor** → step 4a (quick review)
   - **Large** → step 4b (deep review)
4a. **Quick review** — review all changed files yourself in a single pass; load `unity-standards` checklists, check all 6 criteria inline; produce findings as `[{path, line, severity, title, body}]`
4b. **Deep review** — spawn 6 parallel subagents per `unity-standards/references/review/parallel-review-criteria.md`; collect via `background_output`; aggregate (deduplicate by path+line, keep highest severity, sort file→line)
5. **Map lines** — use right-side file line numbers (step 5 from `references/pr-review-workflow.md`)
6. **Build + Submit** — build review JSON per `unity-standards/references/review/pr-submission.md` (JSON payload, event decision, batching rules, gh CLI), submit via `gh api`
7. **Verify** — confirm review posted (step 7 from `references/pr-review-workflow.md`), retry on failure until confirmed

## Review Body Format

Post as the `body` field of the review:

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

**Critical / High (🔴 🟠):** `**🔴 Issue Title**: summary` + `- **Why**: cause` + `- **Fix**: solution` + suggestion block.

**Medium / Low / Style (🟡 🔵 ⚪):** compact: `**🟡 Issue**: Problem → fix.` + suggestion block.

Severity scale: 🔴 CRITICAL → 🟠 HIGH → 🟡 MEDIUM → 🔵 LOW → ⚪ STYLE

## Rules

- Always fetch full file content — diff hunks lack context especially for lifecycle analysis
- Do not post duplicate comments for the same line
- See `unity-standards/references/review/pr-submission.md` for `line`/`side`/batching rules

## Reference Files

- `references/pr-review-workflow.md` — PR fetch, line mapping, submit, verify
- `references/size-assessment.md` — PR size classification and routing rules

Load on demand via `read_skill_file("unity-review-code-pr", "references/{file}")`.

## Standards

Load `unity-standards` for all review criteria. Load on demand via `read_skill_file("unity-standards", "references/review/<file>")`:

- `review/logic-checklist.md` — correctness, edge cases, state, data flow
- `review/unity-lifecycle-risks.md` — order-of-execution, null timing, scene load
- `review/serialization-risks.md` — missing fields, type changes, prefab overrides
- `review/performance-checklist.md` — allocations, Update, physics, rendering
- `review/architecture-checklist.md` — coupling, SOLID, assembly boundaries, event coupling
- `review/concurrency-checklist.md` — threading, race conditions, async/await, main thread rule
- `review/security-checklist.md` — input validation, injection, data exposure
- `review/pr-submission.md` — output template: JSON payload, event decision, batching, gh CLI
- `review/parallel-review-criteria.md` — subagent delegation, criteria table, prompt template
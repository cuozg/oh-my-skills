---
name: unity-review-code-pr
description: GitHub PR C# logic review — posts inline comments via gh api. Triggers — 'review PR', 'review pull request', 'PR review', 'check this PR'.
---
# unity-review-code-pr

Fetch a GitHub PR diff, review changed C# files using **parallel subagents** (one per review criterion), aggregate findings, post inline comments via GitHub API. **NEVER stop until the review is confirmed on GitHub.**

## When to Use

- Reviewing a teammate's open GitHub PR
- Running automated review on a PR before merge
- Need review feedback attached directly to PR lines on GitHub

## Mandatory Rule

**NEVER stop until the review appears on GitHub.** After posting, verify via `gh api …/pulls/{pr}/reviews`.
If the review ID is absent or the call fails — fix the error and retry. Loop until confirmed.

See `references/pr-review-workflow.md` §7 for the exact verify command.

## Workflow

1. **Fetch PR data** — follow `references/pr-review-workflow.md` steps 1-4 (resolve owner/repo → fetch files → fetch diff → fetch full file content)
2. **Spawn 6 parallel subagents** — one `task(category="quick", load_skills=["unity-standards"], run_in_background=true)` per review criterion (see `unity-standards/references/review/parallel-review-criteria.md`)
3. **Each subagent** — loads its assigned checklist from `unity-standards`, reviews ONLY its criterion, returns findings as `[{path, line, severity, title, body}]`
4. **Collect results** — `background_output` on all 6 tasks
5. **Aggregate** — deduplicate by (path, line), keep highest severity, sort by file → line
6. **Map lines** — use right-side file line numbers (step 5 from pr-review-workflow.md)
7. **Build + Submit** — build review JSON per `unity-standards/references/review/pr-submission.md`, submit via `gh api`
8. **Verify** — confirm review posted (step 7 from pr-review-workflow.md), retry on failure

## Review Criteria (6 parallel subagents)

| # | Criterion | Checklist |
|---|-----------|-----------|
| 1 | Logic | `review/logic-checklist.md` |
| 2 | Lifecycle | `review/unity-lifecycle-risks.md` |
| 3 | Serialization | `review/serialization-risks.md` |
| 4 | Performance | `review/performance-checklist.md` |
| 5 | Architecture | `review/architecture-checklist.md` |
| 6 | Concurrency | `review/concurrency-checklist.md` |

See `unity-standards/references/review/parallel-review-criteria.md` for subagent prompt template and aggregation rules.

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

- **MANDATORY**: Never stop until GitHub confirms the review is posted — always verify after submit
- If submit fails (network, auth, rate limit) — fix the issue and retry; never exit without confirmation
- Always fetch full file content, not just diff hunks
- Use severity icons: 🔴 Critical, 🟡 High, 🔵 Medium, 🟢 Low
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
- `review/architecture-checklist.md` — coupling, SOLID, assembly boundaries, event coupling
- `review/concurrency-checklist.md` — threading, race conditions, async/await, main thread rule
- `review/pr-submission.md` — gh api format, comment batching, approval flow
- `review/parallel-review-criteria.md` — subagent delegation, criteria table, prompt template

Load via `read_skill_file("unity-standards", "references/review/<file>")`.

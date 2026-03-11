---
name: unity-review-code-pr
description: >
  Use this skill to review Unity C# code in a GitHub Pull Request — fetches the diff, reviews for logic
  correctness, Unity lifecycle risks, serialization issues, performance concerns, and posts inline
  comments via GitHub API. Use whenever the user wants to review a PR, check a pull request, or get
  automated feedback before merge — even if they don't say "PR review" explicitly. Adapts review depth
  to PR size. For local file review (not on GitHub), use unity-review-code-local.
metadata:
  author: kuozg
  version: "1.0"
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
4b. **Deep review** — spawn 7 parallel subagents per `unity-standards/references/review/parallel-review-criteria.md`; collect via `background_output`; aggregate (deduplicate by path+line, keep highest severity, sort file→line)
6. **Map lines** — use right-side file line numbers (step 5 from `references/pr-review-workflow.md`)
7. **Build + Submit** — build review JSON per `unity-standards/references/review/pr-submission.md`, submit via `gh api`
8. **Verify** — confirm review posted (step 7 from `references/pr-review-workflow.md`), retry on failure until confirmed


## Inline Comment Format

Every finding MUST use this template. The `suggestion` block is **required for MEDIUM severity and above** — show the corrected code, even if multi-line.

**Template:**
````
**{🔴|🟠|🟡|🔵|⚪} Title** — `SEVERITY`

{1-3 lines: what is wrong, why it matters}

```suggestion
{corrected code replacing the commented line(s)}
```
````

**Critical/High (🔴🟠)** — include cause, impact, and `suggestion` block.
**Medium (🟡)** — problem + `suggestion` block.
**Low/Style (🔵⚪)** — compact; `suggestion` encouraged but optional.

Severity scale: 🔴 CRITICAL → 🟠 HIGH → 🟡 MEDIUM → 🔵 LOW → ⚪ STYLE

## Severity Calibration

Minimum floors — do not rate below these:

- `GetComponent`/`Find*` called every frame (Update/FixedUpdate/LateUpdate) → **MEDIUM**
- Missing event unsubscription (`+=` without matching `-=` in OnDestroy/OnDisable) → **HIGH**
- Coroutine not stopped on lifecycle exit (OnDisable/OnDestroy) → **HIGH**
- `async void` on any method (swallows exceptions) → **MEDIUM**
- Exposed internal collection (returning `List<T>` instead of `IReadOnlyList<T>`) → **MEDIUM**
- `Resources.Load<T>()` called at runtime outside initialization (Awake/Start/constructor) → **MEDIUM**

## Rules

- Always fetch full file content — diff hunks lack context for lifecycle and event cleanup analysis
- Prioritize finding coverage: identify all issues first, then format with suggestion blocks. Do not let formatting effort reduce the number of issues found.
- Every finding at MEDIUM severity or above must include a `suggestion` code block
- Do not post duplicate comments for the same line
- See `unity-standards/references/review/pr-submission.md` for review body format, inline comment examples, and `line`/`side`/batching rules

## Reference Files

- `references/pr-review-workflow.md` — PR fetch, line mapping, submit, verify
- `references/size-assessment.md` — PR size classification and routing rules

Load on demand via `read_skill_file("unity-review-code-pr", "references/{file}")`.

## Standards

Load `unity-standards` for all review criteria. Load on demand via `read_skill_file("unity-standards", "references/review/<file>")`:

- `review/logic-checklist.md` — correctness, edge cases, state, data flow
- `review/unity-lifecycle-risks.md` — order-of-execution, null timing, scene load, cleanup pairs
- `review/serialization-risks.md` — missing fields, type changes, prefab overrides
- `review/performance-checklist.md` — allocations, Update, physics, rendering
- `review/architecture-checklist.md` — coupling, SOLID, assembly boundaries, event coupling
- `review/concurrency-checklist.md` — threading, race conditions, async/await, main thread rule
- `review/security-checklist.md` — input validation, injection, data exposure
- `review/pr-submission.md` — output template: JSON payload, event decision, batching, gh CLI
- `review/parallel-review-criteria.md` — subagent delegation, criteria table, prompt template

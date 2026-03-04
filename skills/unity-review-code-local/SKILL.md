---
name: unity-review-code-local
description: Local C# logic review — adds inline REVIEW comments to changed files. Triggers — 'review my code', 'code review', 'review local', 'check my changes', 'review this file'.
---
# unity-review-code-local

Add inline `// ── REVIEW` comments to locally changed C# files using **parallel subagents** (one per review criterion). Apply safe fixes inline. Covers logic, lifecycle, serialization, performance, architecture, concurrency.

## When to Use

- Reviewing uncommitted or staged changes before a commit
- Checking a single file or feature for correctness issues
- Wanting reviewer feedback without opening a GitHub PR

## Workflow

1. **Fetch changes** — run `git diff HEAD` (or `git diff --cached`) to get changed files and hunks
2. **Read changed files** — load full file content for each `.cs` file in the diff
3. **Spawn 6 parallel subagents** — one `task(category="quick", load_skills=["unity-standards"], run_in_background=true)` per review criterion (see `unity-standards/references/review/parallel-review-criteria.md`)
4. **Each subagent** — loads its assigned checklist from `unity-standards`, reviews ONLY its criterion, returns findings as `[{path, line, severity, title, body}]`
5. **Collect results** — `background_output` on all 6 tasks
6. **Aggregate** — deduplicate by (path, line), keep highest severity, sort by file → line
7. **Investigate context** — use `lsp_goto_definition` / `lsp_find_references` to validate findings that need caller/lifecycle context
8. **Annotate** — insert `// ── REVIEW` comments with `What:` / `Why:` lines above the issue line
9. **Apply fixes** — rewrite the problem line when fix is safe (single-line, no cross-file deps); leave unchanged otherwise
10. **Queue fixes** — create `task_create` entries for issues that could not be applied inline

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

## Rules

- Insert comments at the exact line of concern, not at the top of the file
- Use format from `unity-standards/references/review/comment-format.md` for every comment
- Use icon + label + tag: `🔴 CRITICAL`, `🟠 HIGH`, `🟡 MEDIUM`, `🔵 LOW`, `⚪ STYLE`
- Apply safe single-line fixes directly (null checks, caching, unsubscribes); leave complex/design fixes as comments only
- Never commit changes — leave diff for user inspection
- Always read the full file, not just the diff hunk
- Use `lsp_find_references` before flagging a method as unused or dead code
- Flag `Update()` allocations (LINQ, string concat, closures) as MEDIUM or higher
- Flag missing `OnDestroy` unsubscription when `OnEnable` subscribes to events
- Create `task_create` only for issues NOT fixed inline

## Output Format

Inline `// ── REVIEW` comments with icons inserted into source files. Safe fixes applied directly to code.
A summary list of remaining unfixed issues (with created fix tasks) is printed after annotation.

## Standards

Load `unity-standards` for review criteria. Key references:

- `review/logic-checklist.md` — correctness, edge cases, state, data flow
- `review/unity-lifecycle-risks.md` — order-of-execution, null timing, scene load
- `review/serialization-risks.md` — missing fields, type changes, prefab overrides
- `review/performance-checklist.md` — allocations, Update, physics, rendering
- `review/architecture-checklist.md` — coupling, SOLID, assembly boundaries, event coupling
- `review/concurrency-checklist.md` — threading, race conditions, async/await, main thread rule
- `review/comment-format.md` — inline review comment syntax and severity
- `review/parallel-review-criteria.md` — subagent delegation, criteria table, prompt template

Load via `read_skill_file("unity-standards", "references/review/<file>")`.

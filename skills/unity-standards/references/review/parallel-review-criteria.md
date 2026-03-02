# Parallel Review Criteria

## Subagent Delegation Model

Spawn **one subagent per criterion** via `task(category="quick", load_skills=["unity-standards"], run_in_background=true)`.
Each subagent receives: file paths, file contents, diff hunks, and its assigned checklist.

## Criteria Table

| # | Criterion | Checklist Reference | Focus |
|---|-----------|-------------------|-------|
| 1 | Logic | `review/logic-checklist.md` | Null guards, boundaries, edge cases, state, data flow |
| 2 | Lifecycle | `review/unity-lifecycle-risks.md` | Execution order, destroy timing, coroutines, subscribe symmetry |
| 3 | Serialization | `review/serialization-risks.md` | Field renames, type changes, SO risks, prefab overrides, enums |
| 4 | Performance | `review/performance-checklist.md` | Hot-path allocations, component lookup, physics, rendering, memory |
| 5 | Architecture | `review/architecture-checklist.md` | SRP, dependency direction, assembly defs, event coupling, interfaces |
| 6 | Concurrency | `review/concurrency-checklist.md` | Main thread rule, async/await, Job System, race conditions |

## Subagent Prompt Template

```
TASK: Review these C# files for {criterion_name} issues only.
CHECKLIST: Load `read_skill_file("unity-standards", "references/{checklist_path}")` and check every item.
FILES: {file_paths_and_contents}
DIFF: {diff_hunks}

MUST DO:
- Read the checklist reference FIRST
- Check EVERY item in the checklist against the changed code
- Report findings as JSON array: [{path, line, severity, title, body}]
- severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "STYLE"
- body: Use format from `review/comment-format.md` (PR) or inline REVIEW format (local)
- Focus ONLY on your assigned criterion — skip others
- Return empty array if no issues found

MUST NOT DO:
- Review criteria outside your assigned category
- Skip checklist items without checking
- Report issues on unchanged lines (PR mode only)
- Duplicate findings already covered by another criterion
```

## Aggregation

After all 6 subagents complete:
1. Collect all findings arrays
2. Deduplicate by (path, line) — keep highest severity
3. Sort by file → line number
4. Build final output (PR JSON or inline REVIEW comments)

## Severity Precedence

CRITICAL > HIGH > MEDIUM > LOW > STYLE
When two findings hit the same line, keep the higher severity and merge descriptions.

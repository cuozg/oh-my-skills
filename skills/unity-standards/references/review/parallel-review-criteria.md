# Parallel Review Criteria

Spawn **one subagent per criterion** via `task(category="quick", load_skills=["unity-standards"], run_in_background=true)`.
Each subagent receives: file paths, file contents, diff hunks, and its assigned checklist section.

All criteria reference sections of `review/checklist.md`.

## Criteria Table

| # | Criterion | Checklist Section | Focus |
|---|-----------|-------------------|-------|
| 1 | Logic | `## 1. Logic` | Null guards, boundaries, edge cases, state, data flow |
| 2 | Unity Lifecycle | `## 2. Unity Lifecycle` | Execution order, destroy timing, subscribe symmetry, cleanup pairs |
| 3 | Serialization | `## 3. Serialization` | Field renames, type changes, enum stability, SO risks |
| 4 | Performance | `## 4. Performance` | Hot-path allocations, component lookup, physics, rendering |
| 5 | Security | `## 5. Security` | Input validation, secrets, debug code, network |
| 6 | Concurrency | `## 6. Concurrency` | Main thread rule, async/await, Jobs, race conditions |

Architecture (§7) and Assets/Prefabs (§8) are checked by criteria 1-6 where overlap exists, or by a dedicated asset review subagent for asset-heavy PRs.

## Subagent Prompt Template

```
TASK: Review these C# files for {criterion_name} issues only.
CHECKLIST: Load `read_skill_file("unity-standards", "references/review/checklist.md")` — check every item under section {section_number}.
FILES: {file_paths_and_contents}
DIFF: {diff_hunks}

MUST DO:
- Check EVERY item in your assigned section against the changed code
- Report as JSON array: [{path, line, severity, title, body}]
- severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "STYLE"
- Focus ONLY on your assigned criterion
- Return empty array if no issues found

MUST NOT DO:
- Review criteria outside your assigned section
- Report issues on unchanged lines (PR mode only)
```

## Aggregation

1. Collect all findings arrays
2. Deduplicate by (path, line) — keep highest severity
3. Sort by file → line number
4. Build final output (PR JSON or inline REVIEW comments)

Severity precedence: CRITICAL > HIGH > MEDIUM > LOW > STYLE

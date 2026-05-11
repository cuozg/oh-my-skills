# Parallel Review Criteria

Spawn **one subagent per file type** run in background.
Each subagent receives: file paths, file contents, diff hunks for its assigned file type ONLY. Do not pass diffs of other file types.

## Criteria Table

| File Type | Reference File | Focus |
| --------- | -------------- | ----- |
| `.cs` | `review/checklist_cs.md` | Logic, Lifecycle, Performance, Serialization, Concurrency, etc. |
| `.prefab`, `.unity` | `review/checklist_prefab.md` | Hierarchy, overrides, missing scripts, scene references |
| `.mat` | `review/checklist_material.md` | GPU instancing, shared materials, properties |
| `.shader` | `review/checklist_shader.md` | Render queue, fallbacks, passes, properties |

## Subagent Prompt Template

```text
TASK: Review these files for {file_type} issues only.
CHECKLIST: Load `read_skill_file("unity-standards", "references/{reference_file}")` — check every item.
FILES: {file_paths_and_contents}
DIFF: {diff_hunks}

MUST DO:
- Check EVERY item in your assigned checklist against the changed code
- Report as JSON array: [{path, line, severity, title, body}]
- severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "STYLE"
- Focus ONLY on your assigned file type
- Return empty array if no issues found

MUST NOT DO:
- Review files outside your assigned file type
- Report issues on unchanged lines (PR mode only)
```

## Aggregation

1. Collect all findings arrays
2. Deduplicate by (path, line) — keep highest severity
3. Sort by file → line number
4. Build final output (PR JSON or inline REVIEW comments)

Severity precedence: CRITICAL > HIGH > MEDIUM > LOW > STYLE

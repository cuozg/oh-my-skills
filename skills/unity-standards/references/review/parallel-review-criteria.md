# Parallel Review Criteria

Use parallel review only for large diffs with multiple file types. Assign one
review pass per file type, either to available subagents or to separate focused
local passes. Each pass receives only the file paths, file contents, and diff
hunks for its assigned file type.

**Rule: Fast and Focused Reading**

- Review diff hunks first.
- Only fetch surrounding methods/assets when needed.
- Do not read full file by default. (Why: faster, less noise).
- Do not review non-C# assets unless they are changed or the user asks.

## Criteria Table

| File Type               | Reference File                   | Focus                                                           |
| ----------------------- | -------------------------------- | --------------------------------------------------------------- |
| `.cs`                 | `checklist_cs.md`       | Logic, Lifecycle, Performance, Serialization, Concurrency, etc. |
| `.prefab`, `.unity` | `checklist_prefab.md`   | Hierarchy, overrides, missing scripts, scene references         |
| `.mat`                | `checklist_material.md` | GPU instancing, shared materials, properties                    |
| `.shader`             | `checklist_shader.md`   | Render queue, fallbacks, passes, properties                     |

## Focused Review Prompt Template

```text
TASK: Review these files for {file_type} issues only.
CHECKLIST: Load `unity-standards/references/review/{reference_file}` - check every item.
FILES: {file_paths_and_contents}
DIFF: {diff_hunks}

MUST DO:
- Check EVERY item in your assigned checklist against the changed code.
- Report as JSON array with strict schema:
  [{
    "path": string,
    "line": number,
    "severity": "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "STYLE",
    "title": string,
    "impact": string,
    "evidence": string,
    "false_positive_check": string,
    "fix_direction": string,
    "inline_safe": boolean
  }]
- Focus ONLY on your assigned file type.
- Return empty array if no issues found.

MUST NOT DO:
- Review files outside your assigned file type.
- Report issues on unchanged lines (PR mode only).
```

## Large Asset Strategy (Prefabs / Scenes)

If GitHub patch is missing or file is too large:

- Do not force inline comment (`inline_safe: false`).
- Report as body findings with the following structure:
  - prefab path
  - GameObject name
  - component type
  - serialized field name
  - bad value
  - expected fix

Example:

```text
`Assets/_lowrez/.../low_UniversalSystemPopup.prefab`
GameObject: UniversalSystemPopup
Component: UPSystemPopupController
Fields: userInputField, noticeText
Issue: both are `{fileID: 0}`, InputText layout crashes.
Expected Fix: Assign valid references.
```

## Aggregation

1. Collect all findings arrays.
2. Aggregator reviews evidence before submitting findings.
3. Deduplicate by (path, line) - keep highest severity.
4. Sort by severity, then file and line number.
5. Build final output (PR JSON or inline REVIEW comments).

Severity precedence: CRITICAL > HIGH > MEDIUM > LOW > STYLE

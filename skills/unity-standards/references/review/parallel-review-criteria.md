# Parallel Review Criteria

Spawn **one subagent per file type** run in background.
Each subagent receives: file paths, file contents, diff hunks for its assigned file type ONLY. Do not pass diffs of other file types.

**Rule: Fast and Focused Reading**

- Review diff hunks first.
- Only fetch surrounding methods/assets when needed.
- Do not read full file by default. (Why: faster, less noise).
- Do not review other than .cs file, except the user ask.

## Criteria Table

| File Type               | Reference File                   | Focus                                                           |
| ----------------------- | -------------------------------- | --------------------------------------------------------------- |
| `.cs`                 | `review/checklist_cs.md`       | Logic, Lifecycle, Performance, Serialization, Concurrency, etc. |
| `.prefab`, `.unity` | `review/checklist_prefab.md`   | Hierarchy, overrides, missing scripts, scene references         |
| `.mat`                | `review/checklist_material.md` | GPU instancing, shared materials, properties                    |
| `.shader`             | `review/checklist_shader.md`   | Render queue, fallbacks, passes, properties                     |

## Subagent Prompt Template

```text
TASK: Review these files for {file_type} issues only.
CHECKLIST: Load `read_skill_file("unity-standards", "references/{reference_file}")` — check every item.
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
2. Aggregator can trust the detailed schema and submit faster.
3. Deduplicate by (path, line) — keep highest severity.
4. Sort by file → line number.
5. Build final output (PR JSON or inline REVIEW comments).

Severity precedence: CRITICAL > HIGH > MEDIUM > LOW > STYLE

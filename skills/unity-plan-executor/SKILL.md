---
description: 'Execute Unity implementation plans from HTML files with 100% accuracy.
  Apply exact code changes to C# scripts, MonoBehaviours, ScriptableObjects, prefabs,
  and Unity assets. Use when: (1) Plan HTML file from Documents/Plans/*.html is ready,
  (2) Code changes in split diff view must be applied exactly to Unity project, (3)
  Implementing Unity features with no interpretation - execute exactly as shown, (4)
  Applying scripted changes to Unity C# codebase. Triggers: ''execute plan'', ''apply
  plan'', ''implement from HTML'', ''run plan executor'', ''apply Unity changes'',
  ''execute implementation''.'
name: unity-plan-executor
---

# Unity Plan Executor

**Input**: Plan HTML at `Documents/Plans/[FeatureName]_PLAN.html` with GitHub-style split diff views

## Output

Exact code changes applied to Unity project files matching the plan specification 100%.

## Workflow

### Phase 1: Parse HTML Plan
1. Extract task table from `<table class="task-table">`
2. Extract file diffs from `<div class="file-diff">` sections
3. For each diff: file path from `.file-path`, action from `.badge-*` (MODIFIED/NEW/DELETED)
4. Parse diff lines: `diff-line-deletion`→REMOVE, `diff-line-addition`→ADD, `diff-line-context`→verify only

### Phase 2: Apply Changes Exactly
1. Open target file, locate context lines
2. DELETE `-` lines, ADD `+` lines, word highlights (`<x>`, `<y>`) show specific changes
3. Save file

**CRITICAL RULES**:
- ❌ Do NOT paraphrase, add unlisted code, skip changes, or modify order
- ✅ Apply 100% exactly as displayed

### Phase 3: Create New Files
- Create at exact path, add all `+` lines in order, UTF-8 encoding

### Phase 4: Verify
- `unityMCP_check_compile_errors` → fix immediately on failure
- `unityMCP_get_unity_logs(show_errors=true)` → address errors

### Phase 5: Git Commit
```bash
git add -A && git commit -m "[TYPE]: Title (50 chars max, imperative)

- What/why changed
- Files affected"
```
Types: `feat:` `fix:` `refactor:` `ui:` `perf:`

## Error Recovery

1. **Context mismatch** — search for context elsewhere in file
2. **Compile error** — re-check diff application
3. **Missing dependencies** — create files in dependency order

## Checklist

- [ ] All file diffs applied exactly
- [ ] All new files created
- [ ] Unity compiles without errors
- [ ] Git commit created

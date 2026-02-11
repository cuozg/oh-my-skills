---
name: unity-plan-executor
description: "Execute implementation plans from HTML files with 100% accuracy. Use when: (1) Plan HTML file from Documents/Plans/*.html is ready, (2) Code changes shown in split diff view must be applied exactly, (3) No interpretation - implement exactly as shown."
---

# Unity Plan Executor

Execute implementation plans with **100% accuracy**. Apply code changes exactly as shown in the HTML plan file.

## Input Requirement

**Plan HTML file**: `Documents/Plans/[FeatureName]_PLAN.html`

The HTML file contains GitHub-style split diff views showing exact code changes to apply.

## Execution Protocol

### Phase 1: Parse HTML Plan File

1. **Read the plan file** and extract:
   - Task table entries from `<table class="task-table">`
   - All file diffs from `<div class="file-diff">` sections
   - File paths from `.file-path` elements
   - Line numbers and code changes from diff rows

2. **For each file diff section**:
   - Extract file path from `.file-path`
   - Identify action: MODIFIED, NEW, or DELETED from `.badge-*` class
   - Parse all diff lines:
     - `diff-line-deletion` → Lines to REMOVE
     - `diff-line-addition` → Lines to ADD
     - `diff-line-context` → Context lines (verify, don't modify)

### Phase 2: Apply Changes Exactly

For each file in the plan:

```
1. Open the target file
2. Locate the context lines (use line numbers as guide)
3. Apply changes EXACTLY:
   - DELETE lines marked with `-` (class: diff-line-deletion)
   - ADD lines marked with `+` (class: diff-line-addition)
   - Word highlights (<x>, <y>) show specific changes within lines
4. Save the file
```

**CRITICAL RULES**:
- ❌ Do NOT paraphrase or reinterpret code
- ❌ Do NOT add code not shown in the plan
- ❌ Do NOT skip any changes
- ❌ Do NOT modify the order of operations
- ✅ Apply 100% exactly as displayed

### Phase 3: Create New Files

For files marked as NEW:
1. Create the file at the exact path shown
2. Add all lines marked with `+` in order
3. Ensure UTF-8 encoding

### Phase 4: Verify Implementation

| Check | Action | On Failure |
|-------|--------|------------|
| **Compile** | `coplay-mcp_check_compile_errors` | Fix immediately |
| **Console** | `coplay-mcp_get_unity_logs(show_errors=true)` | Address errors |

### Phase 5: Git Commit

After successful implementation:

```bash
git add -A
git commit -m "[TYPE]: Meaningful title

Detailed description of changes:
- What was changed
- Why it was changed
- Files affected"
```

**Commit Message Format**:
- `feat:` New feature implementation
- `fix:` Bug fixes
- `refactor:` Code refactoring
- `ui:` UI/UX changes
- `perf:` Performance improvements

**Title**: 50 characters max, imperative mood
**Body**: Explain what and why, not how

## Error Recovery

1. **Context mismatch**: Lines not at expected location
   - Search for context in file
   - Apply at correct location

2. **Compile error**:
   - Re-check diff application
   - Verify all changes applied exactly

3. **Missing dependencies**:
   - Check if files need to be created first
   - Apply in dependency order

## Execution Checklist

Before completing:

- [ ] All file diffs applied exactly
- [ ] All new files created
- [ ] Unity compiles without errors
- [ ] Git commit created with meaningful message

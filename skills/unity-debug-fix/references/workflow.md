# Unity Debug Fix — Workflow

## Step 1: Parse Error

Extract from user input:
- **Error type**: compiler error (CS####), runtime exception, logic bug
- **File path**: where the error occurs
- **Line number**: exact location if available
- **Stack trace**: call chain for runtime errors
- **Context**: what the user was doing when it occurred

## Step 2: Investigate

### Tool Selection

| Need | Tool |
|:-----|:-----|
| Read target code | `read` |
| Find definition | `lsp_goto_definition` |
| Find all usages | `lsp_find_references` |
| Pattern search | `grep` / `ast_grep_search` |
| Check diagnostics | `lsp_diagnostics` |
| Blast radius | `impact-analyzer` |

### Common Error Quick-Check

Before deep investigation, check `../../unity-shared/references/common-fixes.md` for known patterns:
- NullReferenceException → missing null guard or uninitialized field
- MissingReferenceException → destroyed object access
- IndexOutOfRange → unchecked collection access
- CS0246 (type not found) → missing using directive or assembly reference
- CS0103 (name not found) → typo, wrong scope, missing import

### Deep Investigation (if not a common error)

1. Read the error file ±50 lines around the error location
2. Trace the data flow — who sets the value that causes the error?
3. Check lifecycle — is the object initialized when accessed?
4. Check threading — async/callback boundary issues?

## Step 3: Apply Fix

1. Determine the minimal change needed
2. Apply the fix using code editing — ONLY the target file(s)
3. Do NOT refactor, rename, or reorganize unrelated code
4. Do NOT add features or "improvements" beyond the fix

### Fix Category Guide

| Fix Type | Approach |
|:---------|:---------|
| Missing null check | Add guard clause |
| Wrong type/cast | Fix the type reference |
| Missing import | Add `using` directive |
| Logic error | Fix the condition/calculation |
| Lifecycle issue | Reorder init or add null-safe access |
| Missing reference | Wire up the dependency |

## Step 4: Verify

```
lsp_diagnostics on every changed file
```

- **Zero errors** → fix successful
- **New errors** → fix introduced regression, investigate and fix those too
- **Same error** → fix didn't address root cause, re-investigate

## Step 5: Loop

After successful fix:
> ✅ Fixed `{error}` in `{file}`. Any other issues? (or type `stop` to end)

If fix fails, report why and ask how to proceed.

## Rules

- ALWAYS use `lsp_diagnostics` after every fix — no exceptions
- NEVER commit — user decides when to commit
- NEVER modify unrelated files
- If multiple errors exist, fix them one at a time, verify each
- For architectural fixes (2+ systems affected), delegate to `unity-code-deep`

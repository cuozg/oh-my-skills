---
name: unity-debug-fix
description: "Analyze Unity errors and apply targeted fixes. Parse error messages, stack traces, or issue descriptions — investigate root cause, determine the minimal fix, apply the change, and verify with diagnostics. Loops until all issues are resolved. This skill should be used when: (1) user provides an error and wants it fixed, (2) compiler errors need resolution, (3) runtime exceptions need fixing, (4) 'fix this error', (5) 'resolve this issue', (6) 'fix and verify'."
---

# Unity Debug Fix

Analyze errors, apply targeted fixes, verify with diagnostics. Loop until resolved.

**Input**: Error message, stack trace, issue description, or file path with error.
**Output**: Fixed code with zero compile errors. No report — fixes applied directly.

## Workflow

Follow the workflow in `references/workflow.md`:

1. **Parse** — Extract error type, file, line, stack trace
2. **Investigate** — Read target code, trace root cause
3. **Fix** — Apply minimal, targeted change
4. **Verify** — Run `lsp_diagnostics`, confirm zero errors
5. **Loop** — Ask user if more issues exist

## Rules

- **Fix ONLY the reported issue** — no refactoring, no scope creep
- **Minimal changes** — smallest possible edit to resolve the error
- **Always verify** — `lsp_diagnostics` on every changed file after fix
- **No commits** — fix and verify only, user decides when to commit
- **Common errors first** — check common-fixes.md (loaded below) for known patterns before deep investigation
- **Delegate complex fixes** — for architectural fixes, delegate to `unity-code-deep`

## Shared References

Load shared debug resources from `unity-shared`:

```python
read_skill_file("unity-shared", "references/debug/common-fixes.md")
```

## Reference Files
- workflow.md — Step-by-step fix workflow with tool selection and verification

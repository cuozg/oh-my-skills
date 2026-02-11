---
description: Diagnose and fix Unity compiler errors, exceptions, and build failures
agent: build
---

Load the `unity/unity-fix-errors` skill and fix the reported errors.

## Task

$ARGUMENTS

## Workflow

1. **Identify** all errors - check Unity console logs, compiler output, or user-provided stack traces
2. **Diagnose** root cause for each error systematically
3. **Fix** each error with minimal, targeted changes
4. **Verify** fixes compile cleanly with `lsp_diagnostics`
5. **Report** what was fixed and why

If no specific errors are mentioned, check for compiler errors using `lsp_diagnostics` and Unity console logs.

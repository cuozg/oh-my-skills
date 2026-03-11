---
name: unity-debug-fix
description: >
  Use this skill to auto-fix Unity compile and runtime errors in a loop — parse error, locate root cause,
  apply minimal fix, verify with lsp_diagnostics, repeat until zero errors. Use when the user has compiler
  errors after a merge, refactor, or package update, or runtime exceptions with a clear stack trace.
  Use when they say "fix this error," "auto fix," "resolve these compile errors," or paste an error
  message. Do not use for behavioral bugs with no error — use unity-debug-quick for that.
metadata:
  author: kuozg
  version: "1.0"
---
# unity-debug-fix

Automated fix loop: parse error → locate root cause → minimal fix → verify → repeat until zero diagnostics.

## When to Use

- Compiler errors after a merge, refactor, or package update
- Runtime exceptions with a clear stack trace
- Cascading errors from a renamed or deleted symbol
- Rapid error-clearing before switching to feature work

## Workflow

1. **Parse** — extract error type, message, file, and line from the error output or user message
2. **Locate** — read the file at the reported line; trace to the actual root cause (not just symptom)
3. **Fix** — apply the minimal change that resolves the root cause
4. **Verify** — run lsp_diagnostics on every changed file; check for new errors introduced
5. **Loop** — if errors remain, return to step 1 with updated context; continue until zero errors

## Rules

- Apply minimal changes only — never refactor while fixing
- Fix root causes, not symptoms (e.g., fix the missing method, not callers that fail because of it)
- Read the full file before editing — never edit blind
- Run lsp_diagnostics after every individual file change
- Never suppress errors with pragmas or empty catch blocks
- If a fix introduces new errors, revert and try a different approach
- Resolve errors in dependency order — fix base classes before derived classes
- Never change public API (method signatures, field names) without checking all callers first
- Ask for confirmation before deleting or renaming symbols
- Stop the loop and report if more than 5 iterations pass without progress
- Always verify the final state shows zero errors before declaring done

## Output Format

Fixed code with zero lsp_diagnostics errors. Brief summary: files changed, root causes resolved, error count before/after.

## Standards

Load `unity-standards` for error context. Key references:

- `debug/common-unity-errors.md` — NRE, serialization, lifecycle, physics
- `code-standards/lifecycle.md` — Awake/Start/OnEnable order, coroutine rules
- `code-standards/null-safety.md` — null checks, TryGet, nullable patterns

Load via `read_skill_file("unity-standards", "references/<path>")`.

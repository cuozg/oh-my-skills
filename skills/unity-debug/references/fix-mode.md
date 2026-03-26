# Fix Mode — Auto-Fix Loop

Automated error resolution: parse → locate root cause → propose approaches → fix → verify → loop.

## When to Use

- Compiler errors after merge, refactor, or package update
- Runtime exceptions with a clear stack trace and CS#### code
- Cascading errors from a renamed or deleted symbol
- User says "fix this error," "auto fix," "resolve these compile errors"

## Workflow

1. **Parse** — extract error type, message, file, line from output or user message
2. **Locate** — read file at reported line; trace to actual root cause (not just symptom)
3. **Propose** — present 2–3 fix approaches before applying:
   ```
   1. [Minimal] Add missing using + null guard — Low risk, 2 min
   2. [Proper] Fix the method signature to match interface — Med risk, 10 min
   3. [Structural] Refactor caller chain to avoid the dependency — High risk, 30 min
   ```
4. **Await** — wait for user selection (or apply safest if user says "auto fix")
5. **Fix** — apply chosen fix minimally
6. **Verify** — run `lsp_diagnostics` on every changed file; check for new errors
7. **Loop** — if errors remain, return to step 1. Continue until zero errors.

## Rules

- Fix root causes, not symptoms (e.g., fix missing method, not callers that fail)
- Read the full file before editing — never edit blind
- Run `lsp_diagnostics` after every individual file change
- Never suppress errors with `#pragma`, `@ts-ignore`, or empty catch blocks
- If a fix introduces new errors, revert and try a different approach
- Resolve in dependency order — base classes before derived
- Never change public API (method signatures, field names) without checking all callers via `lsp_find_references`
- Ask for confirmation before deleting or renaming symbols
- Stop the loop and report after 5 iterations without progress
- Verify final state shows zero errors before declaring done

## Output

Brief summary: files changed, root causes resolved, error count before/after.

## Standards

Load on demand from `unity-standards`:
- `debug/common-unity-errors.md` — error reference table
- `code-standards/lifecycle-async-errors.md` — execution order, error handling
- `code-standards/core-conventions.md` — null check patterns

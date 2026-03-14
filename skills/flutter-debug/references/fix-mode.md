# Fix Mode — Auto-Fix Loop

Automated Dart error resolution: run analysis → parse → locate root cause → propose → fix → verify → loop.

## When to Use

- Dart analysis errors after refactor, package update, or migration
- Compile-time type errors, missing imports, undefined names
- Cascading errors from a renamed or deleted symbol
- User says "fix this error," "auto fix," "resolve these analysis errors"

## Workflow

1. **Analyze** — run `dart analyze` (or read LSP diagnostics) to get the full error list
2. **Parse** — extract error type, message, file, line from each diagnostic
3. **Locate** — read file at reported line; trace to actual root cause (not just symptom)
4. **Propose** — present 2-3 fix approaches before applying:
   ```
   1. [Minimal] Add missing import + null check — Low risk, 2 min
   2. [Proper] Fix method signature to match interface — Med risk, 10 min
   3. [Structural] Refactor caller chain to use correct type — High risk, 30 min
   ```
5. **Await** — wait for user selection (or apply safest if user says "auto fix")
6. **Fix** — apply chosen fix minimally
7. **Verify** — run `dart analyze` on changed files; check for new errors
8. **Loop** — if errors remain, return to step 1. Continue until zero errors.

## Common Dart Error Patterns

| Error | Typical Fix |
|-------|-------------|
| `Undefined name 'X'` | Add missing import or fix typo |
| `Type 'A' can't be assigned to 'B'` | Cast, convert, or fix generic parameter |
| `Missing concrete implementation` | Implement required method or mark abstract |
| `Method 'X' isn't defined for type 'Y'` | Check import, extension, or type hierarchy |

## Rules

- Fix root causes, not symptoms
- Read the full file before editing — never edit blind
- Run `dart analyze` after every file change
- Never suppress errors with `// ignore:` directives
- If a fix introduces new errors, revert and try a different approach
- Resolve in dependency order — base classes before consumers
- Never change public API without checking all callers
- Stop and report after 5 iterations without progress

## Output

Brief summary: files changed, root causes resolved, error count before/after.

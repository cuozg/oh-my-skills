# unity-debug-quick — Workflow

## Steps

1. **Parse** — Extract subject (class/method/system), symptom, expected behavior. For error input: extract error type, crash site, call chain from stack trace.

2. **Read** — Open relevant file(s), read ±50 lines around target.

3. **Trace** — Follow execution path via LSP tools; map data flow to failure point.

4. **Assess** — Blast radius via `impact-analyzer` and `lsp_find_references`.

5. **Solve** — 2-4 solutions with trade-offs; also consider workarounds.

6. **Output** — Deliver the tree + interactive prompt (see `output-template.md`).

7. **Fix Loop** — See `../../unity-shared/references/debug-fix-loop.md` for delegation and iteration workflow.

## Tool Selection

| Need | Tool |
|:-----|:-----|
| Read target code | `read` |
| Find definition | `lsp_goto_definition` |
| Find callers | `lsp_find_references` |
| Find symbols | `lsp_symbols` (workspace) |
| Pattern search | `grep` / `ast_grep_search` |
| Blast radius | `impact-analyzer` |
| File discovery | `glob` |
| Check diagnostics | `lsp_diagnostics` |

## Common Error Quick-Check

Before deep investigation, check `../../unity-shared/references/common-fixes.md` for known patterns:
- NullReferenceException → missing null guard
- MissingReferenceException → destroyed object access
- IndexOutOfRange → unchecked collection access
- Race conditions → async/lifecycle ordering

## Fix Delegation

When user picks a solution:
1. Build delegation prompt with root cause + solution approach
2. Delegate via `task(category="quick", load_skills=["unity-code-quick"])`
3. Verify with `lsp_diagnostics` after fix completes
4. Ask if more issues exist — loop until user stops

---
description: Explain Unity issues, flows, or logic
agent: sisyphus-junior
subtask: true
---
Use skill unity-debug-quick to debug $ARGUMENTS

## Workflow

1. **Parse** — extract subject (class/method/system), symptom, expected behavior. For error input: extract error type, crash site, call chain from stack trace.
2. **Read** — open relevant file(s), read ±50 lines around target
3. **Trace** — follow execution path via LSP tools; map data flow to failure point
4. **Assess** — blast radius via `impact-analyzer` and `lsp_find_references`
5. **Solve** — 2-4 solutions with trade-offs; also consider workarounds
6. **Output** — deliver the tree + interactive prompt (see `response-template.md`)
7. **Fix Loop** — see `fix-loop.md` for delegation and iteration workflow

For common Unity errors (NullRef, MissingRef, IndexOutOfRange, race conditions), check `../../unity-shared/references/common-fixes.md` for known fix patterns before deep investigation.

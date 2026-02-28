# unity-debug-log — Workflow

## Steps

1. **Parse** — Extract what the user wants to understand (flow, state, null check, lifecycle, event, timing).

2. **Read** — Open target file(s). Understand method signatures, parameters, fields, and call chain.

3. **Classify** — Determine log types needed. See color guide in `../../unity-shared/references/debug-log-reference.md`.

4. **Generate** — Produce log snippets following `../../unity-shared/references/debug-log-reference.md` format. One code block per insertion point.

5. **Present** — Output using the response template. Show WHERE each snippet goes (file:line, before/after which statement).

## Tool Selection

| Need | Tool |
|:-----|:-----|
| Read target code | `read` |
| Find definition | `lsp_goto_definition` |
| Find callers | `lsp_find_references` |
| Find by pattern | `grep` / `ast_grep_search` |
| Locate file | `glob` |

## Log Format Rules

- Every `Debug.Log` MUST be wrapped in `#if UNITY_EDITOR` / `#endif`
- Every log message starts with `[DBG]` prefix
- Use `<color=X>` tags per the color guide
- Use string interpolation `$"..."` always — never `string.Format` or concatenation
- For null-safe inspection: `(x != null ? x.name : "NULL")` or `x?.ToString() ?? "NULL"`
- Include `ClassName.MethodName` context in every log message
- Keep log messages concise

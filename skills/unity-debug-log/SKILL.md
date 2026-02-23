---
name: unity-debug-log
description: "Generate targeted Debug.Log statements wrapped in #if UNITY_EDITOR to help understand code flow, logic, and state. Produces color-coded, structured log snippets — never modifies or adds code to the project. Use when: (1) Need to trace execution flow through methods, (2) Want to inspect variable state at runtime, (3) Debugging null references or unexpected values, (4) Understanding Unity lifecycle ordering, (5) Tracking event subscriptions and callbacks, (6) Monitoring state machine transitions. Triggers: 'add debug logs', 'trace this flow', 'log this method', 'debug log', 'add logging', 'trace execution', 'monitor state', 'log variables', 'show me the flow', 'instrument this code'."
---

# Unity Debug Log Generator

Generate debug log snippets. Output the template. Nothing else.

## Output Format

Use the response template from `references/debug-log-reference.md` for every response. No prose, no preamble — just the template.

## Hard Constraints

- **READ-ONLY**: Never edit, add, or modify any project file. Output log snippets as text only.
- **No commits**: No git operations.
- **#if UNITY_EDITOR**: Every Debug.Log MUST be wrapped in `#if UNITY_EDITOR` / `#endif`.
- **[DBG] prefix**: Every log message starts with `[DBG]` for easy filtering.
- **Color-coded**: Every log uses `<color=X>` tags per `references/debug-log-reference.md`.

## Workflow

1. **Parse** — Extract what the user wants to understand (flow, state, null check, lifecycle, event, timing).
2. **Read** — Open target file(s). Understand method signatures, parameters, fields, and call chain.
3. **Classify** — Determine log types needed. See color guide in `references/debug-log-reference.md`.
4. **Generate** — Produce log snippets following `references/debug-log-reference.md` format. One code block per insertion point.
5. **Present** — Output using `references/debug-log-reference.md` template. Show WHERE each snippet goes (file:line, before/after which statement).

## Tool Selection

| Need                 | Tool                       |
| :------------------- | :------------------------- |
| Read target code     | `read`                     |
| Find definition      | `lsp_goto_definition`      |
| Find callers         | `lsp_find_references`      |
| Find by pattern      | `grep` / `ast_grep_search` |
| Locate file          | `glob`                     |

## Rules

- Output log snippets only. NEVER edit files.
- Each log must have: `#if UNITY_EDITOR` wrapper, `<color=X>` tag, `[DBG]` prefix, `ClassName.MethodName` context.
- Use string interpolation `$"..."` always. Never `string.Format` or concatenation.
- For null-safe inspection: use `(x != null ? x.name : "NULL")` or `x?.ToString() ?? "NULL"`.
- Include exact file path and line number for each insertion point. Group by file, order by execution flow.
- Keep log messages concise — show the value, not a novel.

---
name: unity-debug-quick
description: "Investigate Unity issues, propose solutions, let user pick one, then delegate the fix to a sub-agent. Loops until user stops. Use when: (1) User asks 'why does X happen?', (2) Need to understand a bug or unexpected behavior, (3) Tracing data flow to find where things go wrong, (4) Understanding why a value is wrong or null, (5) Explaining lifecycle or timing issues, (6) Need impact analysis of a bug, (7) Want proposed solutions and interactive fix application. Triggers: 'explain why', 'why does this happen', 'explain this bug', 'what causes this', 'trace this issue', 'understand this behavior', 'why is this null', 'explain the flow', 'walk me through this', 'what is the impact', 'how to reproduce', 'debug and fix'."
---

# Unity Debug Quick

Investigate the issue. Output the tree. Ask user to pick a solution. Delegate the fix. Repeat until user stops.

## Output Format

Use the Vercel-themed tree template from `references/response-template.md` for every response. Tree connectors (`├──`, `└──`) for flow, repro, verify, prevent, and solutions. Inline code (`cyan`) for all code identifiers, file refs, and values. **Bold** for failure points and labels. Emoji indicators for severity. No prose, no preamble — just the formatted tree, then the interactive prompt.

## Hard Constraints

- **Investigation is READ-ONLY**: Never edit project files during investigation phase.
- **No commits**: No git operations.
- **Direct answer**: No report documents — answer in conversation.
- **Minimum 2 solutions**: Always propose 2-4 solutions.
- **Always ask**: After presenting solutions, ask user which one to apply.
- **Delegate fixes**: Use `task(category, load_skills)` to delegate chosen fix to a sub-agent. Never apply fixes directly.
- **Loop**: After fix is applied and verified, ask if there are more issues. Continue until user stops.

## Workflow
1. **Parse** — extract subject (class/method/system), symptom, expected behavior
2. **Read** — open relevant file(s), read ±50 lines around target
3. **Trace** — follow execution path via LSP tools; map data flow to failure point
4. **Assess** — blast radius via `impact-analyzer` and `lsp_find_references`
5. **Solve** — 2-4 solutions with trade-offs; also consider workarounds
6. **Output** — deliver the tree + interactive prompt (see `references/response-template.md`)
7. **Fix Loop** — see `references/fix-loop.md` for delegation and iteration workflow

## Tool Selection
| Need              | Tool                          |
| :---------------- | :---------------------------- |
| Read target code  | `read`                        |
| Find definition   | `lsp_goto_definition`         |
| Who calls it      | `lsp_find_references`         |
| Find symbols      | `lsp_symbols` (workspace)     |
| Pattern search    | `grep` / `ast_grep_search`    |
| Blast radius      | `impact-analyzer`             |
| Broad sweep       | `glob`                        |
| Check diagnostics | `lsp_diagnostics`             |
| Delegate fix      | `task` (category + skills)    |

Chain tools to build evidence. Stop once root cause is clear.

## Rules
- No preamble, no narration. Investigate directly, output the tree.
- Cite `File.cs:L##` inline throughout. No separate refs section.
- Code snippets only when they clarify — never dump full methods.
- Focus on the path that explains root cause. Don't explain everything.
- If uncertain, state "uncertain: {reason}" inside the tree and note what info would help.
- Stack trace input → extract error type, crash site, call chain first.
- After the tree, ALWAYS present the interactive choice prompt.
- When user picks a solution, delegate via `task()` with appropriate category and `load_skills=["unity-code-quick"]`.
- After fix delegation completes, verify with `lsp_diagnostics` then ask if there are more issues.

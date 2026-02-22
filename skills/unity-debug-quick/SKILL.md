---
name: unity-debug-quick
description: "Investigate Unity issues to understand root cause, impact, and propose solutions — never modifies code. Use when: (1) User asks 'why does X happen?', (2) Need to understand a bug or unexpected behavior, (3) Tracing data flow to find where things go wrong, (4) Understanding why a value is wrong or null, (5) Explaining lifecycle or timing issues, (6) Need impact analysis of a bug, (7) Want proposed solutions without code changes. Triggers: 'explain why', 'why does this happen', 'explain this bug', 'what causes this', 'trace this issue', 'understand this behavior', 'why is this null', 'explain the flow', 'walk me through this', 'what is the impact', 'how to reproduce'."
---

# Unity Debug Quick

**Input**: User question about a bug, unexpected behavior, or issue they want investigated

## Hard Constraints

- **READ-ONLY**: Never edit, add, or modify any project file. Investigate and explain only.
- **Never commit**: No git operations.
- **Direct answer**: No report documents. Answer the user directly in conversation.
- **ALWAYS use template**: Follow the Response Template exactly.
- **Multiple solutions**: ALWAYS propose at least 2 solutions. Let the user choose.

## Workflow

1. **Parse Issue** — What exactly is wrong? Extract: the subject (class/method/system), the symptom (what user observes), and the expected behavior (what should happen instead).
2. **Read Code** — Open the relevant file(s). Read ±50 lines around the target. Understand what the code is doing.
3. **Trace Root Cause** — Follow the execution path using LSP tools. Trace callers, definitions, references. Map the data flow from source to the point of failure. Ask: who set this value? When? Under what conditions?
4. **Assess Impact** — What does this issue break? What systems depend on the affected code? Use `impact-analyzer` and `lsp_find_references` to map downstream effects.
5. **Find Solutions** — Propose 2-4 solutions with different trade-offs. Also consider workarounds. Do NOT write code — describe the approach.
6. **Respond** — Deliver the investigation using the Response Template.

## Tool Selection

| Need | Tool |
|:---|:---|
| Read target code | `read` |
| Find definition | `lsp_goto_definition` |
| Find who calls it | `lsp_find_references` |
| Find symbols | `lsp_symbols` (workspace) |
| Pattern search | `grep` / `ast_grep_search` |
| Blast radius | `impact-analyzer` |
| Broad sweep | `glob` |
| Check diagnostics | `lsp_diagnostics` |

Chain tools to build a complete picture. Stop when you have enough evidence to explain the root cause.

## Output

Structured investigation response per the Response Template below.

## Response Template & Rules

For the complete response template structure and template rules, see [response-template.md](references/response-template.md).

For investigation rules and best practices, see the Rules section below.

## Rules

- Investigate the issue directly. No preamble, no narration.
- Cite with `FileName.cs:L##` inline throughout.
- Code snippets only when they clarify the explanation — never dump full methods.
- If the issue spans multiple systems, focus on the path that explains the root cause. Don't explain everything.
- If you can't determine the root cause with certainty, say "I'm not certain because {reason}" and note what additional information would help.
- If the user provides a stack trace, extract the error type, crash site, and call chain before investigating.
- If the user actually wants code fixes applied, suggest using `unity-debug-fix` or `unity-fix-errors` instead.
- Solutions describe WHAT to do and WHERE — they do NOT include code changes. That's `unity-debug-fix`'s job.

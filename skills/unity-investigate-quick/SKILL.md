---
name: unity-investigate-quick
description: "Quick investigation of Unity projects. Answers questions about how systems work with a short focused summary and 1-3 detailed explanations. No report document — direct conversational answers. Use when: (1) Quick question about how a feature works, (2) Understanding a class or method's purpose, (3) Tracing a call chain or data flow, (4) Finding where something is defined or used, (5) Understanding system dependencies, (6) Answering 'what does X do' or 'how does X work'. Triggers: 'how does X work', 'what does X do', 'explain this code', 'what calls this', 'investigate', 'where is X defined', 'how is X used', 'what triggers X', 'trace the flow', 'analyze this system'."
---

# Unity Quick Investigator

Answer the question. Nothing else.

## Output

Direct conversational answer: short summary + 1-3 detailed explanations with file:line citations.

## How It Works

1. **Parse** — extract the target (class, method, field, system, flow)
2. **Find** — pick the fastest tool, get the answer
3. **Reply** — use the template from `references/output-template.md`

## Tool Selection (pick ONE, go fast)

| Need | Tool |
|:---|:---|
| Definition / source | `lsp_goto_definition` |
| Who calls it | `lsp_find_references` |
| Find by name | `lsp_symbols` (workspace) |
| Blast radius | `impact-analyzer` |
| Pattern match | `grep` / `ast_grep_search` |
| Broad sweep | `scripts/trace_logic.sh [Target]` |

Chain tools only when the first result is incomplete. Stop the moment you can answer.

## Rules

- Answer the question directly. No narration, no preamble.
- Use `references/output-template.md` format. Always.
- 1-3 details max. Skip obvious stuff.
- Code snippets only when they clarify — never dump full methods.
- Cite with `File.cs:L##` inline. No separate refs section.
- If unsure, say so. Don't speculate.

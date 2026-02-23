---
name: unity-investigate-quick
description: "Quick investigation of Unity projects. Answers questions about how systems work with a short focused summary and 1-3 detailed explanations. No report document — direct conversational answers. Use when: (1) Quick question about how a feature works, (2) Understanding a class or method's purpose, (3) Tracing a call chain or data flow, (4) Finding where something is defined or used, (5) Understanding system dependencies, (6) Answering 'what does X do' or 'how does X work'. Triggers: 'how does X work', 'what does X do', 'explain this code', 'what calls this', 'investigate', 'where is X defined', 'how is X used', 'what triggers X', 'trace the flow', 'analyze this system'."
---
# Unity Quick Investigator

Answer the question. Nothing else.

## Output Format

Use the tree template from `references/output-template.md` for every response. No prose, no preamble, no summary — just the tree.

## Workflow

1. **Parse** — extract the target (class, method, field, system, flow)
2. **Find** — pick the fastest tool, get the answer
3. **Reply** — output the tree

## Tool Selection

| Need                | Tool                                                                                      |
| :------------------ | :---------------------------------------------------------------------------------------- |
| Definition / source | `lsp_goto_definition`                                                                     |
| Who calls it        | `lsp_find_references`                                                                     |
| Find by name        | `lsp_symbols` (workspace)                                                                 |
| Blast radius        | `impact-analyzer`                                                                         |
| Pattern match       | `grep` / `ast_grep_search`                                                                |
| Broad sweep         | `scripts/trace_logic.py [Target] [--assets] [--deep] [--root PATH] [--asset-root PATH]`   |

Chain tools only when the first result is incomplete. Stop once the answer is clear.

## Rules

- 1-3 details max. Skip obvious information.
- Code snippets only when they clarify — never dump full methods.
- Cite with `File.cs:L##` inline. No separate refs section.
- State uncertainty inside the tree summary. Never speculate.

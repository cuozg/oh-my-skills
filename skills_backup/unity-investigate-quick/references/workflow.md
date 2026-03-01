# unity-investigate-quick — Workflow

## Steps

1. **Parse** — Extract the target (class, method, field, system, flow).
2. **Find** — Pick the fastest tool, get the answer.
3. **Reply** — Output the tree.

## Tool Selection

| Need | Tool |
|:-----|:-----|
| Definition / source | `lsp_goto_definition` |
| Who calls it | `lsp_find_references` |
| Find by name | `lsp_symbols` (workspace) |
| Blast radius | `impact-analyzer` |
| Pattern match | `grep` / `ast_grep_search` |
| Broad sweep | `../../unity-shared/scripts/investigate/trace_logic.py [Target] [--assets] [--deep] [--root PATH] [--asset-root PATH]` |

Chain tools only when the first result is incomplete. Stop once the answer is clear.

## Rules

- 1-3 details max. Skip obvious information.
- Code snippets only when they clarify — never dump full methods.
- Cite with `File.cs:L##` inline. No separate refs section.
- State uncertainty inside the tree summary. Never speculate.

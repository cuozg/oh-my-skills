# unity-investigate-deep — Workflow

## Steps

1. **Scope** — identify investigation type (logic/data/resources/animation/VFX/audio/physics/UI/networking/performance), primary subject, entry points, boundaries
2. **Discover** — run `../unity-investigate-shared/scripts/trace_logic.py [Target]`, use LSP tools (`lsp_find_references`, `lsp_goto_definition`, `lsp_symbols`), grep/glob for assets, `ast_grep_search` for patterns
3. **Analyze** — read `references/analysis-rules.md`, apply rules for relevant type(s)
4. **Report** — read `assets/templates/INVESTIGATION_REPORT.md` template, fill type field, populate sections, delete unused §8.x sections, include Mermaid diagrams, save
5. **Summary** — present key findings, highlight risks/debt/improvements

## Tool Selection

| Need | Tool |
| --- | --- |
| Broad code search | `../unity-investigate-shared/scripts/trace_logic.py [Target] [--assets] [--deep] [--root PATH]` |
| Definition jump | `lsp_goto_definition` |
| All usages | `lsp_find_references` |
| File outline | `lsp_symbols` (scope=document) |
| Pattern matching | `ast_grep_search` |
| Asset references | `grep` / `glob` for .prefab, .unity, .asset |
| Blast radius | `impact-analyzer` |

## Best Practices

- **Breadth-First**: Scan structure before deep-diving methods
- **Explain "Why"**: Recover engineering intent, not just describe code
- **Highlight Risks**: Flag debt, threading issues, memory leaks, race conditions
- **Use Diagrams**: Mermaid sequence/state/graph diagrams
- **Quantify Impact**: Estimate memory, CPU, draw call costs

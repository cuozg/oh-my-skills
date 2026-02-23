---
name: unity-investigate-deep
description: "Deep investigation of Unity projects with full report output. Produces comprehensive markdown investigation documents with architecture diagrams, execution flows, risk tables, and improvement recommendations. Use when: (1) Need a thorough written report of how a system works, (2) Documenting complex system behavior for team review, (3) Deep-diving into architecture with Mermaid diagrams, (4) Producing investigation artifacts for future reference, (5) Tracing complete execution flows with side effects, (6) Auditing system health with risk assessment. Triggers: 'deep investigate', 'investigation report', 'document how X works', 'full analysis', 'write investigation', 'deep dive report', 'system analysis report', 'trace and document'."
---

# Unity Deep Investigator

**Input**: Question or system to investigate + optional starting file/class

## Output

Comprehensive investigation report (markdown) with architecture diagrams, execution flows, and risk tables. Save to `Documents/Investigations/`.

## Workflow

1. **Scope** — identify investigation type (logic/data/resources/animation/VFX/audio/physics/UI/networking/performance), primary subject, entry points, boundaries
2. **Discover** — run `scripts/trace_logic.py [Target]`, use LSP tools (`lsp_find_references`, `lsp_goto_definition`, `lsp_symbols`), grep/glob for assets, `ast_grep_search` for patterns
3. **Analyze** — read `references/analysis-rules.md`, apply rules for relevant type(s)
4. **Report** — read `assets/templates/INVESTIGATION_REPORT.md` template, fill type field, populate sections, delete unused §8.x sections, include Mermaid diagrams, save
5. **Summary** — present key findings, highlight risks/debt/improvements

## Tool Selection

| Need | Tool |
| --- | --- |
| Broad code search | `scripts/trace_logic.py [Target] [--assets] [--deep] [--root PATH]` |
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

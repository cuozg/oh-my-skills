# unity-document-system — Workflow

## Steps

1. **Scope** — Parse request, define in/out boundaries, normalize document name.

2. **Discover** — Run `../../unity-shared/scripts/investigate/trace_unified.py system [Term]`, use LSP tools, grep/glob for assets.

3. **Analyze** — Reconstruct init + execution flows, map data structures, find constraints.

4. **Generate** — Fill template from `output-template.md`, create Mermaid diagrams.

5. **Validate** — All template headings present, diagrams match real code, guides are actionable.

## Tool Selection

| Need | Tool |
|:-----|:-----|
| Broad system scan | `../../unity-shared/scripts/investigate/trace_unified.py system [Term]` |
| Definition jump | `lsp_goto_definition` |
| All usages | `lsp_find_references` |
| File outline | `lsp_symbols` (scope=document) |
| Pattern matching | `grep` / `glob` / `ast_grep_search` |
| Blast radius | `impact-analyzer` |

## Documentation Checklist

- [ ] Every claim backed by code evidence (`File.cs:L##`)
- [ ] Mermaid diagrams for init flow + execution flow + system context
- [ ] Every template section filled; "N/A — {reason}" only when truly not applicable
- [ ] Explains **why + how**, not just what exists
- [ ] Extension guides are step-by-step and copy-paste ready
- [ ] Bullet points over prose walls

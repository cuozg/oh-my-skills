## Workflow

1. **Scope** — parse request, define in/out boundaries, normalize document name
2. **Discover** — run `../unity-investigate-shared/scripts/trace_unified.py system [Term]`, use LSP tools, grep/glob for assets
3. **Analyze** — reconstruct init + execution flows, map data structures, find constraints
4. **Generate** — fill template from `assets/templates/SYSTEM_DOCUMENT_TEMPLATE_SECTION1.md` + `SECTION2.md`, create Mermaid diagrams
5. **Validate** — all template headings present, diagrams match real code, guides are actionable

## Tool Selection

| Need | Tool |
| --- | --- |
| Broad system scan | `../unity-investigate-shared/scripts/trace_unified.py system [Term]` |
| Definition jump | `lsp_goto_definition` |
| All usages | `lsp_find_references` |
| File outline | `lsp_symbols` (scope=document) |
| Pattern matching | `grep` / `glob` / `ast_grep_search` |
| Blast radius | `impact-analyzer` |

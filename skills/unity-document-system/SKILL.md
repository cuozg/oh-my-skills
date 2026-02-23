---
name: unity-document-system
description: "Documentation-only deep investigation skill. Produces comprehensive system documents covering architecture, data flows, usage, and extension guides. Use when: (1) Documenting a Unity system's architecture and data flow, (2) Creating onboarding docs for a complex system, (3) Generating extension/implementation guides for a system, (4) Producing integration and dependency maps. Triggers: 'document system', 'explain system', 'system overview', 'system document', 'architecture document'."
---

# Unity System Documenter

Read-only. Investigate and document — never modify project code.

**Input**: System/feature/class to document + optional scope boundaries.
**Output**: System document saved to `Documents/Systems/{SystemName}.md`.

## Workflow

1. **Scope** — parse request, define in/out boundaries, normalize document name
2. **Discover** — run `scripts/trace_system.py [Term]`, use LSP tools, grep/glob for assets
3. **Analyze** — reconstruct init + execution flows, map data structures, find constraints
4. **Generate** — fill template from `assets/templates/SYSTEM_DOCUMENT_TEMPLATE_SECTION1.md` + `SECTION2.md`, create Mermaid diagrams
5. **Validate** — all template headings present, diagrams match real code, guides are actionable

## Tool Selection

| Need | Tool |
| --- | --- |
| Broad system scan | `scripts/trace_system.py [Term]` |
| Definition jump | `lsp_goto_definition` |
| All usages | `lsp_find_references` |
| File outline | `lsp_symbols` (scope=document) |
| Pattern matching | `grep` / `glob` / `ast_grep_search` |
| Blast radius | `impact-analyzer` |

## Rules

- Every claim backed by code evidence (`File.cs:L##`)
- Mermaid diagrams mandatory for init flow + execution flow + system context
- Fill every template section; use "N/A — {reason}" only when truly not applicable
- Explain **why + how**, not just what exists
- Extension guides must be step-by-step and copy-paste ready
- Bullet points over prose walls

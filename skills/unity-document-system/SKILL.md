---
name: unity-document-system
description: "Documentation-only deep investigation skill. Produces comprehensive system documents covering architecture, data flows, usage, and extension guides. Triggers: 'document system', 'explain system', 'how does X work', 'system overview'."
---

# Unity System Documenter

Senior Unity developer perspective (15 years). Prioritize architectural clarity, call-chain accuracy, and actionable implementation guidance.

**Input**: Target system/feature/function to document, optional scope boundaries.

## Non-Negotiable Rules

- **Documentation-Only**: Investigate and explain; do not modify gameplay or project code.
- **Strict Template Adherence**: ALWAYS use the exact structure from `assets/templates/SYSTEM_DOCUMENT_TEMPLATE.md`.
- **Complete Coverage**: Fill every section; use explicit "N/A — {reason}" only when truly not applicable.
- **Traceable Claims**: All statements must be backed by code evidence (definitions, references, assets, flows).
- **Visual Architecture**: Mermaid diagrams are mandatory for context and runtime flows.

## Output

Comprehensive system document per the Template Section Mapping below. Save to `Documents/Systems/`.

## Template Section Mapping

Map user requirements to template sections:

1. **What it is?** → Section 1 (What It Is) + Section 2 (Purpose & Responsibility)
2. **Data structure** → Section 3 (Data Structures - Models, SOs, Configs)
3. **How it works?** → Section 4 (How It Works - Flows, Diagrams)
4. **Detailed feature analysis** → Section 5 (Architecture & Feature Details) + Section 8 (Integration) + Section 9 (Error Handling)
5. **How to implement/update?** → Section 6 (How to Implement / Update)
6. **Attention points** → Section 7 (Attention Points - Constraints, Perf, Threads)

## Required Tools

- `scripts/trace_system.sh` for system-level discovery
- `lsp_goto_definition`, `lsp_find_references` for symbol flow validation
- `grep`, `glob`, `read` for code and asset investigation
- `impact-analyzer` for dependency blast-radius checks

## Workflow (Sequential)

1. **Scope**: Parse request. Define boundaries (in-scope/out-of-scope). Normalize document name.
2. **Investigate**: Trace system terms. Resolve entry points. Find related assets/configs. Map dependencies.
3. **Analyze**: Reconstruct init/execution flows. Map data structures. Identify constraints/edge cases.
4. **Generate**: Fill `SYSTEM_DOCUMENT_TEMPLATE.md`. Create Mermaid diagrams. Write concrete implementation guides.
5. **Validate**: Check all headings exist. Verify diagrams match code. Ensure guide is usable.

## Quality Bar

- **Why + How > What**: Explain the *reasoning* and *mechanism*, not just the existence.
- **Diagrams**: Must be syntactically valid Mermaid. Must depict *actual* code paths, not idealized ones.
- **Extension Guides**: Must be step-by-step (1, 2, 3...) and copy-paste ready.
- **Attention Points**: Explicitly list threading rules, initialization order dependencies, and performance cliffs.
- **Conciseness**: High-signal prose. Bullet points over walls of text.

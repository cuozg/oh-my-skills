---
name: unity-investigate-deep
description: Full investigation report with architecture diagrams, execution flows, and risk tables. Triggers — 'deep investigate', 'investigation report', 'full analysis', 'system investigation', 'architecture analysis'.
metadata:
  author: kuozg
  version: "1.0"
---
# unity-investigate-deep

Produce a comprehensive investigation report with Mermaid diagrams, cited evidence, and risk assessment.

## When to Use

- Team needs documented understanding of an unfamiliar system
- Pre-refactor audit of a complex subsystem
- Onboarding material for a non-trivial feature
- Architecture analysis before a major change

## Workflow

1. **Scope** — Define system boundaries: entry points, exit points, key actors
2. **Discover** — Map all files/classes involved via `lsp_goto_definition`, `lsp_find_references`, `glob`
3. **Analyze** — Trace execution paths; record dependencies, data flows, and state mutations
4. **Diagram** — Draw Mermaid flowchart (execution) + class diagram (structure)
5. **Assess** — Identify coupling hotspots, hidden dependencies, and risk areas
6. **Load template** — `read_skill_file("unity-investigate-deep", "references/investigation-template.md")` — **MANDATORY, do this before writing**
7. **Write** — Fill every section of the template exactly; do not omit or reorder sections
8. **Summarize** — Add one-paragraph executive summary at the top

## Rules

- **Output MUST follow `references/investigation-template.md` exactly — non-negotiable**
- All sections required: Executive Summary, System Map, Execution Flow, Data Flow, Risks, References
- Cite `file:line` for every factual claim
- Include at least one Mermaid diagram (flowchart or sequenceDiagram)
- Bullets over prose in all sections
- No speculation — investigate first, then state conclusions
- Never skip or rename template sections

## Output Format

Save to `Documents/Investigations/{SystemName}_{YYYY-MM-DD}.md`.  
Structure is dictated entirely by `references/investigation-template.md` — no deviations.

## Reference Files

- `references/investigation-template.md` — Markdown template for investigation reports

Load references on demand via `read_skill_file("unity-investigate-deep", "references/investigation-template.md")`.

## Standards

Load `unity-standards` for architecture and risk assessment. Key references:

- `review/architecture-checklist.md` — coupling, SOLID, assembly boundaries
- `code-standards/architecture-patterns.md` — state machine, MVC/MVP, command pattern
- `code-standards/events.md` — C# events, UnityEvent, SO channels, Action

Load via `read_skill_file("unity-standards", "references/<path>")`.

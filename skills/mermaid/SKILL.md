---
name: mermaid
description: Create Mermaid diagrams — flowcharts, sequence diagrams, state machines, class diagrams, architecture diagrams. Triggers — 'diagram', 'mermaid', 'flowchart', 'sequence diagram', 'state diagram', 'architecture diagram', 'visualize'.
metadata:
  author: kuozg
  version: "1.0"
---
# mermaid

Produce ```mermaid code blocks for any system, flow, or relationship that benefits from visualization.

## When to Use

- Explaining a system's data flow or architecture
- Documenting state machines or game logic transitions
- Illustrating class relationships or dependencies
- Creating sequence diagrams for async or networked flows
- Embedding diagrams in PRs, wikis, or investigation reports

## Workflow

1. **Identify** — Determine what needs visualizing (flow, state, sequence, class, ER)
2. **Select** — Choose the diagram type that maps best to the subject
3. **Sketch** — List nodes/states/actors and their relationships before writing syntax
4. **Write** — Produce the Mermaid code block using correct syntax for the chosen type
5. **Review** — Check for syntax errors (unclosed quotes, reserved words, missing arrows)

## Rules

- Output diagrams inside triple-backtick ```mermaid blocks — never bare text
- Prefer `flowchart TD` over legacy `graph TD`
- Limit diagram to ~20 nodes; split into sub-diagrams if larger
- Label all edges with meaningful verbs or data names
- Use `note` or `%%` comments to clarify non-obvious nodes

## Output Format

One or more ```mermaid code blocks, each preceded by a one-sentence description of what it shows.

## Reference Files

- `references/diagram-types.md` — ER diagram + common pitfalls (loads `unity-standards/references/other/mermaid-syntax.md` for full syntax)

Load references on demand via `read_skill_file("mermaid", "references/{file}")` and `read_skill_file("unity-standards", "references/other/mermaid-syntax.md")`.

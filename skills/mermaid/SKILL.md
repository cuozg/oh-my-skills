---
name: mermaid
description: "Create Mermaid diagrams. Use when: (1) Documenting logic flows, (2) Creating architecture diagrams, (3) Visualizing state machines, (4) Mapping data structures. Triggers: 'diagram', 'visualize', 'flowchart', 'sequence diagram', 'draw the flow'."
---

# Mermaid Diagram Specialist

Visualize complex systems using Mermaid.js syntax.

## Output Requirement (MANDATORY)

**Every diagram MUST follow the template**: [DIAGRAM_OUTPUT.md](assets/templates/DIAGRAM_OUTPUT.md)

Embed diagrams in context or save to the relevant documentation file.

Read the template first, then populate all sections.

## Diagram Types

| Type | Use Case |
|------|----------|
| Flowchart | Logic flows, decision trees |
| Sequence | Component communication, API calls |
| Class | Data relationships, inheritance |
| State | UI states, game states |

## Workflow

1. **Analyze**: Identify entities and relationships
2. **Choose Type**: Match to diagram type above
3. **Author**: Use patterns from [MERMAID_PATTERNS.md](references/MERMAID_PATTERNS.md)
4. **Validate**: Check syntax, ensure accuracy
5. **Embed**: Wrap in ` ```mermaid ` code blocks

## Quick Examples

```mermaid
%% Flowchart
graph TD
    A[Start] --> B{Check Health}
    B -->|> 0| C[Continue]
    B -->|<= 0| D[Game Over]
```

```mermaid
%% Sequence
sequenceDiagram
    Player->>Server: Attack Request
    Server->>Player: Damage Result
```

## Best Practices

- **Keep Simple**: Multiple small diagrams > one giant chart
- **Top-Down Flow**: Prefer `TD` or `LR` direction
- **Semantic Colors**: Highlight critical paths with `style`/`classDef`
- **Consistent Aliases**: Same participant names across project docs

---
name: mermaid
description: "Create Mermaid diagrams. Use when: (1) Documenting logic flows, (2) Creating architecture diagrams, (3) Visualizing state machines, (4) Mapping data structures. Triggers: 'diagram', 'visualize', 'flowchart', 'sequence diagram', 'draw the flow'."
---

# Mermaid Diagram Specialist

## Input
System/flow to visualize. Optional: preferred diagram type, specific entities.

## Output
Mermaid diagram(s) in ` ```mermaid ` blocks following [DIAGRAM_OUTPUT.md](.opencode/skills/other/mermaid/assets/templates/DIAGRAM_OUTPUT.md).

## Diagram Types

| Type | Use Case |
|------|----------|
| Flowchart | Logic flows, decision trees |
| Sequence | Component communication, API calls |
| Class | Data relationships, inheritance |
| State | UI states, game states |

## Workflow

1. Analyze entities and relationships
2. Choose diagram type
3. Author using [MERMAID_PATTERNS.md](.opencode/skills/other/mermaid/references/MERMAID_PATTERNS.md)
4. Validate syntax, ensure accuracy
5. Embed in ` ```mermaid ` blocks

## Quick Examples

```mermaid
graph TD
    A[Start] --> B{Check Health}
    B -->|> 0| C[Continue]
    B -->|<= 0| D[Game Over]
```

```mermaid
sequenceDiagram
    Player->>Server: Attack Request
    Server->>Player: Damage Result
```

## Best Practices

- Multiple small diagrams > one giant chart
- Prefer `TD` or `LR` direction
- Use `style`/`classDef` for critical paths
- Consistent participant names across docs

# Mermaid Diagram Types

> **Shared syntax reference**: `unity-standards/references/other/mermaid-syntax.md`
> Load via: `read_skill_file("unity-standards", "references/other/mermaid-syntax.md")`
> Covers: flowchart, sequence, state, class diagrams with detailed syntax and styling.

## Flowchart

```mermaid
flowchart TD
    A[Start] --> B{Decision}
    B -- Yes --> C[Action A]
    B -- No --> D[Action B]
    C --> E[End]
    D --> E
```

Key syntax: `-->` (arrow), `--label-->` (labeled), `[rect]`, `{diamond}`, `(rounded)`, `((circle))`

## Sequence Diagram

```mermaid
sequenceDiagram
    participant Client
    participant Server
    Client->>Server: Request(data)
    Server-->>Client: Response(result)
    Note over Client,Server: async gap
    loop Retry
        Client->>Server: Ping
    end
```

Key syntax: `->>` (solid), `-->>` (dashed), `Note over`, `loop`, `alt`, `par`

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Running : StartGame
    Running --> Paused : PauseInput
    Paused --> Running : Resume
    Running --> [*] : GameOver
```

Key syntax: `[*]` (start/end), `-->` with `: EventLabel`

## Class Diagram

```mermaid
classDiagram
    class Animal {
        +string Name
        +Speak() void
    }
    class Dog {
        +Fetch() void
    }
    Animal <|-- Dog : inherits
    Dog --> Bone : uses
```

Key syntax: `<|--` (inherit), `-->` (association), `*--` (composition), `o--` (aggregation)

## ER Diagram

```mermaid
erDiagram
    PLAYER ||--o{ INVENTORY : has
    INVENTORY }o--|| ITEM : contains
    PLAYER {
        int id PK
        string name
    }
```

Key syntax: `||--o{` (one-to-many), `}o--||` (many-to-one), `||--||` (one-to-one)

## Common Pitfalls

- Quote node labels containing special chars: `A["label (with parens)"]`
- Avoid reserved words as node IDs: `end`, `start`, `state`
- Use `%%` for comments: `%% this is ignored`
- `classDiagram` uses `+` (public), `-` (private), `#` (protected)

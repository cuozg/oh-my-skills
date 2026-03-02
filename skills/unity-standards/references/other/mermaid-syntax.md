# Mermaid Syntax

## Flowchart

```mermaid
graph TD
    A[Start] --> B{Condition?}
    B -->|Yes| C[Action A]
    B -->|No| D[Action B]
    C --> E[End]
    D --> E

    subgraph Subsystem
        C
        D
    end
```

Node shapes: `[rect]` `(round)` `{diamond}` `([stadium])` `[[subroutine]]` `((circle))`
Arrows: `-->` `-.->` `==>` `--text-->`
Direction: `TD` (top-down), `LR` (left-right), `BT`, `RL`

## Sequence Diagram

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant DB as Database

    C->>S: Request
    activate S
    S->>DB: Query
    DB-->>S: Result
    S-->>C: Response
    deactivate S

    Note over C,S: Async flow
    loop Every 5s
        C->>S: Heartbeat
    end
    alt Success
        S-->>C: 200 OK
    else Failure
        S-->>C: 500 Error
    end
```

Arrows: `->>` (solid), `-->>` (dashed), `-x` (lost)
Blocks: `loop`, `alt/else`, `opt`, `par`, `critical`

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Running : StartInput
    Running --> Jumping : JumpInput
    Jumping --> Falling : ApexReached
    Falling --> Idle : Grounded

    state choice <<choice>>
    Idle --> choice
    choice --> Attack : hasWeapon
    choice --> Idle : noWeapon
```

## Class Diagram

```mermaid
classDiagram
    class IHealth {
        <<interface>>
        +TakeDamage(int) void
        +Heal(int) void
    }
    class HealthSystem {
        -int _current
        -int _max
        +TakeDamage(int) void
        +Heal(int) void
    }
    IHealth <|.. HealthSystem : implements
    HealthSystem *-- DamageModifier : composition
    HealthSystem o-- HealthBar : aggregation
```

Relations: `<|--` inherit, `<|..` implement, `*--` composition, `o--` aggregation, `-->` association

## Styling

```mermaid
graph TD
    A:::success --> B:::warning
    classDef success fill:#4caf50,color:#fff
    classDef warning fill:#ff9800,color:#fff
```

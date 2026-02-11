# Mermaid Chart Patterns

Common Mermaid syntax patterns for documenting Unity project architectures and logic flows.

## 1. Flowcharts (Process & Logic)

Use for gameplay loops, decision trees, or state transitions.

```mermaid
flowchart TD
    Start([Start Event]) --> Check{Is Local?}
    Check -- Yes --> LoadLocal[Load From Disk]
    Check -- No --> FetchRemote[Fetch From Server]
    LoadLocal --> Done
    FetchRemote --> Done([End])
```

## 2. Sequence Diagrams (Inter-Component Communication)

Use for explaining how systems interact over time (e.g., UI -> Controller -> Manager -> Server).

```mermaid
sequenceDiagram
    participant P as Player
    participant UI as UIManager
    participant C as CombatController
    participant S as Server
    
    P->>UI: Click Attack
    UI->>C: RequestAttack(target)
    C->>S: ValidateAction()
    S-->>C: Confirm(Success)
    C-->>UI: Update Animations
```

## 3. Class Diagrams (Data Structures)

Use for documenting C# class hierarchies or FlatBuffer table relationships.

```mermaid
classDiagram
    MonoBehaviour <|-- PlayerController
    PlayerController *-- HealthSystem
    PlayerController : +int speed
    PlayerController : +Move()
    class HealthSystem{
        +int currentHealth
        +TakeDamage(amount)
    }
```

## 4. State Diagrams

Use for documenting FSM (Finite State Machines) or Animators.

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Moving : Input > 0
    Moving --> Idle : Input = 0
    Moving --> Jumping : Press Space
    Jumping --> Idle : Grounded
```

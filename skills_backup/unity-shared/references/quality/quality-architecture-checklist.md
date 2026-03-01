# Architecture Quality Checklist

> For full-project quality audits. PR-level architecture review → see `review/review-architecture-patterns.md`.

---

## SOLID Principles

### Single Responsibility (SRP)
- Each class has exactly one reason to change
- MonoBehaviours handle Unity lifecycle only — delegate logic to services
- Managers don't mix UI updates with business logic
- Data classes don't contain behavior (pure data containers)
- One event = one concern (no "and" in event names)

### Open/Closed (OCP)
- New features added via new classes, not modifying existing switch/if chains
- Strategy pattern for variant behaviors (e.g., movement types, weapon effects)
- Config-driven behavior where possible (ScriptableObject data, not code branches)
- Extension points provided via virtual methods or interfaces

### Liskov Substitution (LSP)
- Subclasses don't throw `NotImplementedException`
- Overridden methods honor base class contracts (preconditions, postconditions)
- Collections of base type work correctly with any subtype
- No `is`/`as` type checks to handle specific subclasses

### Interface Segregation (ISP)
- Interfaces have ≤5 members; implementors use all of them
- No "fat" interface forcing stub implementations
- Split by consumer need: `IReadable` vs `IWritable`, `IDamageable` vs `IHealable`

### Dependency Inversion (DIP)
- High-level modules depend on abstractions, not concretions
- No `using` from core/domain layer to infrastructure/UI layer
- All service dependencies injected (constructor, `[Inject]`, or SO reference)

---

## Layer Architecture

- Clear dependency direction: **Presentation → Application → Domain → Infrastructure**
- No upward dependencies (infrastructure doesn't reference presentation)
- Domain layer has zero Unity dependencies (pure C#)
- Each assembly's purpose described in one sentence

## Scalability Indicators

- New content added without code changes (data-driven via SO or config)
- Feature toggle system for incomplete features
- Systems handle 10x current entity count without architectural change
- Async loading prevents main thread stalls on large datasets
- Memory budget defined and monitored per platform

# Architecture Checklist

## Single Responsibility

- [ ] Each class has one reason to change
- [ ] MonoBehaviour handles Unity lifecycle only — delegate logic to plain C# classes
- [ ] Manager classes < 300 lines — split if larger
- [ ] No "God objects" (`GameManager` doing input + UI + save + audio)

## Dependency Direction

```
UI Layer  →  Game Logic  →  Data Layer
(Views)      (Systems)      (Models/SOs)

Dependencies flow inward. Inner layers never reference outer layers.
```

- [ ] Data classes have zero Unity dependencies where possible
- [ ] UI references logic via interface, not concrete class
- [ ] Logic layer never references UI components directly
- [ ] ScriptableObjects used as data containers, not behavior hosts

## Assembly Definitions

- [ ] Core/shared code in own assembly (no circular refs)
- [ ] Editor code in Editor assembly (won't ship in build)
- [ ] Test assemblies reference only what they test
- [ ] Platform-specific code in conditional assemblies

| Assembly | References | Notes |
|----------|-----------|-------|
| `Game.Core` | None | Pure data, interfaces |
| `Game.Systems` | Core | Game logic |
| `Game.UI` | Core, Systems | Views only |
| `Game.Editor` | All (Editor only) | Tools, inspectors |
| `Game.Tests` | Core, Systems | Edit/Play mode tests |

## Event Coupling

- [ ] SO event channels over direct C# event references
- [ ] No `FindObjectOfType` for runtime wiring — inject or use events
- [ ] Observer pattern: subscribers don't know each other
- [ ] Event args immutable (struct or readonly class)

```csharp
// BAD: Tight coupling
public class Enemy : MonoBehaviour
{
    void Die() => FindObjectOfType<ScoreManager>().AddScore(10);
}

// GOOD: SO event channel
[CreateAssetMenu] public class IntEvent : ScriptableObject
{
    public event Action<int> OnRaised;
    public void Raise(int value) => OnRaised?.Invoke(value);
}

public class Enemy : MonoBehaviour
{
    [SerializeField] private IntEvent onScoreEvent;
    void Die() => onScoreEvent.Raise(10);
}
```

## Interface Usage

- [ ] Dependencies injected via interface, not concrete type
- [ ] Interfaces in shared assembly, implementations in feature assemblies
- [ ] No empty interfaces (marker interfaces) — use attributes instead
- [ ] Interface segregation: small focused interfaces over large ones

## Circular Dependencies

- [ ] No two classes referencing each other directly
- [ ] No two assemblies referencing each other
- [ ] Break cycles with: events, interfaces, mediator, or shared data

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Singleton everywhere | Hidden deps, test pain | DI or SO references |
| `static` mutable state | Scene bleed, race conditions | Instance-based + SO |
| Deep inheritance (>2) | Fragile base class | Composition |
| String-based messaging | No compile-time safety | Typed events/interfaces |

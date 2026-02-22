# Refactoring Patterns - Advanced Techniques

## Architecture Refactoring

### Service Locator to Dependency Injection

```csharp
// Stage 1: Service Locator (existing)
class Enemy : MonoBehaviour {
    void Start() { GameManager.Instance.RegisterEnemy(this); }
}

// Stage 2: Constructor Injection (intermediate)
class Enemy : MonoBehaviour {
    private GameManager _manager;
    public void Initialize(GameManager mgr) { _manager = mgr; }
}

// Stage 3: Pure DI (target, if possible for MonoBehaviour)
class EnemySpawner : MonoBehaviour {
    [SerializeField] private GameManager _manager;
    Enemy Spawn() { var e = Instantiate(prefab); e.Initialize(_manager); return e; }
}
```

### Decoupling with Events

Replace tight coupling (A calls B.Method) with event broadcasting:
- A raises `OnStateChanged` event
- B subscribes to `OnStateChanged`
- A doesn't know B exists

## Advanced Extraction Patterns

### Extract Interface from Singleton

1. Create interface `IGameManager`
2. Have `GameManager : IGameManager`
3. Create mock `MockGameManager : IGameManager` for tests
4. Pass `IGameManager` instead of accessing `Instance`

### Introduce Strategy Pattern

Replace switch statements with polymorphic strategy objects:
```csharp
// BEFORE
if (type == AttackType.Melee) { /* melee code */ }
else if (type == AttackType.Range) { /* range code */ }

// AFTER
interface IAttackStrategy { void Execute(); }
class MeleeAttack : IAttackStrategy { ... }
class RangeAttack : IAttackStrategy { ... }
_strategy.Execute();  // polymorphic
```

## Data Structure Refactoring

- Flat data structures (struct arrays) for cache locality
- Value types for small immutable data (Vector3, Color)
- Reference types only for large or mutable objects

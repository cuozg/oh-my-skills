# Comments

## XML Docs — Public API Only

```csharp
/// <summary>
/// Applies damage and triggers death if health reaches zero.
/// </summary>
/// <param name="amount">Raw damage before armor reduction.</param>
/// <returns>Actual damage dealt after modifiers.</returns>
public float TakeDamage(float amount)
{
    var actual = amount * (1f - _armorReduction);
    _currentHealth -= actual;
    if (_currentHealth <= 0f) Die();
    return actual;
}
```

## Inline Comments — WHY Not WHAT

```csharp
// ❌ What — obvious from code
// Subtract damage from health
_currentHealth -= damage;

// ✅ Why — explains intent
// Clamp to prevent negative health causing UI overflow
_currentHealth = Mathf.Max(0f, _currentHealth - damage);

// ✅ Why — explains non-obvious decision
// Cache on Awake — GetComponent is expensive in hot paths
_rb = GetComponent<Rigidbody>();

// ✅ Workaround context
// Unity 2022.3 bug: NavMeshAgent.SetDestination fails on first frame
yield return null;
_nav.SetDestination(target);
```

## TODO Format

```csharp
// TODO(alice): Replace magic number with config SO
// TODO(bob): Pool these allocations — GC spike in profiler
// HACK: Workaround for Unity issue UUM-12345, remove after 2023.2
// FIXME: Race condition when spawning during scene transition
```

## When NOT to Comment

- Self-documenting names — `CalculateDamageReduction()` needs no comment
- Obvious Unity callbacks — don't comment `void Start()` or `void Update()`
- Commented-out code — delete it, git remembers
- Trivial getters/setters
- Restating the type: `// The player's health` above `float _health`

## Header Comments for Sections

```csharp
public class GameManager : MonoBehaviour
{
    // --- Serialized Config ---
    [SerializeField] GameConfig _config;

    // --- Runtime State ---
    GameState _state;
    int _score;

    // --- Unity Callbacks ---
    void Awake() { }
    void OnDestroy() { }

    // --- Public API ---
    public void StartGame() { }
    public void EndGame() { }
}
```

## File Headers — Skip

No license headers, author names, or creation dates. Git tracks history.

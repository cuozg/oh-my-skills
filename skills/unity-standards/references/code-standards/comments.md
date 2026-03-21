# Comments

## XML Docs - Public API Only

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

## Inline Comments - Why, Not What

```csharp
// Avoid obvious restatement comments
_currentHealth -= damage;

// Explain intent or non-obvious behavior
_currentHealth = Mathf.Max(0f, _currentHealth - damage);

// Cache in Awake because this path runs every frame later
_rb = GetComponent<Rigidbody>();

// Delay one frame because the navigation graph is initialized in Start
yield return null;
_nav.SetDestination(target);
```

## TODO Format

```csharp
// TODO(alice): Replace magic number with config asset
// TODO(bob): Pool these allocations after profiler capture on the combat loop
// HACK(team): Temporary compatibility shim for legacy save data. Remove after migration window closes.
// FIXME(netcode): Spawn can race scene unload during reconnect.
```

## When Not To Comment

- Self-documenting names - `CalculateDamageReduction()` needs no comment
- Obvious Unity callbacks - do not comment `Start()` or `Update()` just to restate their name
- Commented-out code - delete it; version control keeps history
- Trivial getters and setters
- Restating the type: `// The player's health` above `float _health`

## Header Comments For Sections

```csharp
public class GameManager : MonoBehaviour
{
    // Serialized config
    [SerializeField] private GameConfig _config;

    // Runtime state
    private GameState _state;
    private int _score;

    // Unity callbacks
    private void Awake() { }
    private void OnDestroy() { }

    // Public API
    public void StartGame() { }
    public void EndGame() { }
}
```

## File Headers - Skip

Do not add author names, creation dates, or manual history blocks. Source control already tracks that information.

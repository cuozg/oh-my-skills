# Error Handling — Advanced

## Fail-Fast Patterns

```csharp
// Throw on invalid args in constructors/factories
public static Projectile Create(ProjectileConfig config)
{
    if (config == null) throw new System.ArgumentNullException(nameof(config));
    if (config.Speed <= 0) throw new System.ArgumentOutOfRangeException(nameof(config.Speed));
    var proj = Instantiate(config.Prefab);
    proj.Init(config);
    return proj;
}

// Guard clause — return early for recoverable cases
public void Heal(float amount)
{
    if (amount <= 0f) return;
    if (!_isAlive) return;
    _health = Mathf.Min(_health + amount, _maxHealth);
}
```

## OnValidate — Editor-Time Validation

```csharp
#if UNITY_EDITOR
void OnValidate()
{
    if (_speed < 0) Debug.LogWarning("Speed cannot be negative", this);
    if (_prefab == null) Debug.LogError("Prefab must be assigned", this);
    if (_waypoints != null && _waypoints.Length == 0)
        Debug.LogWarning("Waypoints array is empty", this);

    // Auto-fix: clamp values
    _speed = Mathf.Max(0f, _speed);
    _maxHealth = Mathf.Max(1f, _maxHealth);
}
#endif
```

**Rules:**
- Wrap in `#if UNITY_EDITOR` — `OnValidate` is editor-only but compiles in builds
- Use `Debug.LogWarning` for soft issues, `Debug.LogError` for required fields
- Auto-clamp numeric values where safe
- Never call `GetComponent` in `OnValidate` on prefabs (may not be instantiated)

## Custom Exception Types

```csharp
public class GameStateException : System.Exception
{
    public GameStateException(string message) : base(message) { }
    public GameStateException(string message, System.Exception inner) : base(message, inner) { }
}

// Usage — typed exceptions for specific error domains
public void TransitionTo(GameState next)
{
    if (!_validTransitions.Contains((_current, next)))
        throw new GameStateException($"Invalid transition: {_current} → {next}");
    _current = next;
}
```

# Null Safety

## Guard Clauses — Early Return

```csharp
// ✅ Guard clause — fail fast
public void ApplyDamage(IDamageable target, float amount)
{
    if (target == null) return;
    if (amount <= 0f) return;
    target.TakeDamage(amount);
}

// ❌ Deep nesting
public void ApplyDamage(IDamageable target, float amount)
{
    if (target != null)
    {
        if (amount > 0f)
        {
            target.TakeDamage(amount);
        }
    }
}
```

## TryGetComponent Over GetComponent+Null

```csharp
// ✅ No allocation on failure
if (TryGetComponent<Rigidbody>(out var rb))
{
    rb.AddForce(Vector3.up * 10f, ForceMode.Impulse);
}

// ❌ GetComponent returns null — easy to miss
var rb = GetComponent<Rigidbody>();
if (rb != null) rb.AddForce(Vector3.up * 10f);
```

## Null-Conditional and Null-Coalescing

```csharp
// ?. — safe member access
_audioSrc?.Play();
var name = _target?.gameObject?.name;

// ?? — fallback value
float speed = _config?.moveSpeed ?? 5f;
var spawn = _spawnPoint?.position ?? Vector3.zero;

// ??= — assign if null
_pool ??= new ObjectPool<Bullet>();
```

## ⚠️ Unity Null Gotcha

Unity overrides `==` operator. Destroyed objects are `== null` but NOT `is null`:

```csharp
Destroy(gameObject);
// Next frame:
if (obj == null)  { } // ✅ TRUE — Unity's == catches destroyed
if (obj is null)  { } // ❌ FALSE — C# null check, ref still exists
if (obj is not null) { } // ❌ WRONG — still has ref to destroyed obj
if (!obj)         { } // ✅ TRUE — implicit bool operator

// Rule: Use == null for Unity objects, is null for pure C#
```

## Pattern Matching

```csharp
// Type check + cast in one step
if (collision.gameObject.TryGetComponent<IDamageable>(out var target))
{
    target.TakeDamage(_damage);
}

// Switch expression with patterns
string GetStateLabel(GameState state) => state switch
{
    GameState.Menu => "Main Menu",
    GameState.Playing => "In Game",
    GameState.Paused => "Paused",
    _ => "Unknown"
};
```

## Debug.Assert for Invariants

```csharp
void Awake()
{
    _rb = GetComponent<Rigidbody>();
    Debug.Assert(_rb != null, "Rigidbody missing on " + name, this);
    Debug.Assert(_maxHealth > 0, "MaxHealth must be positive", this);
}
```

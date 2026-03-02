# Formatting

## Brace Style — Allman

```csharp
public class PlayerController : MonoBehaviour
{
    void Update()
    {
        if (_isGrounded)
        {
            Jump();
        }
    }
}
```

## Indentation

- 4 spaces — no tabs
- Max line length: **120 characters**
- Break long lines at operators or after commas

```csharp
// Break long method chains
var result = enemies
    .Where(e => e.IsAlive)
    .OrderBy(e => e.DistanceTo(player))
    .FirstOrDefault();

// Break long parameter lists
public void SpawnEnemy(
    Vector3 position,
    Quaternion rotation,
    EnemyConfig config,
    Transform parent = null)
{
}
```

## Regions — Avoid

```csharp
// ❌ Don't use regions to hide code
#region Movement
void Move() { }
#endregion

// ✅ Use comments if grouping is needed
// --- Movement ---
void Move() { }
```

## Blank Lines

- **1 blank line** between methods
- **1 blank line** between field groups
- **0 blank lines** inside short methods (<5 lines)
- **No trailing whitespace**

## Expression-Bodied Members

Use for single-line getters, methods, and operators:

```csharp
public float Health => _currentHealth;
public bool IsAlive => _currentHealth > 0;
public Vector3 DirectionTo(Transform t) => (t.position - transform.position).normalized;

// ❌ Don't use for multi-statement logic — use block body
public void TakeDamage(float amount)
{
    _currentHealth = Mathf.Max(0, _currentHealth - amount);
    OnHealthChanged?.Invoke(_currentHealth);
}
```

## Ternary — Single Level Only

```csharp
var label = isAlive ? "Alive" : "Dead";                              // ✅
var label = isAlive ? (isHealthy ? "Healthy" : "Hurt") : "Dead";    // ❌ nested
```

## var Usage

Use `var` when type is obvious from right side:

```csharp
var rb = GetComponent<Rigidbody>();       // ✅ type obvious
var enemies = new List<Enemy>();           // ✅ type obvious
float distance = Vector3.Distance(a, b);  // ✅ explicit for primitives
```

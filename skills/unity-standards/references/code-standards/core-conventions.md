# Core Conventions — Naming, Formatting, Attributes & Type Safety

---

## Naming Conventions

### Casing Rules

| Element        | Style       | Example              |
| -------------- | ----------- | -------------------- |
| Class / Struct | PascalCase  | `PlayerController` |
| Interface      | IPascalCase | `IDamageable`      |
| Method         | PascalCase  | `TakeDamage()`     |
| Property       | PascalCase  | `Health { get; }`  |
| Public field   | camelCase   | `maxSpeed`         |
| Private field  | _camelCase  | `_currentHealth`   |
| Parameter      | camelCase   | `damageAmount`     |
| Local variable | camelCase   | `hitCount`         |
| Constant       | PascalCase  | `MaxRetries`       |
| Enum type      | PascalCase  | `WeaponType`       |
| Enum value     | PascalCase  | `WeaponType.Sword` |
| Event          | PascalCase  | `OnDamageReceived` |

### Namespace Convention

```
CompanyName.ProjectName.Feature
```

```csharp
namespace Studio.RPG.Combat { }
namespace Studio.RPG.UI { }
namespace Studio.RPG.Audio { }
```

### File Naming

- One class per file — file name matches class name
- `PlayerController.cs` → `class PlayerController`
- Interfaces: `IDamageable.cs`
- Enums: `WeaponType.cs` (standalone file)

### Field Ordering in Class

```csharp
public class EnemyAI : MonoBehaviour
{
    // 1. Constants
    const float AggroRange = 10f;

    // 2. Static fields
    static int _enemyCount;

    // 3. Serialized fields
    [SerializeField] float _moveSpeed = 5f;
    [SerializeField] Transform _target;

    // 4. Private fields
    Rigidbody _rb;
    NavMeshAgent _nav;
    bool _isAggro;

    // 5. Properties
    public bool IsAlive => _currentHealth > 0;

    // 6. Unity callbacks (lifecycle order)
    // 7. Public methods
    // 8. Private methods
}
```

### Common Abbreviations

| Abbreviation     | Component           |
| ---------------- | ------------------- |
| `_rb`          | `Rigidbody`       |
| `_col`         | `Collider`        |
| `_sr`          | `SpriteRenderer`  |
| `_anim`        | `Animator`        |
| `_cam`         | `Camera`          |
| `_nav`         | `NavMeshAgent`    |
| `_canvasGroup` | `CanvasGroup`     |
| `_audioSrc`    | `AudioSource`     |
| `_tm`          | `TextMeshProUGUI` |

### Async Method Suffix

```csharp
async Awaitable LoadLevelAsync() { }      // ✅ Async suffix
async UniTask<bool> TrySaveAsync() { }    // ✅ Async suffix + Try prefix
async void OnButtonClick() { }            // ✅ Event handler — no suffix needed
```

### Boolean Naming

Prefix with `is`, `has`, `can`, `should`:

```csharp
bool _isGrounded;
bool _hasKey;
bool _canJump;
bool _shouldRespawn;
```

### Generic Type Parameters

```csharp
public class Pool<TComponent> where TComponent : Component { }
public interface IRepository<TEntity> { }
// Single type param: T is fine. Multiple: use descriptive TPrefix names.
```

---

## Formatting

### Brace Style — Allman

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

### Indentation

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

### Regions — Avoid

```csharp
// ❌ Don't use regions to hide code
#region Movement
void Move() { }
#endregion

// ✅ Use comments if grouping is needed
// --- Movement ---
void Move() { }
```

### Blank Lines

- **1 blank line** between methods
- **1 blank line** between field groups
- **0 blank lines** inside short methods (<5 lines)
- **No trailing whitespace**

### Expression-Bodied Members

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

### Ternary — Single Level Only

```csharp
var label = isAlive ? "Alive" : "Dead";                              // ✅
var label = isAlive ? (isHealthy ? "Healthy" : "Hurt") : "Dead";    // ❌ nested
```

### var Usage

Use `var` when type is obvious from right side:

```csharp
var rb = GetComponent<Rigidbody>();       // ✅ type obvious
var enemies = new List<Enemy>();           // ✅ type obvious
float distance = Vector3.Distance(a, b);  // ✅ explicit for primitives
```

---

## Comments

### XML Docs — Public API Only

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

### Inline Comments — Why, Not What

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

### TODO Format

```csharp
// TODO(alice): Replace magic number with config asset
// TODO(bob): Pool these allocations after profiler capture on the combat loop
// HACK(team): Temporary compatibility shim for legacy save data. Remove after migration window closes.
// FIXME(netcode): Spawn can race scene unload during reconnect.
```

### When Not To Comment

- Self-documenting names — `CalculateDamageReduction()` needs no comment
- Obvious Unity callbacks — do not comment `Start()` or `Update()` just to restate their name
- Commented-out code — delete it; version control keeps history
- Trivial getters and setters
- Restating the type: `// The player's health` above `float _health`

### Header Comments For Sections

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

### File Headers — Skip

Do not add author names, creation dates, or manual history blocks. Source control already tracks that information.

---

## Access Modifiers

### Default To Private

```csharp
public class Weapon : MonoBehaviour
{
    [SerializeField] private float _damage = 10f;   // Inspector-visible, hidden from code
    [SerializeField] private AudioClip _fireSound;

    public float Damage => _damage;                  // Read-only API surface
}
```

### Modifier Priority Table

| Modifier                     | When                                          |
| ---------------------------- | --------------------------------------------- |
| `private`                  | Default — everything unless needed elsewhere |
| `[SerializeField] private` | Inspector-visible fields                      |
| `protected`                | Subclass needs access (rare)                  |
| `internal`                 | Same assembly only                            |
| `public`                   | Intentional API surface                       |

### Sealed MonoBehaviours

Seal classes not designed for inheritance. Most gameplay MonoBehaviours should be `sealed` unless they are deliberate extension points.

```csharp
public sealed class PlayerMovement : MonoBehaviour { }

public abstract class BaseEnemy : MonoBehaviour
{
    protected abstract void Attack();
}
```

### Cached References For Awake-Set Fields

Use private non-serialized fields for cached component references. `readonly` is great for pure C# constructor-initialized dependencies, but it does not fit serialized Unity fields.

```csharp
public sealed class ProjectileLauncher : MonoBehaviour
{
    private Rigidbody _rb;
    private AudioSource _audioSrc;

    private void Awake()
    {
        _rb = GetComponent<Rigidbody>();
        _audioSrc = GetComponent<AudioSource>();
    }
}
```

### Const Vs Static Readonly

```csharp
private const float GravityScale = 9.81f;          // compile-time primitive/string only
private const string PlayerTag = "Player";

private static readonly Vector3 SpawnOffset = new(0f, 1f, 0f); // runtime-initialized value
private static readonly WaitForSeconds HalfSecond = new(0.5f);
```

### SerializeField Over Public

```csharp
public Transform target;              // ❌ Avoid public field just for Inspector access
[SerializeField] private Transform _target;
public Transform Target => _target;

// Acceptable only if the repo already uses serialized auto-properties consistently
[field: SerializeField] public int MaxHealth { get; private set; }
```

Prefer explicit backing fields in shared guidance because they are the least version-sensitive and easiest to migrate safely.

### Internal For Assembly Scope

```csharp
// Assembly: Game.Combat.asmdef
public interface IDamageable { }
internal class DamageCalculator { }

public class CombatManager
{
    internal void ResetCombatState() { }
}
```

### Readonly Struct — Immutable Value Types

```csharp
// ✅ readonly struct avoids defensive copies in readonly contexts
public readonly struct DamageResult
{
    public readonly float FinalDamage;
    public readonly bool WasCritical;

    public DamageResult(float finalDamage, bool wasCritical)
    {
        FinalDamage = finalDamage;
        WasCritical = wasCritical;
    }
}
```

---

## Null Safety

### Guard Clauses — Early Return

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

### TryGetComponent Over GetComponent+Null

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

### Null-Conditional and Null-Coalescing

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

### ⚠️ Unity Null Gotcha

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

### Pattern Matching

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

### Debug.Assert for Invariants

```csharp
void Awake()
{
    _rb = GetComponent<Rigidbody>();
    Debug.Assert(_rb != null, "Rigidbody missing on " + name, this);
    Debug.Assert(_maxHealth > 0, "MaxHealth must be positive", this);
}
```

### #nullable Directive (Unity 2021+)

Unity 2021+ supports C# `#nullable enable` for compile-time null analysis:

```csharp
#nullable enable

public class InventoryService
{
    public void AddItem(ItemData item) { _items.Add(item); } // item is non-null
    public ItemData? FindItem(string id) => _items.FirstOrDefault(i => i.Id == id); // may be null
}
```

**⚠️ Limitation with Unity Objects:** `#nullable` does NOT understand Unity's `== null` override. A `GameObject?` annotated as nullable still needs `== null` checks, not `is null`:

```csharp
#nullable enable
GameObject? target;
if (target == null) return; // ✅ still use == for Unity objects
if (target is null) return; // ❌ wrong — bypasses Unity lifetime check
```

**Recommendation:** Use `#nullable enable` for pure C# service classes. Avoid on MonoBehaviour-heavy files where Unity null semantics dominate.

---

## Unity Attributes

### Component Attributes

```csharp
[RequireComponent(typeof(Rigidbody))]
[RequireComponent(typeof(AudioSource))]
public sealed class ProjectileLauncher : MonoBehaviour { }

[DisallowMultipleComponent]
public sealed class Health : MonoBehaviour { }

[AddComponentMenu("Game/Combat/Weapon")]
public sealed class Weapon : MonoBehaviour { }

[SelectionBase]
public sealed class CharacterRoot : MonoBehaviour { }

[DefaultExecutionOrder(-100)]
public sealed class GameManager : MonoBehaviour { }
```

### Inspector Attributes

```csharp
public sealed class EnemyConfig : MonoBehaviour
{
    [Header("Movement")]
    [Tooltip("Units per second")]
    [SerializeField] private float _speed = 5f;

    [Range(0f, 100f)]
    [SerializeField] private float _health = 100f;

    [Min(0f)]
    [SerializeField] private float _damage = 10f;

    [Space(10)]
    [Header("Visuals")]
    [ColorUsage(showAlpha: true, hdr: true)]
    [SerializeField] private Color _emissionColor = Color.white;

    [GradientUsage(hdr: true)]
    [SerializeField] private Gradient _trailGradient;

    [TextArea(3, 5)]
    [SerializeField] private string _description;
}
```

| Attribute                | Effect                              |
| ------------------------ | ----------------------------------- |
| `[Header("X")]`        | Section label in Inspector          |
| `[Tooltip("X")]`       | Hover text in Inspector             |
| `[Range(min, max)]`    | Slider for numeric fields           |
| `[Min(value)]`         | Minimum value clamp                 |
| `[Space(px)]`          | Vertical spacing                    |
| `[TextArea(min, max)]` | Multi-line text input               |
| `[ColorUsage]`         | Color picker options (alpha, HDR)   |
| `[GradientUsage]`      | Gradient editor options             |
| `[Multiline(lines)]`   | Fixed multi-line text               |
| `[HideInInspector]`    | Hide public field from Inspector    |
| `[NonSerialized]`      | Exclude from serialization entirely |

### Serialization Attributes

```csharp
[SerializeField] private float _speed = 5f;

// Preferred default: explicit backing field + read-only property
[SerializeField] private int _maxHealth = 100;
public int MaxHealth => _maxHealth;

// Acceptable only if the repo already standardizes on it
[field: SerializeField] public int BonusLives { get; private set; }

// Safe rename — preserves serialized data
[FormerlySerializedAs("_hp")]
[SerializeField] private float _health = 100f;

// Polymorphic managed-reference serialization
[SerializeReference] private IAbility _ability;
```

Use explicit backing fields by default because Unity serializes fields, not property logic.

### Conditional And Debug Attributes

```csharp
// Method call stripped from non-editor builds (no runtime cost)
[System.Diagnostics.Conditional("UNITY_EDITOR")]
private static void DebugDrawPath(Vector3[] pts) { }

// Preserve from IL2CPP code stripping
[UnityEngine.Scripting.Preserve]
public class NetworkMessage { }

// Mark as obsolete with warning or error
[System.Obsolete("Use TakeDamage(DamageInfo) instead", error: false)]
public void TakeDamage(float amount) { }
```

### Attribute Combinations — Common Patterns

```csharp
[RequireComponent(typeof(Rigidbody))]
[DisallowMultipleComponent]
public sealed class PhysicsController : MonoBehaviour
{
    [Header("Physics Settings")]
    [Tooltip("Applied every FixedUpdate")]
    [SerializeField] private float _thrust = 10f;

    [Range(0f, 1f)]
    [SerializeField] private float _drag = 0.1f;

    [Space]
    [Header("Debug")]
    [SerializeField] private bool _drawGizmos;
}

[CreateAssetMenu(fileName = "NewWeapon", menuName = "Game/Weapon Data", order = 1)]
public sealed class WeaponData : ScriptableObject
{
    [SerializeField] private string _displayName;
    [SerializeField, Range(1f, 100f)] private float _damage = 10f;
    [SerializeField, Min(0.1f)] private float _cooldown = 0.5f;
    [SerializeField] private Sprite _icon;

    public string DisplayName => _displayName;
    public float Damage => _damage;
    public float Cooldown => _cooldown;
    public Sprite Icon => _icon;
}
```

---

## Code Patterns — Quick Reference Templates

### MonoBehaviour

```csharp
namespace Project.Feature
{
    public sealed class ThingController : MonoBehaviour
    {
        [Header("Settings")]
        [SerializeField] private float _speed = 5f;
        [SerializeField] private Transform _target;

        private Rigidbody _rb;

        private void Awake() => _rb = GetComponent<Rigidbody>();

        private void FixedUpdate()
        {
            if (_target == null) return;
            var dir = (_target.position - transform.position).normalized;
            _rb.MovePosition(transform.position + dir * (_speed * Time.fixedDeltaTime));
        }
    }
}
```

### ScriptableObject — Data Container

```csharp
[CreateAssetMenu(fileName = "New Item", menuName = "Game/Item Data")]
public sealed class ItemData : ScriptableObject
{
    [SerializeField] private string _displayName;
    [SerializeField] private int _cost;
    [SerializeField] private Sprite _icon;

    public string DisplayName => _displayName;
    public int Cost => _cost;
    public Sprite Icon => _icon;
}
```

### Interface

```csharp
public interface IDamageable
{
    float CurrentHealth { get; }
    void TakeDamage(float amount, Vector3 hitPoint);
}
```

### UnityEvent

```csharp
[SerializeField] private UnityEvent<int> onScoreChanged;
public void AddScore(int pts) { _score += pts; onScoreChanged?.Invoke(_score); }
```

### Struct vs Class — Value Types for Data

```csharp
// ✅ Struct — small, immutable, no GC pressure
public readonly struct DamageInfo
{
    public readonly float Amount;
    public readonly Vector3 HitPoint;
    public readonly DamageType Type;

    public DamageInfo(float amount, Vector3 hitPoint, DamageType type)
    {
        Amount = amount;
        HitPoint = hitPoint;
        Type = type;
    }
}

// Use struct when: ≤16 bytes, short-lived, frequently created, no inheritance needed
// Use class when: large, long-lived, needs reference semantics, polymorphism
```

### Hot-Path Performance Rules

```csharp
// ❌ NEVER in Update/FixedUpdate/LateUpdate:
GetComponent<T>();           // cache in Awake
FindAnyObjectByType<T>();    // cache in Awake/Start
Camera.main;                 // cache in Awake
new List<T>();               // pre-allocate and reuse
string concatenation;        // use StringBuilder or cached strings
LINQ methods;                // use for loops
Instantiate/Destroy;         // use object pooling
Physics.Raycast();           // use NonAlloc variants

// ✅ DO in hot paths:
// - Use cached references
// - Pre-allocated collections with .Clear()
// - sqrMagnitude instead of Distance
// - CompareTag instead of tag ==
// - Bit operations for layer masks
// - for(int i) instead of foreach on Lists (avoids enumerator alloc in older Unity)
```

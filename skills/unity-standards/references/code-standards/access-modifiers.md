# Access Modifiers

## Default to Private

```csharp
public class Weapon : MonoBehaviour
{
    [SerializeField] float _damage = 10f;   // ✅ Inspector-visible, hidden from code
    [SerializeField] AudioClip _fireSound;

    public float damage = 10f;              // ❌ exposes implementation
    public float Damage => _damage;         // ✅ read-only property
}
```

## Modifier Priority Table

| Modifier | When |
|----------|------|
| `private` | Default — everything unless needed elsewhere |
| `[SerializeField] private` | Inspector-visible fields |
| `protected` | Subclass needs access (rare) |
| `internal` | Same assembly only |
| `public` | Intentional API surface |

## Sealed MonoBehaviours

Seal classes not designed for inheritance — prevents accidental subclassing, enables compiler optimizations:

```csharp
public sealed class PlayerMovement : MonoBehaviour { }  // ✅ most MonoBehaviours

public abstract class BaseEnemy : MonoBehaviour          // only unsealed if base class
{
    protected abstract void Attack();
}
```

## Readonly for Awake-Set Fields

```csharp
public sealed class ProjectileLauncher : MonoBehaviour
{
    Rigidbody _rb;
    AudioSource _audioSrc;

    void Awake()
    {
        _rb = GetComponent<Rigidbody>();
        _audioSrc = GetComponent<AudioSource>();
    }
}
```

`readonly` keyword incompatible with serialization — use for non-serialized cached refs only.

## Const vs Static Readonly

```csharp
const float GravityScale = 9.81f;            // compile-time, primitive/string only
const string PlayerTag = "Player";

static readonly Vector3 SpawnOffset = new(0f, 1f, 0f);   // runtime, reference types
static readonly WaitForSeconds HalfSecond = new(0.5f);
```

## SerializeField Over Public

```csharp
public Transform target;              // ❌ public field for Inspector access
[SerializeField] Transform _target;   // ✅ private + SerializeField
[field: SerializeField] public int MaxHealth { get; private set; }  // ✅ Unity 2023.3+
```

## Internal for Assembly Scope

```csharp
// Assembly: Game.Combat.asmdef
public interface IDamageable { }            // public — other assemblies can use
internal class DamageCalculator { }         // internal — Combat assembly only

public class CombatManager
{
    internal void ResetCombatState() { }    // internal method on public class
}
```

# Access Modifiers

## Default To Private

```csharp
public class Weapon : MonoBehaviour
{
    [SerializeField] private float _damage = 10f;   // Inspector-visible, hidden from code
    [SerializeField] private AudioClip _fireSound;

    public float damage = 10f;                      // Avoid exposing implementation
    public float Damage => _damage;                 // Read-only API surface
}
```

## Modifier Priority Table

| Modifier | When |
|----------|------|
| `private` | Default - everything unless needed elsewhere |
| `[SerializeField] private` | Inspector-visible fields |
| `protected` | Subclass needs access (rare) |
| `internal` | Same assembly only |
| `public` | Intentional API surface |

## Sealed MonoBehaviours

Seal classes not designed for inheritance. Most gameplay MonoBehaviours should be `sealed` unless they are deliberate extension points.

```csharp
public sealed class PlayerMovement : MonoBehaviour { }

public abstract class BaseEnemy : MonoBehaviour
{
    protected abstract void Attack();
}
```

## Cached References For Awake-Set Fields

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

## Const Vs Static Readonly

```csharp
private const float GravityScale = 9.81f;          // compile-time primitive/string only
private const string PlayerTag = "Player";

private static readonly Vector3 SpawnOffset = new(0f, 1f, 0f); // runtime-initialized value
private static readonly WaitForSeconds HalfSecond = new(0.5f);
```

## SerializeField Over Public

```csharp
public Transform target;              // Avoid public field just for Inspector access
[SerializeField] private Transform _target;
public Transform Target => _target;

// Acceptable only if the repo already uses serialized auto-properties consistently
[field: SerializeField] public int MaxHealth { get; private set; }
```

Prefer explicit backing fields in shared guidance because they are the least version-sensitive and easiest to migrate safely.

## Internal For Assembly Scope

```csharp
// Assembly: Game.Combat.asmdef
public interface IDamageable { }
internal class DamageCalculator { }

public class CombatManager
{
    internal void ResetCombatState() { }
}
```

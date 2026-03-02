# Naming Conventions

## Casing Rules

| Element | Style | Example |
|---------|-------|---------|
| Class / Struct | PascalCase | `PlayerController` |
| Interface | IPascalCase | `IDamageable` |
| Method | PascalCase | `TakeDamage()` |
| Property | PascalCase | `Health { get; }` |
| Public field | camelCase | `maxSpeed` |
| Private field | _camelCase | `_currentHealth` |
| Parameter | camelCase | `damageAmount` |
| Local variable | camelCase | `hitCount` |
| Constant | PascalCase | `MaxRetries` |
| Enum type | PascalCase | `WeaponType` |
| Enum value | PascalCase | `WeaponType.Sword` |
| Event | PascalCase | `OnDamageReceived` |

## Namespace Convention

```
CompanyName.ProjectName.Feature
```

```csharp
namespace Studio.RPG.Combat { }
namespace Studio.RPG.UI { }
namespace Studio.RPG.Audio { }
```

## File Naming

- One class per file — file name matches class name
- `PlayerController.cs` → `class PlayerController`
- Interfaces: `IDamageable.cs`
- Enums: `WeaponType.cs` (standalone file)

## Field Ordering in Class

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

## Common Abbreviations

| Abbreviation | Component |
|--------------|-----------|
| `_rb` | `Rigidbody` |
| `_col` | `Collider` |
| `_sr` | `SpriteRenderer` |
| `_anim` | `Animator` |
| `_cam` | `Camera` |
| `_nav` | `NavMeshAgent` |
| `_canvasGroup` | `CanvasGroup` |
| `_audioSrc` | `AudioSource` |
| `_tm` | `TextMeshProUGUI` |

## Boolean Naming

Prefix with `is`, `has`, `can`, `should`:

```csharp
bool _isGrounded;
bool _hasKey;
bool _canJump;
bool _shouldRespawn;
```

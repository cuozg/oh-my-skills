# Unity Attributes — Quick Reference

## Component Attributes

```csharp
// Auto-add required components when this component is added
[RequireComponent(typeof(Rigidbody))]
[RequireComponent(typeof(AudioSource))]
public sealed class ProjectileLauncher : MonoBehaviour { }

// Prevent multiple instances of this component on one GO
[DisallowMultipleComponent]
public sealed class Health : MonoBehaviour { }

// Custom path in Add Component menu
[AddComponentMenu("Game/Combat/Weapon")]
public sealed class Weapon : MonoBehaviour { }

// Make parent selectable when clicking child in Scene view
[SelectionBase]
public sealed class CharacterRoot : MonoBehaviour { }

// Set execution order via attribute instead of Project Settings
[DefaultExecutionOrder(-100)]
public sealed class GameManager : MonoBehaviour { }
```

## Inspector Attributes

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

| Attribute | Effect |
|-----------|--------|
| `[Header("X")]` | Section label in Inspector |
| `[Tooltip("X")]` | Hover text in Inspector |
| `[Range(min, max)]` | Slider for numeric fields |
| `[Min(value)]` | Minimum value clamp |
| `[Space(px)]` | Vertical spacing |
| `[TextArea(min, max)]` | Multi-line text input |
| `[ColorUsage]` | Color picker options (alpha, HDR) |
| `[GradientUsage]` | Gradient editor options |
| `[Multiline(lines)]` | Fixed multi-line text (no scroll) |
| `[HideInInspector]` | Hide public field from Inspector |
| `[NonSerialized]` | Exclude from serialization entirely |

## Serialization Attributes

```csharp
// Expose private field to Inspector
[SerializeField] private float _speed = 5f;

// Auto-property serialization (Unity 2023.3+)
[field: SerializeField] public int MaxHealth { get; private set; }

// Safe rename — preserves serialized data
[FormerlySerializedAs("_hp")]
[SerializeField] private float _health = 100f;

// Polymorphic serialization — serialize interface/abstract refs
[SerializeReference] private IAbility _ability;
```

## Conditional & Debug Attributes

```csharp
// Method call stripped from non-editor builds (no runtime cost)
[System.Diagnostics.Conditional("UNITY_EDITOR")]
private static void DebugDrawPath(Vector3[] pts) { }

// Preserve from IL2CPP code stripping
[UnityEngine.Scripting.Preserve]
public class NetworkMessage { }

// Mark as obsolete with warning/error
[System.Obsolete("Use TakeDamage(DamageInfo) instead", error: false)]
public void TakeDamage(float amount) { }
```

## Attribute Combinations — Common Patterns

```csharp
// Required component with readonly-like exposure
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

// ScriptableObject with full inspector polish
[CreateAssetMenu(fileName = "NewWeapon", menuName = "Game/Weapon Data", order = 1)]
public sealed class WeaponData : ScriptableObject
{
    [field: SerializeField] public string DisplayName { get; private set; }
    [field: SerializeField, Range(1f, 100f)] public float Damage { get; private set; } = 10f;
    [field: SerializeField, Min(0.1f)] public float Cooldown { get; private set; } = 0.5f;
    [field: SerializeField] public Sprite Icon { get; private set; }
}
```

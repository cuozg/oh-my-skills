# Unity Attributes - Advanced

## Conditional And Debug Attributes

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

## Attribute Combinations - Common Patterns

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

If a project already uses `[field: SerializeField]` pervasively, match the local style. Otherwise prefer explicit serialized backing fields in shared reference material.

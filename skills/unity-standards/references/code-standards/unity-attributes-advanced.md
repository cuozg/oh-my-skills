# Unity Attributes — Advanced

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

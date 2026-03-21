# Serialization

## Prefer Explicit Backing Fields

Use explicit serialized fields for inspector-driven state. This is the least surprising pattern across Unity versions and makes rename and migration work easier to review.

```csharp
public sealed class EnemyConfig : MonoBehaviour
{
    [SerializeField] private float _health = 100f;
    [SerializeField] private float _speed = 3f;
    [SerializeField] private GameObject _deathVfx;

    public float Health => _health;
    public float Speed => _speed;
}
```

## Auto-Property Serialization Is Optional, Not The Default

If a repo already standardizes on field-target attributes and the local Unity version supports it, keep that style consistent. Do not introduce it blindly into mixed-version or mixed-style codebases.

```csharp
// Acceptable only when the project already uses this pattern consistently.
[field: SerializeField] public int MaxHealth { get; private set; } = 100;
```

When in doubt, prefer an explicit backing field plus a read-only property.

## Serializable Nested Types

```csharp
[System.Serializable]
public struct WaveConfig
{
    public int enemyCount;
    public float spawnInterval;
    public GameObject prefab;
}

public sealed class WaveSpawner : MonoBehaviour
{
    [SerializeField] private WaveConfig[] _waves;
}
```

## ScriptableObject Data Containers

```csharp
[CreateAssetMenu(fileName = "EnemyConfig", menuName = "Game/Enemy Config")]
public sealed class EnemyConfig : ScriptableObject
{
    [SerializeField] private float _maxHealth = 100f;
    [SerializeField] private float _moveSpeed = 3f;
    [SerializeField] private AnimationCurve _damageFalloff;

    public float MaxHealth => _maxHealth;
    public float MoveSpeed => _moveSpeed;
    public float GetDamage(float dist) => _damageFalloff.Evaluate(dist);
}
```

## SerializeReference For Polymorphism

Use `[SerializeReference]` only when you actually need polymorphic managed references. It is useful, but it is not a general replacement for normal field serialization.

```csharp
public interface IAbility
{
    void Execute(GameObject owner);
}

public sealed class AbilityRunner : MonoBehaviour
{
    [SerializeReference] private IAbility _primaryAbility;
}
```

## FormerlySerializedAs - Safe Renames

```csharp
using UnityEngine.Serialization;

public sealed class Player : MonoBehaviour
{
    [FormerlySerializedAs("_speed")]
    [SerializeField] private float _moveSpeed = 5f;

    [FormerlySerializedAs("hp")]
    [FormerlySerializedAs("_hp")]
    [SerializeField] private float _health = 100f;
}
```

Keep rename attributes until affected scenes, prefabs, and ScriptableObjects have been re-saved and validated.

## JsonUtility Rules

| Feature | Supported | Notes |
|---------|-----------|-------|
| Public fields | Yes | Serialized by default |
| `[SerializeField]` private fields | Yes | Works |
| Properties | No | Inspector does not serialize property accessors |
| Dictionary | No | Use a serializable list or custom serializer |
| Polymorphism | No | `JsonUtility` does not carry managed type info |
| `[NonSerialized]` | Yes | Excludes field |

```csharp
string json = JsonUtility.ToJson(saveData, prettyPrint: true);
File.WriteAllText(path, json);

var data = JsonUtility.FromJson<SaveData>(json);
JsonUtility.FromJsonOverwrite(json, existingData); // avoids allocation
```

## What Unity Does Not Serialize Reliably

- `Dictionary<K, V>` - wrap in a serializable list or use a custom serializer
- Interfaces and abstract types - use `[SerializeReference]` only when you need managed-reference polymorphism
- `static` fields - never serialized
- `readonly` fields - not inspector-authored serialized state
- Properties - use explicit fields unless the project intentionally uses serialized backing-field attributes
- Deeply nested containers and unsupported generic shapes - validate in the inspector before relying on them

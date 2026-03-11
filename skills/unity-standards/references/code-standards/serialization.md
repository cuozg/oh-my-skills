# Serialization

## SerializeField Private Fields

```csharp
public sealed class EnemyConfig : MonoBehaviour
{
    [SerializeField] float _health = 100f;
    [SerializeField] float _speed = 3f;
    [SerializeField] GameObject _deathVfx;
    public float Health => _health;
}
```

## Auto-Property Serialization

```csharp
// Unity 2023.3+ — [field: SerializeField] on auto-properties
public sealed class WeaponData : ScriptableObject
{
    [field: SerializeField] public string DisplayName { get; private set; }
    [field: SerializeField] public float Damage { get; private set; }
    [field: SerializeField] public Sprite Icon { get; private set; }
}
```

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
    [SerializeField] WaveConfig[] _waves;
}
```

## ScriptableObject Data Containers

```csharp
[CreateAssetMenu(fileName = "EnemyConfig", menuName = "Game/Enemy Config")]
public class EnemyConfig : ScriptableObject
{
    [SerializeField] float _maxHealth = 100f;
    [SerializeField] float _moveSpeed = 3f;
    [SerializeField] AnimationCurve _damageFalloff;
    public float MaxHealth => _maxHealth;
    public float MoveSpeed => _moveSpeed;
    public float GetDamage(float dist) => _damageFalloff.Evaluate(dist);
}
```

## FormerlySerializedAs — Safe Renames

```csharp
using UnityEngine.Serialization;

public sealed class Player : MonoBehaviour
{
    [FormerlySerializedAs("_speed")]
    [SerializeField] float _moveSpeed = 5f;

    // Multiple attrs for chained renames — keep until all scenes re-saved
    [FormerlySerializedAs("hp")]
    [FormerlySerializedAs("_hp")]
    [SerializeField] float _health = 100f;
}
```

## JsonUtility Rules

| Feature | Supported | Notes |
|---------|-----------|-------|
| Public fields | ✅ | Serialized by default |
| `[SerializeField]` private | ✅ | Works |
| Properties | ❌ | Not serialized |
| Dictionary | ❌ | Use list of key-value pairs |
| Polymorphism | ❌ | No type info in JSON |
| `[NonSerialized]` | ✅ | Excludes field |

```csharp
string json = JsonUtility.ToJson(saveData, prettyPrint: true);
File.WriteAllText(path, json);
var data = JsonUtility.FromJson<SaveData>(json);
JsonUtility.FromJsonOverwrite(json, existingData); // avoids allocation
```

## What Unity Cannot Serialize

- `Dictionary<K,V>` — wrap in serializable list
- Interfaces — use concrete types or `[SerializeReference]`
- `static` fields — never serialized
- `readonly` fields — never serialized; nested generic types like `List<List<int>>` also fail

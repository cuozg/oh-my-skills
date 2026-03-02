# Serialization Risks

## Field Renaming

- [ ] Renamed fields have `[FormerlySerializedAs("oldName")]` attribute
- [ ] Attribute kept permanently — removing it breaks existing assets

```csharp
// BAD: Silent data loss on rename
[SerializeField] private float moveSpeed; // was "speed"

// GOOD: Preserve old data
[FormerlySerializedAs("speed")]
[SerializeField] private float moveSpeed;
```

## Type Changes

| Change | Risk | Mitigation |
|--------|------|------------|
| `int` → `float` | Data preserved | Safe |
| `float` → `int` | Truncation | Add migration |
| `string` → `enum` | Data loss | Use `[FormerlySerializedAs]` + converter |
| `List<T>` → `T[]` | Data loss | Requires migration script |
| Any → different class | Complete loss | Manual migration |

## Missing Attributes

- [ ] Custom classes have `[System.Serializable]` to serialize as fields
- [ ] Private fields use `[SerializeField]` if inspector-visible
- [ ] Non-serialized fields marked `[System.NonSerialized]` or `[HideInInspector]`
- [ ] Properties never serialize — use backing field with `[SerializeField]`
- [ ] `Dictionary<K,V>` not serializable — use `List` pairs or custom serializable dict

```csharp
// BAD: Won't appear in inspector
private float health;

// BAD: Class not serializable
public class EnemyConfig { public int damage; }

// GOOD:
[SerializeField] private float health;

[System.Serializable]
public class EnemyConfig { public int damage; }
```

## ScriptableObject Risks

- [ ] SO references assigned in prefabs survive domain reload
- [ ] SO shared state mutated at runtime resets on play mode exit (Editor) but persists in build
- [ ] Runtime-modified SO data cloned via `Instantiate(so)` to avoid shared mutation
- [ ] SO asset null after `AssetDatabase.DeleteAsset` — guard consumers

## Prefab Serialization

- [ ] Added field gets default value on existing prefab instances — verify defaults safe
- [ ] Prefab variant overrides break if base field removed
- [ ] Nested prefab changes require "Apply" — unapplied changes lost
- [ ] `[SerializeReference]` for polymorphic fields (Unity 2019.3+)

## Enum Reordering

- [ ] Enums serialize as integer index, not name
- [ ] Adding values mid-enum shifts all subsequent indices
- [ ] Explicit values prevent reorder issues

```csharp
// BAD: Reordering breaks saved data
public enum ItemType { Sword, Shield, Potion }

// GOOD: Explicit values
public enum ItemType { Sword = 0, Shield = 1, Potion = 2 }
```

## JSON / Binary Serialization

- [ ] `JsonUtility` skips properties, dictionaries, polymorphic types
- [ ] `[JsonProperty]` (Newtonsoft) or `[JsonInclude]` (.NET) for non-public members
- [ ] Binary format version header for forward compatibility

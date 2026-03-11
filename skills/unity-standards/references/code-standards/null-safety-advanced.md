# Null Safety — Advanced

## Debug.Assert for Invariants

```csharp
void Awake()
{
    _rb = GetComponent<Rigidbody>();
    Debug.Assert(_rb != null, "Rigidbody missing on " + name, this);
    Debug.Assert(_maxHealth > 0, "MaxHealth must be positive", this);
}
```

## #nullable Directive (Unity 2021+)

Unity 2021+ supports C# `#nullable enable` for compile-time null analysis:

```csharp
#nullable enable

public class InventoryService
{
    // Compiler warns if you pass null where non-null expected
    public void AddItem(ItemData item) // item is non-null
    {
        _items.Add(item);
    }

    public ItemData? FindItem(string id) // return may be null
    {
        return _items.FirstOrDefault(i => i.Id == id);
    }
}
```

**⚠️ Limitation with Unity Objects:**
`#nullable` does NOT understand Unity's `== null` override. A `GameObject?` annotated as nullable still needs `== null` checks, not `is null`:

```csharp
#nullable enable
GameObject? target; // nullable annotation
if (target == null) return; // ✅ still use == for Unity objects
if (target is null) return; // ❌ wrong — bypasses Unity lifetime check
```

**Recommendation:** Use `#nullable enable` for pure C# service classes. Avoid on MonoBehaviour-heavy files where Unity null semantics dominate.

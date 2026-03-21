# Performance Checklist

## Allocations In Hot Paths (Update, FixedUpdate, LateUpdate)

- [ ] No string concatenation in hot loops - use `StringBuilder`, cached formatting, or UI-specific non-alloc formatting
- [ ] No LINQ in Update (`Where`, `Select`, `ToList` often allocate)
- [ ] No lambda or closure captures that allocate delegate state
- [ ] No boxing through `object`, interface calls, or formatting helpers
- [ ] No per-frame `new List<T>()` - reuse buffers with `.Clear()`
- [ ] No repeated `ToString()` on value types in hot paths

```csharp
// BAD: allocations every frame
void Update()
{
    var nearby = enemies.Where(e => e.IsAlive).ToList();
    debugText.text = "HP: " + health;
}

// GOOD: reusable buffers
private readonly List<Enemy> _nearbyCache = new();
private readonly StringBuilder _sb = new();

void Update()
{
    _nearbyCache.Clear();
    foreach (var e in enemies)
        if (e.IsAlive)
            _nearbyCache.Add(e);

    _sb.Clear();
    _sb.Append("HP: ").Append(health);
    debugText.SetText(_sb);
}
```

## Component And Object Lookup

| Pattern | Cost | Alternative |
|---------|------|-------------|
| `GetComponent<T>()` per frame | High | Cache in `Awake` or `Start` |
| `Find("name")` | Very high | Cache reference or inject |
| `FindObjectOfType<T>()` | Extreme | Registry, injection, or explicit wiring |
| `Camera.main` | Usually cached on newer Unity, still a tagged global lookup | Cache for older projects, hot paths, or multi-camera flows |
| `SendMessage("Method")` | Reflection and string dispatch | Direct call or interface |
| `CompareTag("tag")` | Preferred tag check | Use instead of `gameObject.tag == "tag"` |

## Physics

- [ ] `Physics.Raycast` uses a `layerMask` where possible
- [ ] `NonAlloc` variants used in hot loops: `RaycastNonAlloc`, `OverlapSphereNonAlloc`
- [ ] Rigidbody manipulation happens in `FixedUpdate`, not `Update`
- [ ] Static colliders are not moved at runtime
- [ ] Mesh colliders on rigidbodies are validated carefully and usually kept convex

## Rendering

- [ ] `Renderer.material` is not touched repeatedly in gameplay loops
- [ ] `sharedMaterial` used for read-only inspection
- [ ] `MaterialPropertyBlock` used for per-instance overrides without breaking batching
- [ ] Canvas split between static and dynamic UI when rebuild cost matters
- [ ] Text churn is batched instead of triggering repeated rebuilds

## Memory

- [ ] Textures sized appropriately per target platform
- [ ] Music streams, short SFX load appropriately for low latency
- [ ] `Resources.UnloadUnusedAssets()` used deliberately after large transitions
- [ ] Addressables handles released after use
- [ ] Object pooling used for frequent spawn and despawn cycles

<!-- Advanced: performance-checklist-advanced.md -->

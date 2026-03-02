# Performance Checklist

## Allocations in Hot Paths (Update/FixedUpdate/LateUpdate)

- [ ] No string concatenation — use `StringBuilder` or interpolated `Span<char>`
- [ ] No LINQ in Update (`Where`, `Select`, `ToList` allocate)
- [ ] No lambda/closure captures (allocate delegate + closure object)
- [ ] No boxing: `object val = myInt` or `string.Format("{0}", myInt)`
- [ ] No `new List<T>()` — reuse with `.Clear()`
- [ ] No `ToString()` on value types in hot paths

```csharp
// BAD: 3 allocations per frame
void Update()
{
    var nearby = enemies.Where(e => e.IsAlive).ToList(); // LINQ + closure + list
    debugText.text = "HP: " + health.ToString(); // string concat + ToString
}

// GOOD: Zero allocations
private List<Enemy> nearbyCache = new();
private StringBuilder sb = new();
void Update()
{
    nearbyCache.Clear();
    foreach (var e in enemies) if (e.IsAlive) nearbyCache.Add(e);
    sb.Clear(); sb.Append("HP: ").Append(health);
    debugText.SetText(sb);
}
```

## Component / Object Lookup

| Pattern | Cost | Alternative |
|---------|------|-------------|
| `GetComponent<T>()` per frame | High | Cache in `Awake` |
| `Find("name")` | Very High | Cache reference or inject |
| `FindObjectOfType<T>()` | Extreme | Singleton pattern or registry |
| `Camera.main` | Cached since Unity 2020.2 — safe on 2020.2+ | Cache on older versions |
| `SendMessage("Method")` | Reflection | Direct call or interface |
| `CompareTag("tag")` vs `tag == "tag"` | String alloc | Always use `CompareTag` |

## Physics

- [ ] `Physics.Raycast` uses layerMask parameter (avoids checking all layers)
- [ ] `NonAlloc` variants: `RaycastNonAlloc`, `OverlapSphereNonAlloc`
- [ ] Rigidbody manipulation in `FixedUpdate`, not `Update`
- [ ] Static colliders not moved at runtime (rebuilds physics tree)
- [ ] Mesh colliders marked convex if on Rigidbody

## Rendering

- [ ] `Material` access creates instance — use `sharedMaterial` for read
- [ ] `Renderer.material` in Update leaks material instances
- [ ] `MaterialPropertyBlock` for per-instance changes without instancing break
- [ ] Canvas: split dynamic from static elements into separate Canvases
- [ ] UI text changes trigger Canvas rebuild — batch changes

## Memory

- [ ] Textures: appropriate max size (mobile: 1024, desktop: 2048)
- [ ] Audio: streaming for music, decompress-on-load for short SFX
- [ ] `Resources.UnloadUnusedAssets()` after large scene transitions
- [ ] Addressables: release handles after use
- [ ] Object pooling for frequently spawned/destroyed objects

## Profiling Hooks

```csharp
// Mark expensive sections for Profiler
using (new ProfilerMarker("AI.PathFind").Auto())
{
    pathfinder.Calculate(start, end);
}
```

## Burst Compiler

- [ ] Hot-path math in `IJobParallelFor` with `[BurstCompile]` attribute
- [ ] No managed allocations inside Burst jobs (no `new`, `string`, `List<T>`)
- [ ] `[BurstCompile(FloatPrecision.Standard, FloatMode.Fast)]` for perf-critical paths
- [ ] Mathematics library (`float3`, `math.distance`) over `Vector3`/`Mathf` in jobs

```csharp
using Unity.Burst;
using Unity.Jobs;
using Unity.Collections;
using Unity.Mathematics;

[BurstCompile]
struct MoveJob : IJobParallelFor
{
    public NativeArray<float3> Positions;
    [ReadOnly] public NativeArray<float3> Velocities;
    public float DeltaTime;

    public void Execute(int i)
    {
        Positions[i] += Velocities[i] * DeltaTime;
    }
}
```

## ProfilerMarker Best Practices

```csharp
// Define as static readonly — avoid string allocation
static readonly ProfilerMarker s_AIUpdate = new("AI.Update");
static readonly ProfilerMarker s_Pathfinding = new("AI.Pathfinding");

void Update()
{
    using (s_AIUpdate.Auto())
    {
        using (s_Pathfinding.Auto())
        {
            _pathfinder.Calculate();
        }
    }
}
```

- [ ] `ProfilerMarker` defined as `static readonly` (not local `new`)
- [ ] Nested markers for sub-sections of expensive operations
- [ ] Custom markers on all operations taking > 1ms

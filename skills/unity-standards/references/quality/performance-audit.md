# Performance Audit

## Frame Budget

| Target FPS | Budget per Frame | Platform |
|------------|-----------------|----------|
| 60 | 16.67ms | PC, console |
| 30 | 33.33ms | Mobile, VR reprojection |
| 90 | 11.11ms | VR native |

- Scripting budget: ≤ 5ms of total frame
- Rendering budget: ≤ 8ms at 60fps
- Physics budget: ≤ 3ms at 60fps

## GC Hotspot Detection

Flag these in `Update`/`FixedUpdate`/`LateUpdate`:
- `string` concatenation (use `StringBuilder`)
- LINQ queries (allocates enumerators)
- `new` allocations (pool instead)
- Boxing via `object` params
- `foreach` on non-struct enumerators
- `GetComponent<T>()` (cache in `Awake`)
- Closure captures in lambdas

## Update Complexity

| Severity | Pattern |
|----------|---------|
| Critical | `FindObjectOfType` in Update |
| Critical | `Camera.main` in Update (pre-2020.2) |
| High | Nested loops in Update |
| High | Physics queries every frame without need |
| Medium | String operations in Update |
| Low | Multiple GetComponent calls (cacheable) |

## Physics Settings

- `Fixed Timestep`: 0.02 (50Hz) default, justify changes
- `Auto Sync Transforms`: OFF unless explicitly needed
- Layer collision matrix: disable unused layer pairs
- Rigidbody `interpolation`: use only on player-visible objects
- `Physics.Raycast` preferred over `RaycastAll` when single hit suffices

## Draw Call Budget

| Platform | Max Draw Calls | Max Batches |
|----------|---------------|-------------|
| Mobile | 100–200 | 50–100 |
| PC | 2000–3000 | 500–1000 |
| VR | 100–150 per eye | 50–75 |

- Enable GPU instancing on shared materials
- Use SRP Batcher with compatible shaders
- Atlas sprites to reduce material swaps

## Texture Memory Budget

| Platform | VRAM Budget | Max Texture Size |
|----------|-------------|-----------------|
| Mobile | 256–512 MB | 1024×1024 |
| PC | 2–4 GB | 4096×4096 |
| VR | 1–2 GB | 2048×2048 |

- Compress: ASTC (mobile), BC7/DXT5 (PC)
- Mip maps: ON for 3D, OFF for UI
- Read/Write: OFF unless needed at runtime

## Profiler Markers

```csharp
using Unity.Profiling;

static readonly ProfilerMarker s_MyMarker =
    new ProfilerMarker("MySystem.Process");

void Process()
{
    using (s_MyMarker.Auto())
    {
        // measured code
    }
}
```

- Add markers to systems processing > 100 entities
- Name format: `SystemName.MethodName`

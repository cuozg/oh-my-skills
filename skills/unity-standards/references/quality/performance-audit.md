# Performance Audit

## Frame Budget

| Target FPS | Budget per Frame | Platform |
|------------|-----------------|----------|
| 60 | 16.67ms | PC, console |
| 30 | 33.33ms | Mobile, thermally constrained devices |
| 90 | 11.11ms | VR native |

- Scripting budget: <= 5ms of total frame on a 60 FPS target
- Rendering budget: <= 8ms at 60 FPS
- Physics budget: <= 3ms at 60 FPS

## GC Hotspot Detection

Flag these in `Update`, `FixedUpdate`, or `LateUpdate`:
- `string` concatenation
- LINQ queries
- `new` allocations in loops
- Boxing via `object` or interface dispatch
- `foreach` over non-struct enumerators
- Repeated `GetComponent<T>()`
- Closure captures in lambdas

## Update Complexity

| Severity | Pattern |
|----------|---------|
| Critical | `FindObjectOfType` in Update |
| High | Repeated scene-wide lookup in Update (`Find*`, uncached global lookups in complex scenes) |
| High | Nested loops in Update |
| High | Physics queries every frame without need |
| Medium | String operations in Update |
| Low | Multiple cacheable component lookups |

## Physics Settings

- `Fixed Timestep`: 0.02 (50 Hz) by default; justify changes
- `Auto Sync Transforms`: off unless explicitly needed
- Layer collision matrix disables unused layer pairs
- Rigidbody `interpolation` only on player-visible objects that benefit from it
- `Physics.Raycast` preferred over `RaycastAll` when a single hit is enough

## Draw Call Budget

| Platform | Max Draw Calls | Max Batches |
|----------|----------------|-------------|
| Mobile | 100-200 | 50-100 |
| PC | 2000-3000 | 500-1000 |
| VR | 100-150 per eye | 50-75 |

- Enable GPU instancing on shared materials where it helps
- Use SRP Batcher with compatible shaders
- Atlas sprites to reduce material swaps

## Texture Memory Budget

| Platform | VRAM Budget | Max Texture Size |
|----------|-------------|-----------------|
| Mobile | 256-512 MB | 1024x1024 |
| PC | 2-4 GB | 4096x4096 |
| VR | 1-2 GB | 2048x2048 |

- Compress with ASTC for mobile and BC formats for desktop where supported
- Mip maps on for 3D, off for UI unless required
- Read/Write off unless runtime mutation needs it

## Profiler Markers

```csharp
using Unity.Profiling;

private static readonly ProfilerMarker s_MyMarker =
    new ProfilerMarker("MySystem.Process");

void Process()
{
    using (s_MyMarker.Auto())
    {
        // measured code
    }
}
```

- Add markers to systems processing meaningful work each frame
- Name markers `SystemName.MethodName`

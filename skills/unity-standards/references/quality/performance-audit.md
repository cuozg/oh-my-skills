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
- Boxing value types via `object` or interface casts
- `foreach` over non-struct enumerators
- Repeated `GetComponent<T>()`
- Closure captures in lambdas

## Update Complexity

| Severity | Pattern |
|----------|---------|
| Critical | Scene-wide `FindObjectsByType` / `FindFirstObjectByType` / `FindAnyObjectByType` in Update |
| High | Repeated name/tag lookup in Update (`GameObject.Find*`, uncached global lookups) |
| High | Nested loops in Update |
| High | Physics queries every frame without need |
| Medium | String operations in Update |
| Low | Multiple cacheable component lookups |

## Physics Settings

Audit against `references/optimization/physics-settings.md`. Flag:
- `Fixed Timestep` changed from 0.02 (50 Hz) without justification
- `Auto Sync Transforms` on without need
- Layer collision matrix left fully enabled
- `Physics.simulationMode` = `Script` without a matching `Physics.Simulate` owner

## Draw Call Budget

| Platform | Max Draw Calls | Max Batches |
|----------|----------------|-------------|
| Mobile | 100-200 | 50-100 |
| PC | 2000-3000 | 500-1000 |
| VR | 100-150 per eye | 50-75 |

- Batching strategy (SRP Batcher, instancing): `references/optimization/rendering-settings.md`
- UI batching: `references/optimization/canvas-ui-drawcalls-batching.md`

## Texture Memory Budget

| Platform | VRAM Budget | Max Texture Size |
|----------|-------------|-----------------|
| Mobile | 256-512 MB | 1024x1024 |
| PC | 2-4 GB | 4096x4096 |
| VR | 1-2 GB | 2048x2048 |

- Import settings (compression, mipmaps, Read/Write): `references/optimization/memory-settings.md`, `references/optimization/build-settings.md`

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

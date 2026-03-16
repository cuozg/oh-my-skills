# Jobs System & Burst Compiler Migration

## When to Migrate

| Scenario | Migrate to Jobs/Burst? |
|----------|----------------------|
| Processing 100+ entities per frame (movement, AI, pathfinding) | Yes |
| Heavy math (physics simulation, procedural generation) | Yes |
| Data transformation on large arrays | Yes |
| Single MonoBehaviour update logic | No — overhead not worth it |
| UI/event handling | No — not parallelizable |
| I/O, networking, file access | No — managed code required |

**Rule of thumb:** If a `for` loop runs 100+ iterations per frame on value-type data, consider Jobs.

## Basic Job Pattern

```csharp
using Unity.Burst;
using Unity.Collections;
using Unity.Jobs;
using Unity.Mathematics;

// 1. Define the job
[BurstCompile]
struct MoveEntitiesJob : IJobParallelFor
{
    public NativeArray<float3> Positions;
    [ReadOnly] public NativeArray<float3> Velocities;
    public float DeltaTime;

    public void Execute(int index)
    {
        Positions[index] += Velocities[index] * DeltaTime;
    }
}

// 2. Schedule from MonoBehaviour
public class EntityMover : MonoBehaviour
{
    private NativeArray<float3> _positions;
    private NativeArray<float3> _velocities;
    private JobHandle _moveHandle;

    void Update()
    {
        var job = new MoveEntitiesJob
        {
            Positions = _positions,
            Velocities = _velocities,
            DeltaTime = Time.deltaTime
        };
        _moveHandle = job.Schedule(_positions.Length, 64); // batch size 64
    }

    void LateUpdate()
    {
        _moveHandle.Complete(); // sync point — apply results
        // Read _positions here
    }

    void OnDestroy()
    {
        _moveHandle.Complete();
        _positions.Dispose();
        _velocities.Dispose();
    }
}
```

## Job Types

| Type | Use Case | Scheduling |
|------|----------|-----------|
| `IJob` | Single work item | `job.Schedule()` |
| `IJobParallelFor` | Process array in parallel | `job.Schedule(length, batchSize)` |
| `IJobFor` | Process array sequentially | `job.Schedule(length)` or `.ScheduleParallel()` |
| `IJobParallelForTransform` | Modify Transform array | `job.Schedule(transformAccessArray)` |

## Burst Compiler Constraints

**Allowed in Burst:**
- `NativeArray`, `NativeList`, `NativeHashMap` (value-type containers)
- `Unity.Mathematics` types (`float3`, `float4x4`, `quaternion`)
- `math.*` functions (`math.distance`, `math.lerp`, `math.clamp`)
- Fixed-size buffers, `stackalloc`
- Static readonly fields of blittable types

**NOT allowed in Burst:**
- `string`, `List<T>`, `Dictionary<K,V>` (managed types)
- `new` allocations of reference types
- `try/catch` (exception handling)
- Virtual methods, interfaces (non-static)
- `Debug.Log` (use `Unity.Logging` or conditional compilation)
- `UnityEngine.Object` access (Transform, GameObject, etc.)

## Data Layout for Performance

```csharp
// ❌ Array of Structs (AoS) — poor cache locality for Jobs
struct Entity { float3 position; float3 velocity; float health; }
NativeArray<Entity> entities; // jobs access all fields even if only using position

// ✅ Struct of Arrays (SoA) — excellent cache locality
NativeArray<float3> positions;
NativeArray<float3> velocities;
NativeArray<float> healths;
```

## Migration Checklist

1. **Profile first** — confirm the loop is actually a bottleneck (> 1ms)
2. **Extract data** — separate logic from MonoBehaviour, use value types
3. **Allocate NativeContainers** — `Allocator.Persistent` for long-lived, `TempJob` for frame-scoped
4. **Write job struct** — implement `IJobParallelFor`, use `[ReadOnly]` on input arrays
5. **Add `[BurstCompile]`** — verify no managed type errors
6. **Schedule in Update** — complete in LateUpdate (or next frame's Update for one-frame latency)
7. **Dispose in OnDestroy** — all NativeContainers MUST be disposed
8. **Batch size** — start with 64, profile to find optimal (32-256 range)

## Common Pitfalls

- Forgetting `[ReadOnly]` → safety system blocks parallel execution
- Completing immediately after scheduling → no parallelism benefit
- Too-small batch size → scheduling overhead dominates
- Not disposing NativeContainers → memory leak + editor warnings
- Accessing managed objects inside job → Burst compilation error

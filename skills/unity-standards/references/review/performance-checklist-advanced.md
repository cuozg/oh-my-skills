# Performance Checklist — Advanced

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

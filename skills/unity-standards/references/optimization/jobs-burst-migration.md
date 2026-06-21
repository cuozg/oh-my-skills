# Jobs, Burst, And ECS Migration

Use this when moving slow Unity runtime work toward Jobs, Burst, or ECS. Do not
migrate because the API exists; migrate when profiling shows CPU cost, scale, or
allocation pressure that simpler code cannot handle cleanly.

## Migration Decision

| Current Problem | First Move | Escalate When |
| --- | --- | --- |
| Small hot loop in a MonoBehaviour | Cache data, remove allocations, tighten loop | CPU remains high in profiler |
| Many independent calculations | `IJobParallelFor` or `IJobFor` | data is already contiguous |
| Transform-heavy object update | `IJobParallelForTransform` if supported by project | GameObject architecture remains required |
| Large entity simulation | ECS `ISystem` / `IJobEntity` | data ownership can move to components |
| Burst-compatible math bottleneck | Burst job or static Burst method | logic avoids managed objects and UnityEngine API |

Stay with MonoBehaviours when the code is UI, rare, authoring-heavy,
scene-object-heavy, or easier to prove with ordinary C#.

## Preconditions

- Profile first: capture frame time, marker name, call count, GC allocs, and
  target hardware/platform when available.
- Identify data ownership: who writes, who reads, lifetime, and reset rules.
- Check package and Unity version before using Entities, Burst, Collections, or
  TransformAccess APIs.
- Verify the project already accepts the complexity. A one-off job framework for
  one minor feature is usually the wrong trade.

## Data Layout Standards

- Prefer contiguous blittable structs for job data.
- Copy only the data the job needs; do not pass scene objects.
- Use Structure of Arrays when jobs scan one field across many items.
- Use Array of Structs when each item is processed as a coherent unit.
- Keep NativeContainer ownership explicit and dispose at the owner lifetime.

```csharp
public struct SteeringInput
{
    public float3 Position;
    public float3 Target;
    public float Speed;
}
```

## Job Rules

- Mark read-only containers with `[ReadOnly]`.
- Do not access `GameObject`, `Transform`, `Component`, `Debug.Log`, or most
  `UnityEngine` APIs inside Burst jobs.
- Chain `JobHandle`s for read/write dependencies; complete only when the main
  thread needs the result.
- Never dispose a NativeContainer before all jobs using it have completed.
- Avoid scheduling tiny jobs where overhead exceeds work.
- Use `Allocator.TempJob` for short jobs and dispose within the required window;
  use `Persistent` only for long-lived owned buffers.

```csharp
[BurstCompile]
public struct DistanceJob : IJobParallelFor
{
    [ReadOnly] public NativeArray<float3> Positions;
    public float3 Origin;
    public NativeArray<float> Distances;

    public void Execute(int index)
    {
        Distances[index] = math.lengthsq(Positions[index] - Origin);
    }
}
```

## Burst Standards

Burst-compatible code:

- Uses blittable structs and primitive/math types.
- Uses `Unity.Mathematics` instead of `UnityEngine` object APIs.
- Avoids managed allocations, classes, virtual dispatch, delegates, exceptions,
  reflection, LINQ, strings, and most collection types.
- Keeps deterministic math requirements explicit if gameplay depends on them.

Use Burst Inspector or compiler diagnostics when performance or compatibility is
unclear. Disable Burst temporarily only to isolate whether a bug is Burst-specific
or a normal logic/data issue.

## ECS Escalation

Move to ECS when the domain is data-heavy and object identity is less important
than throughput: crowds, projectiles, board cells, status effects, simulation
agents, or repeated stateless processing.

ECS migration shape:

1. Convert authored data with Bakers or an existing authoring pipeline.
2. Represent runtime state as small `IComponentData` structs.
3. Process with systems that have clear query ownership.
4. Use `EntityCommandBuffer` for structural changes.
5. Keep GameObject bridges at the edge for visuals, UI, and legacy systems.

Avoid partial ECS that duplicates truth in both GameObjects and components
without an explicit authority.

## Common Failure Modes

| Symptom | Likely Cause | Check |
| --- | --- | --- |
| NativeContainer leak warning | missing dispose or incomplete dependency | owner lifetime and job handles |
| Safety error on read/write | parallel write or missing dependency | attributes, job chain, ECB timing |
| Entity not processed | query mismatch or wrong world | required components, enableable state, world |
| Burst compile failure | managed type/API in job | diagnostics and Burst-compatible code path |
| Slower after migration | scheduling/copy overhead | profiler marker and batch size |

## Verification

- Compare profiler before/after with the same scene, data size, and platform when
  practical.
- Add tests for pure data transforms before changing the runtime pipeline.
- For ECS, inspect entity counts and query matches in the target world.
- For jobs, verify dependency completion, disposal, and deterministic outputs.
- Document the old bottleneck, new architecture, and measured tradeoff in the PR
  or task notes.

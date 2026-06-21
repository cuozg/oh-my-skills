# ECS, Jobs, And Burst Debugging

Use this when diagnosing Entities, Job System, Burst, NativeContainer, or
data-oriented runtime bugs. Debug the data path first; most failures are query,
world, dependency, lifetime, or baking mismatches.

## First Triage

| Symptom | Likely Area | First Checks |
| --- | --- | --- |
| Works without Burst, fails with Burst | Burst compatibility or unsafe behavior | Burst diagnostics, managed API usage, uninitialized data |
| Works on main thread, fails scheduled | dependency or race | job handles, read/write attributes, completion |
| Entity not processed | query mismatch | components, tags, enableable state, `RequireForUpdate` |
| Entity has wrong data | Baker, system order, ECB timing | baked values, update groups, playback point |
| NativeContainer safety error | ownership/lifetime | allocator, disposal, dependency completion |
| Editor OK, player broken | Burst/IL2CPP/package define | development build, package versions, stripping |

## Debugging Order

1. Reproduce with Burst enabled and disabled.
2. Read console messages from Burst, Jobs, Collections, and Entities.
3. Identify the world: default, test, baking, client, server, or subscene world.
4. Inspect entity existence, component values, tags, and enableable state.
5. Verify query shape and `RequireForUpdate` gates.
6. Verify system group/order and ECB playback timing.
7. Verify job dependencies, completion points, and NativeContainer disposal.
8. Add temporary instrumentation outside Burst jobs or write sampled debug data
   to a NativeContainer and log after completion.

## Query Failures

When an entity is not processed, check:

- The entity exists in the same world as the system.
- It has every `WithAll` / query component.
- It does not have an excluded `WithNone` tag.
- Any `IEnableableComponent` required by the query is enabled.
- The system is not blocked by `RequireForUpdate`.
- The system group runs in the current test/scene/player state.
- ECB commands that create/add components have already played back.

Temporary query count logging is acceptable outside hot Burst paths:

```csharp
EntityQuery query = SystemAPI.QueryBuilder()
    .WithAll<LocalTransform, MoveSpeed>()
    .WithNone<DeadTag>()
    .Build();

UnityEngine.Debug.Log($"Move query matched {query.CalculateEntityCount()} entities");
```

## Job Dependency Failures

Checklist:

- Producer job handle flows into consumer job scheduling.
- ECS jobs assign the final handle to `state.Dependency`.
- Main-thread reads call `Complete()` first.
- NativeContainer disposal happens after all jobs using it complete.
- Parallel writes use `ParallelWriter` or unique indices.
- Safety-disabling attributes have a written proof of non-overlap.

Race smells:

| Smell | Risk |
| --- | --- |
| `[NativeDisableParallelForRestriction]` added to silence errors | real write conflict may remain |
| Multiple jobs write same container | missing dependency or wrong parallel writer |
| Immediate `Complete()` after every schedule | correct but likely no parallelism benefit |
| `Allocator.TempJob` survives too long | leak warning or invalid memory |

## Burst Failures

If disabling Burst changes behavior, inspect for:

- Managed types in the job path: `string`, `class`, `List<T>`, `Dictionary`, Unity objects.
- Managed operations: exceptions, reflection, LINQ, virtual/interface dispatch, logging.
- Undefined or uninitialized data.
- Unsafe pointer code or disabled safety checks.
- Floating-point assumptions changed by Burst optimization settings.

Do not log directly from hot Burst jobs. For diagnostics, write a small sampled
struct to a pre-sized NativeContainer and log it on the main thread after the job
completes.

## Baking And ECB Failures

Baking checks:

- Authoring component exists and Baker assembly is included.
- Required prefab/object fields are assigned.
- `GetEntity` uses the correct transform usage flags.
- Values are validated or clamped during baking.
- Subscenes are reimported/rebaked after authoring changes.

ECB checks:

- Begin/end ECB system matches when the structural change must become visible.
- Destroyed entities are not used before playback.
- Another system does not overwrite component values after playback.
- ECB belongs to the same world/entity manager.

## NativeContainer And Memory Failures

- Persistent containers dispose in the owner cleanup path.
- TempJob containers dispose within their valid lifetime.
- `Dispose(JobHandle)` is used when disposal can be scheduled.
- `Clear()` reuses capacity; it does not free memory.
- Use clear memory when default values matter.

## Evidence Format

Use this compact report shape:

```text
Evidence: Assets/.../MoveSystem.cs:42
World: Default World
System: MoveSystem in SimulationSystemGroup
Query: LocalTransform + MoveSpeed, WithNone<DeadTag>
Observed: query matched 0 entities; expected about 120 enemies
Likely cause: Baker adds SpeedConfig but system queries MoveSpeed
Confidence: High
```

## Verification

- Console safety errors are gone.
- Query counts and entity state match expected data.
- Job dependencies and disposal paths are proven by code or tests.
- Burst-enabled behavior matches Burst-disabled behavior unless the difference is
  intentional and documented.
- Profiling still supports the data-oriented path after the fix.

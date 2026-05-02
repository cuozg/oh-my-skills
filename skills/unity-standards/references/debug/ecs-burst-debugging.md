# ECS, Jobs & Burst Debugging

Use this reference when diagnosing Unity Entities, Job System, Burst compiler, NativeContainer, or data-oriented runtime bugs.

## First Triage

| Symptom | Likely Area | First Checks |
|---------|-------------|--------------|
| Works without Burst, fails with Burst | Burst compatibility or undefined behavior | Disable Burst, inspect Burst errors, check managed API usage |
| Works on main thread, fails when scheduled | Job dependency or race | Verify `state.Dependency`, `Complete()`, read/write attributes |
| Entities not processed | Query mismatch | Check required components, tags, enableable state, system update requirements |
| Entity exists but has wrong data | Baker, ECB playback, or system ordering | Inspect baked components, update groups, ECB timing |
| Safety exception from NativeContainer | Ownership or lifetime bug | Check allocator, disposal, dependency completion |
| Intermittent wrong results | Race or structural-change timing | Look for disabled safety attributes, shared writes, immediate reads after scheduling |
| Editor OK, player build broken | Burst/IL2CPP/package define issue | Test development build, Burst synchronous compile, package versions |

---

## Debugging Order

1. Reproduce with Burst enabled and disabled.
2. Check Console for Burst, Jobs, and Collections safety messages.
3. Check Entities Hierarchy / Entity Debugger for entity existence and component values.
4. Verify query shape against actual components and tags.
5. Verify system update order and `RequireForUpdate` gates.
6. Verify job dependencies and NativeContainer lifetimes.
7. Add minimal instrumentation outside Burst jobs or use data flags written by jobs.
8. Re-profile after fixing to confirm the original performance goal still holds.

---

## Burst Debugging

### Isolate Burst vs Logic

Temporarily disable Burst to determine whether the bug is Burst-specific or general logic:

- Jobs menu / Burst menu: disable Burst compilation for a quick editor check.
- Add `CompileSynchronously = true` when investigating compile behavior.
- Compare behavior in Editor and Development Build.

```csharp
[BurstCompile(CompileSynchronously = true)]
public partial struct SuspectJob : IJobEntity
{
    public void Execute(ref Health health)
    {
        health.Current = math.max(0f, health.Current);
    }
}
```

If disabling Burst fixes the issue, search for managed API usage, uninitialized memory, out-of-bounds access hidden by disabled safety, unsafe pointer code, non-deterministic floating point assumptions, and reliance on exceptions.

### Common Burst Error Causes

| Error Signal | Cause | Fix |
|--------------|-------|-----|
| Managed type not supported | `string`, `List<T>`, `class`, `UnityEngine.Object` in job path | Replace with unmanaged data, fixed strings, NativeContainers, or entity references |
| Exception handling not supported | `try/catch`, throwing exceptions | Return error codes, flags, or validate before scheduling |
| Method not Burst-compatible | Virtual/interface dispatch or managed helper | Use static methods or struct helpers with unmanaged inputs |
| `Debug.Log` unavailable/expensive | Logging inside Burst job | Write debug data to NativeContainer and log after `Complete()` |
| Different player result | Float precision or fast math | Use deterministic math settings and avoid `FloatMode.Fast` for gameplay-critical paths |

### Debug Data Pattern

Do not log from hot Burst jobs. Write compact diagnostic data and inspect after completion.

```csharp
public struct HealthDebugSample
{
    public Entity Entity;
    public float Before;
    public float After;
}

[BurstCompile]
public partial struct DamageDebugJob : IJobEntity
{
    public NativeList<HealthDebugSample>.ParallelWriter Samples;
    public float Damage;

    private void Execute(Entity entity, ref Health health)
    {
        float before = health.Current;
        health.Current = math.max(0f, health.Current - Damage);
        Samples.AddNoResize(new HealthDebugSample
        {
            Entity = entity,
            Before = before,
            After = health.Current
        });
    }
}
```

Pre-size the list and log sampled results on the main thread after the dependency completes.

---

## Job Dependency Debugging

### Dependency Checklist

- Every scheduled job that reads previous job output depends on the producer job handle.
- `state.Dependency` is assigned when scheduling ECS jobs.
- Main-thread reads call `Complete()` first.
- Disposals are scheduled after jobs or happen after completion.
- Parallel writes use `ParallelWriter` or unique indices.
- Safety-disabling attributes are justified by provable non-overlap.

```csharp
JobHandle buildHandle = new BuildJob
{
    Output = output
}.ScheduleParallel(count, 64, state.Dependency);

JobHandle consumeHandle = new ConsumeJob
{
    Input = output
}.ScheduleParallel(count, 64, buildHandle);

state.Dependency = consumeHandle;
```

### Race Smells

| Smell | Risk |
|-------|------|
| `[NativeDisableParallelForRestriction]` added to silence errors | Real write conflict may still exist |
| Multiple jobs write the same container | Missing dependency or concurrent writer misuse |
| `Complete()` called immediately after scheduling | Correct but no parallelism benefit |
| Main thread reads `NativeArray` after scheduling without complete | Undefined behavior or safety exception |
| `Allocator.TempJob` lives beyond four frames | Leak warning or memory corruption risk |

---

## ECS Query Debugging

### Entity Not Processed

Check these in order:

1. Does the entity exist in the expected world?
2. Does it have every component required by the query?
3. Does it have an excluded `WithNone<T>` component or tag?
4. Is an `IEnableableComponent` disabled?
5. Is the system blocked by `RequireForUpdate<T>()`?
6. Is the system in an update group that actually runs?
7. Did an ECB command not play back yet?
8. Was the entity created in a different world, subscene, or test world?

```csharp
public void OnUpdate(ref SystemState state)
{
    EntityQuery query = SystemAPI.QueryBuilder()
        .WithAll<LocalTransform, MoveSpeed>()
        .WithNone<DeadTag>()
        .Build();

    int count = query.CalculateEntityCount();
    UnityEngine.Debug.Log($"Movement query matched {count} entities");
}
```

Keep this kind of logging temporary and outside Burst-compiled hot jobs.

### Wrong World Issues

Entities live in worlds. A query in one world cannot see entities in another.

| Context | World Risk |
|---------|------------|
| Edit Mode tests | Test world vs default world |
| Baking | Baking world vs runtime world |
| NetCode | Client, server, thin client worlds |
| Subscenes | Streaming and conversion timing |

Always identify the world when debugging entity count mismatches.

---

## Baking Debugging

### Common Baker Failures

| Symptom | Cause | Fix |
|---------|-------|-----|
| Component missing on entity | Baker not running or wrong `GetEntity` flags | Verify authoring component and Baker nesting/assembly |
| Transform not updating | Wrong `TransformUsageFlags` | Use `Dynamic` for moving entities, `Renderable` for render-only |
| Prefab entity is null/default | Prefab field missing or not baked as entity | Use `GetEntity(authoring.Prefab, flags)` |
| Values defaulted | Serialized field unset or clamped incorrectly | Inspect authoring object and Baker validation |
| Works in scene, not subscene | Subscene not reopened/rebaked | Reimport/reopen subscene, check baking errors |

### Baker Validation Pattern

Validate authoring data during baking so runtime systems can avoid defensive branches.

```csharp
public override void Bake(SpawnerAuthoring authoring)
{
    Entity entity = GetEntity(TransformUsageFlags.None);

    if (authoring.Prefab == null)
    {
        UnityEngine.Debug.LogError($"Spawner missing prefab on {authoring.name}", authoring);
        return;
    }

    AddComponent(entity, new Spawner
    {
        Prefab = GetEntity(authoring.Prefab, TransformUsageFlags.Dynamic),
        Interval = math.max(0.01f, authoring.Interval)
    });
}
```

---

## EntityCommandBuffer Debugging

### ECB Timing Problems

| Symptom | Likely Cause |
|---------|--------------|
| Entity not visible until next frame | ECB playback happens later in the group |
| Component value overwritten | Another system runs after ECB playback |
| Destroyed entity still appears this frame | Destroy is deferred until playback |
| Invalid entity in ECB | Entity destroyed before playback or wrong world/entity manager |

Pick the ECB system based on when the structural change should become visible:

| ECB Singleton | Visibility Timing |
|---------------|-------------------|
| `BeginInitializationEntityCommandBufferSystem.Singleton` | Early setup |
| `BeginSimulationEntityCommandBufferSystem.Singleton` | Before most gameplay simulation |
| `EndSimulationEntityCommandBufferSystem.Singleton` | After gameplay simulation |
| `BeginPresentationEntityCommandBufferSystem.Singleton` | Before presentation |

---

## NativeContainer & Memory Debugging

### Leak / Disposal Checklist

- Persistent containers are disposed in `OnDestroy` or equivalent cleanup.
- TempJob containers are disposed within four frames.
- Disposal waits for producer/consumer jobs to complete.
- `Dispose(JobHandle)` is used when disposal should be scheduled.
- `NativeList.Clear()` reuses memory; it does not free capacity.

```csharp
JobHandle jobHandle = new FillJob { Output = output }.ScheduleParallel(count, 64, state.Dependency);
JobHandle disposeHandle = output.Dispose(jobHandle);
state.Dependency = disposeHandle;
```

### Uninitialized Memory

Use clear memory when defaults matter.

```csharp
NativeArray<float> scores = new NativeArray<float>(count, Allocator.TempJob, NativeArrayOptions.ClearMemory);
```

Without clear memory, containers may contain undefined values.

---

## Performance Debugging

### ECS/Burst Profiling Checklist

- Use Timeline Profiler to inspect job scheduling, worker utilization, and main-thread sync points.
- Use Entities Systems window to identify expensive systems.
- Use Burst Inspector for generated code, vectorization, and scalar fallbacks.
- Compare Burst on/off timings in a Development Build, not only Editor.
- Look for main-thread waits caused by early `Complete()` or structural changes.
- Check query entity counts to confirm the optimized system processes expected volume.

### False Optimization Signals

| Signal | Why It Misleads |
|--------|-----------------|
| Editor-only speedup | Burst/player behavior can differ from Editor timing |
| Microbenchmark only | Scheduling overhead may dominate in real frame flow |
| Immediate `Complete()` benchmark | Measures job overhead without parallel overlap |
| Empty query timing | Optimized system may be doing no work |
| Safety disabled benchmark | Hides races and may not be production-safe |

---

## Investigation Evidence Format

Use this evidence format in ECS/Burst debug reports:

```text
Evidence: Assets/.../MovementSystem.cs:42
World: Default World
System: MovementSystem in SimulationSystemGroup
Query: LocalTransform + MoveSpeed, WithNone<DeadTag>
Observed: query matched 0 entities; expected ~120 enemies
Likely cause: Baker adds SpeedConfig but system queries MoveSpeed
Confidence: High
```

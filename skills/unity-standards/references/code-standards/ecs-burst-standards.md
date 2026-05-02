# ECS, Jobs & Burst Code Standards

Use this reference when writing or refactoring Unity DOTS / ECS code, Job System code, Burst-compiled code, or data-oriented runtime systems.

## Decision Guide

| Problem | Preferred Approach | Avoid |
|---------|--------------------|-------|
| Many similar entities updated every frame | ECS `ISystem` + `IJobEntity` | Thousands of `MonoBehaviour.Update()` calls |
| Heavy pure math over arrays | `IJobFor` / `IJobParallelFor` + Burst | Managed collections in hot loops |
| GameObject transform batch movement | `IJobParallelForTransform` or ECS transforms | Direct Transform loops in `Update()` |
| Occasional scene object behavior | Plain `MonoBehaviour` | ECS migration without measurable bottleneck |
| Designer-authored data | Authoring `MonoBehaviour` + Baker | Runtime conversion hacks |
| Frequent entity create/destroy | Pool-like enable/disable or ECB batching | Structural changes inside tight loops |

Prefer ECS/Burst for data-parallel, CPU-bound work. Keep normal `MonoBehaviour` code for UI, one-off interactions, scene orchestration, and Unity API-heavy behavior.

---

## Package & Version Awareness

ECS APIs change across Entities versions. Before adding or modifying DOTS code:

- Check `Packages/manifest.json` for `com.unity.entities`, `com.unity.burst`, `com.unity.collections`, `com.unity.mathematics`, and `com.unity.physics` versions.
- Prefer Entities 1.x patterns: `ISystem`, `SystemAPI`, Bakers, `LocalTransform`, `IJobEntity`, `EntityCommandBuffer` singletons.
- Treat older APIs such as `IConvertGameObjectToEntity`, `Translation`, `Rotation`, and `GameObjectConversionUtility` as legacy unless the project already uses pre-1.0 Entities.
- Load `references/other/official-source-map.md` for version-sensitive API behavior.

---

## ECS Architecture Rules

### Data, Logic, Authoring Separation

Use three explicit layers:

| Layer | Types | Responsibility |
|-------|-------|----------------|
| Authoring | `MonoBehaviour`, Baker | Inspector input and conversion to ECS data |
| Data | `IComponentData`, `IBufferElementData`, tags | Runtime state stored in chunks |
| Logic | `ISystem`, `IJobEntity`, `IJobChunk` | Stateless processing over matching entities |

```csharp
using Unity.Entities;
using Unity.Mathematics;
using Unity.Transforms;
using UnityEngine;

public sealed class MoveSpeedAuthoring : MonoBehaviour
{
    [SerializeField] private float _metersPerSecond = 5f;

    private sealed class Baker : Baker<MoveSpeedAuthoring>
    {
        public override void Bake(MoveSpeedAuthoring authoring)
        {
            Entity entity = GetEntity(TransformUsageFlags.Dynamic);
            AddComponent(entity, new MoveSpeed { Value = math.max(0f, authoring._metersPerSecond) });
        }
    }
}

public struct MoveSpeed : IComponentData
{
    public float Value;
}

[BurstCompile]
public partial struct MoveForwardSystem : ISystem
{
    [BurstCompile]
    public void OnUpdate(ref SystemState state)
    {
        float deltaTime = SystemAPI.Time.DeltaTime;

        foreach (var (transform, speed) in SystemAPI.Query<RefRW<LocalTransform>, RefRO<MoveSpeed>>())
        {
            LocalTransform value = transform.ValueRO;
            value.Position += value.Forward() * speed.ValueRO.Value * deltaTime;
            transform.ValueRW = value;
        }
    }
}
```

### Component Design

Prefer small, focused, unmanaged components.

| Rule | Rationale |
|------|-----------|
| Keep components blittable/unmanaged | Required for chunk storage and Burst-friendly jobs |
| Split unrelated fields into separate components | Systems only load data they need |
| Use tag components for state filters | Zero-sized tags are cheap and query-friendly |
| Use enableable components for frequent on/off state | Avoid archetype churn from add/remove |
| Use dynamic buffers for variable-length per-entity data | Avoid managed `List<T>` and separate lookup tables |
| Use shared components sparingly | Shared values partition chunks and can fragment data |

```csharp
public struct Health : IComponentData
{
    public float Current;
    public float Max;
}

public struct DeadTag : IComponentData { }

public struct TargetBufferElement : IBufferElementData
{
    public Entity Value;
}

public struct CanMove : IComponentData, IEnableableComponent { }
```

Avoid large catch-all components such as `CharacterState` with movement, combat, animation, AI, and inventory fields mixed together.

---

## System Standards

### Prefer `ISystem` For Runtime Systems

Use `ISystem` for high-performance systems because it is unmanaged and Burst-compatible. Use `SystemBase` only when the code must hold managed state or integrate with APIs that do not fit `ISystem`.

```csharp
[UpdateInGroup(typeof(SimulationSystemGroup))]
[BurstCompile]
public partial struct DamageOverTimeSystem : ISystem
{
    [BurstCompile]
    public void OnCreate(ref SystemState state)
    {
        state.RequireForUpdate<DamageOverTime>();
    }

    [BurstCompile]
    public void OnUpdate(ref SystemState state)
    {
        float deltaTime = SystemAPI.Time.DeltaTime;

        foreach (var (health, dot) in SystemAPI.Query<RefRW<Health>, RefRO<DamageOverTime>>())
        {
            health.ValueRW.Current -= dot.ValueRO.DamagePerSecond * deltaTime;
        }
    }
}
```

### Require Data Before Updating

Use `state.RequireForUpdate<T>()` or a cached query requirement when a system has no useful work without specific data. This prevents empty query overhead and avoids running bootstrap-dependent logic too early.

### Update Order Is Part Of The Contract

Declare order at the system level when behavior depends on another system.

```csharp
[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateAfter(typeof(SpawnSystem))]
[UpdateBefore(typeof(TransformSystemGroup))]
public partial struct MovementSystem : ISystem { }
```

Avoid relying on file names, assembly order, or incidental system creation order.

---

## Query Standards

### Use Read-Only Access By Default

Use `RefRO<T>` unless the system actually writes the component. Use `RefRW<T>` only for modified data.

```csharp
foreach (var (transform, speed) in SystemAPI.Query<RefRW<LocalTransform>, RefRO<MoveSpeed>>())
{
    transform.ValueRW.Position += transform.ValueRO.Forward() * speed.ValueRO.Value * deltaTime;
}
```

### Avoid Query Construction In Inner Loops

Create queries once in `OnCreate` when reused, or keep `SystemAPI.Query` at the top-level system loop. Do not build queries per entity.

### Use Filters Intentionally

| Filter | Use For | Cost/Risk |
|--------|---------|-----------|
| `WithAll<T>` | Required components or tags | Usually cheap |
| `WithNone<T>` | Excluding dead/disabled/special states | Good for state filters |
| `WithAny<T>` | Alternative component shapes | Can make behavior harder to reason about |
| Change filters | Work only when data changed | Can skip needed work if dependencies are misunderstood |
| Shared component filters | Chunk partitioning | Can cause fragmentation if overused |

---

## Structural Changes

Structural changes alter archetypes and can force synchronization. Treat them as expensive.

| Operation | Structural? | Preferred Timing |
|-----------|-------------|------------------|
| Create/destroy entity | Yes | Batched via ECB |
| Add/remove component | Yes | Batched via ECB or init/cleanup phase |
| Enable/disable `IEnableableComponent` | No archetype move | Good for frequent state toggles |
| Set component value | No | Safe in jobs with correct access |
| Append to dynamic buffer | No archetype move after buffer exists | Safe with ownership rules |

Use `EntityCommandBuffer` for structural changes from systems and jobs.

```csharp
[BurstCompile]
public partial struct KillDeadEntitiesSystem : ISystem
{
    [BurstCompile]
    public void OnCreate(ref SystemState state)
    {
        state.RequireForUpdate<EndSimulationEntityCommandBufferSystem.Singleton>();
    }

    [BurstCompile]
    public void OnUpdate(ref SystemState state)
    {
        EntityCommandBuffer ecb = SystemAPI
            .GetSingleton<EndSimulationEntityCommandBufferSystem.Singleton>()
            .CreateCommandBuffer(state.WorldUnmanaged);

        foreach (var (health, entity) in SystemAPI.Query<RefRO<Health>>().WithEntityAccess())
        {
            if (health.ValueRO.Current <= 0f)
                ecb.AddComponent<DeadTag>(entity);
        }
    }
}
```

For parallel jobs, use `EntityCommandBuffer.ParallelWriter` and pass the chunk index sort key.

---

## Job Standards

### Prefer `IJobEntity` For ECS Entity Processing

```csharp
[BurstCompile]
public partial struct ApplyVelocityJob : IJobEntity
{
    public float DeltaTime;

    private void Execute(ref LocalTransform transform, in Velocity velocity)
    {
        transform.Position += velocity.Value * DeltaTime;
    }
}

[BurstCompile]
public partial struct ApplyVelocitySystem : ISystem
{
    [BurstCompile]
    public void OnUpdate(ref SystemState state)
    {
        state.Dependency = new ApplyVelocityJob
        {
            DeltaTime = SystemAPI.Time.DeltaTime
        }.ScheduleParallel(state.Dependency);
    }
}
```

### Chain Dependencies Explicitly

When scheduling jobs manually, assign the returned handle to `state.Dependency` or complete it before accessing data on the main thread.

```csharp
JobHandle handle = new BuildSpatialHashJob
{
    Positions = positions,
    SpatialHash = spatialHash.AsParallelWriter()
}.ScheduleParallel(count, 64, state.Dependency);

state.Dependency = handle;
```

Do not read `NativeArray`, `NativeList`, component data, or buffers written by a scheduled job until the dependency is completed.

### Batch Size Defaults

| Work Type | Starting Batch Size |
|-----------|---------------------|
| Heavy per-item math | 16-32 |
| Medium transform/movement work | 32-64 |
| Lightweight arithmetic | 64-128 |
| Memory-bound copies | 128-256 |

Profile before finalizing. Too-small batches increase scheduling overhead; too-large batches reduce worker balance.

---

## Burst Standards

### Burst-Compatible Code

Burst-friendly code uses unmanaged data, `Unity.Mathematics`, and explicit data flow.

| Prefer | Avoid In Burst |
|--------|----------------|
| `float3`, `quaternion`, `math.*` | `Vector3` methods that call managed/UnityEngine APIs |
| `NativeArray<T>`, `NativeList<T>`, `NativeParallelHashMap<K,V>` | `List<T>`, `Dictionary<K,V>`, `HashSet<T>` |
| `FixedString64Bytes`, `FixedList128Bytes<T>` | `string`, string interpolation, `StringBuilder` |
| Static methods on structs | Virtual calls and interface dispatch |
| Explicit error flags | Exceptions and `try/catch` |

### Burst Compile Scope

Add `[BurstCompile]` to:

- Job structs
- `ISystem` structs
- `OnCreate`, `OnUpdate`, and `OnDestroy` methods where compatible
- Static helper methods used by Burst jobs when the helper benefits from Burst

### Float Mode And Determinism

Use `FloatMode.Fast` only when small precision differences are acceptable. Avoid fast math for deterministic lockstep, replay validation, authoritative simulation, or gameplay where rounding changes outcomes.

```csharp
[BurstCompile(FloatMode = FloatMode.Default, FloatPrecision = FloatPrecision.Standard)]
public partial struct DeterministicCombatSystem : ISystem { }
```

---

## NativeContainer Standards

### Allocator Selection

| Allocator | Lifetime | Standard |
|-----------|----------|----------|
| `Allocator.Temp` | Current frame only | No jobs; immediate use only |
| `Allocator.TempJob` | Up to 4 frames | Complete and dispose quickly |
| `Allocator.Persistent` | Manual lifetime | Dispose in `OnDestroy` or system cleanup |

Use `[ReadOnly]` for inputs, `AsParallelWriter()` for supported parallel writes, and avoid disabling safety unless there is a documented reason.

```csharp
[BurstCompile]
public struct BuildScoresJob : IJobFor
{
    [ReadOnly] public NativeArray<float> Damage;
    [ReadOnly] public NativeArray<float> Multipliers;
    public NativeArray<float> Scores;

    public void Execute(int index)
    {
        Scores[index] = Damage[index] * Multipliers[index];
    }
}
```

### Safety Attribute Rules

| Attribute | Use Only When |
|-----------|---------------|
| `[ReadOnly]` | Data is never written by the job |
| `[WriteOnly]` | Job writes but never reads previous values |
| `[NativeDisableParallelForRestriction]` | You can prove no two workers write the same index |
| `[NativeDisableContainerSafetyRestriction]` | Last resort for advanced containers; requires review |
| `[DeallocateOnJobCompletion]` | Ownership is clearly transferred to the job |

Safety-disabling attributes should trigger code review scrutiny.

---

## Authoring & Baking Standards

### Bakers Own Conversion

Keep conversion logic in Bakers. Do not create runtime entities from authoring `MonoBehaviour` code unless the feature is explicitly dynamic.

```csharp
public sealed class ProjectileAuthoring : MonoBehaviour
{
    [SerializeField] private float _speed = 20f;
    [SerializeField] private float _lifetime = 3f;

    private sealed class Baker : Baker<ProjectileAuthoring>
    {
        public override void Bake(ProjectileAuthoring authoring)
        {
            Entity entity = GetEntity(TransformUsageFlags.Dynamic);
            AddComponent(entity, new ProjectileSpeed { Value = math.max(0f, authoring._speed) });
            AddComponent(entity, new Lifetime { Remaining = math.max(0f, authoring._lifetime) });
        }
    }
}
```

Validate and clamp authoring values during baking so runtime systems can assume sane data.

### Entity Prefabs

Store entity prefab references in components produced by Bakers. Instantiate entity prefabs through ECB in systems.

---

## ECS Anti-Patterns

| Anti-Pattern | Why It Hurts | Better Approach |
|--------------|--------------|-----------------|
| Managed objects in components | Breaks Burst, chunk efficiency, serialization assumptions | Store IDs, entities, blob assets, or fixed strings |
| One giant component | Systems load unused data, poor cache behavior | Split by behavior and access pattern |
| Add/remove tags every frame | Archetype churn and sync points | Enableable components or state value |
| `EntityManager` structural changes in hot update loops | Main-thread sync and chunk moves | ECB batching |
| Completing immediately after scheduling | Removes parallelism benefit | Schedule early, complete late only when needed |
| Overusing shared components | Chunk fragmentation | Normal components or chunk-level grouping only when needed |
| Calling UnityEngine APIs in jobs | Main-thread API violation | Copy required data into NativeContainers first |
| Disabling safety attributes to silence errors | Masks real races | Fix ownership/dependencies first |

---

## Migration Strategy

1. Profile first and identify CPU-bound hot paths.
2. Extract pure data from `MonoBehaviour` fields into components or NativeContainers.
3. Create authoring + Baker for inspector-authored data.
4. Move per-frame logic into `ISystem` with `SystemAPI.Query`.
5. Add `IJobEntity` or `IJobFor` only after the system behavior is correct.
6. Add `[BurstCompile]` and remove managed APIs from the job path.
7. Batch structural changes with ECB.
8. Profile again using Timeline, System performance, and Burst Inspector.

Do not migrate entire gameplay architecture to ECS just because one subsystem is slow. Migrate bounded hot paths first.

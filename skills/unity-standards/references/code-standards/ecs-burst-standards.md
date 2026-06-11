# ECS, Jobs, And Burst Standards

Use this file for Unity Entities/DOTS, the C# Job System, Burst-compiled code, NativeContainers, Bakers, and data-oriented runtime systems.

## Decision Guide

Use ECS, Jobs, or Burst when the problem is data-parallel, CPU-bound, and measured or obviously likely to be expensive.

| Problem | Prefer | Avoid |
| --- | --- | --- |
| Thousands of similar objects updated every frame | Entities systems and jobs | Thousands of independent `MonoBehaviour.Update` calls |
| Heavy math over arrays | `IJobFor` / parallel jobs with Burst | Managed collections in hot loops |
| Frequent transform batch movement | ECS transforms or transform jobs | Per-object scene API loops |
| One-off scene behavior, UI, orchestration | MonoBehaviour | DOTS migration without a bottleneck |
| Designer-authored ECS data | Authoring MonoBehaviour + Baker | Runtime conversion hacks |
| Frequent enabled/disabled state | Enableable components or state values | Add/remove components every frame |

Do not migrate to ECS just to look modern. Use it when data layout, scheduling, and Burst materially simplify or speed the system.

## Version Awareness

Entities APIs changed substantially across versions. Before editing DOTS code:

- Check `Packages/manifest.json` for Entities, Burst, Collections, Mathematics, and Physics package versions.
- Match the project's current API style.
- Prefer Entities 1.x patterns for new code when the project is already on Entities 1.x: `ISystem`, `SystemAPI`, Bakers, `LocalTransform`, `IJobEntity`, and ECB singletons.
- Treat `IConvertGameObjectToEntity`, `Translation`, `Rotation`, and `GameObjectConversionUtility` as legacy unless the project already uses pre-1.0 Entities.
- Load official docs for version-sensitive details before changing APIs.

## ECS Shape

Separate authoring, data, and logic.

| Layer | Types | Responsibility |
| --- | --- | --- |
| Authoring | `MonoBehaviour`, Baker | Inspector input and conversion. |
| Data | `IComponentData`, `IBufferElementData`, tags | Runtime state in chunks. |
| Logic | `ISystem`, jobs | Stateless processing over queries. |

```csharp
public sealed class MoveSpeedAuthoring : MonoBehaviour
{
    [SerializeField, Min(0f)] private float _metersPerSecond = 5f;

    private sealed class Baker : Baker<MoveSpeedAuthoring>
    {
        public override void Bake(MoveSpeedAuthoring authoring)
        {
            Entity entity = GetEntity(TransformUsageFlags.Dynamic);
            AddComponent(entity, new MoveSpeed { Value = authoring._metersPerSecond });
        }
    }
}

public struct MoveSpeed : IComponentData
{
    public float Value;
}
```

Component standards:

- Keep components unmanaged and focused.
- Split fields by access pattern so systems load only what they need.
- Use tag components for coarse state filters.
- Use enableable components for frequent on/off state.
- Use dynamic buffers for variable-length per-entity data.
- Use shared components sparingly because they partition chunks.
- Avoid managed object references in components unless the project deliberately uses managed components.

## Systems

Prefer `ISystem` for high-performance runtime systems. Use `SystemBase` when managed state or managed APIs are required and the project already accepts that tradeoff.

```csharp
[BurstCompile]
[UpdateInGroup(typeof(SimulationSystemGroup))]
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

        foreach (var (health, damage) in SystemAPI.Query<RefRW<Health>, RefRO<DamageOverTime>>())
        {
            health.ValueRW.Current -= damage.ValueRO.ValuePerSecond * deltaTime;
        }
    }
}
```

System standards:

- Use `RequireForUpdate` when the system has no useful work without required data.
- Declare update groups and ordering when behavior depends on another system.
- Use `RefRO<T>` by default and `RefRW<T>` only when writing.
- Do not construct queries inside per-entity loops.
- Keep main-thread EntityManager access out of hot system updates unless there is a clear reason.

## Structural Changes

Structural changes move entities between archetypes and can force synchronization.

| Operation | Structural? | Standard |
| --- | --- | --- |
| Create/destroy entity | Yes | Batch through ECB. |
| Add/remove component | Yes | Batch or do in setup/cleanup phases. |
| Enable/disable enableable component | No archetype move | Prefer for frequent toggles. |
| Set component value | No | Safe with correct access/dependencies. |
| Append to existing dynamic buffer | Usually no archetype move | Respect ownership and dependencies. |

Use `EntityCommandBuffer` for structural changes from systems and jobs.

```csharp
EntityCommandBuffer ecb = SystemAPI
    .GetSingleton<EndSimulationEntityCommandBufferSystem.Singleton>()
    .CreateCommandBuffer(state.WorldUnmanaged);

foreach (var (health, entity) in SystemAPI.Query<RefRO<Health>>().WithEntityAccess())
{
    if (health.ValueRO.Current <= 0f)
    {
        ecb.AddComponent<DeadTag>(entity);
    }
}
```

For parallel jobs, use `EntityCommandBuffer.ParallelWriter` with the correct sort key.

## Jobs

Use jobs when work can run independently over many items and data can be copied or stored in native containers.

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
```

Dependency standards:

- Assign scheduled handles back to `state.Dependency` or combine them deliberately.
- Complete jobs only when main-thread access is required.
- Schedule early and complete late to preserve parallelism.
- Use `[ReadOnly]` for inputs and parallel writers for supported concurrent writes.
- Do not access UnityEngine scene objects from jobs. Copy needed data into native containers first.

## Burst

Burst-compatible code is unmanaged, explicit, and math-oriented.

Prefer:

- `Unity.Mathematics` types and `math.*`
- native containers
- fixed strings/lists when text-like data is required
- static helper methods without managed state
- explicit result/error flags instead of exceptions

Avoid in Burst:

- managed collections (`List<T>`, `Dictionary<TKey, TValue>`)
- `string` allocation and interpolation
- virtual/interface dispatch in hot Burst paths
- exceptions and `try/catch`
- UnityEngine object APIs

Use `FloatMode.Fast` only when precision differences are acceptable. Avoid it for deterministic combat, replay validation, lockstep simulation, and authoritative gameplay.

## NativeContainers

Pick allocators by lifetime:

| Allocator | Lifetime | Standard |
| --- | --- | --- |
| `Allocator.Temp` | Current frame | No jobs; immediate use only. |
| `Allocator.TempJob` | Short job lifetime | Complete and dispose quickly. |
| `Allocator.Persistent` | Owner lifetime | Dispose in `OnDestroy`/system cleanup. |

All NativeContainers need clear ownership and disposal. Use safety-disabling attributes only after proving ownership and dependency correctness; they should trigger careful review.

## Bakers And Entity Prefabs

Bakers own authoring conversion. Validate and clamp authoring values during baking so runtime systems can assume sane data.

```csharp
public sealed class ProjectileAuthoring : MonoBehaviour
{
    [SerializeField, Min(0f)] private float _speed = 20f;

    private sealed class Baker : Baker<ProjectileAuthoring>
    {
        public override void Bake(ProjectileAuthoring authoring)
        {
            Entity entity = GetEntity(TransformUsageFlags.Dynamic);
            AddComponent(entity, new ProjectileSpeed
            {
                Value = math.max(0f, authoring._speed)
            });
        }
    }
}
```

Store entity prefab references in components produced by Bakers. Instantiate entity prefabs through ECB in systems.

## Anti-Patterns

- Migrating a small scene behavior to ECS without a bottleneck.
- Giant components that mix movement, combat, AI, animation, and inventory.
- Add/remove tags every frame instead of using enableable components or state values.
- Completing a job immediately after scheduling it by default.
- Calling UnityEngine APIs inside jobs.
- Disabling safety attributes to silence race/dependency errors.
- Mixing old and new Entities APIs in the same feature without a migration reason.
- Creating runtime entities from authoring MonoBehaviours when baking would be stable.

## Verification

For ECS/Burst work, compile is not enough. Verify the affected path with at least one of:

- focused Edit Mode or Play Mode test
- scene smoke check with entity counts/state inspection
- Burst compilation enabled in the target environment
- profiler capture for performance-driven changes
- safety system clean run without dependency/race warnings

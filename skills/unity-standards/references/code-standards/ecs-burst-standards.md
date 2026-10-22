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

Unity 6 projects use Entities 1.x. Before editing DOTS code:

- Check `Packages/manifest.json` for Entities, Burst, Collections, Mathematics, and Physics package versions.
- Use Entities 1.x patterns: `ISystem`, `SystemAPI`, `Baker<T>`, `LocalTransform`, `IJobEntity`, and ECB singletons.
- Conversion-era APIs (`IConvertGameObjectToEntity`, `GameObjectConversionUtility`, `Translation`, `Rotation`) do not exist in 1.x; replace them instead of matching them.
- Treat `Entities.ForEach`, `Job.WithCode`, and `IAspect` as legacy; use `SystemAPI.Query` or `IJobEntity` in new code.
- Check version-sensitive details via `references/other/official-source-map.md`.

## ECS Shape

Separate authoring, data, and logic.

| Layer | Types | Responsibility |
| --- | --- | --- |
| Authoring | `MonoBehaviour`, Baker | Inspector input and conversion. |
| Data | `IComponentData`, `IBufferElementData`, tags | Runtime state in chunks. |
| Logic | `ISystem`, jobs | Stateless processing over queries. |

Authoring/Baker example: see Bakers And Entity Prefabs below.

```csharp
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

For parallel jobs, use `EntityCommandBuffer.ParallelWriter` with a deterministic sort key (in `IJobEntity`, a `[ChunkIndexInQuery] int` parameter).

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

For ECS/Burst work, compile is not enough. Run tests via `unity test` (see `references/other/unity-cli-routing.md`). Related refs: `references/debug/ecs-burst-debugging.md`, `references/review/ecs-burst-review.md`, `references/optimization/jobs-burst-migration.md`. Verify the affected path with at least one of:

- focused Edit Mode or Play Mode test
- scene smoke check with entity counts/state inspection
- Burst compilation enabled in the target environment
- profiler capture for performance-driven changes
- safety system clean run without dependency/race warnings

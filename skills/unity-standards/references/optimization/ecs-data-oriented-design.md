# ECS Data-Oriented Design

Use this when a Unity feature may benefit from Entities/ECS because it processes
large volumes of similar data. Prefer ordinary C# and MonoBehaviours until the
project, profiling evidence, and data shape justify ECS complexity. Examples
target Entities 1.x (the line supported on Unity 6). Jobs/Burst rules live in
`jobs-burst-migration.md`; code and review rules in
`references/code-standards/ecs-burst-standards.md` and
`references/review/ecs-burst-review.md`; debugging in
`references/debug/ecs-burst-debugging.md`.

## When ECS Fits

| Signal | ECS Fit |
| --- | --- |
| Thousands of similar objects updated every frame | Strong |
| Data is small, blittable, and processed in batches | Strong |
| Logic is stateless or state lives cleanly in components | Strong |
| Authoring can be baked from prefabs/subscenes | Medium to strong |
| UI, one-off scene behavior, bespoke object graphs | Weak |
| Heavy GameObject/Transform/Component API usage | Weak |

Do not split truth between GameObjects and ECS without an explicit authority.
Hybrid bridges should translate at boundaries, not duplicate gameplay state.

## Core Shape

| ECS Concept | Standard |
| --- | --- |
| Entity | Identity only. No behavior and no hidden data. |
| `IComponentData` | Small unmanaged runtime state. Prefer focused components. |
| `IBufferElementData` | Variable-length per-entity data when needed. |
| Tag component | Zero-size marker for query shape or state. |
| System | Logic over queries. Keep update requirements explicit. |
| Baker | Converts authoring data into runtime components. Validate here. |
| EntityCommandBuffer | Deferred structural changes from jobs or systems. |

Minimal component/system shape:

```csharp
public struct MoveSpeed : IComponentData
{
    public float Value;
}

[BurstCompile]
public partial struct MoveSystem : ISystem
{
    [BurstCompile]
    public void OnUpdate(ref SystemState state)
    {
        float deltaTime = SystemAPI.Time.DeltaTime;

        foreach (var (transform, speed) in
            SystemAPI.Query<RefRW<LocalTransform>, RefRO<MoveSpeed>>())
        {
            transform.ValueRW.Position.z += speed.ValueRO.Value * deltaTime;
        }
    }
}
```

## Data Standards

- Keep components focused and small. Split unrelated concerns.
- Use `RefRO<T>` for read-only and `RefRW<T>` for writes.
- Avoid managed components unless the project already accepts the tradeoff.
- Use enableable/tag components for state filtering instead of branch-heavy
  systems when it improves query clarity.
- Store prefab/entity references as `Entity`, not GameObject references.
- Use dynamic buffers for per-entity lists; avoid global mutable collections
  unless ownership is explicit.

## System Standards

- Declare `RequireForUpdate` gates for singleton config or mandatory data.
- Put systems in the correct update group and document unusual ordering.
- Cache or build queries intentionally; do not construct expensive queries inside
  inner loops.
- Schedule parallel jobs when the data set is large enough to beat scheduling
  overhead.
- Complete dependencies only when the main thread needs results.
- Use `EntityCommandBuffer` for create/destroy/add/remove component operations
  that happen during iteration or jobs.

## Baking Standards

- Validate authoring fields during baking; runtime systems should not carry
  avoidable defensive branches for broken authoring data.
- Choose `TransformUsageFlags` based on actual runtime use.
- Keep Baker output deterministic and small.
- Treat subscene and prefab baking as part of the verification surface.

## Migration Checklist

1. Profile the MonoBehaviour path and name the bottleneck.
2. Identify the authoritative runtime state.
3. Convert only the hot data to components.
4. Write the smallest system that preserves behavior.
5. Add tests for pure data transforms where possible.
6. Verify entity counts, query matches, system ordering, and ECB playback.
7. Profile again with representative data and target platform when practical.

## Common Risks

| Risk | Symptom | Mitigation |
| --- | --- | --- |
| Query mismatch | Entities exist but system processes none | inspect components, tags, enableable state |
| Wrong world | Test/debug query sees different entities | identify world in reports |
| ECB timing | New/destroyed entity appears one frame later | choose begin/end ECB system deliberately |
| Over-migration | More code, no frame improvement | compare profiler before/after |
| Hybrid duplication | GameObject and ECS state disagree | define one authority and sync direction |
| Package drift | API names differ by Entities version | verify against local package docs |

## Verification

- Console has no Entities/Burst/Collections safety errors (live Editor console
  or `Editor.log`; see `references/other/unity-cli-routing.md`).
- Entity count and query count match expected scene/test data.
- Systems run in the intended group/order.
- Structural changes appear at the intended frame.
- Profiling proves the migration helped or documents why it is still justified.

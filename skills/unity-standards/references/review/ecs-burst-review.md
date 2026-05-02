# ECS, Jobs & Burst Review Checklist

Use this reference when reviewing changes that touch Unity Entities, DOTS, Job System, Burst, NativeContainers, Bakers, or data-oriented gameplay systems.

## Severity Guidance

| Finding | Minimum Severity |
|---------|------------------|
| Data race, unsafe NativeContainer access, missing dependency before read/dispose | CRITICAL |
| UnityEngine API called from job/Burst path | HIGH |
| Structural changes in hot loops without ECB | HIGH |
| Missing NativeContainer disposal | HIGH |
| Managed type inside Burst-critical component/job | HIGH |
| Query silently processing wrong entity set | HIGH |
| Missing Baker validation for required prefab/data | MEDIUM |
| Immediate `Complete()` removing parallelism benefit | MEDIUM |
| Over-broad component or query design | MEDIUM |
| Missing profiling evidence for ECS migration | MEDIUM |

---

## 1. ECS Architecture Review

### Authoring / Baking

- [ ] Authoring `MonoBehaviour` contains inspector data only, not runtime ECS logic.
- [ ] Baker validates required references and clamps invalid numeric data.
- [ ] Baker uses correct `TransformUsageFlags` for static, dynamic, renderable, or none.
- [ ] Prefab references are converted with `GetEntity(prefab, flags)`.
- [ ] Runtime systems can assume baked data is valid or explicitly handle invalid data.
- [ ] No legacy conversion API introduced into an Entities 1.x project.

### Components

- [ ] `IComponentData` is unmanaged and focused on one concern.
- [ ] Large catch-all components are split by access pattern.
- [ ] Tag components represent query state cleanly.
- [ ] Frequently toggled state uses `IEnableableComponent` instead of add/remove churn.
- [ ] Dynamic buffers are used for per-entity variable lists instead of managed collections.
- [ ] Shared components are justified and not used for high-cardinality values.

### Systems

- [ ] `ISystem` is preferred for Burst-compatible runtime logic.
- [ ] `SystemBase` is used only when managed state/API access is required.
- [ ] `RequireForUpdate` prevents systems from running before required singleton/query data exists.
- [ ] Update group/order attributes document dependencies between systems.
- [ ] System logic is stateless or stores state in components/singletons, not hidden managed fields.

---

## 2. Query & Data Access Review

- [ ] Queries require the minimum needed components.
- [ ] `RefRO<T>` is used for read-only component access.
- [ ] `RefRW<T>` is used only for components actually modified.
- [ ] `WithNone<T>` filters exclude dead/disabled/cleanup states intentionally.
- [ ] `WithAny<T>` does not obscure behavior or mix unrelated entity shapes.
- [ ] Enableable component state is considered in query behavior.
- [ ] Change filters are not used where skipped updates would break correctness.
- [ ] Query construction is not repeated inside entity loops.
- [ ] Entity access through `.WithEntityAccess()` is present only when entity IDs are needed.

---

## 3. Structural Changes & ECB Review

- [ ] Create/destroy/add/remove component operations use `EntityCommandBuffer` from systems/jobs.
- [ ] ECB playback system matches desired visibility timing.
- [ ] Parallel ECB uses `ParallelWriter` and stable sort keys such as `ChunkIndexInQuery`.
- [ ] Entity destruction does not assume the entity is gone before ECB playback.
- [ ] Structural changes are batched and not performed repeatedly in tight loops when a state component would suffice.
- [ ] Frequent enable/disable behavior uses enableable components where appropriate.
- [ ] Entity references used in ECB are from the same world and still valid at playback.

---

## 4. Jobs Review

- [ ] Job handles are chained correctly through schedule calls.
- [ ] ECS systems assign returned handles to `state.Dependency` when jobs continue asynchronously.
- [ ] Main-thread reads call `Complete()` before accessing job-written data.
- [ ] NativeContainer disposal waits for all dependent jobs.
- [ ] Parallel jobs write unique indices or use supported parallel writers.
- [ ] `[ReadOnly]` is applied to all input containers.
- [ ] `[WriteOnly]` is applied when previous values are not read.
- [ ] Safety-disabling attributes are rare, justified, and backed by non-overlap reasoning.
- [ ] Batch sizes are reasonable and profile-driven for the work type.
- [ ] Jobs are not scheduled for tiny one-off work where scheduling overhead dominates.

---

## 5. Burst Review

- [ ] `[BurstCompile]` is applied to Burst-compatible systems/jobs.
- [ ] Burst path does not reference `string`, managed collections, classes, `GameObject`, `Transform`, or other `UnityEngine.Object` instances.
- [ ] Burst path uses `Unity.Mathematics` types and `math.*` functions for hot math.
- [ ] No exceptions, `try/catch`, reflection, or virtual dispatch in Burst-critical code.
- [ ] Debug logging is outside Burst jobs or uses sampled diagnostic data written to containers.
- [ ] `FloatMode.Fast` is not used for deterministic or authoritative gameplay without explicit acceptance.
- [ ] Unsafe pointer/intrinsics code has a clear performance reason and bounds/aliasing proof.

---

## 6. NativeContainer Review

- [ ] Allocator choice matches lifetime: `Temp`, `TempJob`, or `Persistent`.
- [ ] `Allocator.TempJob` allocations are completed and disposed within four frames.
- [ ] Persistent containers are disposed on cleanup paths.
- [ ] Containers are initialized with `ClearMemory` when default values matter.
- [ ] `NativeList` capacity is pre-sized for `AddNoResize` or overflow is handled safely.
- [ ] `NativeParallelHashMap` / `NativeParallelMultiHashMap` capacity is chosen to avoid reallocation in jobs.
- [ ] No managed collection mirrors become stale relative to NativeContainer data.

---

## 7. Performance Review

- [ ] The change includes profiling evidence or a clear performance hypothesis.
- [ ] ECS migration targets a real hot path, not incidental architecture churn.
- [ ] Jobs are scheduled early and completed late to allow worker overlap.
- [ ] Immediate `Complete()` is justified by correctness or replaced with dependency flow.
- [ ] Component layout avoids loading unused data in hot systems.
- [ ] Structural-change frequency is measured or bounded.
- [ ] Queries match expected entity counts under representative scenes.
- [ ] Burst Inspector / Profiler is used for critical kernels when performance is the motivation.

---

## 8. Testing & Verification Review

- [ ] Edit Mode tests cover pure math/helpers outside ECS where possible.
- [ ] Systems are tested in a controlled world when behavior is complex.
- [ ] Baker behavior is tested or validated for required authoring data.
- [ ] Race-prone code is tested with Burst and Jobs enabled.
- [ ] Development Build behavior is checked for Burst/IL2CPP-sensitive changes.
- [ ] Performance tests compare before/after entity counts and frame timings.

---

## Review Comment Templates

```text
[HIGH] Missing job dependency before reading NativeArray
The job scheduled here writes `positions`, but the main thread reads it before completing or chaining the handle. This can produce safety exceptions or race-like behavior. Assign the returned handle to `state.Dependency` or call `Complete()` before the read.
```

```text
[HIGH] Structural changes should be batched through ECB
This system adds/removes components during the hot update path. In ECS this moves entities between archetypes and can force sync points. Use an `EntityCommandBuffer` and consider an enableable component if this state toggles frequently.
```

```text
[MEDIUM] Component combines unrelated access patterns
`CharacterRuntimeState` mixes movement, combat, and UI-facing fields. The movement system will load data it does not use for every entity. Split the component by system access pattern to improve chunk/cache efficiency.
```

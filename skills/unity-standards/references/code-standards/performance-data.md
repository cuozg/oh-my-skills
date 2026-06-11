# Performance, Data, Pooling, And Serialization

Use this file for runtime allocations, collections, LINQ, object pooling, serialization, ScriptableObject data, save data, and data-loading decisions.

## Performance Priorities

1. Preserve correct behavior first.
2. Avoid obvious hot-path allocations and Unity API misuse.
3. Profile before complex optimizations.
4. Optimize the path that actually runs often on target hardware.
5. Keep optimized code readable enough that future changes do not reintroduce cost.

Hot paths include `Update`, `FixedUpdate`, `LateUpdate`, physics callbacks, input callbacks, animation callbacks, UI rebuild loops, and code called for many entities/items per frame.

## Allocation Rules

- Do not allocate per frame without evidence it is harmless.
- Reuse buffers and result lists owned by the component/system.
- Prefer `NonAlloc` physics APIs when query frequency is high.
- Avoid string formatting/interpolation in hot logs or labels; update UI text only when values change.
- Avoid closures and LINQ in hot paths unless profiling shows no practical cost.
- Do not call scene-wide find APIs from hot paths.

```csharp
private readonly Collider[] _hits = new Collider[32];

private int FindTargets(Vector3 position, float radius)
{
    return Physics.OverlapSphereNonAlloc(position, radius, _hits, _targetMask);
}
```

## Collections

| Need | Preferred Type |
| --- | --- |
| Fixed serialized list | Array or `List<T>` |
| Dynamic ordered list | `List<T>` |
| Lookup by key | `Dictionary<TKey, TValue>` |
| Unique membership / fast contains | `HashSet<T>` |
| FIFO work queue | `Queue<T>` |
| Undo / LIFO | `Stack<T>` |
| Public read-only exposure | `IReadOnlyList<T>` or copied result |
| Jobs/Burst data | `NativeArray<T>`, `NativeList<T>`, native hash maps |

Pre-size when count is predictable:

```csharp
private readonly List<Enemy> _visibleEnemies = new(64);
private readonly Dictionary<string, AbilityData> _abilitiesById = new(128);
```

Do not expose mutable collections directly:

```csharp
public IReadOnlyList<Enemy> VisibleEnemies => _visibleEnemies;
```

## LINQ

LINQ is fine for editor tools, tests, one-time setup, and cold paths. Avoid it in hot runtime paths.

```csharp
// Setup path: acceptable.
_abilitiesById = _abilities.ToDictionary(ability => ability.Id);

// Hot path: prefer a loop.
Enemy closest = null;
float closestDistanceSq = float.MaxValue;

for (int i = 0; i < _visibleEnemies.Count; i++)
{
    Enemy enemy = _visibleEnemies[i];
    float distanceSq = (enemy.Position - origin).sqrMagnitude;

    if (distanceSq < closestDistanceSq)
    {
        closest = enemy;
        closestDistanceSq = distanceSq;
    }
}
```

Avoid `Where(...).First(...)`; use `First(...)` or a loop. Avoid properties that recompute LINQ queries every access.

## Unity Hot-Path Patterns

- Cache `Camera.main` if used repeatedly.
- Cache component references used repeatedly.
- Use `CompareTag` instead of `gameObject.tag ==`.
- Use `sqrMagnitude` for distance comparisons.
- Use `SetPositionAndRotation` when setting both position and rotation.
- Move physics through `Rigidbody` APIs in `FixedUpdate`.
- Do not use `SendMessage` or `BroadcastMessage`; use direct references, interfaces, or events.
- Avoid enabling/disabling large hierarchies repeatedly in one frame unless measured acceptable.

## Object Pooling

Pool objects that are expensive or frequent to create/destroy: projectiles, floating text, VFX bursts, audio emitters, temporary UI rows, and repeated gameplay markers.

Do not pool long-lived objects, rare objects, or objects whose reset logic is more error-prone than instantiation.

Pool contract:

- `Get` fully initializes visible state.
- `Release` stops timers, particles, audio, tweens, coroutines, and event subscriptions owned by the pooled object.
- Releasing twice is a bug; use collection checks in development where supported.
- Pooled objects must not keep stale references to old owners or targets.

```csharp
private ObjectPool<Projectile> _pool;

private void Awake()
{
    _pool = new ObjectPool<Projectile>(
        CreateProjectile,
        projectile => projectile.gameObject.SetActive(true),
        projectile => projectile.gameObject.SetActive(false),
        projectile => Destroy(projectile.gameObject),
        collectionCheck: true,
        defaultCapacity: 32,
        maxSize: 256);
}
```

Use the repository's existing pool abstraction if one exists. Do not introduce a second pool framework for one feature.

## Serialization

Unity serializes fields, not ordinary C# properties. Prefer explicit backing fields for Inspector data.

```csharp
[Serializable]
public struct SpawnWave
{
    [SerializeField] private EnemyDefinition _enemy;
    [SerializeField, Min(0)] private int _count;

    public EnemyDefinition Enemy => _enemy;
    public int Count => _count;
}
```

Rules:

- Use `[Serializable]` for nested serializable data types.
- Use `ScriptableObject` assets for reusable designer-authored data.
- Use `[FormerlySerializedAs]` for existing serialized field renames.
- Avoid serializing dictionaries directly unless the project has a proven drawer/serializer.
- Avoid serializing scene object references into assets unless the asset is scene-specific by design.
- Use `[SerializeReference]` for polymorphic data only when editor tooling and migration risk are acceptable.

## ScriptableObject Data

Use ScriptableObjects for stable authored data and configuration. Keep runtime mutable state out unless the asset is explicitly a runtime state holder.

Good uses:

- item definitions
- ability definitions
- economy tables
- tuning curves
- event channels when the architecture already uses them

Risky uses:

- global mutable game state
- per-save player progress
- hidden service locator references
- data that must differ per scene instance without clear ownership

## Save And External Data

Treat save files, remote config, and server payloads as untrusted input.

- Parse into DTOs, validate, then apply to runtime state.
- Keep previous valid state until replacement data passes validation.
- Version save data and write migrations intentionally.
- Do not use `PlayerPrefs` for sensitive data or large structured saves.
- Do not log tokens, raw auth payloads, or personally identifying data.
- For WebGL, remember persistence and file APIs differ from desktop; isolate storage behind an interface.

## Native And Rented Buffers

Use `NativeArray`, `NativeList`, and related containers for Jobs/Burst. Dispose them at the owner lifetime.

Use `ArrayPool<T>` only when the code has clear ownership and always returns buffers in `finally`.

```csharp
RaycastHit[] buffer = ArrayPool<RaycastHit>.Shared.Rent(64);
try
{
    int count = Physics.RaycastNonAlloc(ray, buffer, maxDistance, layerMask);
    ProcessHits(buffer, count);
}
finally
{
    ArrayPool<RaycastHit>.Shared.Return(buffer);
}
```

Do not retain rented arrays beyond the operation unless ownership is documented and return is guaranteed.

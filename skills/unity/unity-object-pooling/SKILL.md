---
name: unity-object-pooling
description: "(opencode-project - Skill) Object pooling patterns for Unity. Covers generic ObjectPool, Unity's built-in ObjectPool API, particle system pooling, UI element pooling, projectile pools, and pool warming strategies. Use when: (1) Reducing GC allocations from frequent Instantiate/Destroy, (2) Building bullet/projectile systems, (3) Pooling UI elements for lists, (4) Managing particle system lifecycles, (5) Optimizing spawn-heavy gameplay. Triggers: 'object pool', 'pooling', 'reduce GC', 'spawn optimization', 'bullet pool', 'projectile pool', 'pool manager'."
---

# unity-object-pooling — Object Pooling Patterns

Eliminate garbage collection spikes from frequent object creation and destruction by implementing efficient pooling systems — from simple generic pools to complex multi-type pool managers.

## Purpose

Design and implement object pooling architectures that recycle GameObjects and plain C# objects instead of allocating and destroying them repeatedly. Reduce GC pressure, eliminate frame hitches from Instantiate/Destroy, and provide predictable memory usage in spawn-heavy gameplay.

## Input

- **Required**: Description of objects to pool (prefab type, spawn frequency, lifetime pattern)
- **Optional**: Pool size constraints, warming requirements, multi-type pooling needs, performance budget

## Output

Production-ready pooling code: pool manager, IPoolable interface implementation, warming logic, and integration with existing spawn systems. All code compiles and follows `unity-code` quality standards.

## Examples

| User Request | Skill Action |
|:---|:---|
| "Pool projectiles for a bullet-hell game" | Implement typed pool with pre-warming, auto-expand, and OnSpawn/OnDespawn lifecycle |
| "Reduce GC from enemy spawning" | Replace Instantiate/Destroy with ObjectPool<T>, add pool warming during loading |
| "Pool UI elements in a scrolling list" | Implement component pool for UI items with data binding on checkout/return |
| "Create a generic pool manager for multiple prefabs" | Build dictionary-based multi-pool manager with per-type configuration |

## Workflow

1. **Identify pool candidates** — Find objects with frequent Instantiate/Destroy cycles (Profiler GC.Alloc markers)
2. **Choose pool implementation** — Unity built-in `ObjectPool<T>` for simple cases, custom pool for complex lifecycle needs
3. **Implement IPoolable interface** — Define OnSpawn/OnDespawn contracts for clean object reset
4. **Build pool manager** — Centralized pool registry with configurable initial size, max capacity, and auto-expand policy
5. **Add pool warming** — Pre-instantiate objects during loading screens or scene init to avoid runtime hitches
6. **Profile to verify** — Compare GC allocations before and after pooling via Unity Profiler

---

## Pool Implementation Selection

| Approach | Best For | Complexity |
|:---------|:---------|:-----------|
| `UnityEngine.Pool.ObjectPool<T>` | Single-type pooling, quick setup | Low |
| `UnityEngine.Pool.CollectionPool<T,V>` | Pooling Lists, HashSets, Dictionaries | Low |
| Custom `MonoBehaviourPool<T>` | GameObject pooling with lifecycle hooks | Medium |
| Multi-type `PoolManager` | Many prefab types, centralized management | High |

---

## Key Patterns

### Unity Built-in ObjectPool (Simplest)

```csharp
using UnityEngine.Pool;

/// <summary>
/// Projectile spawner using Unity's built-in ObjectPool.
/// Eliminates GC from repeated Instantiate/Destroy calls.
/// </summary>
public class ProjectileSpawner : MonoBehaviour
{
    [SerializeField] private Projectile _prefab;
    [SerializeField] private int _defaultCapacity = 20;
    [SerializeField] private int _maxSize = 100;

    private ObjectPool<Projectile> _pool;

    private void Awake()
    {
        _pool = new ObjectPool<Projectile>(
            createFunc: () => Instantiate(_prefab),
            actionOnGet: p => p.gameObject.SetActive(true),
            actionOnRelease: p => p.gameObject.SetActive(false),
            actionOnDestroy: p => Destroy(p.gameObject),
            collectionCheck: false,
            defaultCapacity: _defaultCapacity,
            maxSize: _maxSize
        );
    }

    /// <summary>
    /// Get a projectile from the pool, positioned and aimed.
    /// </summary>
    public Projectile Spawn(Vector3 position, Quaternion rotation)
    {
        Projectile p = _pool.Get();
        p.transform.SetPositionAndRotation(position, rotation);
        p.Initialize(_pool);
        return p;
    }
}
```

### IPoolable Interface Pattern

```csharp
/// <summary>
/// Contract for objects managed by a pool.
/// Guarantees clean state transitions on checkout and return.
/// </summary>
public interface IPoolable
{
    /// <summary>Called when retrieved from pool. Initialize state here.</summary>
    void OnSpawn();

    /// <summary>Called when returned to pool. Reset all state here.</summary>
    void OnDespawn();
}

/// <summary>
/// Projectile with pool lifecycle — resets all state on return.
/// </summary>
public class Projectile : MonoBehaviour, IPoolable
{
    [SerializeField] private float _speed = 20f;
    [SerializeField] private float _lifetime = 3f;

    private IObjectPool<Projectile> _pool;
    private float _timer;

    public void Initialize(IObjectPool<Projectile> pool)
    {
        _pool = pool;
        OnSpawn();
    }

    public void OnSpawn()
    {
        _timer = _lifetime;
        // Reset any runtime state (trails, damage counters, etc.)
    }

    public void OnDespawn()
    {
        _timer = 0f;
        // Clear references, stop particles, reset trails
    }

    private void Update()
    {
        transform.Translate(Vector3.forward * (_speed * Time.deltaTime));
        _timer -= Time.deltaTime;

        if (_timer <= 0f)
        {
            ReturnToPool();
        }
    }

    /// <summary>
    /// Return this projectile to the pool instead of destroying it.
    /// </summary>
    public void ReturnToPool()
    {
        OnDespawn();
        _pool?.Release(this);
    }
}
```

### Multi-Type Pool Manager

```csharp
/// <summary>
/// Centralized pool manager that handles multiple prefab types.
/// Register prefabs at initialization, then spawn/despawn by type.
/// </summary>
public class PoolManager : MonoBehaviour
{
    public static PoolManager Instance { get; private set; }

    [Serializable]
    public class PoolConfig
    {
        public GameObject prefab;
        public int initialSize = 10;
        public int maxSize = 50;
    }

    [SerializeField] private List<PoolConfig> _poolConfigs = new();

    // Keyed by prefab instance ID for O(1) lookup
    private readonly Dictionary<int, ObjectPool<GameObject>> _pools = new();
    private readonly Dictionary<int, int> _instanceToPrefabId = new();

    private void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }
        Instance = this;

        // Create pools for all configured prefabs
        foreach (PoolConfig config in _poolConfigs)
        {
            RegisterPool(config);
        }
    }

    private void RegisterPool(PoolConfig config)
    {
        int prefabId = config.prefab.GetInstanceID();
        GameObject prefab = config.prefab;

        var pool = new ObjectPool<GameObject>(
            createFunc: () =>
            {
                GameObject obj = Instantiate(prefab, transform);
                // Track which pool this instance belongs to
                _instanceToPrefabId[obj.GetInstanceID()] = prefabId;
                return obj;
            },
            actionOnGet: obj => obj.SetActive(true),
            actionOnRelease: obj => obj.SetActive(false),
            actionOnDestroy: obj =>
            {
                _instanceToPrefabId.Remove(obj.GetInstanceID());
                Destroy(obj);
            },
            collectionCheck: false,
            defaultCapacity: config.initialSize,
            maxSize: config.maxSize
        );

        _pools[prefabId] = pool;
    }

    /// <summary>
    /// Spawn an object from the pool matching the given prefab.
    /// </summary>
    public GameObject Spawn(GameObject prefab, Vector3 position, Quaternion rotation)
    {
        int prefabId = prefab.GetInstanceID();
        if (!_pools.TryGetValue(prefabId, out ObjectPool<GameObject> pool))
        {
            Debug.LogError($"[PoolManager] No pool registered for prefab: {prefab.name}");
            return Instantiate(prefab, position, rotation);
        }

        GameObject obj = pool.Get();
        obj.transform.SetPositionAndRotation(position, rotation);
        return obj;
    }

    /// <summary>
    /// Return an object to its originating pool.
    /// </summary>
    public void Despawn(GameObject obj)
    {
        int instanceId = obj.GetInstanceID();
        if (!_instanceToPrefabId.TryGetValue(instanceId, out int prefabId) ||
            !_pools.TryGetValue(prefabId, out ObjectPool<GameObject> pool))
        {
            Debug.LogWarning($"[PoolManager] Object not tracked, destroying: {obj.name}");
            Destroy(obj);
            return;
        }

        pool.Release(obj);
    }
}
```

### Pool Warming

```csharp
/// <summary>
/// Pre-instantiate pooled objects during loading to avoid runtime frame spikes.
/// Call from loading screen or scene initialization.
/// </summary>
public async Awaitable WarmPoolsAsync(int objectsPerFrame = 5)
{
    foreach (PoolConfig config in _poolConfigs)
    {
        int prefabId = config.prefab.GetInstanceID();
        ObjectPool<GameObject> pool = _pools[prefabId];

        // Pre-allocate in batches to spread across frames
        var temp = new List<GameObject>();
        for (int i = 0; i < config.initialSize; i++)
        {
            temp.Add(pool.Get());

            // Yield every N objects to avoid frame spikes
            if (i % objectsPerFrame == 0)
            {
                await Awaitable.NextFrameAsync();
            }
        }

        // Return all to pool — they are now pre-instantiated and ready
        foreach (GameObject obj in temp)
        {
            pool.Release(obj);
        }
    }
}
```

### Collection Pooling (Lists, HashSets)

```csharp
using UnityEngine.Pool;

/// <summary>
/// Pool temporary collections to avoid GC from new List/HashSet allocations.
/// </summary>
public void ProcessNearbyEnemies(Vector3 center, float radius)
{
    // Get a pooled list instead of new List<Collider>()
    var results = ListPool<Collider>.Get();
    try
    {
        int count = Physics.OverlapSphereNonAlloc(center, radius, _hitBuffer);
        for (int i = 0; i < count; i++)
        {
            results.Add(_hitBuffer[i]);
        }

        // Process results...
    }
    finally
    {
        // Return list to pool — clears and recycles the allocation
        ListPool<Collider>.Release(results);
    }
}
```

---

## Best Practices

### Do

- **Use Unity's built-in ObjectPool<T>** — Covers most cases without custom code; available in `UnityEngine.Pool`
- **Reset all state in OnDespawn** — Trails, particle effects, timers, counters, event subscriptions must all be cleared
- **Warm pools during loading** — Pre-instantiate to `initialSize` during load screens, not during gameplay
- **Set reasonable max sizes** — Prevent unbounded pool growth; excess objects should be destroyed
- **Parent pooled objects** — Use a dedicated transform parent to keep hierarchy organized
- **Use `collectionCheck: false` in production** — The duplicate-return check has overhead; enable only for debugging
- **Profile before and after** — Verify GC reduction with Unity Profiler's GC.Alloc timeline

### Do Not

- **Never pool objects that are rarely instantiated** — Pooling adds complexity; only pool high-frequency objects
- **Never forget to return objects to the pool** — Leaked objects defeat the purpose; use auto-return timers as safety nets
- **Never access pooled objects after return** — Treat `Release()` as equivalent to `Destroy()`; null out references
- **Never pool objects with unique persistent state** — Objects that accumulate state across lifetimes are poor pool candidates
- **Never use large initial pool sizes blindly** — Profile actual usage to right-size pools; over-allocation wastes memory

---

## When to Pool vs When Not To

| Scenario | Pool? | Reason |
|:---------|:------|:-------|
| Bullets fired 60 per second | Yes | High frequency Instantiate/Destroy causes GC spikes |
| Enemies spawning every 5 seconds | Maybe | Only if GC from Instantiate is measurable in Profiler |
| Player character (1 instance) | No | Single instance, never recycled |
| UI popup shown once per session | No | Instantiate once, Destroy on close is fine |
| Particle effects on hit | Yes | Frequent spawn/despawn, recyclable state |
| Audio sources for SFX | Yes | Many short-lived sources benefit from pooling |

---

## Handoff & Boundaries

### Delegates To

| Skill | When |
|:------|:-----|
| `unity-optimize-performance` | Profiling GC allocations, memory analysis, and verifying pool effectiveness |
| `unity-code` | General C# implementation beyond pooling-specific patterns |

### Does Not Handle

- **Memory layout optimization** — Cache-line optimization, struct-of-arrays patterns are `unity-optimize-performance` territory
- **ECS/DOTS entity pooling** — Entity management in DOTS uses different paradigms (archetypes, structural changes)
- **Asset Bundle memory management** — Loading/unloading asset bundles is `unity-build-pipeline` territory

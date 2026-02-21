---
name: unity-object-pooling
description: "(opencode-project - Skill) Object pooling patterns for Unity. Covers generic ObjectPool, Unity's built-in ObjectPool API, particle system pooling, UI element pooling, projectile pools, and pool warming strategies. Use when: (1) Reducing GC allocations from frequent Instantiate/Destroy, (2) Building bullet/projectile systems, (3) Pooling UI elements for lists, (4) Managing particle system lifecycles, (5) Optimizing spawn-heavy gameplay. Triggers: 'object pool', 'pooling', 'reduce GC', 'spawn optimization', 'bullet pool', 'projectile pool', 'pool manager'."
---

# unity-object-pooling — Object Pooling Patterns

**Input**: Objects to pool (prefab type, spawn frequency, lifetime pattern), pool size constraints, warming needs

## Output

Production-ready C# object pooling code following the patterns above.

## Workflow

1. **Identify pool candidates** — Find objects with frequent Instantiate/Destroy (Profiler GC.Alloc markers)
2. **Choose implementation** — Unity `ObjectPool<T>` for simple cases, custom pool for complex lifecycle
3. **Implement IPoolable** — Define OnSpawn/OnDespawn contracts for clean reset
4. **Build pool manager** — Centralized registry with configurable initial size, max capacity, auto-expand
5. **Add warming** — Pre-instantiate during loading screens to avoid runtime hitches
6. **Profile to verify** — Compare GC allocations before/after via Unity Profiler

## Pool Implementation Selection

| Approach | Best For | Complexity |
|:---------|:---------|:-----------|
| `UnityEngine.Pool.ObjectPool<T>` | Single-type pooling, quick setup | Low |
| `UnityEngine.Pool.CollectionPool<T,V>` | Pooling Lists, HashSets, Dictionaries | Low |
| Custom `MonoBehaviourPool<T>` | GameObject pooling with lifecycle hooks | Medium |
| Multi-type `PoolManager` | Many prefab types, centralized management | High |

## Key Patterns

### Unity Built-in ObjectPool (Simplest)

```csharp
using UnityEngine.Pool;

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

    public Projectile Spawn(Vector3 position, Quaternion rotation)
    {
        Projectile p = _pool.Get();
        p.transform.SetPositionAndRotation(position, rotation);
        p.Initialize(_pool);
        return p;
    }
}
```

### IPoolable Interface + Projectile

```csharp
public interface IPoolable
{
    void OnSpawn();
    void OnDespawn();
}

public class Projectile : MonoBehaviour, IPoolable
{
    [SerializeField] private float _speed = 20f;
    [SerializeField] private float _lifetime = 3f;
    private IObjectPool<Projectile> _pool;
    private float _timer;

    public void Initialize(IObjectPool<Projectile> pool) { _pool = pool; OnSpawn(); }
    public void OnSpawn() { _timer = _lifetime; }
    public void OnDespawn() { _timer = 0f; }

    private void Update()
    {
        transform.Translate(Vector3.forward * (_speed * Time.deltaTime));
        _timer -= Time.deltaTime;
        if (_timer <= 0f) { OnDespawn(); _pool?.Release(this); }
    }
}
```

### Pool Warming (Async)

```csharp
public async Awaitable WarmPoolsAsync(int objectsPerFrame = 5)
{
    foreach (PoolConfig config in _poolConfigs)
    {
        int prefabId = config.prefab.GetInstanceID();
        ObjectPool<GameObject> pool = _pools[prefabId];
        var temp = new List<GameObject>();
        for (int i = 0; i < config.initialSize; i++)
        {
            temp.Add(pool.Get());
            if (i % objectsPerFrame == 0) await Awaitable.NextFrameAsync();
        }
        foreach (GameObject obj in temp) pool.Release(obj);
    }
}
```

### Collection Pooling

```csharp
using UnityEngine.Pool;

var results = ListPool<Collider>.Get();
try { /* process results */ }
finally { ListPool<Collider>.Release(results); }
```

## Best Practices

### Do
- Use Unity's built-in `ObjectPool<T>` — covers most cases
- Reset ALL state in OnDespawn (trails, particles, timers, subscriptions)
- Warm pools during loading, not gameplay
- Set reasonable max sizes to prevent unbounded growth
- Use `collectionCheck: false` in production (overhead)
- Profile before and after with Unity Profiler GC.Alloc

### Do Not
- Pool rarely-instantiated objects — complexity not worth it
- Forget to return objects (use auto-return timers as safety nets)
- Access pooled objects after Release() — treat as Destroy()
- Pool objects with unique persistent state across lifetimes
- Over-allocate initial sizes — profile actual usage first

## When to Pool

| Scenario | Pool? | Reason |
|:---------|:------|:-------|
| Bullets fired 60/sec | Yes | High-freq Instantiate/Destroy = GC spikes |
| Enemies every 5 sec | Maybe | Only if GC measurable in Profiler |
| Player character (1) | No | Single instance, never recycled |
| Particle effects on hit | Yes | Frequent spawn/despawn, recyclable |
| Audio sources for SFX | Yes | Many short-lived sources |

## Handoff & Boundaries

- **Delegates to**: `unity-optimize-performance` (profiling, memory analysis), `unity-code-deep` (general C# beyond pooling)
- **Does NOT handle**: Memory layout/cache-line optimization, ECS/DOTS pooling, Asset Bundle memory management

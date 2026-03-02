# Object Pooling

## Unity 2021+ Built-In ObjectPool

```csharp
using UnityEngine;
using UnityEngine.Pool;

public sealed class ProjectileSpawner : MonoBehaviour
{
    [SerializeField] private GameObject _projectilePrefab;
    [SerializeField] private int _defaultCapacity = 20;
    [SerializeField] private int _maxSize = 100;

    private ObjectPool<GameObject> _pool;

    void Awake()
    {
        _pool = new ObjectPool<GameObject>(
            createFunc: () => Instantiate(_projectilePrefab),
            actionOnGet: obj => { obj.SetActive(true); },
            actionOnRelease: obj => { obj.SetActive(false); },
            actionOnDestroy: Destroy,
            collectionCheck: true, // debug: warns on double-release
            defaultCapacity: _defaultCapacity,
            maxSize: _maxSize
        );
    }

    public GameObject Spawn(Vector3 position, Quaternion rotation)
    {
        var obj = _pool.Get();
        obj.transform.SetPositionAndRotation(position, rotation);
        return obj;
    }

    public void Despawn(GameObject obj) => _pool.Release(obj);

    void OnDestroy() => _pool.Dispose();
}
```

## Pool Lifecycle

| Callback | When | Use For |
|----------|------|---------|
| `createFunc` | Pool empty, need new instance | `Instantiate()` |
| `actionOnGet` | Object retrieved from pool | `SetActive(true)`, reset state |
| `actionOnRelease` | Object returned to pool | `SetActive(false)`, stop VFX |
| `actionOnDestroy` | Pool exceeds `maxSize` | `Destroy()` |

## IPoolable Pattern — Self-Returning Objects

```csharp
public interface IPoolable
{
    void OnSpawn();
    void OnDespawn();
    void SetPool(IObjectPool<GameObject> pool);
}

public sealed class Projectile : MonoBehaviour, IPoolable
{
    private IObjectPool<GameObject> _pool;

    public void SetPool(IObjectPool<GameObject> pool) => _pool = pool;

    public void OnSpawn()
    {
        // Reset state
        _lifetime = 0f;
        _hasHit = false;
    }

    public void OnDespawn()
    {
        // Cleanup
        _trail?.Clear();
    }

    void Update()
    {
        _lifetime += Time.deltaTime;
        if (_lifetime > _maxLifetime || _hasHit)
            _pool.Release(gameObject); // self-return
    }
}
```

## Generic Component Pool

```csharp
using UnityEngine.Pool;

public sealed class ComponentPool<T> where T : Component
{
    readonly ObjectPool<T> _pool;
    readonly Transform _parent;

    public ComponentPool(T prefab, Transform parent, int capacity = 10, int max = 50)
    {
        _parent = parent;
        _pool = new ObjectPool<T>(
            () => { var obj = Object.Instantiate(prefab, parent); obj.gameObject.SetActive(false); return obj; },
            obj => obj.gameObject.SetActive(true),
            obj => obj.gameObject.SetActive(false),
            obj => Object.Destroy(obj.gameObject),
            defaultCapacity: capacity,
            maxSize: max
        );
    }

    public T Get() => _pool.Get();
    public void Release(T obj) => _pool.Release(obj);
    public void Dispose() => _pool.Dispose();
}
```

## Pre-2021 Custom Pool

```csharp
// Simple pool using Queue — for projects before Unity 2021
public sealed class SimplePool<T> where T : Component
{
    readonly Queue<T> _available = new();
    readonly T _prefab;
    readonly Transform _parent;

    public SimplePool(T prefab, Transform parent, int prewarm = 10)
    {
        _prefab = prefab;
        _parent = parent;
        for (int i = 0; i < prewarm; i++)
        {
            var obj = Object.Instantiate(prefab, parent);
            obj.gameObject.SetActive(false);
            _available.Enqueue(obj);
        }
    }

    public T Get()
    {
        var obj = _available.Count > 0 ? _available.Dequeue() : Object.Instantiate(_prefab, _parent);
        obj.gameObject.SetActive(true);
        return obj;
    }

    public void Release(T obj)
    {
        obj.gameObject.SetActive(false);
        _available.Enqueue(obj);
    }
}
```

## When to Pool

| Scenario | Pool? | Reason |
|----------|-------|--------|
| Bullets, VFX, particles | ✅ | High spawn/destroy frequency |
| Enemies, NPCs | ✅ | Frequent spawn during waves |
| UI list items | ✅ | ScrollView virtualization |
| Scene-lifetime objects | ❌ | Created once, never destroyed |
| Player character | ❌ | Single instance |
| Audio one-shots | ⚠️ | Pool if > 10/sec, otherwise OK |

## Common Mistakes

- ❌ Forgetting to reset state in `actionOnGet` (stale data from previous use)
- ❌ Destroying pooled objects instead of releasing them
- ❌ Not clearing event subscriptions on release (memory leaks)
- ❌ Releasing an object that's already in the pool (use `collectionCheck: true`)
- ❌ Setting `maxSize` too low (causes frequent Destroy/Instantiate)

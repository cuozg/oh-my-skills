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
        _lifetime = 0f;
        _hasHit = false;
    }

    public void OnDespawn()
    {
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

## When to Pool

| Scenario | Pool? | Reason |
|----------|-------|--------|
| Bullets, VFX, particles | ✅ | High spawn/destroy frequency |
| Enemies, NPCs | ✅ | Frequent spawn during waves |
| UI list items | ✅ | ScrollView virtualization |
| Scene-lifetime objects | ❌ | Created once, never destroyed |
| Player character | ❌ | Single instance |
| Audio one-shots | ⚠️ | Pool if > 10/sec, otherwise OK |

<!-- Advanced: object-pooling-advanced.md -->

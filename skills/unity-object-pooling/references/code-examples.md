# Code Examples: Object Pooling Patterns

## Unity Built-in ObjectPool (Simplest)

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

## IPoolable Interface + Projectile

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

## Pool Warming (Async)

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

## Collection Pooling

```csharp
using UnityEngine.Pool;

var results = ListPool<Collider>.Get();
try { /* process results */ }
finally { ListPool<Collider>.Release(results); }
```

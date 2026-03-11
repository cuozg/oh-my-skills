# Object Pooling — Advanced

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

## Common Mistakes

- ❌ Forgetting to reset state in `actionOnGet` (stale data from previous use)
- ❌ Destroying pooled objects instead of releasing them
- ❌ Not clearing event subscriptions on release (memory leaks)
- ❌ Releasing an object that's already in the pool (use `collectionCheck: true`)
- ❌ Setting `maxSize` too low (causes frequent Destroy/Instantiate)

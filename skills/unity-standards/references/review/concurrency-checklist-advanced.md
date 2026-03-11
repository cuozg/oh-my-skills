# Concurrency Checklist — Advanced

## Race Conditions

- [ ] Shared mutable state protected by `lock` or concurrent collection
- [ ] `Interlocked` for simple counters: `Interlocked.Increment(ref count)`
- [ ] Event unsubscribe is thread-safe (use `lock` around delegate)
- [ ] `ConcurrentDictionary` / `ConcurrentQueue` over `Dictionary` + `lock`
- [ ] Double-checked locking for lazy init uses `volatile`

## Common Patterns

```csharp
// Thread-safe singleton
private static volatile GameManager _instance;
private static readonly object _lock = new();
public static GameManager Instance
{
    get
    {
        if (_instance == null)
            lock (_lock)
                if (_instance == null)
                    _instance = FindObjectOfType<GameManager>();
        return _instance;
    }
}

// Main thread dispatcher (pre-2022)
private readonly ConcurrentQueue<Action> mainThreadQueue = new();
void Update()
{
    while (mainThreadQueue.TryDequeue(out var action)) action();
}
public void RunOnMainThread(Action action) => mainThreadQueue.Enqueue(action);
```

## Awaitable (Unity 6+)

- [ ] `Awaitable` used instead of UniTask for Unity 6+ projects
- [ ] `Awaitable.BackgroundThreadAsync()` / `MainThreadAsync()` for thread switching
- [ ] `Awaitable.NextFrameAsync()` instead of `yield return null`
- [ ] Cancellation via `destroyCancellationToken` on MonoBehaviour methods

```csharp
// Unity 6 thread switching — no external package needed
async Awaitable ProcessDataAsync()
{
    await Awaitable.BackgroundThreadAsync();
    var result = ExpensiveComputation(); // runs on thread pool
    await Awaitable.MainThreadAsync();
    transform.position = result; // safe — back on main thread
}
```

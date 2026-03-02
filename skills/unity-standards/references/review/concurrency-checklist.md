# Concurrency Checklist

## Main Thread Rule

- [ ] All Unity API calls on main thread (Transform, GameObject, Component)
- [ ] `UnityEngine.Object` access from background thread → crash
- [ ] UI updates dispatched to main thread

```csharp
// BAD: Unity API from background thread
Task.Run(() => transform.position = newPos); // CRASH

// GOOD: Dispatch to main thread
private SynchronizationContext mainThread;
void Awake() => mainThread = SynchronizationContext.Current;
void DoAsync()
{
    Task.Run(() =>
    {
        var result = HeavyComputation();
        mainThread.Post(_ => transform.position = result, null);
    });
}
```

## Async/Await

- [ ] `async void` only for event handlers — use `async UniTask` or `async Task`
- [ ] `ConfigureAwait(false)` for non-Unity continuations
- [ ] Cancellation via `CancellationToken` — pass `destroyCancellationToken` (2022+)
- [ ] `await` in `OnDestroy` — object may be destroyed mid-await
- [ ] Exception handling: `async void` swallows exceptions silently

```csharp
// BAD: Fire-and-forget with no error handling
async void Start() { await LoadDataAsync(); }

// GOOD: UniTask with cancellation
async UniTaskVoid Start()
{
    try { await LoadDataAsync(destroyCancellationToken); }
    catch (OperationCanceledException) { } // Expected on destroy
}
```

## Job System / Burst

- [ ] `NativeArray` / `NativeList` disposed after use (memory leak)
- [ ] No managed types in Jobs (class references, strings)
- [ ] `[ReadOnly]` attribute on input NativeArrays
- [ ] Job dependencies chained: `jobB.Schedule(jobA_handle)`
- [ ] `Complete()` called before reading results

| Type | Thread-Safe | Notes |
|------|------------|-------|
| `NativeArray<T>` | With safety checks | Dispose required |
| `NativeList<T>` | No | Single writer only |
| `NativeHashMap<K,V>` | Parallel writer variant | Use `.AsParallelWriter()` |
| `NativeQueue<T>` | Parallel writer variant | Use `.AsParallelWriter()` |

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

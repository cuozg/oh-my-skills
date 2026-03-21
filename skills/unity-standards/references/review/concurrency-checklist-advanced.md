# Concurrency Checklist - Advanced

## Race Conditions

- [ ] Shared mutable state protected by `lock`, `Interlocked`, or a concurrent collection
- [ ] Event subscribe and unsubscribe paths stay on the expected thread
- [ ] `ConcurrentDictionary` / `ConcurrentQueue` used instead of ad-hoc locking where appropriate
- [ ] No Unity API calls inside background-thread code paths
- [ ] Background work returns plain data, then re-enters the main thread before touching scene objects

## Common Patterns

```csharp
// Pure C# singleton - no Unity API involved
private static readonly Lazy<PathCache> s_Instance = new(() => new PathCache());
public static PathCache Instance => s_Instance.Value;

// Main-thread dispatcher for projects that need one
private readonly ConcurrentQueue<Action> _mainThreadQueue = new();

private void Update()
{
    while (_mainThreadQueue.TryDequeue(out var action))
        action();
}

public void RunOnMainThread(Action action) => _mainThreadQueue.Enqueue(action);
```

If a project already has UniTask or Awaitable-based thread switching helpers, prefer those over inventing another dispatcher.

## Awaitable And UniTask Review Points

- [ ] Project uses one async stack consistently inside the feature under review
- [ ] `Awaitable.BackgroundThreadAsync()` / `MainThreadAsync()` used only around pure data work
- [ ] `destroyCancellationToken` or another lifetime token is forwarded through long-lived async methods
- [ ] No code awaits the same `Awaitable` instance multiple times
- [ ] No Unity object access happens after switching to a background thread

```csharp
async Awaitable ProcessDataAsync(CancellationToken ct)
{
    await Awaitable.BackgroundThreadAsync();
    var result = ExpensiveComputation();

    ct.ThrowIfCancellationRequested();

    await Awaitable.MainThreadAsync();
    transform.position = result;
}
```

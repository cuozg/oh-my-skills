# UniTask Async Patterns

Use UniTask for all async operations. Allocation-free async/await, cancellation, parallel ops.
**Note:** UniTask does NOT use ThreadPool by default — it runs on the Unity main thread's PlayerLoop.

## Signatures & Rules
```csharp
// ✅ UniTask — awaitable, allocation-free
public async UniTask LoadDataAsync(CancellationToken ct = default) { ... }
// ✅ UniTask<T> — awaitable with result
public async UniTask<PlayerData> GetPlayerAsync(string id, CancellationToken ct = default) { ... }
// ✅ UniTaskVoid — fire-and-forget (Unity entry points only)
public async UniTaskVoid OnButtonClick() { await ProcessAsync(this.GetCancellationTokenOnDestroy()); }
// ❌ NEVER: Task (allocates), async void (swallows exceptions)
```

## Threading & Streams
```csharp
// Thread pool switching (UniTask v2)
await UniTask.SwitchToThreadPool();
ComputeHeavyData(); // Runs on background thread
await UniTask.SwitchToMainThread();

// Channels for producer-consumer (replaces AsyncReactiveProperty)
var channel = Channel.CreateSingleConsumerUnbounded<int>();
channel.Writer.TryWrite(1);

// IUniTaskAsyncEnumerable for streams (button clicks, physics triggers)
await foreach (var item in channel.Reader.ReadAllAsync(ct)) { ... }
```

## Cancellation, Waiting & State
```csharp
// Manual CTS (debounce, search, etc.)
this.searchCts?.Cancel(); this.searchCts?.Dispose();
this.searchCts = new CancellationTokenSource();

// MonoBehaviour lifetime — auto-cancel on destroy
var ct = this.GetCancellationTokenOnDestroy();

await UniTask.Delay(1000, cancellationToken: ct);                     // milliseconds
await UniTask.DelayFrame(1, cancellationToken: ct);                   // one frame
await UniTask.Yield(PlayerLoopTiming.Update, cancellationToken: ct);
await UniTask.WaitUntil(() => this.isReady, cancellationToken: ct);
await UniTask.WaitWhile(() => this.isLoading, cancellationToken: ct);
await UniTask.Never(ct);                                              // infinite wait

// Deferred async (runs only when awaited)
var lazyTask = UniTask.Lazy(() => LoadAssetAsync(ct));

// Unity Integration
await SceneManager.LoadSceneAsync(scene).ToUniTask(progress: p, cancellationToken: ct);
using var req = UnityWebRequest.Get(url);
await req.SendWebRequest().ToUniTask(cancellationToken: ct);
```

## Error Handling & Parallel
```csharp
// Proper try/catch — let cancellation propagate
try { await DoWorkAsync(ct); }
catch (OperationCanceledException) { /* Expected */ }
catch (Exception ex) { this.logger.Error(ex.Message); throw; }

// SuppressCancellationThrow — clean bool check
var (isCanceled, result) = await LoadAsync(ct).SuppressCancellationThrow();
if (isCanceled) return;

// Parallel & race
var (a, b, c) = await UniTask.WhenAll(Task1(ct), Task2(ct), Task3(ct));
var (idx, result) = await UniTask.WhenAny(task, UniTask.Delay(5000, cancellationToken: ct));
```

## Anti-Patterns
- ❌ No `CancellationToken` param — always accept and propagate `ct`
- ❌ `.Result` / `.GetAwaiter().GetResult()` — deadlock risk
- ❌ Fire-and-forget without `.Forget()` — use `DoWorkAsync(ct).Forget()`
- ❌ `ForgetOnCancel` anti-pattern — canceling a forgotten task without awaiting it can leave dangling state
- ❌ Catch all exceptions — swallows cancellation; catch specific types
- ❌ `async void` — use `UniTaskVoid` for fire-and-forget entry points

## Cheat Sheet
| Pattern | Code |
|:--------|:-----|
| Threading | `UniTask.SwitchToThreadPool()` / `SwitchToMainThread()` |
| Streams | `IUniTaskAsyncEnumerable<T>`, `Channel<T>` |
| State | `UniTask.Never(ct)`, `UniTask.Lazy(() => ...)` |
| Delay | `UniTask.Delay(1000, cancellationToken: ct)` |
| Next frame | `UniTask.NextFrame(ct)` |
| Wait condition | `UniTask.WaitUntil(() => ready, cancellationToken: ct)` |
| Parallel | `UniTask.WhenAll(t1, t2, t3)` |
| Race / timeout | `UniTask.WhenAny(task, timeout)` |
| Cancel on destroy | `this.GetCancellationTokenOnDestroy()` |
| Fire-and-forget | `DoWorkAsync(ct).Forget()` |
| Suppress cancel | `.SuppressCancellationThrow()` |

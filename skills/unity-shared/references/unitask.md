# UniTask Async Patterns

Use UniTask for all async operations in Unity. Allocation-free async/await, cancellation, parallel ops.

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

## Cancellation

```csharp
// MonoBehaviour lifetime — auto-cancel on destroy
var ct = this.GetCancellationTokenOnDestroy();
await LoadAllDataAsync(ct);

// Manual CTS (debounce, search, etc.)
this.searchCts?.Cancel(); this.searchCts?.Dispose();
this.searchCts = new CancellationTokenSource();
await UniTask.Delay(300, cancellationToken: this.searchCts.Token);
```

## Waiting & Unity Integration

```csharp
await UniTask.Delay(1000);                          // milliseconds
await UniTask.Delay(TimeSpan.FromSeconds(1.5f));    // timespan
await UniTask.DelayFrame(1);                        // one frame
await UniTask.Yield();                              // yield current frame
await UniTask.WaitUntil(() => this.isReady);        // condition true
await UniTask.WaitWhile(() => this.isLoading);      // condition false

// Scene loading with progress
var op = SceneManager.LoadSceneAsync(sceneName);
await op.ToUniTask(progress: Progress.Create<float>(p => Debug.Log(p)), cancellationToken: ct);

// UnityWebRequest
using var req = UnityWebRequest.Get(url);
await req.SendWebRequest().ToUniTask(cancellationToken: ct);
```

## Error Handling & Parallel

```csharp
// Proper try/catch — let cancellation propagate
try { await DoWorkAsync(ct); }
catch (OperationCanceledException) { /* Expected — do not rethrow */ }
catch (Exception ex) { this.logger.Error(ex.Message); throw; }

// SuppressCancellationThrow — clean bool check
var (isCanceled, result) = await LoadAsync(ct).SuppressCancellationThrow();
if (isCanceled) return;

// Parallel & race
var (a, b, c) = await UniTask.WhenAll(Task1(ct), Task2(ct), Task3(ct));
var (idx, result) = await UniTask.WhenAny(task, UniTask.Delay(5000, cancellationToken: ct));
```

## Anti-Patterns

- ❌ No CancellationToken param — always accept and propagate `ct`
- ❌ `.Result` / `.GetAwaiter().GetResult()` — deadlock risk
- ❌ Fire-and-forget without `.Forget()` — use `DoWorkAsync(ct).Forget()`
- ❌ Catch all exceptions — swallows cancellation; catch specific types
- ❌ `async void` — use `UniTaskVoid` for fire-and-forget entry points

## Cheat Sheet

| Pattern | Code |
|:--------|:-----|
| Delay | `UniTask.Delay(1000, cancellationToken: ct)` |
| Next frame | `UniTask.NextFrame(ct)` |
| Wait condition | `UniTask.WaitUntil(() => ready, cancellationToken: ct)` |
| Parallel | `UniTask.WhenAll(t1, t2, t3)` |
| Race / timeout | `UniTask.WhenAny(task, timeout)` |
| Cancel on destroy | `this.GetCancellationTokenOnDestroy()` |
| Fire-and-forget | `DoWorkAsync(ct).Forget()` |
| Suppress cancel | `.SuppressCancellationThrow()` |

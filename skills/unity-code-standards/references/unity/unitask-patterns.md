# UniTask Async Patterns

Use UniTask for all async operations in Unity projects. UniTask provides allocation-free async/await, cancellation support, and Unity lifecycle integration.

## Basic Patterns

### Async Method Signatures

```csharp
// ✅ GOOD: UniTask return type
public async UniTask LoadDataAsync(CancellationToken ct = default)
{
    var data = await LoadFromServerAsync(ct);
    ProcessData(data);
}

// ✅ GOOD: UniTask<T> for results
public async UniTask<PlayerData> GetPlayerAsync(string id, CancellationToken ct = default)
{
    return await this.api.FetchPlayerAsync(id, ct);
}

// ✅ GOOD: UniTaskVoid for fire-and-forget (Unity entry points)
public async UniTaskVoid OnButtonClick()
{
    await ProcessAsync(this.GetCancellationTokenOnDestroy());
}

// ❌ BAD: Task (allocates, no Unity integration)
public async Task LoadDataAsync() { }

// ❌ BAD: async void (swallows exceptions, no cancellation)
public async void LoadData() { }
```

### Cancellation

```csharp
// ✅ GOOD: CancellationToken from MonoBehaviour lifetime
public sealed class DataLoader : MonoBehaviour
{
    private async UniTaskVoid Start()
    {
        var ct = this.GetCancellationTokenOnDestroy();
        await LoadAllDataAsync(ct);
    }

    private async UniTask LoadAllDataAsync(CancellationToken ct)
    {
        var playerData = await LoadPlayerAsync(ct);
        ct.ThrowIfCancellationRequested();
        var inventoryData = await LoadInventoryAsync(ct);
    }
}

// ✅ GOOD: Manual CancellationTokenSource
public sealed class SearchService : IDisposable
{
    private CancellationTokenSource? searchCts;

    public async UniTask SearchAsync(string query)
    {
        // Cancel previous search
        this.searchCts?.Cancel();
        this.searchCts?.Dispose();
        this.searchCts = new CancellationTokenSource();

        try
        {
            await UniTask.Delay(300, cancellationToken: this.searchCts.Token); // Debounce
            var results = await this.api.SearchAsync(query, this.searchCts.Token);
            DisplayResults(results);
        }
        catch (OperationCanceledException)
        {
            // Expected when cancelled — do nothing
        }
    }

    public void Dispose()
    {
        this.searchCts?.Cancel();
        this.searchCts?.Dispose();
    }
}
```

## Injection with UniTask

```csharp
// ✅ GOOD: VContainer with async initialization
public sealed class GameInitializer : IInitializable
{
    private readonly ConfigService configService;
    private readonly PlayerService playerService;

    [Preserve]
    public GameInitializer(ConfigService configService, PlayerService playerService)
    {
        this.configService = configService;
        this.playerService = playerService;
    }

    public void Initialize()
    {
        InitializeAsync().Forget(); // Fire-and-forget from sync context
    }

    private async UniTask InitializeAsync()
    {
        await this.configService.LoadAsync();
        await this.playerService.InitializeAsync();
    }
}
```

## Parallel Operations

```csharp
// ✅ GOOD: WhenAll for parallel async
public async UniTask LoadGameAsync(CancellationToken ct)
{
    var (playerData, worldData, uiData) = await UniTask.WhenAll(
        LoadPlayerAsync(ct),
        LoadWorldAsync(ct),
        LoadUIAsync(ct)
    );

    InitializeGame(playerData, worldData, uiData);
}

// ✅ GOOD: WhenAny for race conditions
public async UniTask<T> LoadWithTimeout<T>(UniTask<T> task, float timeoutSeconds)
{
    var (hasValue, result) = await UniTask.WhenAny(
        task,
        UniTask.Delay(TimeSpan.FromSeconds(timeoutSeconds))
    );

    if (hasValue == 0)
        return result;

    throw new TimeoutException($"Operation timed out after {timeoutSeconds}s");
}
```

## Unity Integration

### Waiting Patterns

```csharp
// ✅ GOOD: UniTask delay (allocation-free)
await UniTask.Delay(1000); // milliseconds
await UniTask.Delay(TimeSpan.FromSeconds(1.5f));
await UniTask.DelayFrame(1); // Wait one frame
await UniTask.Yield(); // Yield current frame
await UniTask.NextFrame(); // Wait until next frame

// ✅ GOOD: Wait for Unity events
await UniTask.WaitUntil(() => this.isReady);
await UniTask.WaitWhile(() => this.isLoading);
await UniTask.WaitForEndOfFrame(this); // Pass MonoBehaviour

// ❌ BAD: Coroutine-style waits
yield return new WaitForSeconds(1f); // Use UniTask.Delay instead
yield return null; // Use UniTask.Yield instead
```

### Scene Loading

```csharp
// ✅ GOOD: Async scene loading with progress
public async UniTask LoadSceneAsync(string sceneName, IProgress<float> progress = null, CancellationToken ct = default)
{
    var operation = SceneManager.LoadSceneAsync(sceneName);
    operation.allowSceneActivation = false;

    while (operation.progress < 0.9f)
    {
        progress?.Report(operation.progress);
        await UniTask.Yield(ct);
    }

    progress?.Report(1f);
    operation.allowSceneActivation = true;
    await operation.ToUniTask(cancellationToken: ct);
}
```

### UnityWebRequest

```csharp
// ✅ GOOD: UniTask with UnityWebRequest
public async UniTask<string> FetchJsonAsync(string url, CancellationToken ct = default)
{
    using var request = UnityWebRequest.Get(url);
    await request.SendWebRequest().ToUniTask(cancellationToken: ct);

    if (request.result != UnityWebRequest.Result.Success)
    {
        throw new HttpRequestException($"Request failed: {request.error}");
    }

    return request.downloadHandler.text;
}
```

## Error Handling

```csharp
// ✅ GOOD: Proper try/catch with cancellation awareness
public async UniTask ProcessAsync(CancellationToken ct)
{
    try
    {
        await DoWorkAsync(ct);
    }
    catch (OperationCanceledException)
    {
        // Expected — object destroyed or token cancelled
        // Don't log, don't rethrow unless needed
    }
    catch (Exception ex)
    {
        this.logger.Error($"Processing failed: {ex.Message}");
        throw; // Re-throw for caller to handle
    }
}

// ✅ GOOD: SuppressCancellationThrow for clean handling
public async UniTask SafeLoadAsync(CancellationToken ct)
{
    var (isCanceled, result) = await LoadAsync(ct).SuppressCancellationThrow();
    if (isCanceled) return;

    ProcessResult(result);
}
```

## UniTask vs Coroutine Migration

```csharp
// ❌ OLD: Coroutine
private IEnumerator LoadSequence()
{
    yield return new WaitForSeconds(1f);
    yield return StartCoroutine(LoadData());
    yield return new WaitForEndOfFrame();
    OnLoadComplete();
}

// ✅ NEW: UniTask
private async UniTask LoadSequenceAsync(CancellationToken ct = default)
{
    await UniTask.Delay(1000, cancellationToken: ct);
    await LoadDataAsync(ct);
    await UniTask.WaitForEndOfFrame(this, ct);
    OnLoadComplete();
}
```

## Anti-Patterns

```csharp
// ❌ BAD: Ignoring CancellationToken
public async UniTask LoadAsync()
{
    await SomeOperationAsync(); // No cancellation support!
}

// ❌ BAD: Using .Result or .GetAwaiter().GetResult()
var data = LoadAsync().GetAwaiter().GetResult(); // Deadlock risk!

// ❌ BAD: Fire-and-forget without Forget()
async UniTask DoWork() { }
DoWork(); // Warning: not awaited

// ✅ GOOD: Explicit fire-and-forget
DoWork().Forget();

// ❌ BAD: Catching all exceptions (including cancellation)
try { await DoWork(ct); }
catch (Exception) { } // Swallows cancellation!

// ✅ GOOD: Catch specific, let cancellation propagate
try { await DoWork(ct); }
catch (OperationCanceledException) { /* Expected */ }
catch (Exception ex) { this.logger.Error(ex.Message); throw; }
```

## Cheat Sheet

| Pattern | Code |
|:--------|:-----|
| Delay | `await UniTask.Delay(1000, cancellationToken: ct)` |
| Next frame | `await UniTask.NextFrame(ct)` |
| Wait condition | `await UniTask.WaitUntil(() => ready, cancellationToken: ct)` |
| Parallel | `await UniTask.WhenAll(task1, task2, task3)` |
| Race | `await UniTask.WhenAny(task, timeout)` |
| Cancel on destroy | `this.GetCancellationTokenOnDestroy()` |
| Fire-and-forget | `DoWorkAsync(ct).Forget()` |
| Suppress cancel | `.SuppressCancellationThrow()` |

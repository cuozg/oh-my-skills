# UniTask Integration & Error Handling

Continued from [unitask-patterns.md](unitask-patterns.md).

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

**Continue in [unitask-patterns-advanced.md](unitask-patterns-advanced.md) for Migration, Anti-Patterns, and Cheat Sheet.**

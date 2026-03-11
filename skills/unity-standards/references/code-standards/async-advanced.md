# Async Patterns — Advanced

## Error Handling & Converting Unity Async

```csharp
async UniTask<bool> TrySave(CancellationToken ct)
{
    try
    {
        await WriteFile(_savePath, _data, ct);
        return true;
    }
    catch (OperationCanceledException) { return false; } // normal — don't log
    catch (System.Exception ex) { Debug.LogException(ex); return false; }
}

// AsyncOperation → UniTask: await SceneManager.LoadSceneAsync("Level1"); await Resources.LoadAsync<Texture2D>("splash");
// Coroutine → UniTask: await SomeLegacyCoroutine().ToUniTask(cancellationToken: ct);
// UnityWebRequest: await UnityWebRequest.Get(url).SendWebRequest().WithCancellation(ct);
```

## Awaitable — Unity 6+ Built-In

Unity 6 (2023.1+) introduces `Awaitable` as a built-in async primitive — no UniTask dependency needed:

```csharp
// Awaitable replaces UniTask for Unity-native async
async Awaitable LoadLevelAsync(string sceneName)
{
    await SceneManager.LoadSceneAsync(sceneName);
    await Awaitable.WaitForSecondsAsync(0.5f);
    _ui.ShowHUD();
}

// Frame waits
await Awaitable.NextFrameAsync();
await Awaitable.EndOfFrameAsync();
await Awaitable.FixedUpdateAsync();

// Background thread round-trip
await Awaitable.BackgroundThreadAsync();
var result = HeavyComputation();
await Awaitable.MainThreadAsync(); // back to main thread
ApplyResult(result);
```

| Feature | UniTask | Awaitable (Unity 6+) |
|---------|---------|---------------------|
| Dependency | External package | Built-in |
| Thread switching | `UniTask.SwitchToThreadPool()` | `Awaitable.BackgroundThreadAsync()` |
| Frame wait | `UniTask.Yield()` | `Awaitable.NextFrameAsync()` |
| Cancellation | `CancellationToken` | `CancellationToken` + `destroyCancellationToken` |
| Min Unity version | 2019.3+ | 2023.1+ (Unity 6) |

**Guideline:** Use `Awaitable` for new projects on Unity 6+. Use `UniTask` for older projects or when you need features like `UniTask.WhenAll` with value-type returns.

## Version Compatibility

| Feature | Min Unity Version |
|---------|------------------|
| `destroyCancellationToken` | 2022.2+ |
| `Awaitable` | 2023.1+ (Unity 6) |
| `async/await` in Unity | 2017.1+ |
| UniTask recommended | 2019.3+ |

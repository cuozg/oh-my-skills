# Async Patterns - Advanced

## Error Handling And Converting Unity Async

```csharp
async UniTask<bool> TrySaveAsync(CancellationToken ct)
{
    try
    {
        await WriteFile(_savePath, _data, ct);
        return true;
    }
    catch (OperationCanceledException)
    {
        return false; // normal cancellation path
    }
    catch (System.Exception ex)
    {
        Debug.LogException(ex);
        return false;
    }
}

// AsyncOperation -> UniTask: await SceneManager.LoadSceneAsync("Level1");
// Coroutine -> UniTask: await SomeLegacyCoroutine().ToUniTask(cancellationToken: ct);
// UnityWebRequest -> UniTask: await UnityWebRequest.Get(url).SendWebRequest().WithCancellation(ct);
```

## Awaitable - Built-In Unity Async

Use `Awaitable` in Unity versions that ship it, including Unity 6. It is a strong default for Unity-native async operations when the project does not already standardize on UniTask.

```csharp
async Awaitable LoadLevelAsync(string sceneName)
{
    await SceneManager.LoadSceneAsync(sceneName);
    await Awaitable.WaitForSecondsAsync(0.5f);
    _ui.ShowHUD();
}

await Awaitable.NextFrameAsync();
await Awaitable.BackgroundThreadAsync();
var result = HeavyComputation();
await Awaitable.MainThreadAsync();
ApplyResult(result);
```

## Awaitable Vs UniTask Vs Task

| Concern | Awaitable | UniTask | Task |
|---------|-----------|---------|------|
| Unity-native async | Strong fit | Strong fit | Fine but heavier |
| Extra dependency | None | Package dependency | None |
| Multiple await on same result | No - do not reuse same instance | Usually fine | Fine |
| Third-party .NET interop | Bridge as needed | Bridge as needed | Best fit |
| Older Unity support | Verify local version | Good when repo already uses it | Works broadly |

Important difference: official Unity docs note that `Awaitable` instances are pooled, so a single instance is not safe to await multiple times.

## Guidance

- Prefer `Awaitable` for Unity-native async in projects that already use it.
- Prefer UniTask when the repo already uses it or needs older-version support.
- Prefer `Task` for external library interop or APIs that already expose `Task`.
- Do not convert a codebase to a new async stack opportunistically inside an unrelated feature.

## Version Notes

- `destroyCancellationToken` exists on recent Unity versions; verify exact availability in `references/other/official-source-map.md` before making a hard version claim.
- Do not describe `Awaitable` as "Unity 6 only". Confirm against the official docs for the local editor version.

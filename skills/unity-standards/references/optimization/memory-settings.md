# Memory Optimization Settings

## Texture Memory Management

### Import Settings Checklist

- [ ] Max Size: match actual display size (don't use 4096 for a 256px icon)
- [ ] Read/Write Enabled: OFF (doubles memory if ON)
- [ ] Generate Mip Maps: ON for 3D objects, OFF for UI/sprites
- [ ] Compression: platform-appropriate (see build-settings.md)
- [ ] sRGB: ON for color textures, OFF for data textures (normal maps, masks)

### Texture Streaming (Unity 2018.2+)

Loads mip levels on demand based on camera distance — reduces peak memory.

**Enable:**
1. Edit → Project Settings → Quality → Texture Streaming: ON
2. Set Memory Budget (default 512 MB — adjust per platform)
3. Individual textures: Import Settings → Streaming Mipmaps: ON

**Caveats:**
- Adds ~1ms CPU overhead for mip management
- May cause visible pop-in on fast camera movement
- Not suitable for UI textures (need full resolution always)

## Audio Memory

| Setting | Memory Impact |
|---------|--------------|
| Decompress On Load | Full PCM in memory — fast playback, high memory |
| Compressed In Memory | Compressed in memory — CPU decode on play |
| Streaming | Minimal memory — disk I/O on play |

**Rules:**
- Short SFX (< 200KB compressed): Decompress On Load
- Everything else: Compressed In Memory or Streaming
- Music: Always Streaming
- Mobile: Force Mono on SFX, reduce sample rate to 22050Hz

## Asset Lifecycle Management

### Addressables Release Pattern

```csharp
// MUST release handles — unreleased = memory leak
private AsyncOperationHandle<GameObject> _handle;

async UniTask LoadEnemy(string key, CancellationToken ct)
{
    _handle = Addressables.LoadAssetAsync<GameObject>(key);
    await _handle.WithCancellation(ct);
    Instantiate(_handle.Result);
}

void OnDestroy()
{
    if (_handle.IsValid())
        Addressables.Release(_handle);
}
```

### Resources API Cleanup

```csharp
// After scene transition — unload unused assets
await SceneManager.LoadSceneAsync("NewScene");
await Resources.UnloadUnusedAssets(); // triggers GC + asset unload
System.GC.Collect(); // optional: force GC after unload
```

### Asset Reference Counting

- Every `Addressables.LoadAssetAsync` needs a matching `Release`
- Every `Addressables.InstantiateAsync` needs `ReleaseInstance` or `Release` on the handle
- Profile with Addressables Event Viewer to find leaks

## Scene Loading Strategies

| Strategy | Memory | Transition |
|----------|--------|-----------|
| Single (LoadSceneMode.Single) | Previous scene fully unloaded | Clean but jarring |
| Additive + Unload | Both scenes briefly in memory | Smooth transitions possible |
| Additive persistent | Multiple scenes stacked | Flexible but memory-heavy |

**Pattern:** Keep a lightweight "persistent" scene (managers, UI) loaded always. Load/unload gameplay scenes additively.

```csharp
// Additive load + unload previous
async UniTask TransitionScene(string next, CancellationToken ct)
{
    await SceneManager.LoadSceneAsync(next, LoadSceneMode.Additive).WithCancellation(ct);
    await SceneManager.UnloadSceneAsync(_currentScene).WithCancellation(ct);
    _currentScene = next;
    await Resources.UnloadUnusedAssets();
}
```

## Memory Budget Guidelines

| Platform | Total Budget | Textures | Audio | Meshes | Scripts/Other |
|----------|-------------|----------|-------|--------|---------------|
| Mobile (2GB) | 600-800 MB | 200-300 MB | 30-50 MB | 50-100 MB | 200-350 MB |
| Mobile (4GB) | 1.2-1.5 GB | 400-600 MB | 50-80 MB | 100-200 MB | 400-600 MB |
| PC | 2-4 GB | 1-2 GB | 100-200 MB | 200-500 MB | 500 MB-1 GB |
| Console | 3-5 GB | 1.5-3 GB | 150-300 MB | 300-600 MB | 500 MB-1 GB |

Use Unity Memory Profiler to verify against these targets.

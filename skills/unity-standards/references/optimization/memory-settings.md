# Memory Optimization Settings

## Texture Memory Management

### Import Settings Checklist

- [ ] Max Size: match actual display size (don't use 4096 for a 256px icon)
- [ ] Read/Write Enabled: OFF (doubles memory if ON)
- [ ] Generate Mip Maps: ON for 3D objects, OFF for UI/sprites
- [ ] Compression: platform-appropriate (see build-settings.md)
- [ ] sRGB: ON for color textures, OFF for data textures (normal maps, masks)

### Mipmap Streaming

Loads mip levels on demand based on camera distance - reduces peak memory.
(Called Texture Streaming before Unity 6.)

**Enable:**
1. Edit -> Project Settings -> Quality -> Mipmap Streaming: ON
2. Set Memory Budget (default 512 MB - adjust per platform)
3. Individual textures: enable mipmap streaming in the texture import settings

**Caveats:**
- Adds CPU cost for mip management; profile on target devices
- May cause visible pop-in on fast camera movement
- Not suitable for UI textures (need full resolution always)

## Audio Memory

Single source for audio import rules in these references; deeper Unity 6
guidance (codecs per platform, mixer CPU) lives in the `unity:optimize-audio` skill.

| Load Type | Memory Impact | Use For |
|-----------|--------------|---------|
| Decompress On Load | Full PCM in memory - fast playback, high memory | Short, frequent SFX (< 200KB compressed) |
| Compressed In Memory | Compressed in memory - CPU decode on play | Medium SFX, voice lines |
| Streaming | Minimal memory - disk I/O on play | Music, long ambient beds |

**Mobile:** Force To Mono on SFX and 3D sources (~50% size), reduce sample rate
to 22050Hz for non-music.

## Managed Memory And GC

- Keep **Use Incremental GC** ON (Player Settings, default) - spreads collection
  over frames instead of one long pause. It does not reduce allocation; remove
  per-frame allocations first.
- Avoid `System.GC.Collect()` in gameplay; it forces a full blocking collection.

## Asset Lifecycle Management

### Addressables Release Pattern

Examples use Unity 6 `Awaitable`; follow the project's async style (UniTask etc.)
per `references/code-standards/lifecycle-async-errors.md`.

```csharp
// MUST release handles - unreleased = memory leak
private AsyncOperationHandle<GameObject> _handle;

async Awaitable LoadEnemy(string key, CancellationToken ct)
{
    _handle = Addressables.LoadAssetAsync<GameObject>(key);
    await _handle.Task;
    ct.ThrowIfCancellationRequested(); // owner died mid-load; OnDestroy still releases
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
// After scene transition - unload unused assets
await SceneManager.LoadSceneAsync("NewScene");
await Resources.UnloadUnusedAssets(); // runs a GC + unloads unreferenced assets
```

### Asset Reference Counting

- Every `Addressables.LoadAssetAsync` needs a matching `Release`
- Every `Addressables.InstantiateAsync` needs `ReleaseInstance` or `Release` on the handle
- Find leaks with the Addressables Profiler module (Profiler window; replaces the
  removed Event Viewer in Addressables 2.x)
- For remote bundles, include an unload strategy in the feature design. Every
  loaded bundle or asset family needs an owner, release point, and verification
  path.

## Scene Loading Strategies

| Strategy | Memory | Transition |
|----------|--------|-----------|
| Single (LoadSceneMode.Single) | Previous scene fully unloaded | Clean but jarring |
| Additive + Unload | Both scenes briefly in memory | Smooth transitions possible |
| Additive persistent | Multiple scenes stacked | Flexible but memory-heavy |

**Pattern:** Keep a lightweight "persistent" scene (managers, UI) loaded always. Load/unload gameplay scenes additively.

```csharp
// Additive load + unload previous
async Awaitable TransitionScene(string next, CancellationToken ct)
{
    await SceneManager.LoadSceneAsync(next, LoadSceneMode.Additive);
    ct.ThrowIfCancellationRequested();
    await SceneManager.UnloadSceneAsync(_currentScene);
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

Verify with the Memory Profiler package (`com.unity.memoryprofiler` 1.x): capture
snapshots from a development build on the target device and compare
before/after; Editor captures include Editor overhead.

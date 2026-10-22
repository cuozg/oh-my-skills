# Startup & Iteration Optimization

## Enter Play Mode Settings (Editor Only)

Dramatically reduces Enter Play Mode time in Editor.

**Enable:** Edit -> Project Settings -> Editor -> Enter Play Mode Settings ->
"When entering Play Mode" (Unity 6 dropdown replacing the old checkboxes)

| Option | Effect |
|--------|--------|
| Reload Domain and Scene (default) | Full reset; slowest |
| Reload Scene only | Skips C# domain reload (largest savings); requires static resets below |
| Reload Domain only | Skips scene reload |
| Do not reload Domain or Scene | Fastest; requires static resets and scene-state discipline |

### Domain Reload OFF - Required Code Changes

Without domain reload, static fields persist between play sessions:

```csharp
// BAD: static state carries over - stale data on second play
private static int s_score = 0;
private static List<Enemy> s_activeEnemies = new();
private static event Action OnGameOver;

// GOOD: reset in RuntimeInitializeOnLoadMethod
[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
static void ResetStatics()
{
    s_score = 0;
    s_activeEnemies?.Clear();
    OnGameOver = null;
}
```

**Checklist for domain reload OFF:**
- [ ] All static fields have `[RuntimeInitializeOnLoadMethod]` reset
- [ ] All static events are nulled in reset
- [ ] Singleton instances cleared in reset
- [ ] Static caches/dictionaries cleared
- [ ] No `static readonly` that depends on runtime state

## Reducing Assembly Count Impact

More assemblies = longer domain reload (even when domain reload is ON).

**Strategies:**
- Merge small assemblies that always load together
- Use `Assembly Definition References` to limit recompilation scope
- Keep test asmdefs behind the `UNITY_INCLUDE_TESTS` define constraint (default for Test Framework templates) so they stay out of player builds
- Move third-party code to precompiled DLLs (Plugin folder)

## Startup Time Optimization

Measure the complete app-launch-to-home-screen flow before optimizing. Break the
timeline into app launch, SDK init, config load, Addressables/local bundles,
remote catalog or API calls, and home UI render. Do not guess which step is slow.

For production startup work, load
`references/production/full-cycle-ownership.md` and include analytics, attribution, ads,
IAP, remote config, and other SDK initialization costs in the timeline.

### Splash Screen

| Setting | Impact |
|---------|--------|
| Show Splash Screen | Disable for faster start (Unity 6 allows this on Personal too) |
| Splash Duration | Minimum if required |
| Background | Static color (no texture load) |

The splash shows while the first scene loads; a heavy first scene extends it.
Keep the first scene a lightweight bootstrap.

### Preloading Strategy

```csharp
// Use [RuntimeInitializeOnLoadMethod] for critical init
[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
static void InitCriticalSystems()
{
    // Load critical managers before scene
    ServiceLocator.Initialize();
}

// Addressables: preload during loading screen.
// The returned handle is the preload owner - release it when the cache is dropped.
async Awaitable<AsyncOperationHandle<IList<Object>>> PreloadCriticalAssets()
{
    var keys = new List<string> { "UI/MainMenu", "Audio/BGM", "Config/GameSettings" };
    var handle = Addressables.LoadAssetsAsync<Object>(keys, null,
        Addressables.MergeMode.Union);
    await handle.Task;
    return handle;
}
```

### Script Execution Order

Heavy `Awake()`/`Start()` methods delay first frame. Solutions:
- Spread initialization across frames with `Awaitable` (or the project's UniTask)
- Use lazy initialization (init on first access, not startup)
- Move heavy init to loading screen async flow

```csharp
// Instead of heavy Start() - Unity 6 Awaitable; swap for UniTask if the project uses it
async void Start() // Unity message entry point; exceptions surface in the Console
{
    // Show loading UI immediately
    _loadingScreen.Show();

    await Awaitable.NextFrameAsync(destroyCancellationToken); // let first frame render
    await LoadGameData(destroyCancellationToken);
    await Awaitable.NextFrameAsync(destroyCancellationToken);
    await InitializeSystems(destroyCancellationToken);

    _loadingScreen.Hide();
}
```

## Build Startup

| Optimization | Time Saved | How |
|-------------|-----------|-----|
| IL2CPP Faster runtime | +build time, -startup | Player Settings -> Code Generation: Faster Runtime |
| Strip Engine Code | Smaller binary, faster load | Player Settings -> Strip Engine Code: ON (IL2CPP) |
| Preloaded Shaders | Prevents runtime compile | Graphics -> Preloaded Shaders array |
| Addressables: local bundles | ~100-500ms | Avoids remote catalog fetch at start |

Measure cold start on a development build with the Profiler attached (build via
`unity build`, see `references/other/unity-cli-routing.md`); Editor timings do
not represent device startup.

## Startup Production Rules

- Prioritize only essential startup data. Delay non-critical APIs, analytics
  enrichments, ads, attribution, or secondary content until after home renders
  when product requirements allow it.
- Optimize config size and deserialization before adding complex loading
  infrastructure.
- Avoid blocking startup on remote bundles unless the first screen cannot
  function without them.
- State the target metric and evidence source, such as app launch to home
  screen, first interactive frame, cold start on low-end Android, or profiler
  timeline capture.

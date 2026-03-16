# Startup & Iteration Optimization

## Enter Play Mode Settings (Editor Only)

Dramatically reduces Enter Play Mode time in Editor.

**Enable:** Edit → Project Settings → Editor → Enter Play Mode Settings

| Setting | Default | Optimized | Effect |
|---------|---------|-----------|--------|
| Reload Domain | ON | OFF | Skips C# domain reload (2-10s savings) |
| Reload Scene | ON | OFF | Skips scene reload (1-3s savings) |

### Domain Reload OFF — Required Code Changes

Without domain reload, static fields persist between play sessions:

```csharp
// ❌ Static state carries over — stale data on second play
private static int s_score = 0;
private static List<Enemy> s_activeEnemies = new();
private static event Action OnGameOver;

// ✅ Reset in RuntimeInitializeOnLoadMethod
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
- Mark test assemblies as "Test" to exclude from builds
- Move third-party code to precompiled DLLs (Plugin folder)

## Startup Time Optimization

### Splash Screen

| Setting | Impact |
|---------|--------|
| Show Splash Screen | Disable in Pro license for faster start |
| Splash Duration | Minimum if required |
| Logo Draw Mode | Unity Logo Below (fastest) |
| Background | Static color (no texture load) |

### Preloading Strategy

```csharp
// Use [RuntimeInitializeOnLoadMethod] for critical init
[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
static void InitCriticalSystems()
{
    // Load critical managers before scene
    ServiceLocator.Initialize();
}

// Addressables: preload during loading screen
async UniTask PreloadCriticalAssets(CancellationToken ct)
{
    var keys = new List<string> { "UI/MainMenu", "Audio/BGM", "Config/GameSettings" };
    await Addressables.LoadAssetsAsync<Object>(keys, null, 
        Addressables.MergeMode.Union).WithCancellation(ct);
}
```

### Script Execution Order

Heavy `Awake()`/`Start()` methods delay first frame. Solutions:
- Spread initialization across frames with coroutines
- Use lazy initialization (init on first access, not startup)
- Move heavy init to loading screen async flow

```csharp
// Instead of heavy Start()
async UniTaskVoid Start()
{
    // Show loading UI immediately
    _loadingScreen.Show();
    
    await UniTask.Yield(); // let first frame render
    await LoadGameData(destroyCancellationToken);
    await UniTask.Yield();
    await InitializeSystems(destroyCancellationToken);
    
    _loadingScreen.Hide();
}
```

## Build Startup

| Optimization | Time Saved | How |
|-------------|-----------|-----|
| IL2CPP Faster runtime | +build time, -startup | Player Settings → Code Generation: Faster Runtime |
| Strip Engine Code | ~50-200ms | Player Settings → Strip Engine Code: ON |
| Preloaded Shaders | Prevents runtime compile | Graphics → Preloaded Shaders array |
| Disable Domain Reload | No effect on build | Editor-only setting |
| Addressables: local bundles | ~100-500ms | Avoids remote catalog fetch at start |

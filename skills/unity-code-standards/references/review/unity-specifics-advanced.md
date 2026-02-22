# Unity-Specific Review Checklist — Advanced Topics

## Camera

- [ ] Camera.main cached (it uses `FindObjectOfType` internally)
- [ ] Camera follow logic in `LateUpdate()`
- [ ] No multiple active audio listeners
- [ ] Appropriate near/far clip planes
- [ ] Camera stacking configured correctly (URP)

## Audio

- [ ] AudioSource pooled for frequent sounds
- [ ] Audio clips loaded via Addressables (not Resources)
- [ ] No 3D spatial audio on UI sounds
- [ ] Audio mixer used for volume control
- [ ] Mute handled via AudioMixer snapshot (not disabling AudioSources)

## DontDestroyOnLoad

- [ ] Duplicate instance guard in `Awake()`
- [ ] Used sparingly (prefer explicit lifetime management)
- [ ] References cleaned up on scene transition
- [ ] Not used for data that should be managed by a dedicated service

## Editor vs Runtime

- [ ] `#if UNITY_EDITOR` guards on editor-only code
- [ ] `[ExecuteAlways]` classes handle both modes
- [ ] Debug visualization in `OnDrawGizmos` / `OnDrawGizmosSelected`
- [ ] No `UnityEditor` namespace in runtime assemblies
- [ ] Editor scripts in Editor-only assembly definitions

## Platform Considerations

- [ ] No `Application.platform` checks at runtime if avoidable (use preprocessor)
- [ ] `Application.targetFrameRate` set appropriately per platform
- [ ] Screen.sleepTimeout configured for mobile
- [ ] No hardcoded screen sizes (use `Screen.width` / `Screen.height`)
- [ ] Touch input handled for mobile builds

## Common Unity Anti-Patterns

### Critical
- Empty `Update()` methods (remove them — still costs per-frame)
- `FindObjectOfType` in hot paths
- Uncached `Camera.main`
- Missing `OnDisable` / `OnDestroy` cleanup
- `Resources.Load` at runtime (use Addressables)

### Major
- `SendMessage` / `BroadcastMessage` usage
- String-based animator parameter access
- Legacy Input API in new projects
- Mutable ScriptableObject state persisting across sessions
- Deep hierarchy nesting (>5 levels)

### Minor
- Public fields instead of `[SerializeField] private`
- Missing `[Tooltip]` on designer-facing fields
- Missing `[Range]` / `[Min]` on numeric fields
- `Debug.Log` without `#if UNITY_EDITOR` guard
- Hardcoded layer/tag strings (use constants)

See also [unity-specifics.md](unity-specifics.md) for Lifecycle, Serialization, Coroutine, Transform, Input, and Physics sections.

# Unity Best Practices Checklist

## MonoBehaviour Lifecycle

### Initialization Order
- [ ] `Awake` — self-initialization only (cache own components, set defaults)
- [ ] `OnEnable` — subscribe to events, register with systems
- [ ] `Start` — cross-component initialization (access other objects safely)
- [ ] No cross-component access in `Awake` (other components may not exist)
- [ ] `Script Execution Order` used sparingly, with documentation

### Cleanup & Teardown
- [ ] `OnDisable` — unsubscribe events, stop coroutines, kill tweens
- [ ] `OnDestroy` — dispose native resources, release Addressable handles
- [ ] `OnApplicationQuit` — save state, cleanup platform services
- [ ] Coroutines stopped in `OnDisable` (stored handles, `StopAllCoroutines`)
- [ ] DOTween/LeanTween killed in `OnDisable` (`_tween?.Kill()`)
- [ ] No accessing other objects in `OnDestroy` (destroy order undefined)

### Enable/Disable Symmetry
Check EVERY MonoBehaviour for balanced pairs:
```
OnEnable:  event += Handler     ↔  OnDisable:  event -= Handler
OnEnable:  Register(this)       ↔  OnDisable:  Unregister(this)
OnEnable:  StartCoroutine(...)  ↔  OnDisable:  StopCoroutine(...) / StopAllCoroutines()
OnEnable:  DOTween.To(...)      ↔  OnDisable:  tween.Kill()
```

## Serialization

### Field Serialization
- [ ] `[SerializeField]` on private fields (not making fields public for Inspector)
- [ ] `[NonSerialized]` on public fields that shouldn't persist
- [ ] `[FormerlySerializedAs("old")]` when renaming serialized fields
- [ ] `[SerializeReference]` for polymorphic fields (with type stability plan)
- [ ] No `[SerializeField]` on properties (Unity serializes fields only)
- [ ] Default values set for all serialized fields

### ScriptableObject Usage
- [ ] Used for configuration data, not runtime-mutable state
- [ ] Runtime mutation uses `Instantiate()` copy, not original asset
- [ ] `[CreateAssetMenu]` attribute for easy asset creation
- [ ] Proper `OnValidate()` for Inspector-time validation
- [ ] No MonoBehaviour references in SO (scene-bound refs can't serialize to assets)

### Data Persistence
- [ ] Save/load has versioning for forward compatibility
- [ ] Deserialization handles missing/extra fields gracefully
- [ ] `PlayerPrefs` not used for sensitive data (plaintext, user-editable)
- [ ] Save data validated after load (corrupt file recovery)
- [ ] No `BinaryFormatter` (security vulnerability, deprecated)

## Scene & Prefab Management

### Scene Organization
- [ ] Scenes have clear hierarchy (Environment, Gameplay, UI, Systems)
- [ ] No "floating" GameObjects at root without clear purpose
- [ ] Scene bootstrap/initialization pattern consistent
- [ ] Additive scene loading for large content (not one mega-scene)
- [ ] Build settings scene list matches actual flow

### Prefab Best Practices
- [ ] Prefab variants used for shared-base objects
- [ ] No missing script references on prefabs
- [ ] Prefab overrides intentional and minimal
- [ ] Nested prefabs used appropriately (not > 3 levels deep)
- [ ] No direct scene object references from prefabs (use events/SO)

### Asset Organization
- [ ] Folder structure is logical and consistent
- [ ] No assets in root `Assets/` folder (organized into subfolders)
- [ ] Art, Audio, Scripts, Prefabs, Scenes in separate top-level folders
- [ ] Third-party assets isolated (Plugins/ or ThirdParty/)
- [ ] No duplicate assets (same texture/mesh imported twice)
- [ ] `.meta` files committed to version control

## Input System

- [ ] Using New Input System (not legacy `Input.GetKey`)
- [ ] InputAction assets used (not hardcoded key bindings)
- [ ] Input handling separated from gameplay logic
- [ ] Multiple control schemes supported (keyboard, gamepad, touch)
- [ ] Input rebinding support for accessibility

## Async & Coroutines

## Advanced Practices

For cross-platform implementation, advanced build configurations, and specialized patterns, see UNITY_BEST_PRACTICES-advanced.md.

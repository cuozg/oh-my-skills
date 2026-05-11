# C# Scripts (.cs) Review Checklist

Check every item against changed code. Report as severity: CRITICAL > HIGH > MEDIUM > LOW > STYLE.

### Logic
- [ ] `GetComponent<T>()` null-checked — prefer `TryGetComponent`
- [ ] Destroyed `UnityEngine.Object` checked with `== null` (NOT `is null` — Unity overloads `==`)
- [ ] Event invocation null-safe: `OnEvent?.Invoke()`
- [ ] Optional SO/prefab fields validated in `OnEnable` or `Awake`
- [ ] Empty collection guarded before indexing (`list.Count == 0` before `list[0]`)
- [ ] Loop bounds: `<` for `Length`/`Count`, not `<=`
- [ ] Float comparison uses `Mathf.Approximately`, not `==`
- [ ] Integer division truncation handled (`5 / 2 == 2`)
- [ ] Zero/negative input guarded (division, array size, timer duration)
- [ ] Enum switch has `default` case or exhaustive match
- [ ] Collection not modified during iteration (use reverse loop or `ToList()`)
- [ ] Input validated at system boundary (public methods, events, deserialized data)
- [ ] Boolean flags reset after one-shot use
- [ ] Cross-component init order documented or enforced via `[DefaultExecutionOrder]`
- [ ] Coroutine references stored for `StopCoroutine` cleanup

### Unity Lifecycle
- [ ] No `FindObjectOfType` / cross-object `GetComponent` in `Awake` (target may not exist yet)
- [ ] `OnEnable` does not assume `Start` has run
- [ ] `OnDisable` guards: check `gameObject.scene.isLoaded` (fires during scene unload too)
- [ ] `DontDestroyOnLoad` has duplicate instance check
- [ ] Every `+=` on event/delegate has matching `-=` in `OnDisable` or `OnDestroy`
- [ ] `public event` fields nulled in `OnDestroy` if object can be destroyed at runtime
- [ ] Every `StartCoroutine()` has matching `StopCoroutine()` / `StopAllCoroutines()` in `OnDisable`/`OnDestroy`
- [ ] Every `InvokeRepeating()` has matching `CancelInvoke()` on lifecycle exit
- [ ] `Destroy()` is end-of-frame — object still accessible this frame (don't re-check same frame)
- [ ] `DestroyImmediate()` used only in Editor scripts, never runtime
- [ ] Coroutines stop on `SetActive(false)` — won't auto-resume on re-enable
- [ ] Static references cleared on scene unload
- [ ] Additive scene objects explicitly unloaded

### Serialization
- [ ] Renamed field has `[FormerlySerializedAs("oldName")]` — never remove this attribute
- [ ] Type change reviewed: `float→int` truncates, `List→Array` loses data, cross-type = migration needed
- [ ] New field on existing prefab/SO — verify default value is safe
- [ ] Custom classes have `[System.Serializable]`
- [ ] Private inspector fields use `[SerializeField]`
- [ ] `Dictionary<K,V>` not natively serializable — use `List` pairs or custom wrapper
- [ ] Enum values explicit: `Sword = 0, Shield = 1` (insertion shifts indices, breaks saved data)
- [ ] Runtime-mutated SO data cloned via `Instantiate(so)` (shared state persists in build)
- [ ] SO assets in builds are readable — no secrets in SO fields

### Performance
- [ ] No LINQ in Update (`Where`, `Select`, `ToList` allocate)
- [ ] No string concat in hot loops — use `StringBuilder` or cached formatting
- [ ] No lambda captures that allocate delegate state per frame
- [ ] No `new List<T>()` per frame — reuse with `.Clear()`
- [ ] No boxing through `object` params or interface calls in hot paths
- [ ] No repeated `ToString()` on value types in hot paths
- [ ] `GetComponent<T>()` cached in `Awake`/`Start`, not called per frame
- [ ] No `Find("name")` / `FindObjectOfType<T>()` in hot paths — cache or inject
- [ ] `CompareTag("tag")` used instead of `gameObject.tag == "tag"`
- [ ] `Physics.Raycast` uses `layerMask`
- [ ] `NonAlloc` variants in hot loops: `RaycastNonAlloc`, `OverlapSphereNonAlloc`
- [ ] Rigidbody manipulation in `FixedUpdate`, not `Update`
- [ ] Static colliders not moved at runtime (triggers rebuild)
- [ ] No `Renderer.material` in gameplay loops (creates instance) — use `sharedMaterial` or `MaterialPropertyBlock`
- [ ] Object pooling for frequent spawn/despawn cycles
- [ ] Addressable handles released after use
- [ ] Canvas split: static vs dynamic UI when rebuild cost matters

### Security
- [ ] User text input length-capped
- [ ] Numeric inputs clamped (`Mathf.Clamp`)
- [ ] File paths sanitized — no `..` traversal
- [ ] Deserialized data validated before use (don't trust save files)
- [ ] Player names stripped of rich text / HTML tags
- [ ] No API keys / tokens in client code — use server proxy
- [ ] No secrets in `PlayerPrefs` (plain text, easily edited)
- [ ] No secrets in ScriptableObject fields (readable in builds)
- [ ] Save file integrity: hash or HMAC to detect tampering
- [ ] Debug panels behind `#if UNITY_EDITOR || DEVELOPMENT_BUILD`
- [ ] Cheat commands stripped from release builds
- [ ] `Debug.Log` stripped or conditional-compiled in production
- [ ] Test scenes excluded from build settings
- [ ] Server authoritative — client sends intent, server validates
- [ ] No client-side trust for damage, currency, position
- [ ] All communication over HTTPS/TLS
- [ ] SQL queries parameterized
- [ ] Rate limiting on client actions

### Concurrency
- [ ] ALL Unity API calls on main thread (`Transform`, `GameObject`, `Component`)
- [ ] Background work returns plain data, then dispatches to main thread for scene changes
- [ ] No `async void` except Unity event handlers — use `async UniTask` or `async Task`
- [ ] `CancellationToken` passed through (use `destroyCancellationToken` in 2022+)
- [ ] No `await` in `OnDestroy` without cancellation guard (object may be mid-destroy)
- [ ] Exception handling: `async void` swallows exceptions silently
- [ ] No Unity object access after `Awaitable.BackgroundThreadAsync()`
- [ ] `destroyCancellationToken` or lifetime token forwarded through long-lived async methods
- [ ] Same `Awaitable` instance not awaited multiple times

### Architecture
- [ ] MonoBehaviour handles Unity lifecycle only — business logic in plain C# classes
- [ ] ECS systems separate authoring, data components, and stateless processing logic
- [ ] No God objects (one class doing input + UI + save + audio) — split at ~300 lines
- [ ] Dependencies flow inward: UI → Logic → Data (inner layers never reference outer)
- [ ] No `FindObjectOfType` for runtime wiring — inject or use SO events
- [ ] No circular references between classes or assemblies
- [ ] Editor code in Editor assembly (won't ship in build)
- [ ] No deep inheritance (>2 levels) — prefer composition

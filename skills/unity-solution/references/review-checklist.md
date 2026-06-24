# Unity Solution Review Checklist

Use this rubric to evaluate a user-supplied Unity solution (Mode B). For each dimension, gather
evidence first, then classify findings:

- ✅ **Pass** — solid; no action needed.
- 🟡 **Concern (medium)** — should be addressed; non-blocking.
- 🟠 **Concern (high)** — should be addressed before / during implementation.
- 🔴 **Block** — must change before implementation; solution as-is will fail.
- ❓ **Unknown** — needs investigation; not yet a problem.

Every finding must cite evidence: `<file:line>`, Unity doc URL, package doc, project setting, or
observed pattern. No evidence → not a finding.

---

## 1. Correctness

Does the solution actually solve the stated problem? Are edge cases handled?

- [ ] **Solves the stated goal** — match the user's success criteria to the proposed behavior.
- [ ] **Edge cases enumerated** — null inputs, empty collections, missing references, off-by-one,
      first-frame, last-frame, scene reload, domain reload.
- [ ] **Concurrency / timing** — `Update` vs `FixedUpdate`, `Time.deltaTime` vs `Time.fixedDeltaTime`,
      `Time.unscaledDeltaTime` for UI, async/await in Unity contexts.
- [ ] **State transitions** — initial state, terminal state, invalid state, recovery.
- [ ] **Determinism** — if relevant (replays, networked, AI), is behavior reproducible?
- [ ] **Undo / cancel** — can the user abort? Can the system roll back?

---

## 2. Unity Fit

Uses Unity APIs, packages, and patterns idiomatically? Avoids reinventing wheels?

- [ ] **Built-in first** — uses Unity-provided systems before custom code (input system, physics,
      animation, UI Toolkit, navigation, audio mixer, render pipeline).
- [ ] **Packages vs custom** — official UPM packages preferred over third-party or homegrown when
      the official package is mature (Addressables, Cinemachine, Input System, Localization, etc.).
- [ ] **Engine patterns respected** — `MonoBehaviour`, `ScriptableObject`, `ScriptableSingleton`,
      `EditorWindow`, `PropertyDrawer`, `[SerializeField]`, `[CreateAssetMenu]` used idiomatically.
- [ ] **Reinvented wheel** — custom event bus when UnityEvents suffice; custom DI when Zenject is
      already in the project; custom serializer when JsonUtility / Newtonsoft fits.
- [ ] **Render pipeline match** — URP/HDRP/Built-in — solution doesn't assume one when project uses
      another.
- [ ] **Platform APIs** — uses `#if UNITY_IOS / UNITY_ANDROID / UNITY_WEBGL` correctly; not just
      `#if UNITY_EDITOR`.

---

## 3. Performance

GC, allocations, draw calls, physics, loading, mobile/WebGL limits considered?

- [ ] **Allocation hotspots** — `new` in `Update`, LINQ in hot paths, string concatenation,
      boxing, `Find` / `GetComponent` in hot paths.
- [ ] **GC pressure** — frequent small allocations vs pooled / cached references.
- [ ] **Physics cost** — `Rigidbody` per object when compound colliders suffice, raycasts in
      `Update`, `OnTriggerStay` misuse.
- [ ] **Rendering cost** — material instances, shader variants, overdraw, transparency, dynamic
      batching breaks (different materials, multi-pass shaders).
- [ ] **Loading cost** — synchronous loads on startup, Addressables not released, missing async
      loading, scene additive vs single.
- [ ] **Platform ceilings** — mobile fillrate, WebGL memory cap, IL2CPP vs Mono, texture
      compression format per platform.
- [ ] **Profiler-aware** — would the author know if this regressed? (counters, markers, custom
      sampler.)

---

## 4. Lifecycle & Safety

Awake/Start/OnEnable/OnDisable/OnDestroy, scene transitions, domain reload, hot reload,
Addressables release, event subscriptions, IDisposable.

- [ ] **Subscription lifecycle** — every `+=` has a matching `-=`; subscriptions cleared in
      `OnDisable` / `OnDestroy`, not `OnApplicationQuit`.
- [ ] **Addressables lifecycle** — `LoadAssetAsync` has matching `Release`; reference counting
      understood; no leaks across scene reloads.
- [ ] **Domain reload** — static state, `RuntimeInitializeOnLoadMethod` attributes, `[SerializeField]`
      vs static, ScriptableObject reload.
- [ ] **Scene transitions** — DontDestroyOnLoad use justified; `SceneManager.sceneLoaded` cleanup.
- [ ] **Async cancellation** — CancellationTokenSource disposed; async ops not orphaned across
      scene unload.
- [ ] **Null safety** — `[SerializeField]` references checked; `OnValidate` validates; defensive
      nulls only where unavoidable.
- [ ] **Dispose pattern** — `IDisposable` implemented when owning unmanaged / pooled / native
      resources.
- [ ] **PlayerLoop hooks** — `PlayerLoopSystem` insertions cleaned up; coroutines not orphaned.

---

## 5. Architecture

Separation of concerns, testability, designer workflow, ScriptableObject use, assembly
definitions, dependency direction.

- [ ] **Single responsibility** — MonoBehaviours are thin orchestrators; logic in plain C# or
      ScriptableObjects.
- [ ] **Testability** — game logic separable from Unity APIs (interfaces, plain classes); can be
      unit-tested in EditMode without scene.
- [ ] **Designer workflow** — non-programmers can configure via Inspector, ScriptableObjects, or
      custom editors; not hardcoded in code.
- [ ] **Dependency direction** — gameplay → data, not data → gameplay; assembly definitions enforce
      boundaries.
- [ ] **Asmdef coverage** — feature lives in its own assembly definition; test assembly separated.
- [ ] **Naming & conventions** — matches `unity-standards` (PascalCase, namespaces, folders).
- [ ] **Decoupling** — direct references avoided; events / interfaces / ScriptableObject events
      used where multiple systems must react.

---

## 6. Risk & Migration

Breaking changes, package compatibility, platform-specific behavior, rollback plan.

- [ ] **Package version pins** — `packages.json` / `Packages/manifest.json` constraints stated;
      breaking changes between versions called out.
- [ ] **Engine version compatibility** — Unity 2022 LTS vs 6 / Unity 6 vs future — APIs valid for
      target version.
- [ ] **Platform-specific behavior** — iOS / Android / WebGL / console quirks called out.
- [ ] **Rollback plan** — can this change be reverted cleanly? Is the previous state preserved?
- [ ] **Data migration** — serialized data format changes; versioning in save data / ScriptableObject.
- [ ] **Asset import impact** — texture reimport, shader recompile, GUID conflicts, meta-file churn.
- [ ] **Build pipeline impact** — build time, build size, link time, IL2CPP code stripping.

---

## 7. Standards Compliance

Read `unity-standards` and check code / prefab / asset / shader / test patterns.

- [ ] **Code standards** — naming, file header, `using` order, brace style, XML doc on public API,
      regions avoided.
- [ ] **Asset standards** — naming conventions, folder layout, addressable groups, atlas policy.
- [ ] **Prefab standards** — variant usage, nested prefab depth, override hygiene.
- [ ] **Material / shader standards** — SRP-batcher compatible (URP), shared materials, no
      runtime `material` clones.
- [ ] **UI standards** — Canvas scaler, CanvasRenderer pooling, UI Toolkit vs UGUI choice justified.
- [ ] **Test standards** — EditMode for pure logic, PlayMode for scene-bound; AAA / Given-When-Then.
- [ ] **Logging standards** — structured Debug.Log; not `print`; `[ContextMenu]` for designer debug.
- [ ] **Optimization standards** — `Profiler.BeginSample`, `ProfilerMarker`, no per-frame allocs in
      hot paths.

---

## Severity Heuristics

Use these to assign severity consistently:

| Severity | Meaning | Examples |
|---|---|---|
| 🔴 Block | Will fail or corrupt; must change | Wrong render pipeline API; missing unsubscription that crashes; data loss on quit |
| 🟠 High | Will cause user-visible bug or technical debt | GC spike in Update; lifecycle leak across scenes; tight coupling that blocks testability |
| 🟡 Medium | Should fix; can ship but degrades | Magic strings instead of constants; missing `[Tooltip]`; no `[ContextMenu]` for designer |
| 🔵 Low | Polish; doesn't affect correctness | Naming nit; missing XML doc; comment could be clearer |

---

## Anti-Patterns to Flag

These are common mistakes — flag as 🟠 or 🔴 depending on context:

- ❌ **Singleton abuse** — global state without lifecycle; couples systems; blocks testability.
- ❌ **Coroutine for async** — `StartCoroutine` for non-Unity async (use `UniTask` / `async`).
- ❌ **Find / GetComponent in hot paths** — `Update`, `FixedUpdate`, `OnTriggerStay`.
- ❌ **Public fields on MonoBehaviour** — should be `[SerializeField] private`.
- ❌ **Material instantiation** — `renderer.material` clones per-instance, breaks batching.
- ❌ **String-based lookups** — `Find("Player")`, `SendMessage("Method")`, tag strings.
- ❌ **Update polling** — `Update` checking `Input.GetKeyDown` instead of Input System actions.
- ❌ **Object.Destroy on DontDestroyOnLoad chain** — destroys persistent system by accident.
- ❌ **Static event with no clear owner** — memory leak + ordering bugs.
- ❌ **Missing null check on SerializeField** — Inspector forgets to assign; runtime NRE.
- ❌ **Layer / tag string magic** — string vs `LayerMask.NameToLayer` / `[Layer]` attribute.
- ❌ **Hardcoded time** — `Time.deltaTime * 5f` magic; use ScriptableObject config.
- ❌ **Async void** — unobservable async errors; use UniTask or async Task.
- ❌ **Mesh / Texture leak** — `new Texture2D` without `Destroy`; `Mesh` not released.

---

## Output Discipline

When using this checklist in Mode B:

1. **Don't dump the whole checklist.** Apply only dimensions relevant to the solution.
2. **Lead with verdict.** The 7 dimensions support the verdict, not replace it.
3. **Group, don't scatter.** All correctness findings together, all performance findings together.
4. **Cite evidence inline.** `// ── REVIEW` style is for code; here it's `<file:line>` and doc URLs.
5. **Propose alternatives, not just complaints.** For every 🟠 or 🔴, give a `current → proposed`.
6. **Mark unknowns separately.** Don't promote an unknown to a risk without investigation.
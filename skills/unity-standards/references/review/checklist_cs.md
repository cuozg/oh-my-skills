# C# Scripts (.cs) Review Checklist

Use this for Unity C# review. Start from changed lines, then inspect nearby
lifecycle, serialization, and data-flow context only when needed. Report only
actionable issues with concrete behavior, build, data-loss, security, or
maintainability impact.

Severity: CRITICAL > HIGH > MEDIUM > LOW > STYLE.

## Review Procedure

1. Identify the changed behavior and the runtime/editor surface it touches.
2. Check lifecycle, serialization, performance, and security only where relevant.
3. Prefer project conventions over generic advice.
4. For each finding, include file/line, user impact, and minimal fix.
5. Do not report speculative rewrites, style-only preferences, or pre-existing
   issues unless the change makes them worse.

### Logic

- [ ] Required component references are validated or guaranteed by `[RequireComponent]`.
- [ ] Destroyed `UnityEngine.Object` references use Unity null checks (`== null`), not `is null`.
- [ ] Events are invoked safely and payloads do not expose mutable internal state.
- [ ] Collections are checked before indexing and are not modified during unsafe iteration.
- [ ] Numeric inputs that affect timers, array sizes, division, currency, health, or physics are clamped or rejected.
- [ ] Float equality is intentional; otherwise use tolerances, ranges, or squared-distance comparisons.
- [ ] Enum/switch handling is exhaustive or has a safe fallback.
- [ ] One-shot flags, timers, and state transitions reset on all relevant paths.
- [ ] Public APIs, deserialized data, save data, remote config, and server payloads are validated before use.
- [ ] Cross-component initialization order is explicit through references, bootstrap code, or documented execution order.

### Unity Lifecycle

- [ ] `Awake` handles self-setup; `Start` or a bootstrapper handles cross-object binding.
- [ ] `OnEnable` does not assume `Start` has already run.
- [ ] Event subscriptions pair `+=` and `-=` at the same lifetime (`OnEnable`/`OnDisable` or `Awake`/`OnDestroy`).
- [ ] Coroutines, invokes, tweens, async flows, input actions, and timers stop or cancel on lifecycle exit.
- [ ] `DontDestroyOnLoad` objects have duplicate-instance and stale-static handling.
- [ ] `DestroyImmediate()` is editor-only; runtime code uses `Destroy()`.
- [ ] Additive scene, pooled object, and inactive-object paths reset state deliberately.
- [ ] Async continuations do not touch destroyed Unity objects.

### Serialization

- [ ] Serialized field renames preserve data with `[FormerlySerializedAs]`.
- [ ] Serialized type changes include migration or asset/default-value review.
- [ ] New serialized fields have safe defaults for existing prefabs, scenes, and ScriptableObjects.
- [ ] Custom nested data types that need Inspector persistence are `[Serializable]`.
- [ ] Inspector data uses private `[SerializeField]` unless public mutation is an intentional API.
- [ ] Dictionary, interface, polymorphic, and `[SerializeReference]` data have proven editor and migration support.
- [ ] Enum reorder/insert changes do not break saved data or serialized asset values.
- [ ] Runtime-mutated ScriptableObject data is cloned or explicitly owned as runtime state.
- [ ] Build-readable assets do not contain secrets, credentials, or sensitive endpoints.

### Performance

- [ ] Hot paths avoid avoidable allocations: LINQ, closures, `ToList`, string formatting, boxing, and temporary collections.
- [ ] Repeated component, camera, transform, and scene lookups are cached or injected.
- [ ] Tags use `CompareTag`; distance checks use `sqrMagnitude` where exact distance is unnecessary.
- [ ] Physics queries use layer masks and `NonAlloc` variants when called frequently.
- [ ] Rigidbody and physics writes happen in `FixedUpdate` or through deliberate simulation steps.
- [ ] Runtime material changes avoid accidental `Renderer.material` instance churn in loops.
- [ ] Frequent spawn/despawn paths use the project pool and reset pooled state fully.
- [ ] Addressables, asset handles, native containers, and rented buffers are released at owner lifetime.
- [ ] UI updates avoid unnecessary layout/canvas rebuilds; text changes only when values change.

### Security

- [ ] User-entered text is length-capped and rich text/HTML is stripped where rendered.
- [ ] File paths and imported filenames prevent traversal and unsupported extensions.
- [ ] Save data, remote config, deep links, IAP payloads, and server responses are treated as untrusted.
- [ ] Client code contains no API keys, service credentials, private signing keys, or auth tokens.
- [ ] `PlayerPrefs`, ScriptableObjects, bundles, and client assets are not used for secrets.
- [ ] Currency, inventory, damage, score, and competitive state are server-authoritative when the game has a backend.
- [ ] Debug panels, cheat commands, test menus, and verbose logs are editor/development-build only.
- [ ] Network calls use HTTPS/TLS and do not log sensitive payloads.
- [ ] Backend-adjacent Unity code validates inputs before sending actions that can affect economy or player state.

### Production Ownership

- [ ] Analytics events have clear trigger timing, schema, required parameters, and duplicate/missing-event protection.
- [ ] Revenue, IAP, attribution, economy, inventory, and progression events are server-authoritative when backend support exists.
- [ ] Remote config or blueprint changes validate required fields, versions, missing-data behavior, rollback, and expired-data cleanup.
- [ ] Server API changes handle timeout, network failure, business error, retry, cancellation, and double-submit behavior.
- [ ] Risky features include observable breadcrumbs, dashboard checks, crash/error monitoring, or rollback controls.
- [ ] Store, billing, privacy, and SDK behavior is checked against current official docs when the change depends on policy or package behavior.

### Concurrency

- [ ] Unity API calls stay on the main thread unless the API explicitly supports background use.
- [ ] Background work returns plain data and dispatches scene/object changes back to the main thread.
- [ ] `async void` is limited to Unity/UI event handlers and catches/logs exceptions internally.
- [ ] Long-lived async methods accept and forward cancellation tokens.
- [ ] Await continuations check object lifetime before touching Unity objects.
- [ ] Awaitable/UniTask/Task usage matches the project's established async stack and Unity version.
- [ ] Jobs complete or chain dependencies before reading/writing/disposal.

### Architecture

- [ ] MonoBehaviours own lifecycle and scene binding; reusable rules live in testable C# types where practical.
- [ ] Dependencies flow toward stable core logic; UI, platform, SDK, and editor code stay at boundaries.
- [ ] Runtime assemblies do not reference editor-only APIs or assemblies.
- [ ] No new service locator, singleton, event bus, or DI framework usage unless it matches the existing architecture.
- [ ] Large classes and methods are flagged only when the change worsens readability or risk.
- [ ] ECS code separates authoring/baking, data components, systems, structural changes, and Burst-compatible work.
- [ ] Inheritance is intentional and shallow; composition is preferred for gameplay variation.

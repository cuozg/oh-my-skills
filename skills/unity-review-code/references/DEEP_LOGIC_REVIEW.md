# Deep Logic Review — Advanced Patterns

Beyond the shared LOGIC_REVIEW.md patterns. These require reading full file context, not just diffs.

## Control Flow Analysis

### 🔴 Critical

| Pattern | Why | What to check |
|:--------|:----|:--------------|
| Unreachable code after early return changes cleanup | Resource leak, state inconsistency | Trace all `return`/`break`/`continue` — does skipping remaining lines skip `Dispose()`, `-=`, `Release()`? |
| Conditional logic inverted (`!` misplaced) | Silent wrong behavior | Read the method name + condition together. Does `if (!isAlive)` guard match intent? |
| Exception swallowed in catch-all | Hides real bugs | `catch (Exception)` without rethrow or logging = black hole. Especially in Init/Load paths. |
| Recursive call without base case bound | Stack overflow | Check termination condition covers ALL input ranges. What if input is 0? Negative? |
| Multiple return values via out/ref with partial assignment | Caller uses uninitialized data | If method returns `false`, are all `out` params still set to safe defaults? |
| `try/finally` with `return` in both blocks | Finally return silently overrides try result | Verify no `return` in `finally`. If present, confirm override is intentional and documented. |
| `using` scope with `await` and escaped work | Resource disposed before async work finishes | Check if async continuation/task captures disposable resource after scope exit. Prefer `await using`/lifetime-safe refactor. |
| `FirstOrDefault()` on value type | `default(T)` can mean "not found" or valid value | Verify caller distinguishes not-found via `.Any()`, nullable wrapper, or sentinel check. |
| `yield return` inside `try/catch` in `foreach` iterator | Compile-time invalid pattern | Flag immediately: C# forbids `yield` in `try` with `catch`; require redesign (`try/finally` only). |
| `goto` crossing scope boundaries | Can skip initialization and break invariants | Validate labels do not jump over variable init/guards; replace with structured control flow. |
| Method with 5+ parameters | High coupling, call-site mistakes | Recommend parameter object/builder when parameters represent one concept or optional config. |
| Deep callback nesting (3+ lambdas/delegates) | Callback hell, hidden error paths | Flatten with async/await, extracted methods, or pipeline object; verify error handling at each level. |

### 🟡 Major

| Pattern | Why | What to check |
|:--------|:----|:--------------|
| Nested ternary (3+ levels) | Unreadable, easy to misread precedence | Expand to if/else or extract method |
| Boolean parameter controls branching | Caller intent unclear | Consider splitting into two methods or using enum |
| Guard clause inconsistency across overloads | Some paths validate, some don't | All public entry points should validate |
| `else if` chain without final `else` | Unhandled case | What happens when no branch matches? Is silent no-op correct? |
| Fallthrough in switch via `goto case` | Intentional? Often a bug source | Verify intent, add comment if intentional |
| `string.IsNullOrEmpty` used where whitespace is invalid too | Whitespace-only input slips through validation | Verify business rule: if whitespace is invalid, use `string.IsNullOrWhiteSpace`. |
| `as` cast used without null check | Silent null propagation to later crash | Require immediate null guard after cast or use pattern matching with `is`. |
| `is` pattern chain without exhaustive `else` | Unhandled runtime types/states | Ensure fallback path logs/handles unsupported types. |
| `Enum.Parse` on untrusted input | Throws on invalid value | Prefer `Enum.TryParse` with explicit failure branch and case-sensitivity rule. |
| Deferred LINQ chain re-enumerated | Re-executes query with changed source/state | Materialize with `.ToList()`/`.ToArray()` when iterated multiple times. |
| `Array.Sort` relied on as stable sort | Equal keys may reorder unpredictably | If stability matters, use `OrderBy(...).ThenBy(...)` or custom stable strategy. |

## State Management Deep Dive

### 🔴 Critical

| Pattern | Why | What to check |
|:--------|:----|:--------------|
| Field set in coroutine, read in Update | Race between yield and frame | Can the coroutine be mid-yield when Update reads? What value does Update see? |
| State changed without notifying observers | UI/systems show stale data | Find all subscribers — are they notified on every state mutation path? |
| Initialization order dependency between components | NullRef in Awake/Start depending on script execution order | Use `[DefaultExecutionOrder]` or move to lazy init |
| Boolean state machine (3+ bools) | 2^N possible states, most invalid | Extract enum/FSM. Check: can `isLoading=true` AND `isComplete=true`? |
| Collection exposed as public field | External code can Add/Remove/Clear without owner knowing | Return `IReadOnlyList<>` or defensive copy |
| Field initialized inline but serialized in Inspector | Inspector value overwrites code default silently | Confirm intended source of truth; document defaults in prefab/SO, not inline initializer. |
| `[HideInInspector]` on serialized field | Hidden value still persists and mutates data | Verify hidden serialized state is intentional; audit prefabs/assets for stale values. |
| ScriptableObject side effects in `OnEnable` | Runs during import/domain reload, mutates assets unexpectedly | Ensure `OnEnable` is pure/init-only or gated from import/editor mutation paths. |
| Prefab override tied to component index after reorder | Overrides can apply to wrong component | Check recent component reorder + prefab overrides; validate serialized override targets. |
| Static event declared on MonoBehaviour | Subscribers leak across scene/domain lifecycle | Enforce unsubscribe/reset strategy on scene unload/domain reload. |
| `FindObjectOfType<T>(true)` vs default overload mismatch | Includes inactive objects, changes behavior silently | Verify intended search scope and document expectation (active-only vs include inactive). |

### 🟡 Major

| Pattern | Why | What to check |
|:--------|:----|:--------------|
| Property setter with side effects | Caller may not expect side effects from assignment | Document or use explicit method instead |
| Cached value never invalidated | Stale data after source changes | Find all mutations of source — do they clear/update the cache? |
| Enum with `[Flags]` but switch uses `==` | Misses combined flags | Use `HasFlag()` or bitwise `&` |
| Static state on MonoBehaviour | Survives scene load, shared across instances | Should it reset on scene change? Use `[RuntimeInitializeOnLoadMethod]` reset? |
| Transform/position cached then parent changed | Cached world position becomes wrong | Re-cache after reparenting |
| `[SerializeField]` backing field + public property diverge | Confusing source of truth and stale reads | Verify all writes go through one path; avoid dual state (`_value` vs computed property cache). |
| `Reset()` has side effects beyond defaults | Inspector Reset triggers unintended runtime/editor behavior | Ensure `Reset()` only assigns safe defaults and no external mutations. |
| `[ExecuteInEditMode]`/`[ExecuteAlways]` writes runtime state | Editor update can permanently modify assets/scenes | Split editor/play paths and guard asset mutation with explicit checks. |
| Singleton `Instance` accessed during teardown (`OnDestroy`) | Destroy order can null/replace singleton unexpectedly | Guard access and avoid cross-singleton logic in destroy path. |
| `enabled = false` used instead of `SetActive(false)` assumption | Lifecycle/coroutine/event behavior differs | Verify intended disable scope: component-only vs whole GameObject and child hierarchy. |

## Data Flow Tracing

### 🔴 Critical

| Pattern | Why | What to check |
|:--------|:----|:--------------|
| User input flows to file path without sanitization | Path traversal | Trace from UI/network input to `File.Open`/`Resources.Load` |
| Deserialized data used without validation | Corrupted/tampered save breaks game | After `JsonUtility.FromJson`, validate ranges, null refs, enum bounds |
| Collection index from external source without bounds check | `IndexOutOfRangeException` | What if server sends index 999? What if config has wrong array size? |
| Float comparison with `==` | Floating point imprecision | Use `Mathf.Approximately` or epsilon comparison |
| Integer overflow in calculation | Wrap-around produces negative/wrong value | Check max realistic values: `count * size * price` — can it overflow int? |
| `Mathf.InverseLerp(a, b, value)` where `a == b` | Degenerate range can produce invalid normalization (`NaN`) assumptions | Guard equal endpoints before call; define fallback behavior explicitly. |
| `Vector3.Normalize()` on zero vector | Returns zero vector, not unit direction | Verify downstream code handles zero magnitude and does not assume normalized length 1. |
| Linear/gamma color space mixed usage | Wrong brightness/tint in rendering/UI | Verify conversion expectations when passing `Color` between authored data, shaders, and UI. |
| `Texture2D.GetPixels` on compressed texture | Full decompression allocates large RAM spike | Validate texture format/readability and avoid runtime full readbacks in gameplay path. |
| `AnimationCurve.Evaluate` outside key range | Extrapolation may produce unexpected values | Check `preWrapMode`/`postWrapMode` and clamp input time when needed. |
| `NavMesh.SamplePosition` with tiny `maxDistance` | Frequent silent miss and fallback logic errors | Verify radius matches gameplay scale and check return bool every call. |

### 🟡 Major

| Pattern | Why | What to check |
|:--------|:----|:--------------|
| String used as identifier (magic string) | Typo = silent failure | Extract to `const` or use `nameof()`. Grep for all usages. |
| Enum serialized as int | Adding enum values shifts all indices | Use `[JsonProperty]` with string name, or add explicit values `= 1, = 2` |
| DateTime without timezone handling | 12h offset bugs | `DateTime.UtcNow` for storage, local only for display |
| Division without zero-check | `DivideByZeroException` or `NaN`/`Infinity` | What sets the divisor? Can it ever be 0? |
| Implicit conversion loses precision | `double` → `float`, `long` → `int` silently | Check if precision loss matters for this value |
| `Mathf.Clamp` called with `min > max` | Returns wrong bound silently | Validate min/max ordering at source; assert or normalize before clamp. |
| LayerMask treated as plain int math | Wrong layers included/excluded | Ensure bit-shifts use `1 << layer` and masks built with `LayerMask.GetMask`. |
| `Quaternion.Euler` fed angles outside expected range | Works but hides upstream angle drift/confusion | Confirm angle normalization intent and source units/degrees logic. |
| `Physics.OverlapSphereNonAlloc` buffer too small | Results silently truncated | Check return count equals buffer length; resize/retry for correctness-critical queries. |
| ScriptableObject `List<T>` where `T` stores scene refs | Scene refs become null in builds/runtime instances | Replace with GUID/Addressable IDs or runtime binding step. |
| Frequent `Color32` ↔ `Color` conversion | Precision loss and subtle color drift | Keep canonical representation and convert only at boundaries. |

## Concurrency & Async Patterns

### 🔴 Critical

| Pattern | Why | What to check |
|:--------|:----|:--------------|
| Shared mutable state across async operations | Race condition | Two async methods write to same field — what interleaving produces wrong state? |
| `async void` event handler that throws | Unobserved exception crashes app | Wrap body in try/catch, log error |
| `Task.Run` accessing Unity API | Main thread only | `Transform`, `GameObject`, UI, Physics — all main thread. Use `Awaitable.MainThreadAsync()` |
| `CancellationToken` not checked in loop body | Can't cancel, runs to completion | Check `token.ThrowIfCancellationRequested()` or `token.IsCancellationRequested` |
| Multiple awaits modifying same state without lock | Interleaved execution | Between two awaits, another caller could modify the same field |
| `UniTask.WhenAll` without per-task error capture | One failure hides sibling outcomes and cancels aggregate path | Handle individual task results/exceptions before aggregate fail-fast. |
| Addressables load without release ownership tracking | Handle leak and memory growth over long sessions | Track owner + release path (`OnDisable`/`OnDestroy`/scene unload). |
| `AsyncOperationHandle` stored but never released | Native/resource leak | Verify every stored handle has deterministic `Addressables.Release`. |
| `UnityWebRequest` not disposed | Native handle/socket leak | Use `using`/`Dispose()` on every request path (success, fail, cancel). |
| Additive scene loads without unload plan | Duplicate objects and memory leak over session | Verify matching `UnloadSceneAsync` and ownership of loaded scenes. |
| `Resources.UnloadUnusedAssets()` called during gameplay loop | Large stall + GC spike | Restrict to loading screens or controlled transition windows. |

### 🟡 Major

| Pattern | Why | What to check |
|:--------|:----|:--------------|
| Fire-and-forget async without error handling | Silent failures | Use `UniTask.Forget(e => Debug.LogException(e))` or similar |
| Coroutine and async mixed for same operation | Confusing lifetime management | Pick one paradigm. Coroutine if simple, async if complex |
| Lock held across `await` | Deadlock risk (Monitor/lock not async-safe) | Use `SemaphoreSlim` instead |
| Event fired during iteration of subscriber list | `InvalidOperationException` if subscriber modifies list | Copy list before invoking, or use `event` keyword (safe) |
| `Task.Delay` used for gameplay timing | Ignores `Time.timeScale` and play mode timing semantics | Use `Awaitable.WaitForSecondsAsync`/`UniTask.Delay` with explicit timing mode. |
| `ConfigureAwait(false)` in Unity flow | Continuation may resume off main thread | Ensure post-await Unity API usage returns to main thread explicitly. |
| Multiple `LoadSceneAsync` without activation coordination | Scene activation races and broken transition UX | Coordinate `allowSceneActivation` and loading state machine. |
| Addressables `InstantiateAsync` without ownership tracking | Spawned objects orphaned and hard to clean up | Track instance handles/parents and release on scene/object teardown. |

## Unity-Specific Gotchas

### 🔴 Critical

| Pattern | Why | What to check |
|:--------|:----|:--------------|
| `Application.isPlaying` used incorrectly in editor code paths | False in edit-time operations; guards can misfire | In `#if UNITY_EDITOR` flows, verify edit-mode + play-mode checks are explicit and correct. |
| Missing `EditorApplication.isPlayingOrWillChangePlaymode` check before asset mutation | Asset changes can happen during playmode transition | Guard editor-time writes when entering/exiting play mode. |
| `[InitializeOnLoadMethod]` depends on runtime-only APIs | Editor init crashes or build/runtime coupling issues | Ensure method only references editor-safe APIs and no runtime scene assumptions. |
| `AssetDatabase` called from runtime assembly path | Build/runtime failures outside editor | Require `#if UNITY_EDITOR` guards and assembly split when needed. |
| `PrefabUtility` usage during play mode | Unexpected prefab edits/state drift | Verify calls are editor-tooling only and gated from play mode operations. |

### 🟡 Major

| Pattern | Why | What to check |
|:--------|:----|:--------------|
| `[Conditional("UNITY_EDITOR")]` on method with return expectation | Call site still compiles but return behavior is misleading | Avoid conditional attribute on value-returning API used by runtime logic. |
| `Debug.Assert` condition has side effects | Assert removed in build, side effects still alter logic flow | Ensure assert expressions are pure and side-effect free. |
| Multiple `[RuntimeInitializeOnLoadMethod]` relying on order | Initialization race between systems | Add explicit bootstrap ordering strategy instead of implicit attribute order. |
| Platform code uses only `#if UNITY_ANDROID` fallback | Other platforms unintentionally excluded/misconfigured | Use full `#if/#elif/#else` chain for all supported targets. |
| `Screen.orientation` set without autorotate flags | Orientation lock behaves inconsistently per device | Verify `Screen.autorotateTo...` flags align with orientation policy. |
| Optional feature used without `SystemInfo.supportsXxx` gate | Runtime failures on unsupported hardware | Guard usage and provide fallback path. |
| `QualitySettings` accessed by index | Reordered quality levels break behavior | Resolve by quality name mapping or config abstraction, not hard-coded index. |

## Edge Case Checklist

Run this against EVERY changed method:

| Question | If Yes → |
|:---------|:---------|
| What if this is called with null? | Add guard or document `[NotNull]` contract |
| What if the collection is empty? | Check `.Count`/`.Any()` before `.First()`/`[0]` |
| What if this is called twice? | Is it idempotent? Does double-subscribe happen? |
| What if this is called before Init? | Add initialization guard or lazy init |
| What if this is called after Destroy? | Check `this != null` / `isActiveAndEnabled` |
| What if the value is negative? | Check unsigned assumption, add `Mathf.Max(0, ...)` |
| What if the value is MAX_INT? | Check overflow in arithmetic |
| What if two of these run concurrently? | Check shared state, add synchronization if needed |
| What if the network/file operation fails? | Check error handling path exists |
| What if the referenced object was destroyed? | Check for null/MissingReferenceException |

## Investigation Commands

```bash
# Trace all callers of a method
grep -rn "MethodName\s*(" Assets/Scripts/ --include="*.cs"

# Find all state mutations of a field
grep -rn "_fieldName\s*=" Assets/Scripts/ --include="*.cs"

# Find all subscribers to an event
grep -rn "EventName\s*[+-]=" Assets/Scripts/ --include="*.cs"

# Check for catch-all exception handlers
grep -rn "catch\s*(Exception" Assets/Scripts/ --include="*.cs"

# Find async void methods (non-event)
grep -rn "async\s\+void\s\+[^O]" Assets/Scripts/ --include="*.cs"

# Find float equality comparisons
grep -rn "==\s*[0-9]*\.[0-9]" Assets/Scripts/ --include="*.cs"

# Find division operations (check for zero guards)
grep -rn "[^/]/[^/\*=]" Assets/Scripts/ --include="*.cs"
```

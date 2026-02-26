# Logic Review Patterns — Unity C# (Part 3)

Advanced patterns: Data Flow, Concurrency & Async, UI-Specific, Networking, and Unity Gotchas.

---

## 7. Data Flow

### 7.1 Critical

| Pattern | Why | What to check |
|:--------|:----|:--------------|
| User input flows to file path without sanitization | Path traversal | Trace from UI/network input to `File.Open`/`Resources.Load` |
| Deserialized data used without validation | Corrupted/tampered save breaks game | After `JsonUtility.FromJson`, validate ranges, null refs, enum bounds |
| Collection index from external source without bounds check | `IndexOutOfRangeException` | What if server sends index 999? What if config has wrong array size? |
| Float comparison with `==` | Floating point imprecision | Use `Mathf.Approximately` or epsilon comparison |
| Integer overflow in calculation | Wrap-around produces negative/wrong value | Check max realistic values: `count * size * price` — can it overflow int? |
| `Mathf.InverseLerp(a, b, value)` where `a == b` | Degenerate range can produce `NaN` | Guard equal endpoints before call; define fallback behavior explicitly. |
| `Vector3.Normalize()` on zero vector | Returns zero vector, not unit direction | Verify downstream code handles zero magnitude and does not assume normalized length 1. |
| Linear/gamma color space mixed usage | Wrong brightness/tint in rendering/UI | Verify conversion expectations when passing `Color` between authored data, shaders, and UI. |
| `Texture2D.GetPixels` on compressed texture | Full decompression allocates large RAM spike | Validate texture format/readability and avoid runtime full readbacks in gameplay path. |
| `AnimationCurve.Evaluate` outside key range | Extrapolation may produce unexpected values | Check `preWrapMode`/`postWrapMode` and clamp input time when needed. |
| `NavMesh.SamplePosition` with tiny `maxDistance` | Frequent silent miss and fallback logic errors | Verify radius matches gameplay scale and check return bool every call. |

### 7.2 Major

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

---

## 8. Concurrency & Async (Advanced)

### 8.1 Critical

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

### 8.2 Major

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

---

<!-- See also: logic-review-patterns-advanced-ui-networking.md (Sections 9-11) and logic-review-patterns-advanced-edge-cases.md (Sections 12-13) -->
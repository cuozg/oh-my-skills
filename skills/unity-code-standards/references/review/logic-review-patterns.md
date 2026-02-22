# Logic Review Patterns — Unity C# (Part 1)

Load when reviewing, writing, or refactoring `.cs` files. Covers standard patterns — Part 1 covers Unity performance and async/lifecycle patterns.

---

## 1. Unity Performance

### 1.1 Critical

| Pattern | Why | Fix |
|:--------|:----|:----|
| `GetComponent` in Update/FixedUpdate | O(n) per frame | Cache in Awake |
| `Camera.main` in loop | FindWithTag each access | Cache in Awake |
| `Find()`/`FindObjectOfType()` runtime | O(n) traversal | `[SerializeField]` inject |
| `Instantiate`/`Destroy` spam | GC spikes | Object pool |
| String concat / LINQ / `new List` in Update | Per-frame alloc | Pre-allocate, `NonAlloc` |
| `foreach` on non-cached collection in Update | Iterator alloc (older Mono) | Cache or use `for` loop |
| `Physics.Raycast` without layer mask | Checks all colliders/layers | Use explicit `LayerMask` |
| `string.Format` / string interpolation in hot paths | Per-frame alloc + boxing | Cache formatters or use `StringBuilder` |
| `if (obj)` on `UnityEngine.Object` | Unity fake-null semantic mismatch | Use explicit `obj != null`/`obj == null` checks intentionally |
| `Resources.Load` repeatedly at runtime | Sync load + repeated I/O | Cache loaded assets or move to Addressables |
| `Texture2D.Apply()` called multiple times per batch | Re-uploads texture to GPU each call | Batch pixel changes, call `Apply()` once |
| `SendMessage`/`BroadcastMessage` | Reflection dispatch + no compile-time safety | Direct calls, interfaces, or event bus |
| `OnGUI` in runtime gameplay path | IMGUI runs/rebuilds every frame | Move to uGUI/UI Toolkit or editor-only |
| `yield return new WaitForEndOfFrame` in WebGL flow | Can hang on browser frame timing edge cases | Use `yield return null`/other safe yield strategy |
| `Animator.SetTrigger("Name")` string every call | Hash lookup/string typo risk | Cache `Animator.StringToHash` IDs |
| Large `switch` on animation state names (strings) | String compare cost + typo risk | Compare hashed state IDs |
| `Material.SetFloat/SetColor("Prop")` in Update | Per-call property name lookup | Cache `Shader.PropertyToID` |

---

## 2. Async & Lifecycle

### 2.1 Critical

| Pattern | Why | Fix |
|:--------|:----|:----|
| `this`/`gameObject` after `await` no null check | MissingRef | `if (this == null) return;` |
| `StartCoroutine` without stop in OnDisable | Runs after destroy | Store handle, stop in OnDisable |
| `+=` without `-=` in OnDisable | Event leak | OnEnable/OnDisable pair |
| `async void` on non-Unity-event | Swallowed exceptions | `async Task` / `async UniTask` |
| Missing `CancellationToken` on long-running async | Can't cancel on destroy | Pass `destroyCancellationToken` (Unity 6) or manual CTS |
| `await` without `try/catch` in fire-and-forget | Unobserved exception crash | Wrap or use UniTask `.Forget()` with error handler |
| Coroutine yields `new WaitForSeconds` each frame | GC per yield | Cache `WaitForSeconds` instance |
| `OnDestroy` accesses other components/singletons | Destroy order undefined during teardown | Guard null and avoid cross-object logic in destroy path |
| `DontDestroyOnLoad` without singleton guard | Duplicate persistent instances across scenes | Add instance guard + duplicate self-destroy |
| `SceneManager.sceneLoaded +=` without unsubscribe | Handler leak and duplicate callbacks | Unsubscribe in OnDisable/OnDestroy |
| `Addressables.LoadAssetAsync` without release ownership tracking | Addressable handle leak | Track handles and call `Addressables.Release` |
| `UnityWebRequest` not disposed | Native memory/socket leak risk | Use `using var req = ...` or explicit `Dispose()` |
| Coroutine continues after owner destroy/disable | MissingReference/null access | Guard with `isActiveAndEnabled` and stop on disable |
| `Time.deltaTime` in `FixedUpdate` | Physics step mismatch | Use `Time.fixedDeltaTime` |
| `Application.targetFrameRate` set ignoring vSync | Conflicting frame pacing settings | Set with explicit `QualitySettings.vSyncCount` strategy |

**Lifecycle order:** Awake(self) → OnEnable(subscribe) → Start(cross-component) → OnDisable(unsubscribe) → OnDestroy(cleanup)

### 2.2 Critical — General

Breaking API change, NullRef without guard, memory leak (undisposed resources/events), data corruption (serialization change without migration), race conditions, hardcoded secrets.

---

## Investigation Commands (Part 1)

```bash
# Callers of a method
grep -rn "MethodName\s*(" Assets/Scripts/ --include="*.cs"

# Event subscribers
grep -rn "EventName\s*[+-]=" Assets/Scripts/ --include="*.cs"

# Async void methods (non-event)
grep -rn "async\s\+void\s\+[^O]" Assets/Scripts/ --include="*.cs"

# Float equality comparisons
grep -rn "==\s*[0-9]*\.[0-9]" Assets/Scripts/ --include="*.cs"
```

Continue reading in **logic-review-patterns-intermediate.md** for Serialization, Control Flow, Logic, and State Management patterns. See **logic-review-patterns-advanced.md** for Data Flow, Concurrency, UI, Networking, Unity Gotchas, Edge Cases.

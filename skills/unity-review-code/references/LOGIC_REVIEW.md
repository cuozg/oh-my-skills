# Logic Review — C# Files

Load when PR modifies `.cs` files.

## 🔴 Critical — Unity Performance

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

## 🔴 Critical — Async & Lifecycle

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

Lifecycle: Awake(self) → OnEnable(subscribe) → Start(cross-component) → OnDisable(unsubscribe) → OnDestroy(cleanup)

## 🔴 Critical — General

Breaking API change, NullRef without guard, memory leak (undisposed resources/events), data corruption (serialization change without migration), race conditions, hardcoded secrets.

## 🔴 Critical — Serialization & Data

| Pattern | Why | Fix |
|:--------|:----|:----|
| `[SerializeField]` applied to property | Unity serializes fields, not C# properties | Convert to backing field serialization |
| Public field should not persist but lacks `[NonSerialized]`/`[System.NonSerialized]` | Unintended state persistence across saves/domain reload | Mark non-persistent fields explicitly |
| Interface/abstract type serialized with default Unity serializer | Unity cannot serialize most interface/abstract field data | Use concrete type, custom serializer, or `[SerializeReference]` with constraints |
| `[SerializeReference]` used without migration/type-stability plan | Type rename/move breaks polymorphic payloads | Add stable type strategy and migration handling |
| ScriptableObject asset mutated directly at runtime | Shared project asset state corruption | `Instantiate()` runtime copy before mutation |
| `JsonUtility.FromJson` on Unity object graph expecting references | Object references not restored in plain JSON load | Use ID-based remap/custom serialization layer |

## 🟡 Major — Logic Patterns

| Pattern | Fix |
|:--------|:----|
| Field renamed without `[FormerlySerializedAs]` | Add attribute |
| DOTween not killed in OnDisable | `_tween?.Kill()` |
| Cross-component access in Awake | Move to Start |
| SO mutated runtime without clone | `Instantiate(configSO)` |
| Physics calls in Update | Move to FixedUpdate |
| `private` → `public` on SerializeField | Keep private, add property |
| Nullable type without null-check before use | Add guard clause or `?.` operator |
| `switch` on enum without `default` case | Add `default` with warning log |
| Mutable static field on MonoBehaviour | Race condition across scenes — use SO or singleton pattern |
| Public field where property needed | Encapsulate: `[field: SerializeField] public int Hp { get; private set; }` |
| `Mathf.Lerp(current, target, Time.deltaTime)` used as smoothing | Never reaches target predictably, frame-rate dependent | Use damp/speed-based interpolation (`MoveTowards`, exponential decay with tuned factor) |
| `Vector3 == Vector3` for precision checks | Float equality unstable | Compare `(a - b).sqrMagnitude < epsilon` |
| `Quaternion == Quaternion` for orientation checks | Float equality unstable | Use `Quaternion.Angle(a, b) < threshold` |
| `transform.position += ...` in FixedUpdate on Rigidbody object | Bypasses physics solver/interpolation | Use `Rigidbody.MovePosition`/forces in FixedUpdate |
| `Rigidbody.MovePosition` called from Update | Desync with physics timestep | Move to FixedUpdate |
| `gameObject.tag == "..."` comparisons | Slower/string-based and typo-prone | Use `CompareTag("...")` |
| Incorrect layer-mask bit math (`1 << layer` misuse) | Wrong collision/query filter | Validate with `LayerMask.GetMask` or precomputed mask constants |
| `Debug.DrawRay` endpoint passed as direction | Visual debug lies about actual cast | Pass direction * length, not endpoint |
| `Invoke`/`InvokeRepeating("Method")` string API | No compile-time safety/rename breakage | Replace with coroutine/timer + direct delegate |
| `PlayerPrefs` stores sensitive tokens/PII | Plaintext, user-editable storage | Use secure storage/encryption strategy |
| Misread `Random.Range` bounds (`int` max exclusive, `float` max inclusive) | Off-by-one and spawn distribution bugs | Apply correct overload semantics explicitly |

## 🟡 Major — State & Data

| Pattern | Fix |
|:--------|:----|
| Bool flags for state management (3+ bools) | Extract state machine / enum |
| Collection modified during enumeration | Copy or use removal list |
| Dictionary lookup without `TryGetValue` | Replace `ContainsKey` + index with `TryGetValue` |
| `List.Find()` / `FirstOrDefault()` in hot path | Use Dictionary or HashSet for O(1) lookup |
| Enum changed without updating all `switch` statements | Grep all switch/if-chains for that enum |
| `[Serializable]` class with no default constructor | Deserialization will fail silently |

## 🟡 Major — UI-Specific

| Pattern | Fix |
|:--------|:----|
| Canvas dirtied/rebuilt every frame (SetDirty/text/layout toggles) | Batch updates and avoid per-frame UI mutations |
| Deeply nested LayoutGroups causing cascade recalculation | Flatten hierarchy, minimize nested layout groups |
| Frequent UI enable/disable toggles for visibility | Use `CanvasGroup` alpha/interactable/blockRaycasts where possible |
| ScrollRect with large dataset and no virtualization | Implement item pooling/virtualized list |
| Text/TMP content updated each frame without need | Update only on value change, throttle refresh |
| Decorative Images keep `raycastTarget=true` | Disable raycast target on non-interactive graphics |
| Multiple `GraphicRaycaster` components on nested canvases | Keep only required raycasters to reduce UI input overhead |

## 🟡 Major — Networking

Apply when networking/web request code is modified.

| Pattern | Fix |
|:--------|:----|
| `UnityWebRequest` without timeout | Set `timeout` or equivalent cancellation policy |
| JSON parse without error handling | Wrap parse in `try/catch` with fallback/error path |
| Network calls without retry/backoff strategy | Add bounded retry with jitter/backoff |
| Missing `Content-Type`/accept headers for payload APIs | Set explicit headers matching backend contract |
| Deprecated `isNetworkError`/`isHttpError` checks only | Use `UnityWebRequest.result` + status code handling |
| Large payloads sent uncompressed | Enable/request compression and chunk strategy where supported |

## 🔵 Minor

Magic numbers, Debug.Log without `#if UNITY_EDITOR`, empty Update/Start, dead code, naming violations, nesting 4+, missing XML docs on public API, `#region` blocks (remove — use partial classes or extract), unnecessary `this.` qualifier.

## Suggestion Quality — DO / DON'T

**DO**: Provide exact replacement code in ` ```suggestion ``` `. One issue per comment. Show evidence (caller count, file:line). Explain *why*, not just *what*.

**DON'T**: Combine multiple fixes in one suggestion. Suggest style-only changes as 🔴/🟡. Flag patterns without grepping for evidence. Suggest rewrites > 20 lines inline (use `<details>` block).

## Investigation — MUST DO before flagging

```bash
grep -rn "MethodName\s*(" Assets/Scripts/ --include="*.cs"  # callers
grep -rn "EventName\s*[+-]=" Assets/Scripts/ --include="*.cs"  # subscribers
grep -rn "TypeName" Assets/ --include="*.prefab" --include="*.asset"  # serialization refs
grep -rn "EnumType" Assets/Scripts/ --include="*.cs" | grep -E "switch|case"  # enum usage
```

Every 🔴 needs caller count + affected files. Every 🟡 needs trigger conditions.

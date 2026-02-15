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

## 🔴 Critical — Async & Lifecycle

| Pattern | Why | Fix |
|:--------|:----|:----|
| `this`/`gameObject` after `await` no null check | MissingRef | `if (this == null) return;` |
| `StartCoroutine` without stop in OnDisable | Runs after destroy | Store handle, stop in OnDisable |
| `+=` without `-=` in OnDisable | Event leak | OnEnable/OnDisable pair |
| `async void` on non-Unity-event | Swallowed exceptions | `async Task` / `async UniTask` |

Lifecycle: Awake(self) → OnEnable(subscribe) → Start(cross-component) → OnDisable(unsubscribe) → OnDestroy(cleanup)

## 🔴 Critical — General

Breaking API change, NullRef without guard, memory leak (undisposed resources/events), data corruption (serialization change without migration), race conditions, hardcoded secrets.

## 🟡 Major

| Pattern | Fix |
|:--------|:----|
| Field renamed without `[FormerlySerializedAs]` | Add attribute |
| DOTween not killed in OnDisable | `_tween?.Kill()` |
| Cross-component access in Awake | Move to Start |
| SO mutated runtime without clone | `Instantiate(configSO)` |
| Physics calls in Update | Move to FixedUpdate |
| `private` → `public` on SerializeField | Keep private, add property |

## 🔵 Minor

Magic numbers, Debug.Log without `#if UNITY_EDITOR`, empty Update/Start, dead code, naming violations, nesting 4+, missing XML docs on public API.

## Investigation — MUST DO before flagging

```bash
grep -rn "MethodName\s*(" Assets/Scripts/ --include="*.cs"  # callers
grep -rn "EventName\s*[+-]=" Assets/Scripts/ --include="*.cs"  # subscribers
grep -rn "TypeName" Assets/ --include="*.prefab" --include="*.asset"  # serialization refs
```

Every 🔴 needs caller count + affected files. Every 🟡 needs trigger conditions.

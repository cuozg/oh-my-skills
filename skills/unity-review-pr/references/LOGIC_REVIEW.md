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

Lifecycle: Awake(self) → OnEnable(subscribe) → Start(cross-component) → OnDisable(unsubscribe) → OnDestroy(cleanup)

## 🔴 Critical — General

Breaking API change, NullRef without guard, memory leak (undisposed resources/events), data corruption (serialization change without migration), race conditions, hardcoded secrets.

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

## 🟡 Major — State & Data

| Pattern | Fix |
|:--------|:----|
| Bool flags for state management (3+ bools) | Extract state machine / enum |
| Collection modified during enumeration | Copy or use removal list |
| Dictionary lookup without `TryGetValue` | Replace `ContainsKey` + index with `TryGetValue` |
| `List.Find()` / `FirstOrDefault()` in hot path | Use Dictionary or HashSet for O(1) lookup |
| Enum changed without updating all `switch` statements | Grep all switch/if-chains for that enum |
| `[Serializable]` class with no default constructor | Deserialization will fail silently |

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

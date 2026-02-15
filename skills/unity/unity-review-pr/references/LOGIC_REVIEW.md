# Logic Review — C# Files

Load when PR modifies `.cs` files.

## 🔴 Critical — Unity Performance

| Pattern | Why | Fix |
|:--------|:----|:----|
| `GetComponent` in Update/FixedUpdate/LateUpdate | O(n) per frame | Cache in Awake |
| `Camera.main` in loop | FindWithTag each access | Cache in Awake |
| `Find()`/`FindObjectOfType()` at runtime | O(n) scene traversal | `[SerializeField]` inject |
| `Instantiate`/`Destroy` spam in loops | GC spikes | Object pool |
| String concat / LINQ / `new List` in Update | Per-frame allocation | Pre-allocate, `NonAlloc` |

## 🔴 Critical — Async & Lifecycle

| Pattern | Why | Fix |
|:--------|:----|:----|
| Use `this`/`gameObject` after `await` without null check | Destroyed during await → MissingRef | `if (this == null) return;` after await |
| `StartCoroutine` without stop in OnDisable | Runs after destroy | Store handle, stop in OnDisable |
| `+=` without matching `-=` in OnDisable | Event leak, crash on destroyed | OnEnable/OnDisable pair |
| `async void` on non-Unity-event methods | Swallowed exceptions | `async Task` or `async UniTask` |

Lifecycle: `Awake` (self only) → `OnEnable` (subscribe) → `Start` (cross-component) → `OnDisable` (unsubscribe) → `OnDestroy` (cleanup, null-check others)

## 🔴 Critical — General

Breaking API change (find callers first), NullRef without guard, memory leak (undisposed resources/events), data corruption (serialization change without migration), race conditions, hardcoded secrets.

## 🟡 Major — Unity Patterns

| Pattern | Fix |
|:--------|:----|
| Field renamed without `[FormerlySerializedAs]` | Add attribute |
| DOTween not killed in OnDisable | `_tween?.Kill()` |
| Cross-component access in Awake | Move to Start |
| SO mutated at runtime without clone | `Instantiate(configSO)` |
| Physics calls in Update | Move to FixedUpdate |
| `transform.position.x = 5f` (no-op) | Copy struct, modify, assign back |
| `private` → `public` on SerializeField | Keep private, add property |

## 🟡 Major — General

Potential NullRef (edge conditions), visibility escalation without justification, tight coupling (cross-system GetComponent), missing error handling (I/O, network), incorrect conditionals (off-by-one), undisposed IDisposable.

## 🔵 Minor

Magic numbers, Debug.Log without `#if UNITY_EDITOR`, empty Update/Start, dead code, naming violations, excessive nesting (4+), missing XML docs on public API.

## Investigation — MUST DO before flagging

```bash
# Method signature changes → find callers
grep -rn "MethodName\s*(" Assets/Scripts/ --include="*.cs"
# Events → subscribers + unsubscribe check
grep -rn "EventName\s*[+-]=" Assets/Scripts/ --include="*.cs"
# Serialization → prefab/SO refs
grep -rn "TypeName" Assets/ --include="*.prefab" --include="*.asset"
# Inheritance → derived types
grep -rn ":\s*BaseClassName" Assets/Scripts/ --include="*.cs"
```

Every 🔴 needs caller count + affected files. Every 🟡 needs trigger conditions.

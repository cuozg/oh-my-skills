## 6. State Management

### 6.1 Critical

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

### 6.2 Major

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
| Bool flags for state management (3+ bools) | Combinatorial explosion of states | Extract state machine / enum |
| Collection modified during enumeration | InvalidOperationException | Copy or use removal list |
| Dictionary lookup without `TryGetValue` | Double-lookup waste | Replace `ContainsKey` + index with `TryGetValue` |
| `List.Find()` / `FirstOrDefault()` in hot path | O(n) search per call | Use Dictionary or HashSet for O(1) lookup |
| Enum changed without updating all `switch` statements | Unhandled case | Grep all switch/if-chains for that enum |
| `[Serializable]` class with no default constructor | Deserialization will fail silently | Add parameterless constructor |

---

Continue reading in **logic-data.md** for Data Flow, Concurrency, UI/Networking/Gotchas, Edge Cases, and Minor Issues.

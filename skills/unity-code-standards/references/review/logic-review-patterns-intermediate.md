# Logic Review Patterns — Unity C# (Part 2)

Intermediate patterns: Serialization, Control Flow, Logic Patterns, and State Management basics.

---

## 3. Serialization & Data

### 3.1 Critical

| Pattern | Why | Fix |
|:--------|:----|:----|
| `[SerializeField]` applied to property | Unity serializes fields, not C# properties | Convert to backing field serialization |
| Public field should not persist but lacks `[NonSerialized]` | Unintended state persistence across saves/domain reload | Mark non-persistent fields explicitly |
| Interface/abstract type serialized with default Unity serializer | Unity cannot serialize most interface/abstract field data | Use concrete type, custom serializer, or `[SerializeReference]` with constraints |
| `[SerializeReference]` used without migration/type-stability plan | Type rename/move breaks polymorphic payloads | Add stable type strategy and migration handling |
| ScriptableObject asset mutated directly at runtime | Shared project asset state corruption | `Instantiate()` runtime copy before mutation |
| `JsonUtility.FromJson` on Unity object graph expecting references | Object references not restored in plain JSON load | Use ID-based remap/custom serialization layer |

---

## 4. Control Flow

### 4.1 Critical

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

### 4.2 Major

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

---

## 5. Logic Patterns

### 5.1 Major

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
| `Mathf.Lerp(current, target, Time.deltaTime)` used as smoothing | Never reaches target predictably, frame-rate dependent. Use damp/speed-based interpolation (`MoveTowards`, exponential decay) |
| `Vector3 == Vector3` for precision checks | Float equality unstable. Compare `(a - b).sqrMagnitude < epsilon` |
| `Quaternion == Quaternion` for orientation checks | Float equality unstable. Use `Quaternion.Angle(a, b) < threshold` |
| `transform.position += ...` in FixedUpdate on Rigidbody object | Bypasses physics solver/interpolation. Use `Rigidbody.MovePosition`/forces in FixedUpdate |
| `Rigidbody.MovePosition` called from Update | Desync with physics timestep. Move to FixedUpdate |
| `gameObject.tag == "..."` comparisons | Slower/string-based and typo-prone. Use `CompareTag("...")` |
| Incorrect layer-mask bit math (`1 << layer` misuse) | Wrong collision/query filter. Validate with `LayerMask.GetMask` or precomputed mask constants |
| `Debug.DrawRay` endpoint passed as direction | Visual debug lies about actual cast. Pass direction * length, not endpoint |
| `Invoke`/`InvokeRepeating("Method")` string API | No compile-time safety/rename breakage. Replace with coroutine/timer + direct delegate |
| `PlayerPrefs` stores sensitive tokens/PII | Plaintext, user-editable storage. Use secure storage/encryption strategy |
| Misread `Random.Range` bounds (`int` max exclusive, `float` max inclusive) | Off-by-one and spawn distribution bugs. Apply correct overload semantics explicitly |

---

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

Continue reading in **logic-review-patterns-advanced.md** for Data Flow, Concurrency, UI/Networking/Gotchas, Edge Cases, and Minor Issues.

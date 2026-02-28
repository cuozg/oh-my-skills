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


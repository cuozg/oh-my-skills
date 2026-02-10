# Logic Review Checklist

Load this reference when PR modifies `.cs` files. Covers C# code quality, Unity performance patterns, async/lifecycle safety, and general code issues. Each issue follows: **Issue → Evidence → Why → Fix → Priority**.

---

## Table of Contents

1. [Unity Performance](#1-unity-performance)
2. [Async & Lifecycle](#2-async--lifecycle)
3. [Unity-Specific Patterns](#3-unity-specific-patterns)
4. [General — Critical](#4-general--critical)
5. [General — Major](#5-general--major)
6. [General — Minor](#6-general--minor)
7. [Investigation Patterns](#7-investigation-patterns)

---

## 1. Unity Performance

🔴 Critical — these cause frame drops, GC spikes, or stuttering in production.

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **GetComponent in hot path** | `GetComponent<T>()` inside `Update`/`FixedUpdate`/`LateUpdate` | Reflection-based lookup every frame; O(n) component search | Cache in `Awake`/`Start`: `private T _cached;` | 🔴 Critical |
| **Camera.main in loop** | `Camera.main` in `Update`/`FixedUpdate` | Calls `FindGameObjectWithTag("MainCamera")` every access | Cache: `private Camera _cam; void Awake() => _cam = Camera.main;` | 🔴 Critical |
| **Find in runtime** | `Find()`, `FindObjectOfType()`, `FindObjectsOfType()` in gameplay code | O(n) scene traversal per call; freezes on large scenes | Inject via `[SerializeField]` or service locator | 🔴 Critical |
| **Instantiate/Destroy spam** | Frequent `Instantiate`/`Destroy` in gameplay loops (bullets, VFX, UI) | GC spikes from allocation + finalization; frame hitches | Object pooling: `ObjectPool<T>` or custom pool | 🔴 Critical |
| **String concat in Update** | `string + string` or `$""` interpolation in hot paths | New `string` allocation every frame → GC pressure | `StringBuilder` or cache; avoid per-frame string ops | 🔴 Critical |
| **Allocating in hot path** | `new List<>()`, `.ToList()`, `.ToArray()`, LINQ `.Where()`/`.Select()` in Update | Heap allocation every frame; GC spikes | Pre-allocate collections; use `NonAlloc` variants | 🔴 Critical |

---

## 2. Async & Lifecycle

🔴 Critical — these cause crashes, leaks, or undefined behavior.

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Null after await** | `await` then use `this`/`gameObject`/any `UnityEngine.Object` without null check | Object may be destroyed during await → `MissingReferenceException` | Add `if (this == null) return;` after every `await` | 🔴 Critical |
| **Coroutine orphan** | `StartCoroutine` without storing handle or stopping in `OnDisable` | Coroutine runs after disable/destroy → null refs, logic bugs | Store `Coroutine _cr;` → `StopCoroutine(_cr)` in `OnDisable` | 🔴 Critical |
| **Event leak** | `+=` subscription without matching `-=` in `OnDisable`/`OnDestroy` | Memory leak; callbacks fire on destroyed objects → crashes | Subscribe in `OnEnable`, unsubscribe in `OnDisable` | 🔴 Critical |
| **async void** | `async void` on non-Unity-event methods | Exceptions silently swallowed; can't await; crashes hard to diagnose | Use `async Task` or `async UniTask`; `async void` only for Unity events | 🔴 Critical |

### Lifecycle Order Reference

```
Awake → OnEnable → Start → FixedUpdate → Update → LateUpdate → OnDisable → OnDestroy
```

- `Awake`: Self-initialization only (`GetComponent` on same GO). Order not guaranteed across GOs.
- `OnEnable`/`OnDisable`: Subscribe/unsubscribe events. Paired.
- `Start`: Cross-component access. Runs after all `Awake` calls.
- `OnDestroy`: Final cleanup. Null-check other objects — they may already be destroyed.

---

## 3. Unity-Specific Patterns

🟡 Major — these cause subtle bugs, data loss, or maintenance problems.

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **SerializedField visibility flip** | `private` → `public` on `[SerializeField]` fields | Can break prefab serialization; exposes internals | Keep `[SerializeField] private`; add property if needed | 🟡 Major |
| **Missing FormerlySerializedAs** | Field renamed without `[FormerlySerializedAs("oldName")]` | Loses serialized data on existing prefabs/SOs | Add attribute before renaming | 🟡 Major |
| **DOTween not killed** | `DOTween.To()` / `.DOMove()` without `.Kill()` in `OnDisable`/`OnDestroy` | Tween runs after destroy → null ref, visual artifacts | `_tween?.Kill();` in `OnDisable` | 🟡 Major |
| **Lifecycle order violation** | Accessing sibling components in `Awake()` | `Awake` execution order not guaranteed across objects | Use `Start` for cross-component access; or Script Execution Order | 🟡 Major |
| **ScriptableObject mutation** | Modifying SO fields at runtime without `.Instantiate()` clone | Changes persist in Editor; affects all references | Clone: `var local = Instantiate(configSO);` | 🟡 Major |
| **Physics in Update** | `Physics.Raycast`, `OverlapSphere` in `Update` instead of `FixedUpdate` | Inconsistent results; physics on fixed timestep | Move to `FixedUpdate`; or use `Time.fixedDeltaTime` | 🟡 Major |
| **Implicit vector ops** | `transform.position.x = 5f;` (no-op; position is value type) | Silently does nothing; common Unity trap | `var pos = transform.position; pos.x = 5f; transform.position = pos;` | 🟡 Major |

---

## 4. General — Critical

🔴 Critical — crash, data loss, security in any codebase.

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Breaking API change** | Method/property signature changed (params added/removed/retyped) | All callers break at compile or runtime | Investigate callers first; add overload for backward compat | 🔴 Critical |
| **NullReferenceException** | No null check on common code paths (deserialization, external data, collections) | Crash in production; hard to diagnose | Defensive null checks; `?.` and `??` operators | 🔴 Critical |
| **Memory leak** | Resources, streams, native arrays, events not disposed/unsubscribed | Unbounded memory growth over session | `IDisposable`; `using` statements; clean up in `OnDestroy` | 🔴 Critical |
| **Data corruption** | Serialization format change without migration; field type change | Existing saves/prefabs lose data silently | `[FormerlySerializedAs]`; migration code | 🔴 Critical |
| **Race condition** | Shared mutable state from multiple threads/async paths | Non-deterministic behavior; intermittent crashes | Lock critical sections; thread-safe collections; single-writer | 🔴 Critical |
| **Security vulnerability** | Unsanitized input, hardcoded secrets, API keys in source | Exploitable in production builds | Sanitize input; use env vars or encrypted config | 🔴 Critical |

---

## 5. General — Major

🟡 Major — conditional failures, encapsulation breaks, maintainability.

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Potential NullReference** | Null possible under edge conditions (first frame, missing prefab, network timeout) | Crash in edge cases that pass basic testing | Null guards with meaningful error logging | 🟡 Major |
| **Visibility escalation** | `private` → `public` without justification | Breaks encapsulation; increases coupling surface | Keep private; expose via interface or read-only property | 🟡 Major |
| **Tight coupling** | Direct `GetComponent<OtherController>()` cross-system; concrete dependencies | Untestable; refactor cascades across systems | Events, interfaces, or ScriptableObject channels | 🟡 Major |
| **Missing error handling** | No try/catch around I/O, network, file, deserialization | Silent failures in production; data loss | Wrap in try/catch with logging; fallback behavior | 🟡 Major |
| **Incorrect conditional** | Off-by-one, wrong operator (`<` vs `<=`), inverted logic, missing `break` | Logic bugs that pass basic testing, fail edge cases | Review boundaries; add unit tests | 🟡 Major |
| **Resource not disposed** | `IDisposable` created without `using` or explicit `Dispose()` | Native resource leak (file handles, connections) | `using var x = ...;` or dispose in `finally` | 🟡 Major |

---

## 6. General — Minor

🔵 Minor — style, conventions, readability.

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Magic numbers** | Hardcoded `0.5f`, `100`, `"some_key"` without context | Intent unclear; hard to tune; scattered constants | `const`, `static readonly`, or `[SerializeField]` | 🔵 Minor |
| **Debug.Log in production** | `Debug.Log/Warn/Error` not in `#if UNITY_EDITOR` or conditional | Perf cost in release builds; log spam | `#if UNITY_EDITOR` or logging framework with levels | 🔵 Minor |
| **Empty Unity callback** | Empty `Update()`, `Start()`, `OnGUI()` body | Unity still calls them → overhead per frame | Delete empty callbacks entirely | 🔵 Minor |
| **Dead code** | Unreachable branches, unused variables, commented-out blocks | Maintenance burden; confusion | Remove or document with TODO | 🔵 Minor |
| **Naming convention** | Breaks project PascalCase/camelCase/underscore rules | Inconsistent codebase; harder to navigate | Follow project conventions | 🔵 Minor |
| **Excessive nesting** | 4+ levels of `if`/`for`/`while` | Hard to read, reason about, test | Early returns; extract methods; guard clauses | 🔵 Minor |
| **Missing XML docs** | Public API without `/// <summary>` | Consumers can't understand intent | Add XML doc comments on public members | 🔵 Minor |

---

## 7. Investigation Patterns

**Never flag an issue without investigating callers/impact first.** Every 🔴 must include evidence (caller count, affected files). Every 🟡 must explain conditions under which the issue manifests.

### Method Signature Changes

Find all callers that will break:

```bash
grep -rn "MethodName\s*(" Assets/Scripts/ --include="*.cs"
grep -rn "\"MethodName\"" Assets/Scripts/ --include="*.cs"        # reflection
grep -rn "nameof(.*MethodName)" Assets/Scripts/ --include="*.cs"  # nameof
grep -rn "IInterfaceName" Assets/Scripts/ --include="*.cs"        # interface impls
```

**Report format:**
```markdown
🔴 **Breaking Change**: `ClassName.MethodName` signature changed.
**Before**: `void MethodName(int x)` → **After**: `void MethodName(Vector3 position)`
**Callers requiring update** (N found):
| File | Line | Current Call |
|:-----|:-----|:-------------|
| Foo.cs | 42 | `MethodName(1)` |
```

### Event/Delegate Changes

```bash
grep -rn "EventName\s*+=" Assets/Scripts/ --include="*.cs"  # subscribers
grep -rn "EventName\s*-=" Assets/Scripts/ --include="*.cs"  # unsubscribers
grep -rn "EventName\s*+=\s*(" Assets/Scripts/ --include="*.cs"  # lambda (can't unsub)
```

**Report format:**
```markdown
🔴 **Breaking Change**: Event `ClassName.EventName` signature changed.
**Subscribers affected** (N found):
| File | Line | Subscription |
|:-----|:-----|:-------------|
| Bar.cs | 15 | `EventName += OnEvent` |
**Unsubscribe check**: [All have matching `-=` | Missing in N files]
```

### Serialization Changes

```bash
grep -rn "TypeName" Assets/ --include="*.asset"    # SO references
grep -rn "TypeName" Assets/ --include="*.prefab"   # prefab references
grep -rn "\[SerializeField\]" Assets/Scripts/ChangedFile.cs
grep -rn "\[SerializeReference\]" Assets/Scripts/ChangedFile.cs
```

### Inheritance/Interface Changes

```bash
grep -rn ":\s*BaseClassName" Assets/Scripts/ --include="*.cs"
grep -rn ":\s*.*IInterfaceName" Assets/Scripts/ --include="*.cs"
```

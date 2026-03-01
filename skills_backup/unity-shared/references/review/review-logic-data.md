# Logic & Data Flow Review — PR Checklist

> Authoritative for: data flow analysis, concurrency & async, edge cases.
> Cross-ref: `review-csharp.md` (exception handling, null safety), `review-architecture-patterns.md` (coupling, events)

---

## 🔴 Critical — Data Flow

| Name | Issue | Fix |
|------|-------|-----|
| Shared Mutable State | Multiple systems read/write same data without synchronization | Single owner writes; others read via events, copies, or immutable snapshots |
| Stale Cache | Cached value never invalidated after source changes | Invalidate on source change; use dirty flag or event-driven refresh |
| Silent Data Loss | Operation fails but calling code proceeds as if success | Return `Result<T>` or throw; never return default silently |
| Unvalidated External Input | Network, file, or user data used without schema/bounds validation | Validate at system boundary: null, range, type, format checks |
| State Machine Missing Transition Guard | State transitions allowed from invalid source states | Add `CanTransition(from, to)` guard; whitelist valid transitions |
| Infinite Loop / Recursion | Unbounded loop or recursive call without base case | Add max iteration guard; verify base case terminates; add depth limit |
| Event Ordering Dependency | System assumes event A fires before event B — but order isn't guaranteed | Make each handler self-sufficient; use explicit sequencing if order matters |
| Write-After-Read Hazard | Value read early in frame, mutated mid-frame, stale read used for decision | Process all reads, then all writes; or use double-buffer pattern |
| Dictionary Key Mutation | Object used as dictionary key has mutable `GetHashCode` | Use immutable keys (`string`, `int`, `readonly struct`); override `Equals`/`GetHashCode` properly |
| Float Equality Check | `if (a == b)` for floats — fails due to precision | Use `Mathf.Approximately(a, b)` or threshold comparison |

## 🟡 Major — Data Flow

| Name | Issue | Fix |
|------|-------|-----|
| Missing Default/Fallback | Switch/if-chain has no `default` case — unknown values silently ignored | Add `default: throw new ArgumentOutOfRangeException()` or safe fallback |
| Implicit Data Contract | Two systems agree on data format by convention, not by type | Define shared interface, struct, or DTO; enforce at compile time |
| Transform Dependency Chain | System reads `Transform.position` of object moved by another system same frame | Use `LateUpdate` for reads after movement; or explicit execution order |
| Collection Modified During Iteration | `foreach` over list while adding/removing elements | Iterate over copy (`ToArray()`), or use reverse `for` loop for removal |
| Event Handler Modifies Source | Event subscriber modifies the collection/state that triggered the event | Queue modifications; apply after event dispatch completes |
| String-Based Data Lookup | `dictionary["playerHP"]` instead of typed key — typos cause silent null | Use `enum`, `const`, or typed key; compile-time safety over runtime lookup |
| Unprotected Divide | Division by zero possible when denominator comes from data | Check denominator ≠ 0 before division; provide fallback value |

## 🔴 Critical — Concurrency & Async

| Name | Issue | Fix |
|------|-------|-----|
| Async Without Cancellation | `async Task LoadAsync()` with no `CancellationToken` — can't abort on scene change | Pass `CancellationToken`; check `token.ThrowIfCancellationRequested()` in loops |
| Main Thread Violation | Accessing Unity API (`Transform`, `GameObject`) from background thread | Use `UnityMainThreadDispatcher` or `await UniTask.SwitchToMainThread()` |
| Missing `ConfigureAwait(false)` | Library async code captures `SynchronizationContext` — potential deadlock | Add `ConfigureAwait(false)` in non-Unity library code |
| Fire-and-Forget Async | `_ = DoSomethingAsync()` — exception silently lost | Use `UniTask.Void()`, `SafeFireAndForget()`, or proper error handler |
| Lock Contention | Multiple threads waiting on same `lock` — defeats parallelism | Reduce lock scope; use `ConcurrentDictionary`; consider lock-free patterns |
| Callback After Destroy | Async callback executes after `MonoBehaviour` destroyed — `MissingReferenceException` | Check `this != null` or `destroyCancellationToken` before accessing members |
| Task.Result on Main Thread | `task.Result` or `task.Wait()` blocks Unity main thread — freezes game | `await` instead of `.Result`; use `UniTask` for Unity-aware async |
| Coroutine Exception Swallowed | Exception in coroutine silently stops it — no error logged | Wrap coroutine body in try-catch with explicit logging |

## 🟡 Major — Concurrency & Async

| Name | Issue | Fix |
|------|-------|-----|
| Missing Timeout | Async operation can hang forever (network, file I/O) | Use `CancellationTokenSource.CreateLinkedTokenSource` with timeout |
| Concurrent Collection Misuse | `List<T>` shared across threads instead of `ConcurrentBag<T>` | Use `System.Collections.Concurrent` types for cross-thread collections |
| Async Init Without Ready Signal | System starts using async-loaded data before load completes | Use initialization state machine: `Loading → Ready → Active`; block consumers until Ready |
| Double-Dispatch | Async callback triggers another async chain — exponential fan-out | Use command queue with sequential processing; debounce duplicate triggers |

---

## Edge Case Checklist

When reviewing any logic change, verify these edge cases are handled:

| Edge Case | What to Check |
|-----------|---------------|
| **Empty input** | Does the method handle empty list, null string, zero count? |
| **Single element** | Does the algorithm work with exactly one item? |
| **Boundary values** | Are `int.MaxValue`, `float.Infinity`, `0`, `-1` handled? |
| **Concurrent modification** | Can two callers trigger this simultaneously? |
| **Rapid re-entry** | What if called again before previous invocation completes? |
| **First-time execution** | Does it work on first call when cache/state is empty? |
| **Destroy during execution** | What if the object is destroyed mid-operation? |
| **Scene transition** | Does this survive scene load/unload? Should it? |
| **Platform difference** | Does this behave differently on mobile, console, or editor? |
| **Time scale zero** | Does this break when `Time.timeScale = 0` (pause)? |

---

## Suggestion Quality Guide

When leaving review comments about logic issues:

| Quality | Example |
|---------|---------|
| ❌ Vague | "This might have issues" |
| ❌ Prescriptive | "Use ConcurrentDictionary" (no context) |
| ✅ Specific | "This `Dictionary<int, Player>` is read in `Update()` and written in async callback `OnPlayerJoined()` — race condition. Either access from main thread only, or switch to `ConcurrentDictionary<int, Player>`." |

**Rule:** Every comment must state **what's wrong**, **why it matters**, and **how to fix it**.

---

## PR Investigation Commands

```bash
# Find shared mutable state
grep -rn "static.*List\|static.*Dictionary\|static.*HashSet" Assets/Scripts/ --include="*.cs"

# Find async without cancellation
grep -rn "async Task" Assets/Scripts/ --include="*.cs" | grep -v "CancellationToken"

# Find fire-and-forget
grep -rn "_ =" Assets/Scripts/ --include="*.cs" | grep -i "async\|task"

# Find coroutine starts without stops
grep -rn "StartCoroutine" Assets/Scripts/ --include="*.cs"
```

# Review Code Standards

Consolidated review reference: common rules, severity, verification gates, approval criteria, C# checklist, general checklist, logic & data flow, and architecture patterns.

---

## Common Rules

Rules shared by `unity-review-code-pr` and `unity-review-code-local`.

### Input → Diff Command

| Input | Command |
| :------ | :--------|
| None (default) | `git diff` + `git diff --cached` |
| Commit SHA | `git show <hash>` |
| Commit range | `git diff <base>..<head>` |
| Branch | `git diff <branch>...HEAD` |
| PR number/URL | `gh pr diff <N>` + `gh pr view <N> --json title,body,files` |
| Feature/logic request | Find relevant files via grep/LSP |

### File Reading

- Only review `.cs` files. Read **full files**, not just diffs. Logic bugs hide in surrounding context.
- Trace data flow end-to-end. Verify lifecycle ordering.

### Unity-Specific

- If project uses UniTask, `async UniTaskVoid` can be valid for Unity event entry points.
- For serialization findings, check whether the project has migration/versioning support.

### Evidence & Investigation

- Never comment without evidence. Investigate first — see [Verification Gates](#verification-gates).
- One issue = one comment (severity + evidence + suggestion/fix description).
- Same issue in N files → full explanation on first occurrence, short reference on rest (batch pattern).

### Fix Delegation

- Delegate code fixes to `unity-code-quick` via `task(category="quick", load_skills=["unity-code-quick"], run_in_background=true)`.
- Include in delegation prompt: file path, line number, the review comment, and the exact fix to apply.
- One task per fix or per file. Multiple fixes → multiple parallel background tasks.

### Severity Usage

- Severity labels are for categorization only.
- This skill always posts as `COMMENT`. Approval decisions are made exclusively by `unity-review-general`.

---

## Severity Classification

| Severity | Emoji | Meaning |
| :---------|:------|:--------|
| CRITICAL | 🔴 | Crash, data loss, security, breaking API |
| HIGH | 🟡 | Logic bugs, missing tests, arch violations |
| MEDIUM | 🔵 | Code quality, conventions, minor perf |
| LOW | 🟢 | Style preferences, typos, micro-optimization |

### 🔴 Critical — Block Merge

**Security**: Secrets in code, SQL/command injection, XSS, auth bypass, unvalidated deserialization.
**Stability**: NullReferenceException on common paths, data corruption, infinite loops, memory leaks in Update/FixedUpdate.
**Breaking**: Removed/renamed public API used by other assemblies, changed serialized field names/types (data loss), broken prefab references, DB schema changes without migration.
**Unity Runtime**: Addressables loaded without release tracking, infinite coroutine without stop condition, UI Canvas rebuild every frame in production, unguarded division-by-zero on common execution paths.

### 🟡 High — Request Changes

**Logic**: Incorrect conditional logic, off-by-one in loops, race conditions in async/coroutine, unhandled edge cases that cause silent failures.
**Testing**: No tests for new public API, removed test coverage for modified code.
**Architecture**: Violates established project patterns (e.g., bypassing event system with direct coupling), circular dependencies between assemblies.
**Reliability**: Missing null-propagation in long call chains, event handler not removed causing memory pressure, Addressable label mismatch between code and groups.

### 🔵 Medium — Comment (Allow Merge)

**Quality**: God class (>500 lines), deep nesting (>4 levels), duplicated logic across files, magic numbers without constants, empty catch blocks.
**Performance**: Avoidable allocations in hot paths, LINQ in Update, unnecessary GetComponent calls, suboptimal algorithm (O(n²) where O(n) is trivial).
**Conventions**: Inconsistent naming, missing XML docs on public API, non-standard file/folder structure.
**Unity Hygiene**: `FindObjectOfType` used outside init/bootstrap paths, missing `[Tooltip]` on public inspector fields, inconsistent enum naming style (PascalCase vs SCREAMING_CASE).

### 🟢 Low — Approve with Suggestions

**Style**: Formatting preferences, comment wording, variable name alternatives, import ordering.
**Minor optimization**: Micro-optimizations with negligible impact, suggested but not required refactors.
**Documentation**: Typos in comments, slightly better doc phrasing.

---

## Verification Gates

Evidence before claims. Investigate before commenting.

### Evidence Requirements by Severity

| Severity | Required Before Commenting | NOT Sufficient |
|:---------|:--------------------------|:---------------|
| 🔴 CRITICAL | Caller count + affected files + reproduction scenario | "Looks wrong", "might crash" |
| 🟡 HIGH | Trigger conditions + what state leads to the bug | "Could be a problem" |
| 🔵 MEDIUM | Brief explanation of why current code is suboptimal | "I prefer it differently" |
| 🟢 LOW | Brief note why this is worth mentioning | Style preference alone |

### Investigation Protocol

```
BEFORE adding any review comment:

1. IDENTIFY: What evidence proves this is a real issue?
2. SEARCH: grep/LSP for callers, subscribers, state mutations
3. TRACE: Follow the data flow — can this state actually occur?
4. VERIFY: Does evidence confirm the issue is real, not theoretical?
   - If NO: Don't comment. Move on.
   - If YES: Write comment with evidence inline.
```

### Investigation Commands

```bash
# Count callers of a method
grep -rn "MethodName\s*(" Assets/Scripts/ --include="*.cs" | wc -l

# Find all state mutations
grep -rn "_fieldName\s*=" Assets/Scripts/ --include="*.cs"

# Find event subscribers
grep -rn "EventName\s*[+-]=" Assets/Scripts/ --include="*.cs"

# Check if null guard exists anywhere in call chain
grep -rn "MethodName" Assets/Scripts/ --include="*.cs" | grep -E "null|==\s*null|\?\."
```

### Cross-File Verification

| What to Verify | How | Why |
|:---------------|:----|:----|
| All callers handle new exception | grep for method name + check try/catch | API contract changed |
| Serialized field rename handled | grep for FormerlySerializedAs | Prefab data loss |
| Event subscribers updated | grep for event += and -= | Missing notification |
| Interface implementation complete | LSP find implementations | Abstract contract |
| Enum switch exhaustive | grep for switch + enum type | Missing case |

### False Positive Detection

- Pattern exists but wrapped in `#if UNITY_EDITOR` -> not a runtime issue, downgrade
- Pattern exists but class has `[ExecuteInEditMode]` -> may be intentional
- GetComponent in method called from Awake/Start only -> not a hot path issue
- Allocation in method behind feature flag / `#if DEBUG` -> not shipped
- Null reference pattern but field has `[RequireComponent]` on the class -> guaranteed present

### Red Flags — Don't Comment

- Pattern is theoretical only — no real caller triggers it
- Issue exists but is already guarded elsewhere in the call chain
- "Best practice" violation with zero practical impact in this codebase
- Style/formatting preference (handled by linters)
- Naming suggestions without logic impact
- "Consider refactoring" without concrete cause
- Code that's already self-documenting
- Test-only code with no production impact

### When to Upgrade Severity

| Situation | Upgrade to |
|:----------|:-----------|
| Bug affects serialized data (saves, configs, network) | 🔴 — data corruption |
| Bug only triggers in editor, not runtime | Downgrade to 🟢 |
| Bug affects 10+ callers | 🔴 — wide blast radius |
| Bug requires specific rare state to trigger | Keep at 🟡, note rarity |

If a pattern would be 🔴 but the project has an established convention/wrapper that handles it (e.g., a SafeGetComponent wrapper, event bus with auto-cleanup), downgrade to 🟢 and note the convention.

---

## Approval Criteria

Decision tree for review verdict. Severity tiers map to GitHub review events.

### Decision Tree

```
Has CRITICAL issue?  ──yes──▶  🔴 REQUEST_CHANGES (block merge)
        │ no
Has HIGH issue?      ──yes──▶  🟡 REQUEST_CHANGES
        │ no
Has MEDIUM issue?    ──yes──▶  🔵 COMMENT (allow merge)
        │ no
Has LOW issue?       ──yes──▶  🟢 APPROVE (with suggestions)
        │ no
Clean                ──────▶  ✅ APPROVE
```

### Edge Cases

- **Mixed severities** → Highest severity wins for the review event. All issues still get inline comments.
- **Pre-existing issues** → Only flag if the PR makes them worse or touches the affected code. Note: "Pre-existing, surfaced by this change."
- **Partial fix is OK** → If a PR fixes 3 of 5 issues, approve the fix. File a follow-up for the remaining 2.
- **Unity-specific references take precedence** → `unity-shared` logic review patterns, PREFAB_REVIEW, ASSET_REVIEW checklists override generic guidance when they conflict.

### Grading Criteria

| Grade | Criteria |
|:------|:---------|
| A | 0 Critical, <=3 High, clean architecture, good test coverage, follows conventions |
| B | 0 Critical, <=8 High, mostly clean architecture, some tests, minor debt |
| C | <=2 Critical, <=15 High, architectural concerns, limited tests, moderate debt |
| D | <=5 Critical, >15 High, significant architectural issues, no tests, heavy debt |
| F | >5 Critical, project stability at risk, major architectural failures |

---

## C# Code Review Checklist

### 🔴 Critical

| Name | Issue | Fix |
|------|-------|-----|
| Empty Catch Block | `catch (Exception) { }` silently swallows errors — masks bugs | Log, rethrow, or handle specifically; never swallow silently |
| Catch-All in Business Logic | `catch (Exception ex)` at every call site hides root cause | Catch specific exceptions; let unexpected ones propagate to global handler |
| Null Dereference Unguarded | Accessing `.Value`, `.Result`, or member without null check | Use `?.`, null check, or `TryGet` pattern; enable nullable reference types |
| Public Mutable Collection | `public List<T> Items` — anyone can `.Clear()`, mutate state | Return `IReadOnlyList<T>` or `ReadOnlyCollection<T>`; expose `Add/Remove` methods |
| Async Void | `async void` cannot be awaited or caught — crashes on exception | Use `async Task` always; `async void` only for Unity event handlers (Start, OnEnable) |
| Magic Strings/Numbers | Hardcoded `"PlayerTag"`, `0.5f`, `100` scattered through code | Extract to `const`, `static readonly`, `enum`, or config SO |
| BinaryFormatter Usage | `BinaryFormatter` is insecure — arbitrary code execution via deserialized data | Use JSON (Newtonsoft), MessagePack, or FlatBuffers |

### 🟡 Major — Nullable & Access

| Name | Issue | Fix |
|------|-------|-----|
| Missing `#nullable enable` | No nullable analysis — compiler won't flag null risks | Add `#nullable enable` at file or project level |
| Nullable Warning Suppressed | `null!` or `#pragma warning disable` hides real null risks | Fix the null flow; use `?? throw`, guard clause, or redesign |
| Wrong Access Modifier | `public` field/method that should be `private` or `internal` | Apply least-privilege: `private` default, `internal` for assembly, `public` for API |
| Mutable Struct Exposed | `public struct Config { public float Speed; }` — mutation bugs | Use `readonly struct` or class; make fields `init`-only |
| Missing `sealed` on Leaf Class | Non-`abstract` class without `sealed` — allows unintended inheritance | Add `sealed` unless designed for extension |
| `protected` Field | Subclass directly mutates parent state — fragile base class problem | Use `protected` property with validation, or pass via constructor |

### 🟡 Major — Exception Handling

| Name | Issue | Fix |
|------|-------|-----|
| Throwing `System.Exception` | `throw new Exception("failed")` — too generic to catch specifically | Throw specific: `InvalidOperationException`, `ArgumentException`, or custom |
| Missing Stack Trace on Rethrow | `catch (Exception ex) { throw ex; }` resets stack trace | Use `throw;` (no argument) to preserve original stack trace |
| Exception in Constructor | Constructor throws — leaves object in invalid partial state | Use factory method or `Init()` pattern; validate args before construction |
| Missing Validation on Public API | Public method accepts any input without checks | Add guard clauses: `ArgumentNullException`, `ArgumentOutOfRangeException` at entry |
| Logging Without Context | `Debug.LogError("Failed")` — no info about what, where, or why | Include method name, entity ID, and relevant state: `$"[{name}] Failed to load {id}: {ex.Message}"` |
| Excessive Try-Catch Nesting | 3+ nested try-catch blocks — unreadable flow | Extract inner blocks to methods; use early return; let exceptions propagate to single handler |

### 🟡 Major — Method & Class Quality

| Name | Issue | Fix |
|------|-------|-----|
| Long Method | Method >30 LOC — hard to test, read, and reason about | Extract logical blocks into well-named private methods |
| Too Many Parameters | Method has 5+ parameters — signals it does too much | Group into parameter object, config struct, or builder pattern |
| Boolean Parameter | `Process(data, true, false)` — unreadable at call site | Use enum, named constants, or separate methods (`ProcessFast`, `ProcessSafe`) |
| Mixed Abstraction Levels | Method mixes high-level flow with low-level details | Keep one abstraction level per method; extract details to helper methods |
| Large Class | Class >300 LOC with 3+ concerns — violates SRP | Split into focused classes; use composition over inheritance |
| Deep Nesting | 4+ levels of `if/for/while` nesting | Use guard clauses (early return), extract methods, invert conditions |
| Side Effect in Getter | Property getter modifies state or triggers I/O | Use method instead of property for operations with side effects |

### 🔵 Medium — Anti-Patterns

| Name | Issue | Fix |
|------|-------|-----|
| Feature Envy | Method uses 5+ members of another class instead of its own | Move method to the class it envies; expose behavior, not data |
| Data Clump | Same 3+ fields passed together everywhere | Extract into a value object or struct |
| Middle Man | Class delegates every call to another class without adding value | Remove middle man; call target directly or merge |
| Inappropriate Intimacy | Class accesses another class's private/internal state via reflection or tricks | Expose proper API; redesign dependency |
| Speculative Generality | Abstract class or interface with only one implementation and no plan for more | Remove abstraction until second use case exists (YAGNI) |
| Divergent Change | One class modified for 3+ unrelated reasons | Split by reason-to-change into separate classes |

### 🔵 Medium — Logging & Documentation

| Name | Issue | Fix |
|------|-------|-----|
| Missing ILogger | Using `Debug.Log` directly everywhere — can't filter, route, or disable | Use `ILogger` / `ILogHandler` abstraction; inject via DI |
| Log Level Misuse | `Debug.LogError` for info, `Debug.Log` for errors | Error=unexpected failure, Warning=recoverable issue, Log=info/flow |
| Sensitive Data in Logs | Logging passwords, tokens, PII, or secrets | Strip sensitive fields; log IDs and operation names, not values |
| Missing XML Docs on Public API | Public method/class has no `///` summary | Add `<summary>`, `<param>`, `<returns>` for all public members |
| Commented-Out Code | Dead code in `//` blocks — clutters and misleads | Delete it; version control preserves history |
| TODO Without Ticket | `// TODO: fix later` with no tracking ticket | Add ticket reference: `// TODO(PROJ-123): reason` or remove |

### 🟢 Minor

| Name | Issue | Fix |
|------|-------|-----|
| Inconsistent Naming | Mix of `_field`, `m_Field`, `field` for private fields | Follow project convention; Unity default: `_camelCase` for private, `PascalCase` for public |
| Missing `readonly` on Injected Field | DI-injected field can be reassigned accidentally | Add `readonly` to all injected/constructor-assigned fields |
| Redundant `this.` Qualifier | `this.name` when `name` is unambiguous | Remove `this.` unless disambiguating from local variable |
| Missing `nameof()` | String literal `"PropertyName"` instead of `nameof(PropertyName)` | Use `nameof()` for refactor-safe property/method name references |
| Region Abuse | `#region` used to hide complexity instead of extracting classes | Remove regions; extract to focused classes/methods instead |

> **Style reference:** See `csharp-hygiene.md` for naming conventions, formatting rules, and `using` organization.

---

## General Review Checklist

### PR Size Guide

| Size | Files | Risk | Review Strategy |
|------|-------|------|----------------|
| XS | 1–3 | Low | Single-pass review |
| S | 4–10 | Low–Med | File-by-file, check dependencies |
| M | 11–25 | Medium | Split by concern, verify integration points |
| L | 26–50 | High | Multi-reviewer, staged review, test plan required |
| XL | 50+ | Very High | Request split into smaller PRs |

### 🔴 Critical — Security

| Name | Issue | Fix |
|------|-------|-----|
| Secrets in Code | API keys, tokens, passwords hardcoded in source | Use environment variables, encrypted config, or Unity's `CloudProjectSettings` |
| SQL/Command Injection | User input passed directly to queries or `Process.Start` | Parameterize queries; validate/sanitize all external input |
| Insecure Deserialization | `BinaryFormatter` or unvalidated JSON from untrusted source | Use safe serializer (Newtonsoft with TypeNameHandling.None); validate schema |
| Debug Code in Build | `Debug.Log` floods, test cheats, god-mode flags in release | Guard with `#if UNITY_EDITOR` or `[Conditional("DEBUG")]`; strip in build |
| PlayerPrefs for Sensitive Data | Storing tokens/passwords in `PlayerPrefs` (plaintext on disk) | Use OS keychain, encrypted file, or server-side session |

> **Deep dive:** See `code/security.md` for full security implementation checklist.

### 🔴 Critical — Correctness

| Name | Issue | Fix |
|------|-------|-----|
| Race Condition | Shared state accessed from multiple threads/callbacks without sync | Use `lock`, `Interlocked`, `ConcurrentDictionary`, or confine to main thread |
| Off-by-One Error | Loop bounds, array index, or count calculation off by 1 | Verify boundary: `< length` not `<= length`; test empty and single-element cases |
| Uninitialized State | Field used before assignment — default value causes silent bug | Initialize in constructor/`Awake`; use `[field: SerializeField]` for required refs |
| Missing Null Check on External Data | Deserialized/loaded data assumed non-null | Validate after load: null-check, schema validation, fallback defaults |

### 🟡 Major — Testing

| Name | Issue | Fix |
|------|-------|-----|
| No Tests for New Logic | New feature has zero test coverage | Add unit tests for business logic; integration tests for system boundaries |
| Test Depends on Execution Order | Tests pass in isolation but fail when run together | Each test sets up and tears down its own state; no shared mutable state |
| Test Asserts on Implementation | Test checks internal method calls instead of behavior | Assert on outputs and observable side effects, not internal wiring |
| Flaky Test | Test passes 90% of the time — timing, randomness, or external dependency | Remove timing dependencies; mock externals; use deterministic seed |
| Missing Edge Case Tests | Only happy path tested — no empty, null, overflow, boundary cases | Add tests for: empty input, null, max/min values, concurrent access |

### 🟡 Major — Performance

| Name | Issue | Fix |
|------|-------|-----|
| Allocation in Update | `new`, `string concat`, LINQ, or `ToString()` in `Update()` | Pre-allocate, cache, use `StringBuilder`, or `NonAlloc` variants |
| Missing Object Pooling | `Instantiate`/`Destroy` called frequently (projectiles, particles, VFX) | Use object pool; return to pool instead of `Destroy` |
| Unbounded Collection Growth | `List<T>` grows forever without cleanup | Cap size, use ring buffer, or clear periodically |
| Physics Every Frame | `Raycast` or overlap query in `Update` instead of `FixedUpdate` | Move physics queries to `FixedUpdate`; cache results; use layer masks |
| Unoptimized LINQ in Hot Path | `.Where().Select().ToList()` in per-frame code — allocations per call | Use `for` loop with pre-allocated list; reserve LINQ for init/editor |

> **Deep dive:** See `quality-performance-checklist.md` for advanced CPU, memory, GPU, and physics optimization.

### 🔵 Medium — Lifecycle & Unity

| Name | Issue | Fix |
|------|-------|-----|
| Work in `Awake` Depending on Other Objects | `Awake` references another object that isn't initialized yet | Use `Start` for cross-object setup; `Awake` for self-init only |
| Missing `OnDisable`/`OnDestroy` Cleanup | Coroutines, events, or timers not cleaned up | Stop coroutines, unsubscribe events, cancel tokens in `OnDisable`/`OnDestroy` |
| `DontDestroyOnLoad` Leak | Object persists across scenes but accumulates duplicates | Check for existing instance in `Awake`; destroy duplicate |
| Coroutine Without Stop | `StartCoroutine` without `StopCoroutine` or `StopAllCoroutines` on disable | Track coroutine handle; stop in `OnDisable` |
| `[SerializeField]` on Wrong Type | Serializing `Dictionary`, interface, or abstract class (won't serialize) | Use `List<KeyValuePair>` for dicts; use concrete type or SO reference |

### 🔵 Medium — Documentation & Process

| Name | Issue | Fix |
|------|-------|-----|
| PR Missing Description | No context for reviewer — what changed and why | Add summary, motivation, testing steps, and screenshots if UI |
| Breaking Change Without Migration | API change breaks existing callers with no upgrade guide | Add `[Obsolete("Use X instead")]`, migration notes, or adapter |
| Missing Changelog Entry | User-facing change not documented | Add entry to CHANGELOG.md with version, change type, and description |

### 🟢 Minor

| Name | Issue | Fix |
|------|-------|-----|
| Inconsistent Code Style | Mixed brace style, spacing, or naming in same file | Run formatter (`dotnet format`); follow `.editorconfig` |
| Large Commit | Single commit with 20+ files changed across concerns | Split into atomic commits: one per logical change |
| Missing `.meta` File | New asset added without Unity `.meta` file in version control | Always commit `.meta` files alongside assets |

---

## Logic & Data Flow Review Checklist

### 🔴 Critical — Data Flow

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

### 🟡 Major — Data Flow

| Name | Issue | Fix |
|------|-------|-----|
| Missing Default/Fallback | Switch/if-chain has no `default` case — unknown values silently ignored | Add `default: throw new ArgumentOutOfRangeException()` or safe fallback |
| Implicit Data Contract | Two systems agree on data format by convention, not by type | Define shared interface, struct, or DTO; enforce at compile time |
| Transform Dependency Chain | System reads `Transform.position` of object moved by another system same frame | Use `LateUpdate` for reads after movement; or explicit execution order |
| Collection Modified During Iteration | `foreach` over list while adding/removing elements | Iterate over copy (`ToArray()`), or use reverse `for` loop for removal |
| Event Handler Modifies Source | Event subscriber modifies the collection/state that triggered the event | Queue modifications; apply after event dispatch completes |
| String-Based Data Lookup | `dictionary["playerHP"]` instead of typed key — typos cause silent null | Use `enum`, `const`, or typed key; compile-time safety over runtime lookup |
| Unprotected Divide | Division by zero possible when denominator comes from data | Check denominator ≠ 0 before division; provide fallback value |

### 🔴 Critical — Concurrency & Async

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

### 🟡 Major — Concurrency & Async

| Name | Issue | Fix |
|------|-------|-----|
| Missing Timeout | Async operation can hang forever (network, file I/O) | Use `CancellationTokenSource.CreateLinkedTokenSource` with timeout |
| Concurrent Collection Misuse | `List<T>` shared across threads instead of `ConcurrentBag<T>` | Use `System.Collections.Concurrent` types for cross-thread collections |
| Async Init Without Ready Signal | System starts using async-loaded data before load completes | Use initialization state machine: `Loading → Ready → Active`; block consumers until Ready |
| Double-Dispatch | Async callback triggers another async chain — exponential fan-out | Use command queue with sequential processing; debounce duplicate triggers |

### Edge Case Checklist

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

### Suggestion Quality Guide

When leaving review comments about logic issues:

| Quality | Example |
|---------|---------|
| ❌ Vague | "This might have issues" |
| ❌ Prescriptive | "Use ConcurrentDictionary" (no context) |
| ✅ Specific | "This `Dictionary<int, Player>` is read in `Update()` and written in async callback `OnPlayerJoined()` — race condition. Either access from main thread only, or switch to `ConcurrentDictionary<int, Player>`." |

**Rule:** Every comment must state **what's wrong**, **why it matters**, and **how to fix it**.

### PR Investigation Commands

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

---

## Architecture Review — PR Checklist

> Authoritative for: DI, events, assemblies, module boundaries, scene architecture, coupling, SOLID.

---

## 🔴 Critical

| Name | Issue | Fix |
|------|-------|-----|
| Service Locator | Direct `FindObjectOfType` / static `Instance` in business logic couples everything | Inject via constructor, `[Inject]`, or SO channel; reserve locator for bootstrapper only |
| Circular Assembly Refs | Assembly A → B → A creates build order issues and tight coupling | Extract shared interfaces into a third assembly (e.g., `Core.Interfaces`) |
| God Class | Single class >500 LOC handling multiple responsibilities | Split by SRP — one concern per class; extract strategies, services, data objects |
| Missing Event Cleanup | `+=` without `-=` causes memory leaks and ghost callbacks | Pair every subscribe with unsubscribe in `OnDisable`/`OnDestroy`; use `RemoveAllListeners()` for UnityEvents |
| Scene Singleton Duplication | Multiple instances of a singleton across scenes | Use `DontDestroyOnLoad` with duplicate-check in `Awake`, or additive scene loading |
| Init Order Dependency | System A reads System B data before B initializes | Use explicit init phases (Bootstrap → Init → Ready), or reactive patterns (events/observables) |
| Tight Cross-Module Coupling | Module A directly references Module B internals | Communicate via interfaces, events, or SO channels; enforce assembly boundary |

## 🟡 Major

| Name | Issue | Fix |
|------|-------|-----|
| Missing Assembly Definitions | All scripts in one default assembly — slow compilation, no boundary enforcement | Create `.asmdef` per module; enforce dependency direction via assembly references |
| Wrong DI Scope | Transient service holding state, or singleton service referencing scene objects | Match DI lifetime to data lifetime: transient=stateless, singleton=app-wide, scoped=scene |
| Stringly-Typed Events | Events identified by magic strings (`"OnPlayerDied"`) — no compile-time safety | Use typed C# events, `UnityEvent<T>`, or SO event channels |
| Monolithic Scene | Everything in one scene — slow loading, merge conflicts, hard to test | Split into additive scenes (UI, Gameplay, Environment); load/unload per feature |
| Feature Envy | Class A constantly reads Class B's fields to make decisions | Move the logic to where the data lives; expose behavior, not data |
| Shotgun Surgery | One change requires editing 5+ files across unrelated modules | Consolidate related logic; use polymorphism or strategy pattern |
| Leaky Abstraction | Interface exposes implementation details (e.g., `IPlayerService.GetRigidbody()`) | Expose behavior (`Move`, `TakeDamage`), not implementation types |
| Primitive Obsession | Using `float hp`, `string id` instead of domain types | Create `Health`, `PlayerId` value types for type safety and validation |

## 🔵 Medium

| Name | Issue | Fix |
|------|-------|-----|
| Missing Interface | Concrete class used directly — hard to test and swap | Extract interface for any service consumed by 2+ classes |
| Over-Engineering | Abstract factory for a system with one implementation | YAGNI — use concrete class until second consumer exists |
| Mixed Communication | Same system uses events AND direct calls AND SO channels | Pick one primary pattern per communication layer; document in ADR |
| Unused Assembly Ref | `.asmdef` references assembly it doesn't actually use | Remove unused references; keeps compile times fast |
| Deep Hierarchy Coupling | Child component calls `GetComponentInParent<>` 3+ levels up | Pass dependencies via inspector injection or local event bus |

## 🟢 Minor

| Name | Issue | Fix |
|------|-------|-----|
| Missing `[DisallowMultipleComponent]` | Component can be accidentally added twice | Add attribute to components that must be unique per GameObject |
| Inconsistent Event Naming | Mix of `OnX`, `XEvent`, `XHappened` conventions | Standardize: `On{Verb}{Subject}` for C# events, `{Subject}{Verb}` for SO channels |
| No Architecture Decision Records | Design choices undocumented — future devs don't know why | Add ADR for DI framework choice, event pattern, scene strategy |

---

## SOLID Quick-Reference

| Principle | Violation Signal | Fix |
|-----------|-----------------|-----|
| **SRP** | Class has 3+ reasons to change, or mixes UI + logic + data | Extract into focused classes — one responsibility each |
| **OCP** | Adding a feature requires modifying existing switch/if chains | Use polymorphism, strategy, or visitor; extend via new classes |
| **LSP** | Subclass throws `NotImplementedException` or ignores base contract | Redesign hierarchy — if substitution breaks, inheritance is wrong |
| **ISP** | Interface has 8+ methods, implementors stub half of them | Split into focused interfaces (`IReadable`, `IWritable`) |
| **DIP** | High-level module `using` low-level module's namespace directly | Depend on abstractions; inject via interface, not concrete class |

## Dependency Management Verdict

| Pattern | When to Use | Risk |
|---------|-------------|------|
| Constructor Injection | Default for all services | Low — explicit, testable |
| `[Inject]` Field | MonoBehaviours (no constructor) | Medium — hidden deps |
| Service Locator | Bootstrap/composition root only | High if leaked into business logic |
| Static Singleton | Truly global, no-teardown systems (e.g., Logger) | High — untestable, couples everything |
| SO Channel | Cross-scene, decoupled events | Low — fire-and-forget, no ref needed |

## Communication Pattern Selection

| Pattern | Coupling | When to Use |
|---------|----------|-------------|
| Direct Call | High | Same module, synchronous, simple |
| C# Event | Medium | Publisher doesn't know subscribers, same assembly |
| UnityEvent | Medium | Designer-configurable in Inspector |
| SO Channel | Low | Cross-scene, cross-assembly, fire-and-forget |
| Message Bus | Low | Complex routing, filtering, many-to-many |
| Interface Callback | Medium | Need return value from subscriber |

## Coupling Health Indicators

**🔴 Red Flags:**
- Changing one module breaks 3+ others
- Circular `using` statements between namespaces
- Test setup requires instantiating 5+ dependencies
- Can't describe module's job in one sentence
- Merge conflicts on same file from unrelated features

**🟢 Healthy Signs:**
- Modules testable in isolation with simple mocks
- New feature = new files, minimal edits to existing
- Assembly compile times under 3 seconds
- Clear dependency direction (UI → Game → Core → Shared)
- Each assembly has a one-line purpose in its `.asmdef`

---

## PR Investigation Commands

```bash
# Find circular assembly references
grep -r "reference" Assets/**/*.asmdef | sort

# Find singleton access patterns
grep -rn "\.Instance\." Assets/Scripts/ --include="*.cs"

# Find direct FindObjectOfType usage
grep -rn "FindObjectOfType" Assets/Scripts/ --include="*.cs"

# Find event subscriptions without cleanup
grep -rn "+=" Assets/Scripts/ --include="*.cs" | grep -v "test\|Test"
```

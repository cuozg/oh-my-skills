# Blueprint Review Checklist

Load this reference when PR introduces new systems, refactors architecture, or changes design patterns. Covers high-level design, SOLID principles, Unity architecture, and system-level concerns. Each issue follows: **Issue → Evidence → Why → Fix → Priority**.

---

## Table of Contents

1. [Architecture & SOLID](#1-architecture--solid)
2. [Unity Architecture Patterns](#2-unity-architecture-patterns)
3. [System Design](#3-system-design)
4. [API Design](#4-api-design)
5. [Dependency Management](#5-dependency-management)
6. [Investigation Patterns](#6-investigation-patterns)

---

## 1. Architecture & SOLID

### 🔴 Critical

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **God class** | Single class >500 lines with 5+ responsibilities | Impossible to test, maintain, or extend; merge conflict magnet | Extract responsibilities into focused classes | 🔴 Critical |
| **Circular dependency** | Class A depends on B, B depends on A (directly or transitively) | Compilation issues; tight coupling; refactor cascades | Introduce interface or event at the boundary | 🔴 Critical |

### 🟡 Major

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Single Responsibility violation** | Class handles both data fetching and UI rendering | Changes to one concern break the other; hard to test | Split into separate data and presentation classes | 🟡 Major |
| **Open/Closed violation** | Adding new behavior requires modifying existing class (switch/if-else chain) | Every new feature risks breaking existing features | Strategy pattern, polymorphism, or ScriptableObject config | 🟡 Major |
| **Liskov Substitution violation** | Derived class overrides method with different semantics or throws unexpected exceptions | Callers can't trust base type contract | Respect base contract; prefer composition over inheritance | 🟡 Major |
| **Interface Segregation violation** | Interface has 10+ methods; implementors leave half empty | Implementors forced to depend on methods they don't use | Split into focused interfaces: `IReadable`, `IWritable` | 🟡 Major |
| **Dependency Inversion violation** | High-level module directly `new`s low-level dependencies | Untestable; can't swap implementations | Inject via constructor, `[SerializeField]`, or service locator | 🟡 Major |
| **Feature envy** | Method mostly accesses data/methods of another class | Logic in wrong place; tight coupling | Move method to the class it envies | 🟡 Major |

### 🔵 Minor

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Premature abstraction** | Interface with single implementation and no test mocks | Unnecessary complexity; YAGNI | Remove interface until second consumer exists | 🔵 Minor |
| **Deep inheritance** | 4+ levels of inheritance | Fragile base class problem; hard to understand behavior | Prefer composition; flatten hierarchy | 🔵 Minor |

---

## 2. Unity Architecture Patterns

### 🟡 Major

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Singleton abuse** | `public static Instance` pattern for non-infrastructure classes | Hidden global state; untestable; initialization order issues | ScriptableObject channels, dependency injection, or service locator | 🟡 Major |
| **MonoBehaviour as data class** | MonoBehaviour with only fields, no behavior | Unnecessary scene dependency; can't exist without GameObject | Use plain C# class, struct, or ScriptableObject | 🟡 Major |
| **Manager of managers** | One "GameManager" controlling all subsystems directly | God object; everything coupled through one class | Decompose into independent systems communicating via events/SO channels | 🟡 Major |
| **Update polling** | `Update()` checking boolean/state every frame instead of reacting to change | Wasted CPU on 99% of frames where nothing changed | Event-driven: `Action`, `UnityEvent`, or SO event channel | 🟡 Major |
| **Component doing too much** | MonoBehaviour handling input, animation, physics, and audio | Violates SRP; impossible to reuse or test parts | Split into `InputHandler`, `AnimationController`, `AudioPlayer` etc. | 🟡 Major |
| **ScriptableObject as runtime state** | SO used to store per-session mutable state without cloning | State leaks between Editor sessions; affects all references | Clone at runtime: `Instantiate(configSO)` or use plain C# for runtime state | 🟡 Major |

### 🔵 Minor

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **String-based messaging** | `SendMessage("MethodName")` or `BroadcastMessage` | No compile-time checking; reflection overhead; silently fails | Direct reference, interface, or event | 🔵 Minor |
| **Resources folder usage** | Assets in `Resources/` folder | All Resources assets load at startup; can't be stripped | Use Addressables or direct references | 🔵 Minor |

---

## 3. System Design

### 🔴 Critical

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **No error recovery path** | System has no fallback for network/IO/dependency failure | Complete feature failure on any transient error | Add retry, fallback, or graceful degradation | 🔴 Critical |
| **Unbounded collection growth** | List/Dictionary grows without limit (e.g., event history, cache, log) | OOM over long sessions | Add max capacity, LRU eviction, or periodic cleanup | 🔴 Critical |

### 🟡 Major

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Synchronous blocking on main thread** | `Task.Result`, `Task.Wait()`, synchronous file I/O on main thread | Frame freeze; ANR on mobile | Use `async/await`, coroutines, or background thread | 🟡 Major |
| **Missing cancellation** | Long-running async operation with no `CancellationToken` | Can't cancel on scene change or object destruction | Pass and check `CancellationToken`; cancel in `OnDestroy` | 🟡 Major |
| **State machine without explicit states** | Multiple booleans controlling flow: `isLoading`, `isReady`, `isError` | Invalid state combinations possible (loading + error) | Use enum state or state machine pattern | 🟡 Major |
| **Hardcoded configuration** | Server URLs, timing values, feature flags in code | Requires recompile to change; no per-environment config | Extract to ScriptableObject, config file, or remote config | 🟡 Major |
| **Missing idempotency** | Operation that can be triggered multiple times (button, event) without guard | Duplicate actions, data corruption, visual glitches | Add guard: `if (_processing) return; _processing = true;` | 🟡 Major |

---

## 4. API Design

### 🔴 Critical

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Breaking public API** | Method signature changed on public/internal member | All callers break; downstream assemblies fail | Add overload preserving old signature; deprecate old one | 🔴 Critical |
| **Removed public member** | Public method/property/field deleted | Compile errors across codebase | Deprecate first (`[Obsolete]`); remove in next major version | 🔴 Critical |

### 🟡 Major

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Boolean parameter** | `void DoThing(bool useNewMode)` | Unclear at call site: `DoThing(true)` — true what? | Use enum, separate methods, or builder pattern | 🟡 Major |
| **Output parameter overuse** | `void GetResult(out int x, out string y, out bool z)` | Hard to use; error-prone | Return struct or tuple | 🟡 Major |
| **Side effects in property getter** | Property `get` that modifies state, triggers events, or does I/O | Violates principle of least surprise; debugger calls getters | Make it a method; properties should be lightweight | 🟡 Major |
| **Inconsistent naming** | `GetItems()` vs `FetchData()` vs `LoadContent()` for similar operations | Confusing API surface | Standardize verbs: `Get` (sync), `Load` (async), `Fetch` (remote) | 🟡 Major |

---

## 5. Dependency Management

### 🟡 Major

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Assembly-crossing dependency** | Script in `Assembly-CSharp` depends on internal of another asmdef | Breaks compilation if assembly changes | Use public interface; add assembly reference in `.asmdef` | 🟡 Major |
| **Missing asmdef boundary** | Large feature with no Assembly Definition | Slower compile; no encapsulation; everything is public | Create `.asmdef` for the feature; expose only public API | 🟡 Major |
| **Third-party update risk** | Direct usage of third-party API without abstraction layer | Library update breaks all callsites | Wrap in adapter/facade | 🟡 Major |

---

## 6. Investigation Patterns

### New System/Feature Review

When reviewing a new system or major feature:

```bash
# How many files/lines is this system?
find Assets/Scripts/NewFeature/ -name "*.cs" | wc -l
find Assets/Scripts/NewFeature/ -name "*.cs" -exec cat {} \; | wc -l

# What does it depend on?
grep -rn "using " Assets/Scripts/NewFeature/ --include="*.cs" | grep -v "System" | sort -u

# Who depends on it already?
grep -rn "NewFeatureNamespace" Assets/Scripts/ --include="*.cs" | grep -v "NewFeature/"

# Singleton check
grep -rn "static.*Instance" Assets/Scripts/NewFeature/ --include="*.cs"

# Update/FixedUpdate usage (performance surface)
grep -rn "void Update\|void FixedUpdate\|void LateUpdate" Assets/Scripts/NewFeature/ --include="*.cs"
```

### Architecture Decision Verification

When a PR claims to implement a specific pattern:

```bash
# Verify interface segregation
grep -rn "interface I" Assets/Scripts/NewFeature/ --include="*.cs"

# Count methods per interface (flag if >7)
grep -A50 "interface I" Assets/Scripts/NewFeature/*.cs | grep -c ";"

# Check for concrete dependencies (should use interfaces)
grep -rn "new.*Controller\|new.*Manager\|new.*Service" Assets/Scripts/NewFeature/ --include="*.cs"

# Event-driven check (vs polling)
grep -rn "event\|Action<\|UnityEvent" Assets/Scripts/NewFeature/ --include="*.cs"
```

### Report Format

```markdown
🟡 **Architecture: [Pattern Name]**: [What's wrong in one line]

**Evidence**: [Concrete file/class/method showing the issue]
**Why**: [Impact on testability, maintainability, or performance]
**Recommendation**: [Specific refactoring with class names]
```

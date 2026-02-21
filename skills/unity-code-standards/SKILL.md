---
name: unity-code-standards
description: "Unity C# coding standards, architecture patterns (VContainer DI, SignalBus events), and code review guidelines. Enforces 4-priority quality gates: code hygiene, modern C#, Unity architecture, and performance."
---

# Unity C# Development Standards

Comprehensive coding standards for Unity C# development. Covers code quality, modern C# patterns, Unity architecture (VContainer + SignalBus), and performance optimization.

## How to Use This Skill

This skill is a **reference library**. Load specific references based on the task:

- **Writing new code** → Load relevant C# + Unity references
- **Reviewing code** → Load relevant review references
- **Fixing issues** → Load the specific category reference

## Priority System

All rules follow a 4-priority hierarchy. Higher priority = more important to enforce.

### Priority 1: Code Quality & Hygiene
**Non-negotiable basics that prevent bugs and maintain readability.**

| Rule | Quick Check |
|:-----|:-----------|
| Enable `<Nullable>enable</Nullable>` | All projects, all files |
| Least accessible modifier | `private` > `internal` > `public` |
| Fix all warnings | Treat warnings as errors |
| Throw exceptions for errors | Never return default, never swallow |
| ILogger for runtime logging | Inject via DI; handles conditional compilation and prefixes automatically |
| Debug.Log only in `#if UNITY_EDITOR` | Never in runtime code |
| No logging in constructors | Keep constructors fast and side-effect free |

**Full reference:** [quality-hygiene.md](references/csharp/quality-hygiene.md)

### Priority 2: Modern C# Patterns
**Leverage modern C# for cleaner, safer, more expressive code.**

| Rule | Quick Check |
|:-----|:-----------|
| LINQ over manual loops | `Where`, `Select`, `Any`, `All`, `FirstOrDefault` |
| Expression-bodied members | Single-expression methods, properties, operators |
| Null-coalescing (`??`, `??=`, `?.`) | Replace null checks with operators |
| Pattern matching (`is`, `switch`) | Replace type checks and casts |
| String interpolation `$""` | Replace `string.Format` and concatenation |
| `var` for obvious types | `var list = new List<string>()` |
| Init-only / required properties | Immutable data objects |
| Raw string literals | Multi-line strings, JSON, regex |
| Collection expressions `[..]` | Replace `new List<T> { }` |
| Global using directives | Common namespaces in one file |
| File-scoped namespaces | One less indentation level |

**Full reference:** [modern-csharp-features.md](references/csharp/modern-csharp-features.md)
**LINQ patterns:** [linq-patterns.md](references/csharp/linq-patterns.md)

### Priority 3: Unity Architecture
**Consistent architecture using VContainer + SignalBus.**

#### Framework Stack: VContainer + SignalBus

| Concern | Tool | Pattern |
|:--------|:-----|:--------|
| Dependency Injection | VContainer | `[Inject]` / `[Preserve]` + LifetimeScope |
| Event Communication | SignalBus | `SignalBus.Fire<T>()` / `SignalBus.Subscribe<T>()` |
| Async Operations | UniTask | `async UniTask` / `UniTaskVoid` for fire-and-forget |
| Data Management | Data Controllers | `IDataController` → `IReadOnlyReactiveProperty<T>` |

**Key patterns:**

```csharp
// VContainer injection
public sealed class GameService : IInitializable
{
    [Preserve] // Required for VContainer
    public GameService(ILogger logger, SignalBus signalBus)
    {
        this.logger = logger;
        this.signalBus = signalBus;
    }

    public void Initialize()
    {
        this.signalBus.Subscribe<GameStartedSignal>(this.OnGameStarted);
    }
}

// SignalBus events (struct signals)
public readonly record struct GameStartedSignal(int Level);

// Firing
this.signalBus.Fire(new GameStartedSignal(1));
```

**Full references:**
- [vcontainer-di.md](references/unity/vcontainer-di.md)
- [signalbus-events.md](references/unity/signalbus-events.md)
- [data-controllers.md](references/unity/data-controllers.md)
- [integration-patterns.md](references/unity/integration-patterns.md)
- [unitask-patterns.md](references/unity/unitask-patterns.md)

### Priority 4: Performance & Review
**Optimize hot paths, minimize allocations, enforce review checklists.**

| Rule | Quick Check |
|:-----|:-----------|
| No allocations in Update/FixedUpdate | Cache everything, use pools |
| Cache component references | `GetComponent` in Awake, not Update |
| Use `CompareTag()` not `== "tag"` | Avoids string allocation |
| Prefer `TryGetComponent` | Returns bool, no exception on miss |
| Pool frequently spawned objects | `ObjectPool<T>` or custom pools |
| Avoid LINQ in hot paths | Manual loops for per-frame code |
| Use `NativeArray` for large data | Burst-compatible, no GC |

**Full references:**
- [performance-optimizations.md](references/csharp/performance-optimizations.md)
- [architecture-review.md](references/review/architecture-review.md)
- [csharp-quality.md](references/review/csharp-quality.md)
- [performance-review.md](references/review/performance-review.md)
- [unity-specifics.md](references/review/unity-specifics.md)

## Assembly Definition Structure

```
YourProject.Core/          # Shared interfaces, models, utils
YourProject.Services/      # Business logic services
YourProject.UI/            # UI controllers and views
YourProject.Editor/        # Editor-only tools
```

Each assembly should:
- Have a `.asmdef` file
- Reference only what it needs
- Use `internal` by default, `[InternalsVisibleTo]` for tests

## Logging Standards

**ILogger** (project-level abstraction injected via DI):
- ✅ Handles conditional compilation internally (no `#if` guards needed)
- ✅ Handles prefixes automatically (no `[ClassName]` needed)
- ❌ NEVER log in constructors
- ❌ NEVER use `this.logger?.Method()` — DI guarantees non-null
- ❌ NEVER use Debug.Log in runtime code

**Debug.Log**: ONLY in `#if UNITY_EDITOR` blocks for editor tools.

**Exceptions**: Throw for errors — never log-and-continue.

> **Note:** Adapt the ILogger interface to your project's choice (e.g., `Microsoft.Extensions.Logging.ILogger`, Serilog, or a custom wrapper). The key principle is: inject a logger via DI, don't use static logging methods.

## Quick Decision Trees

### "Should I use field injection or constructor injection?"
→ **Constructor injection** (always). Field `[Inject]` only for MonoBehaviours where constructors don't work.

### "Should I use events or direct method calls?"
→ **SignalBus** for cross-system communication. Direct calls for same-system internal logic.

### "Should I use async/await or coroutines?"
→ **UniTask** for all new async code. Coroutines only for legacy code maintenance.

### "Should I cache this?"
→ If called more than once per frame: **yes, cache it**.

## Reference Index

### C# References
| File | Content |
|:-----|:--------|
| [quality-hygiene.md](references/csharp/quality-hygiene.md) | Nullable, access modifiers, logging, exceptions |
| [linq-patterns.md](references/csharp/linq-patterns.md) | LINQ usage, common patterns, anti-patterns |
| [modern-csharp-features.md](references/csharp/modern-csharp-features.md) | C# 9-12 features, expression bodies, pattern matching |
| [performance-optimizations.md](references/csharp/performance-optimizations.md) | Allocation reduction, caching, pooling |

### Unity References
| File | Content |
|:-----|:--------|
| [vcontainer-di.md](references/unity/vcontainer-di.md) | VContainer DI patterns, LifetimeScope, registration |
| [signalbus-events.md](references/unity/signalbus-events.md) | SignalBus event patterns, signal structs |
| [data-controllers.md](references/unity/data-controllers.md) | Data controller pattern, reactive properties |
| [integration-patterns.md](references/unity/integration-patterns.md) | Cross-system integration, service patterns |
| [unitask-patterns.md](references/unity/unitask-patterns.md) | UniTask async patterns, cancellation, error handling |

### Review References
| File | Content |
|:-----|:--------|
| [architecture-review.md](references/review/architecture-review.md) | Architecture review checklist |
| [csharp-quality.md](references/review/csharp-quality.md) | C# quality review checklist |
| [performance-review.md](references/review/performance-review.md) | Performance review checklist |
| [unity-specifics.md](references/review/unity-specifics.md) | Unity-specific review checklist |

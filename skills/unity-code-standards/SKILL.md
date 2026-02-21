---
name: unity-code-standards
description: "Unity C# coding standards and code review guidelines. Enforces 4-priority quality gates: code hygiene, modern C#, Unity best practices, and performance."
---

# Unity C# Development Standards

Comprehensive coding standards for Unity C# development. Covers code quality, modern C# patterns, Unity best practices, and performance optimization.

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
| ILogger for runtime logging | Use project-level logging abstraction; handles conditional compilation and prefixes automatically |
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

### Priority 3: Unity Best Practices
**Consistent architecture patterns for Unity development.**

| Rule | Quick Check |
|:-----|:-----------|
| Use dependency injection | Constructor injection for services; avoid `FindObjectOfType` and static singletons |
| Event-driven communication | C# events, delegates, or event bus for cross-system decoupling |
| Async with UniTask | `async UniTask` with `CancellationToken`; no `async void`; no coroutines for new code |
| Interface-based design | Depend on abstractions, not concrete implementations |
| Single responsibility | One purpose per class; split when a class does too many things |

**Full reference:** [unitask-patterns.md](references/unity/unitask-patterns.md)

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

**ILogger** (project-level logging abstraction):
- ✅ Handles conditional compilation internally (no `#if` guards needed)
- ✅ Handles prefixes automatically (no `[ClassName]` needed)
- ❌ NEVER log in constructors
- ❌ NEVER use `this.logger?.Method()` — Ensure logger is always initialized
- ❌ NEVER use Debug.Log in runtime code

**Debug.Log**: ONLY in `#if UNITY_EDITOR` blocks for editor tools.

**Exceptions**: Throw for errors — never log-and-continue.

> **Note:** Adapt the ILogger interface to your project's logging solution. The key principle is: use a project-level logging abstraction, don't scatter Debug.Log calls throughout runtime code.

## Quick Decision Trees

### "Should I use field injection or constructor injection?"
→ **Constructor injection** for services. For MonoBehaviours, use initialization methods or `[SerializeField]` references.

### "Should I use events or direct method calls?"
→ **Events** (C# events, delegates, or event bus) for cross-system communication. Direct calls for same-system internal logic.

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
| [unitask-patterns.md](references/unity/unitask-patterns.md) | UniTask async patterns, cancellation, error handling |

### Review References
| File | Content |
|:-----|:--------|
| [logic-review-patterns.md](references/review/logic-review-patterns.md) | Comprehensive logic review patterns — performance, async, state, data flow, concurrency, edge cases |
| [architecture-review.md](references/review/architecture-review.md) | Architecture review checklist |
| [csharp-quality.md](references/review/csharp-quality.md) | C# quality review checklist |
| [performance-review.md](references/review/performance-review.md) | Performance review checklist |
| [unity-specifics.md](references/review/unity-specifics.md) | Unity-specific review checklist |

---
name: unity-code-shared
description: "Unity C# coding standards and code review guidelines. Enforces 4-priority quality gates: code hygiene, modern C#, Unity best practices, and performance. Not intended to be activated directly — loaded by code and review skills as needed."
---

# Unity C# Development Standards

Comprehensive coding standards for Unity C# development. Covers code quality, modern C# patterns, Unity best practices, and performance optimization.

## Output
Code review feedback and C# code following the 4-priority quality gates defined below.

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

**Full reference:** [unitask-patterns-part1.md](references/unity/unitask-patterns-part1.md) and [unitask-patterns-part2.md](references/unity/unitask-patterns-part2.md)

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
- [performance-optimizations-part1.md](references/csharp/performance-optimizations-part1.md)
- [performance-optimizations-part2.md](references/csharp/performance-optimizations-part2.md)
- [architecture-review.md](references/review/architecture-review.md)
- [csharp-quality.md](references/review/csharp-quality.md)
- [performance-review.md](references/review/performance-review.md)
- [unity-specifics.md](references/review/unity-specifics.md)

 [decision-trees.md](references/decision-trees.md) — Assembly structure, decision trees, quick reference guidance
 [reference-index.md](references/reference-index.md) — Complete index of C#, Unity, and review references
 [SCRIPT_TEMPLATE.md](references/SCRIPT_TEMPLATE.md) — Starting template for every new script (Plain C# Service + MonoBehaviour)
 [patterns-core.md](references/patterns-core.md) — Service with Events, State with Read-Only Interface, MonoBehaviour View
 [patterns-advanced.md](references/patterns-advanced.md) — Async/UniTask, State Machine, ScriptableObject Config, Cleanup & CTS

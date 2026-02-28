# Architecture Review Patterns

Cross-cutting architecture review. Always load alongside `unity-shared` skill.

## 🔴 Critical

| Pattern | Issue | Fix |
|:--------|:------|:----|
| Circular assembly dependency introduced | Build breaks or fragile coupling | Refactor shared types to Core assembly |
| Service directly references MonoBehaviour (non-injected) | Untestable, tight coupling | Inject via interface or use events |
| `new Service()` instead of DI registration | Bypasses dependency graph, untestable | Use dependency injection |
| Public mutable state on injected service | Race conditions, unpredictable behavior | Use encapsulated methods or read-only interfaces |
| Event firing inside constructor or field initializer | Event subscribers not yet registered | Move to Initialize() or Start() |
| Breaking change to event data type (renamed/removed fields) | All subscribers silently break | Add new event type, deprecate old |

## 🟡 High

| Pattern | Issue | Fix |
|:--------|:------|:----|
| Direct coupling between systems that should use events | Tight coupling, hard to test/extend | Replace with event-based communication |
| Field injection instead of constructor injection (non-MonoBehaviour) | Hidden dependency, harder to test | Use constructor injection |
| Singleton pattern used where DI service would suffice | Global state, test difficulty | Convert to scoped/singleton service via DI |
| Event subscription without corresponding unsubscription | Memory leak, stale callbacks | Add unsubscribe in OnDisable/OnDestroy/Dispose |
| Data access bypassing proper interfaces | Inconsistent state, no change notification | Route through data access interfaces |
| Assembly .asmdef missing required reference for new using | Compile error in CI even if IDE resolves it | Add assembly reference |

## 🔵 Medium

| Pattern | Issue | Fix |
|:--------|:------|:----|
| God class (>500 lines, multiple responsibilities) | Hard to maintain, test, extend | Extract responsibilities into focused classes |
| Service with 5+ constructor parameters | Too many responsibilities | Split service or introduce facade |
| using statements referencing implementation assemblies | Coupling to implementation, not interface | Depend on abstraction assembly only |
| Magic strings for event names | Typo-prone, no compile-time safety | Use nameof() or typed events |
| Inconsistent async pattern (mixing UniTask, Task, coroutine) | Confusion, potential deadlocks | Standardize on UniTask |

## 🟢 Low

- Minor naming inconsistency in event data types
- Slightly suboptimal DI registration order
- Missing XML doc on internal service method

## Cross-System Dependency Checks

When a PR modifies multiple systems:
1. Trace the dependency graph: does System A now depend on System B AND vice versa?
2. Check if new `using` statements introduce unwanted coupling
3. Verify event fire → subscribe chains are complete (no orphan events)
4. Check data access patterns — no direct field mutation from outside

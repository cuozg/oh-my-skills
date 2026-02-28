# Architecture Review

Cross-cutting architecture review. Always load alongside `unity-shared` skill.

## Dependency Injection

### Dependency Injection
- [ ] Constructor injection used for services (not field injection or service locators)
- [ ] Dependencies provided through abstractions (interfaces), not concrete implementations
- [ ] No `FindObjectOfType<T>()` for resolving dependencies
- [ ] No static singletons for services that could be injected
- [ ] Circular dependencies resolved via interfaces or events

## Event Architecture

### Event Architecture
- [ ] Cross-system communication uses events (C# events, delegates, or event bus)
- [ ] Event naming follows conventions (e.g., `OnPlayerDied`, `PlayerDiedEvent`)
- [ ] Subscribe/unsubscribe always paired (subscribe in OnEnable, unsubscribe in OnDisable)
- [ ] No lambda subscriptions if unsubscription is needed
- [ ] Event handlers are fast (no heavy computation)
- [ ] No circular event chains
- [ ] Event data is immutable where possible

## Assembly Structure

### Assembly Definitions
- [ ] Each module has its own `.asmdef`
- [ ] References are minimal (only what's needed)
- [ ] `internal` by default, `[InternalsVisibleTo]` for tests
- [ ] No circular assembly references
- [ ] Editor assemblies don't reference runtime assemblies unnecessarily

### Namespace Conventions
- [ ] File-scoped namespaces
- [ ] Namespace matches folder structure
- [ ] One type per file (with exception for small related types)

## Initialization Order
- [ ] Explicit initialization sequence (not relying on undefined Awake/Start ordering)
- [ ] No `FindObjectOfType` during initialization
- [ ] Configuration loaded before dependent systems initialize

## Module Boundaries
- [ ] Clear module boundaries with proper assembly definitions
- [ ] Cross-module communication via events or shared interfaces (not direct references)
- [ ] Shared types in Core assembly
- [ ] No circular module dependencies
- [ ] Each module can be tested independently

## Scene Architecture
- [ ] Scene-scoped services cleaned up on scene transition
- [ ] Global services persist across scenes properly
- [ ] Scene transition via service (not direct `SceneManager` calls)
- [ ] No hardcoded scene names (use constants or ScriptableObject)

## 🔴 Critical Patterns & Fixes

| Pattern | Issue | Fix |
|:--------|:------|:----|
| Circular assembly dependency introduced | Build breaks or fragile coupling | Refactor shared types to Core assembly |
| Service directly references MonoBehaviour (non-injected) | Untestable, tight coupling | Inject via interface or use events |
| `new Service()` instead of DI registration | Bypasses dependency graph, untestable | Use dependency injection |
| Public mutable state on injected service | Race conditions, unpredictable behavior | Use encapsulated methods or read-only interfaces |
| Event firing inside constructor or field initializer | Event subscribers not yet registered | Move to Initialize() or Start() |
| Breaking change to event data type (renamed/removed fields) | All subscribers silently break | Add new event type, deprecate old |

## 🟡 High Priority Patterns & Fixes

| Pattern | Issue | Fix |
|:--------|:------|:----|
| Direct coupling between systems that should use events | Tight coupling, hard to test/extend | Replace with event-based communication |
| Field injection instead of constructor injection (non-MonoBehaviour) | Hidden dependency, harder to test | Use constructor injection |
| Singleton pattern used where DI service would suffice | Global state, test difficulty | Convert to scoped/singleton service via DI |
| Event subscription without corresponding unsubscription | Memory leak, stale callbacks | Add unsubscribe in OnDisable/OnDestroy/Dispose |
| Data access bypassing proper interfaces | Inconsistent state, no change notification | Route through data access interfaces |
| Assembly .asmdef missing required reference for new using | Compile error in CI even if IDE resolves it | Add assembly reference |

## 🔵 Medium Priority Patterns & Fixes

| Pattern | Issue | Fix |
|:--------|:------|:----|
| God class (>500 lines, multiple responsibilities) | Hard to maintain, test, extend | Extract responsibilities into focused classes |
| Service with 5+ constructor parameters | Too many responsibilities | Split service or introduce facade |
| using statements referencing implementation assemblies | Coupling to implementation, not interface | Depend on abstraction assembly only |
| Magic strings for event names | Typo-prone, no compile-time safety | Use nameof() or typed events |
| Inconsistent async pattern (mixing UniTask, Task, coroutine) | Confusion, potential deadlocks | Standardize on UniTask |

## 🟢 Low Priority Patterns

- Minor naming inconsistency in event data types
- Slightly suboptimal DI registration order
- Missing XML doc on internal service method

## Anti-Patterns to Flag

### Critical
- Service locator pattern
- Static singletons for services that should be injected
- `FindObjectOfType` for dependency resolution
- God class (class doing too many things)
- Circular dependencies

### Major
- Event subscription without corresponding unsubscription
- Missing sealed on non-inheritable classes
- Assembly .asmdef missing required reference

### Minor
- Over-injection (too many dependencies → split class)
- Public members that should be internal
- Missing interface for testable services

## Cross-System Dependency Checks

When a PR modifies multiple systems:
1. Trace the dependency graph: does System A now depend on System B AND vice versa?
2. Check if new `using` statements introduce unwanted coupling
3. Verify event fire → subscribe chains are complete (no orphan events)
4. Check data access patterns — no direct field mutation from outside

# Architecture Review Checklist

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

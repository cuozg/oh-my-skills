# Architecture Review Checklist

## Dependency Injection

### VContainer Patterns
- [ ] Constructor injection used (not field `[Inject]`) for non-MonoBehaviour classes
- [ ] `[Preserve]` attribute on constructors for VContainer
- [ ] `[Inject]` method used for MonoBehaviours (not field injection)
- [ ] Dependencies registered in appropriate LifetimeScope
- [ ] Correct lifetime chosen (Singleton vs Transient)
- [ ] No service locator pattern (`Container.Resolve<T>()`)
- [ ] No `FindObjectOfType<T>()` for dependencies
- [ ] No static singletons for DI-managed services
- [ ] Circular dependencies resolved via signals or interfaces

### Registration
- [ ] Interface → implementation bindings where appropriate
- [ ] Entry points registered with `RegisterEntryPoint<T>()`
- [ ] ScriptableObject configs registered as instances
- [ ] No over-registration (only register what's needed)

## Event Architecture

### SignalBus
- [ ] Signals are `readonly record struct` (not class)
- [ ] Signal naming: `[Subject][Verb-PastTense]Signal`
- [ ] Subscribe in `Initialize()`, unsubscribe in `Dispose()`
- [ ] No lambda subscriptions (can't unsubscribe)
- [ ] No signal firing in constructors
- [ ] Signal handlers are fast (no heavy computation)
- [ ] No circular signal chains (A→B→A)
- [ ] Signal data is immutable (no mutable reference types)

## Data Controller Pattern

- [ ] Interface exposes `IReadOnlyReactiveProperty<T>` only
- [ ] Implementation uses `ReactiveProperty<T>` internally
- [ ] Implements `IDisposable` to clean up reactive properties
- [ ] Input validation with exceptions (not logging)
- [ ] Single responsibility (one domain per controller)
- [ ] No business logic in data controllers (state management only)
- [ ] No MonoBehaviour inheritance (plain C# class)

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

- [ ] `IInitializable` used for post-injection setup
- [ ] No dependency on Unity lifecycle ordering (`Awake` order)
- [ ] Explicit initialization sequence in bootstrap
- [ ] No `FindObjectOfType` during initialization
- [ ] No `Resources.Load` during initialization (use DI-provided configs)

## Module Boundaries

- [ ] Clear module boundaries with separate LifetimeScopes
- [ ] Cross-module communication via SignalBus (not direct reference)
- [ ] Shared types in Core assembly
- [ ] No circular module dependencies
- [ ] Each module can be tested independently

## Scene Architecture

- [ ] One root LifetimeScope per scene
- [ ] Scene-specific services scoped to scene LifetimeScope
- [ ] Global services in root LifetimeScope (DontDestroyOnLoad)
- [ ] Scene transition via service (not direct `SceneManager` calls)
- [ ] No hardcoded scene names (use constants or ScriptableObject)

## Anti-Patterns to Flag

### Critical
- Service locator pattern
- Static singletons for DI-managed services
- `FindObjectOfType` for dependency resolution
- God class (class doing too many things)
- Circular dependencies

### Major
- Field injection instead of constructor injection
- Missing `[Preserve]` on VContainer constructors
- Mutable signal data
- Lambda signal subscriptions
- Missing unsubscribe/Dispose

### Minor
- Over-injection (too many dependencies → split class)
- Missing `sealed` on non-inheritable classes
- Public members that should be internal
- Missing interface for testable services

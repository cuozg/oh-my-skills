# Architecture & Design Checklist

## SOLID Principles

### Single Responsibility
- [ ] Each class has ONE reason to change
- [ ] MonoBehaviours < 300 lines (flag > 500 as God class)
- [ ] No class handles both UI logic and business logic
- [ ] Managers/Controllers don't mix data persistence with gameplay logic

### Open/Closed
- [ ] Systems extensible without modifying core code
- [ ] ScriptableObject-based configuration for tuning
- [ ] Event-driven communication between systems
- [ ] Strategy/Template patterns used where behavior varies

### Liskov Substitution
- [ ] Derived classes don't break base class contracts
- [ ] Virtual methods have clear contracts documented
- [ ] No `is`/`as` type checks cascading in base class consumers

### Interface Segregation
- [ ] Interfaces are focused (< 5 methods)
- [ ] No "fat" interfaces forcing empty implementations
- [ ] Consumers depend on only what they use

### Dependency Inversion
- [ ] High-level modules don't depend on low-level details
- [ ] Dependencies injected or configured via SO, not hardcoded
- [ ] Concrete types referenced at composition root, not throughout codebase

## Architecture Patterns

### Dependency Management
| Pattern | Verdict | Check |
|:--------|:--------|:------|
| Direct singleton access everywhere | :red_circle: | Find `*.Instance.` pattern count |
| Service locator with registration | :yellow_circle: | Acceptable if well-organized |
| DI framework (any) | :white_circle: | Check proper scope/lifetime config |
| ScriptableObject injection | :white_circle: | Check asset references not null in builds |
| Interface-based decoupling | :white_circle: | Verify interfaces aren't over-abstracted |

### Communication Patterns
| Pattern | Check |
|:--------|:------|
| Direct method calls | Acceptable for parent-child, flag tight coupling otherwise |
| C# events/delegates | Check subscribe/unsubscribe pairing |
| UnityEvent | Check serialized listener validity, performance in hot paths |
| ScriptableObject event channels | Check listener registration lifecycle |
| Static event bus | Flag if no unsubscribe mechanism or type safety |
| SendMessage/BroadcastMessage | :red_circle: Flag always — reflection, no compile-time safety |

### Layer Architecture
- [ ] Clear separation: Data / Logic / Presentation
- [ ] No circular dependencies between layers
- [ ] Assembly definitions enforce layer boundaries
- [ ] Editor code isolated from runtime assemblies

## Assembly Definitions

- [ ] Every folder with scripts has appropriate .asmdef
- [ ] Editor scripts in separate Editor assemblies
- [ ] Test scripts in separate Test assemblies
- [ ] No circular assembly references
- [ ] Assembly references are minimal (not referencing everything)
- [ ] Platform-specific code in platform-filtered assemblies
- [ ] Third-party code isolated in own assemblies

## Coupling Analysis

### Tight Coupling Red Flags
- Direct `GetComponent<ConcreteType>()` for cross-system communication
- Multiple systems reading/writing same static field
- Concrete class references across unrelated systems
- Chain of `transform.parent.parent.GetComponent<X>()` navigation
- Hard-coded scene names, tag strings, layer numbers scattered

### Healthy Coupling Indicators
- Interface-based dependencies
- Event-driven decoupling between systems
- ScriptableObject configuration/channels
- Assembly definitions enforcing boundaries
- Dependency injection at composition root

## Scalability Concerns

- [ ] No O(n^2) or worse algorithms in core systems
- [ ] Collection sizes bounded or documented
- [ ] Entity/object counts have pooling strategy
- [ ] Scene loading strategy scales (additive scenes, Addressables)
- [ ] Data loading handles growth (pagination, streaming, lazy load)

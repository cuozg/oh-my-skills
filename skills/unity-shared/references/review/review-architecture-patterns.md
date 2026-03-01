# Architecture Review — PR Checklist

> Authoritative for: DI, events, assemblies, module boundaries, scene architecture, coupling, SOLID.
> Cross-ref: `review-csharp.md` (namespace hygiene), `review-general-checklists.md` (lifecycle)

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

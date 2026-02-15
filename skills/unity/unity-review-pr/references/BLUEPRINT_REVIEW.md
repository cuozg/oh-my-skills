# Blueprint Review — Architecture & System Design

Load when PR introduces new systems, refactors architecture, or changes design patterns.

## 🔴 Critical

| Issue | Fix |
|:------|:----|
| God class (>500 lines, 5+ responsibilities) | Extract focused classes |
| Circular dependency (A↔B) | Interface or event at boundary |
| No error recovery for network/IO/dependency failure | Retry, fallback, graceful degradation |
| Unbounded collection growth (List/Dict without limit) | Max capacity, LRU eviction |
| Breaking public API (signature changed/member removed) | Add overload, `[Obsolete]` old |

## 🟡 Major — Architecture

| Issue | Fix |
|:------|:----|
| SRP violation (data + UI in one class) | Split concerns |
| Open/Closed violation (switch/if-else for new behavior) | Strategy, polymorphism, SO config |
| Liskov violation (override changes semantics) | Respect contract, prefer composition |
| Fat interface (10+ methods, half unused) | Split: `IReadable`, `IWritable` |
| DI violation (high-level `new`s low-level) | Constructor inject, `[SerializeField]`, service locator |
| Feature envy (method uses another class's data) | Move method |

## 🟡 Major — Unity Architecture

| Issue | Fix |
|:------|:----|
| Singleton abuse (non-infra `static Instance`) | SO channels, DI |
| MonoBehaviour as data-only class | Plain C# class or SO |
| Manager of managers (one god controller) | Independent systems + events |
| Update polling (bool check every frame) | Event-driven |
| Component doing too much (input+anim+physics+audio) | Split by responsibility |
| SO as mutable runtime state without clone | `Instantiate(configSO)` |

## 🟡 Major — System & API

`Task.Result`/`.Wait()` on main thread → async. Missing `CancellationToken` → add + cancel in OnDestroy. Boolean params → enum. Side effects in property getter → make method. Multiple booleans for state → enum/state machine. Hardcoded config → SO/remote config. Missing idempotency guard → add `if (_processing) return;`.

## 🔵 Minor

Premature abstraction (interface with 1 impl), deep inheritance (4+), `SendMessage`/`BroadcastMessage`, `Resources/` folder usage.

## Investigation

```bash
# New system scope
find Assets/Scripts/NewFeature/ -name "*.cs" | wc -l
# Dependencies in/out
grep -rn "using " Assets/Scripts/NewFeature/ --include="*.cs" | grep -v "System" | sort -u
grep -rn "NewFeatureNamespace" Assets/Scripts/ --include="*.cs" | grep -v "NewFeature/"
# Anti-patterns
grep -rn "static.*Instance\|void Update\|new.*Manager\|new.*Controller" Assets/Scripts/NewFeature/ --include="*.cs"
```

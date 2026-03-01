# Unity C# Coding Standards — Quick Reference Index

> All files live in this directory. This index provides navigation and the summary DO/DO NOT table.

## Navigation

### C# Language
| Topic | File | Covers |
|:---|:---|:---|
| Naming & Hygiene | `csharp-hygiene.md` | Naming, nullable, access modifiers, sealed/readonly, dispose, guards |
| Modern C# | `csharp-modern.md` | Expression-bodied, pattern matching, records, file-scoped, Span |
| LINQ | `csharp-linq.md` | Core ops, chaining, materialization, anti-patterns |
| Performance | `csharp-perf.md` | Caching, string ops, struct vs class, ArrayPool, NonAlloc |

### Unity Systems
| Topic | File | Covers |
|:---|:---|:---|
| Lifecycle | `unity-lifecycle.md` | Init/cleanup order, Update rules, coroutines, SO rules, async matrix |
| UniTask | `unitask.md` | Async patterns, cancellation, waiting, error handling, cheat sheet |
| Async & State | `patterns-async-state.md` | Jobs/Burst, state machines, CTS cleanup |

### Architecture & Patterns
| Topic | File | Covers |
|:---|:---|:---|
| Architecture | `architecture.md` | SOLID, DI (VContainer), SO event channels, assembly defs, folders |
| Service Patterns | `patterns-service.md` | Service, state, view patterns, composition |
| Editor | `editor-patterns.md` | Custom inspectors, windows, property drawers, IMGUI/UIToolkit |
| Security | `security.md` | Serialization safety, anti-cheat, network, build hardening |
| Template | `template.md` | Starting template for new MonoBehaviours |

---

## Quick Reference — DO / DO NOT

| Rule | DO | DO NOT |
|:---|:---|:---|
| Fields | `private readonly _camelCase` | Public fields, `m_` prefix |
| Nullable | `<Nullable>enable` + `is null` | `!` without comment |
| Records | Non-serialized value types only | `[Serializable]` records |
| Async | `UniTask` / `Awaitable` | `Task`, `async void` |
| Hot path | Pre-allocate, manual loops | LINQ, `new`, `GetComponent` |
| Physics | `NonAlloc` APIs + layer mask | `RaycastAll`, no layer mask |
| Pooling | `UnityEngine.Pool.ObjectPool<T>` | `Instantiate`/`Destroy` in loops |
| Events | Subscribe `OnEnable`, unsub `OnDisable` | Lambda subs without unsub |
| DI | Constructor injection + interfaces | `FindObjectOfType`, static singletons |
| Serialization | `JsonUtility`, `MessagePack` | `BinaryFormatter`, `PlayerPrefs` for secrets |
| Assembly | One `.asmdef` per module | No `.asmdef` (compiler unity is fragile) |
| Security | Server-authoritative for game values | Client-only validation |

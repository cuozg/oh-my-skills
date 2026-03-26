# Reference Routing

Read local files first. Load one workflow ref, then only the smallest extra set needed to write correctly.

## Baseline

- Quick → `code-standards/architecture-systems.md` (§ Single-File Runtime Workflow)
- Deep → `code-standards/architecture-systems.md` (§ Multi-File Workflow)
- Optimize → `code-standards/architecture-systems.md` (§ Refactoring Patterns)
- New `MonoBehaviour`, `ScriptableObject`, or interface skeleton → `code-standards/core-conventions.md`

## Add By Need

| Task clue | Load |
|-----------|------|
| Serialized fields, inspector data, safe renames, `JsonUtility`, `SerializeReference` | `code-standards/performance-data.md` § Serialization |
| Component lookups, nullable refs, destroyed Unity objects, guard clauses | `code-standards/core-conventions.md` § Null Safety |
| `Awake`, `Start`, `OnEnable`, `FixedUpdate`, coroutines, app lifecycle | `code-standards/lifecycle-async-errors.md` § Unity Lifecycle |
| C# events, `UnityEvent`, event channels, subscription ownership | `code-standards/architecture-systems.md` § Events |
| 2+ runtime files, services, DI, asmdefs, registration, assembly boundaries | `code-standards/architecture-systems.md` § Dependency Management |
| State machine, MVP/MVC, command flow, feature architecture | `code-standards/architecture-systems.md` § Architecture Patterns |
| Extract class/interface, composition, data extraction, event-driven migration | `code-standards/architecture-systems.md` § Refactoring Patterns |
| Collection choice, lookup-heavy code, pre-sizing, `Contains` cost | `code-standards/performance-data.md` § Collections |
| LINQ in gameplay code or repeated loops | `code-standards/performance-data.md` § LINQ Usage |
| `async`/`await`, `Task`, UniTask, `Awaitable`, cancellation | `code-standards/lifecycle-async-errors.md` § Async Patterns |
| `RequireComponent`, `SerializeField`, `CreateAssetMenu`, inspector attributes | `code-standards/core-conventions.md` § Unity Attributes |
| `private` vs `public`, `readonly`, `const`, `sealed`, API surface cleanup | `code-standards/core-conventions.md` § Access Modifiers |
| Try/catch, asserts, error logs, editor-only safety guards | `code-standards/lifecycle-async-errors.md` § Error Handling |
| Naming cleanup, namespaces, file names, boolean names | `code-standards/core-conventions.md` § Naming Conventions |
| Brace/style cleanup, `var`, terse comments, section headers | `code-standards/core-conventions.md` § Formatting / § Comments |
| New folders, namespace layout, asmdef placement | `code-standards/architecture-systems.md` § Project Folder Structure |
| Pooling is part of the feature design, not a perf pass | `code-standards/performance-data.md` § Object Pooling |
| Web target or browser restrictions matter | `code-standards/architecture-systems.md` § Web Platform Restrictions |

## Do Not Load Yet

- Editor-specific patterns → route to `unity-editor`
- Optimization refs for GC/frame-budget work → route to `unity-optimize`
- Style refs if local style is already clear and style cleanup is not requested

## Budget

- Start with 1 workflow ref
- Add 1-3 targeted refs
- Reassess after discovery or scope changes
- Prefer correctness refs before style refs

# Reference Routing

Read local files first. Load one workflow ref, then only the smallest extra set needed to write correctly.

## Baseline

- Quick -> `code-standards/single-file-runtime-workflow.md`
- Deep -> `code-standards/multi-file-workflow.md`
- Optimize -> `code-standards/refactoring-patterns.md`
- New `MonoBehaviour`, `ScriptableObject`, or interface skeleton -> `code-standards/code-patterns.md`

## Add By Need

| Task clue | Load |
|-----------|------|
| Serialized fields, inspector data, safe renames, `JsonUtility`, `SerializeReference` | `code-standards/serialization.md` |
| Component lookups, nullable refs, destroyed Unity objects, guard clauses | `code-standards/null-safety.md` |
| `Awake`, `Start`, `OnEnable`, `FixedUpdate`, coroutines, app lifecycle | `code-standards/lifecycle.md` |
| C# events, `UnityEvent`, event channels, subscription ownership | `code-standards/events.md` |
| 2+ runtime files, services, DI, asmdefs, registration, assembly boundaries | `code-standards/dependencies.md` |
| State machine, MVP/MVC, command flow, feature architecture | `code-standards/architecture-patterns.md` |
| Extract class/interface, composition, data extraction, event-driven migration | `code-standards/refactoring-patterns.md` |
| Collection choice, lookup-heavy code, pre-sizing, `Contains` cost | `code-standards/collections.md` |
| LINQ in gameplay code or repeated loops | `code-standards/linq.md` |
| `async`/`await`, `Task`, UniTask, `Awaitable`, cancellation | `code-standards/async.md` |
| `RequireComponent`, `SerializeField`, `CreateAssetMenu`, inspector attributes | `code-standards/unity-attributes.md` |
| `private` vs `public`, `readonly`, `const`, `sealed`, API surface cleanup | `code-standards/access-modifiers.md` |
| Try/catch, asserts, error logs, editor-only safety guards | `code-standards/error-handling.md` |
| Naming cleanup, namespaces, file names, boolean names | `code-standards/naming.md` |
| Brace/style cleanup, `var`, terse comments, section headers | `code-standards/formatting.md`, `code-standards/comments.md` |
| New folders, namespace layout, asmdef placement | `code-standards/project-structure.md` |
| Pooling is part of the feature design, not a perf pass | `code-standards/object-pooling.md` |
| Web target or browser restrictions matter | `code-standards/webgl-restrictions.md` |

## Advanced Refs

Load `*-advanced.md` only when the base ref is not enough:

- `async-advanced.md` for stack selection, conversion, or complex async error flow
- `architecture-patterns-advanced.md` for ScriptableObject strategy or mediator/event bus
- `collections-advanced.md` for `NativeArray`, `Span<T>`, `ArrayPool<T>`, or `NativeContainer` work
- `dependencies-advanced.md` for Zenject-specific work
- `null-safety-advanced.md` for `#nullable` or invariant enforcement
- `lifecycle-advanced.md` for execution order, app pause/focus, visibility, or `Reset()`
- `unity-attributes-advanced.md` for debug/conditional attributes or dense attribute combinations
- `error-handling-advanced.md` for fail-fast patterns, `OnValidate`, or custom exceptions
- `object-pooling-advanced.md` for custom or generic pools

## Do Not Load Yet

- `editor-patterns.md`, `gizmos-handles.md` -> route to `unity-editor`
- Optimization refs for GC/frame-budget work -> route to `unity-optimize`
- `formatting.md` or `comments.md` if local style is already clear and style cleanup is not requested
- Advanced refs just because a file is large

## Budget

- Start with 1 workflow ref
- Add 1-3 targeted refs
- Reassess after discovery or scope changes
- Prefer correctness refs before style refs

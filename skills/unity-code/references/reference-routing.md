# Reference Routing — Code-Standards On Demand

Code-standards is the single source of truth for all Unity C# patterns and conventions. Use this table to load only the sections relevant to your current task.

## How to Use

1. Scan the task description for clues in the left column
2. Load the indicated code-standards file via `read_skill_file("unity-standards", "references/code-standards/<file>.md")`
3. Focus on the section indicated after §
4. Load **1-3 files maximum** per task — reassess if scope changes

## Route By Task Clue

### core-conventions.md

| Task clue | Section |
|-----------|---------|
| New MonoBehaviour, ScriptableObject, interface, enum, struct, helper class | § Code Patterns |
| Naming, namespaces, file names, boolean names, async suffix | § Naming Conventions |
| Brace style, `var` usage, line breaks, expression-bodied members | § Formatting |
| XML docs, inline comments, header comments, TODO format | § Comments |
| `private` vs `public`, `readonly`, `const`, `sealed`, API surface | § Access Modifiers |
| Component lookups, nullable refs, destroyed Unity objects, guard clauses | § Null Safety |
| `RequireComponent`, `SerializeField`, `CreateAssetMenu`, inspector attributes | § Unity Attributes |

### lifecycle-async-errors.md

| Task clue | Section |
|-----------|---------|
| `Awake`, `Start`, `OnEnable`, `FixedUpdate`, coroutines, app lifecycle | § Unity Lifecycle |
| `async`/`await`, `Task`, UniTask, `Awaitable`, cancellation | § Async Patterns |
| Try/catch, asserts, error logs, editor-only safety guards | § Error Handling |
| Input validation, save data security, rate limiting | § Security — Input & Data Validation |

### performance-data.md

| Task clue | Section |
|-----------|---------|
| Serialized fields, inspector data, safe renames, `JsonUtility`, `SerializeReference` | § Serialization |
| Collection choice, lookup-heavy code, pre-sizing, `Contains` cost | § Collections |
| LINQ in gameplay code or repeated loops | § LINQ Usage |
| Object pooling as part of feature design (not perf pass) | § Object Pooling |

### architecture-systems.md

| Task clue | Section |
|-----------|---------|
| C# events, `UnityEvent`, event channels, subscription ownership | § Events |
| 2+ runtime files, services, DI, asmdefs, registration, assembly boundaries | § Dependency Management |
| State machine, MVP/MVC, command flow, strategy pattern | § Architecture Patterns |
| Extract class/interface, composition, data extraction, event-driven migration | § Refactoring Patterns |
| New folders, namespace layout, asmdef placement | § Project Folder Structure |
| Web target or browser restrictions matter | § Web Platform Restrictions |

## Loading Priority

For most writing tasks, start with these (unless discovery shows clear established conventions):

1. `core-conventions.md` — almost always relevant (naming, patterns, attributes)
2. The domain-specific file indicated by task clues (async, architecture, serialization, etc.)
3. A second domain file only if the task clearly spans two concerns

## Do Not Load

- Editor-specific patterns → route to `unity-editor` skill
- Optimization refs for GC/frame-budget work → route to `unity-optimize` skill
- All 4 code-standards files at once — pick the 1-3 that matter
- Style refs if local style is already clear from discovery and style cleanup is not requested

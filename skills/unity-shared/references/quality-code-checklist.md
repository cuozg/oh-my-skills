# Code Quality Checklist

## Code Structure

### Method Quality
- [ ] Methods < 30 lines (flag > 50)
- [ ] Nesting depth < 4 levels (flag > 5)
- [ ] Single return point per method (or early returns for guards)
- [ ] No more than 4 parameters per method
- [ ] Boolean parameters replaced with enums or separate methods
- [ ] No methods with side effects that the name doesn't indicate

### Class Quality
- [ ] Classes < 300 lines (flag > 500 as God class)
- [ ] One class per file (except small nested types)
- [ ] No empty MonoBehaviour methods (Update, Start, Awake with no body)
- [ ] No `#region` blocks hiding complexity (extract classes instead)
- [ ] Proper access modifiers (not everything public)
- [ ] `sealed` on classes not designed for inheritance

### Naming Conventions
- [ ] PascalCase for public methods, properties, classes, enums
- [ ] camelCase for private fields, local variables, parameters
- [ ] `_camelCase` or `m_camelCase` for private fields (consistent within project)
- [ ] `I` prefix for interfaces
- [ ] No abbreviations except widely understood ones (UI, ID, HP)
- [ ] Boolean names read as questions: `isReady`, `hasItem`, `canMove`
- [ ] Event handlers named `On[Event]`: `OnPlayerDied`, `OnItemCollected`

## Anti-Patterns

### :red_circle: Critical Anti-Patterns
| Anti-Pattern | Detection | Fix |
|:-------------|:----------|:----|
| God class (> 500 lines, multiple responsibilities) | Line count + mixed concerns | Extract focused classes |
| Lava flow (dead code left "just in case") | Unreachable branches, commented-out code | Delete (git has history) |
| Singleton abuse (> 5 singletons) | Count `*.Instance` patterns | Evaluate each — DI, SO, or plain class? |
| Empty catch blocks `catch(e) {}` | Grep for empty catch | Log error or handle specifically |
| Stringly-typed programming | Hardcoded strings for tags, layers, scenes, anim params | Constants, enums, StringToHash |
| Circular dependencies | Assembly ref graph, class import analysis | Extract shared interface/data layer |

### :orange_circle: High Anti-Patterns
| Anti-Pattern | Detection | Fix |
|:-------------|:----------|:----|
| Feature envy (method uses other class's data more than its own) | Cross-class field access count | Move method to data owner |
| Shotgun surgery (change requires editing many files) | Feature-to-file ratio analysis | Consolidate related logic |
| Primitive obsession (using int/string where domain type needed) | Raw primitives for IDs, currencies, health | Value objects, typed wrappers |
| Copy-paste code (duplicated logic blocks) | Structural similarity scan | Extract shared method/base class |
| Deep inheritance (> 3 levels) | Class hierarchy depth | Prefer composition |
| Magic numbers/strings | Literal values in logic | Named constants, config SO |

### :yellow_circle: Medium Anti-Patterns
| Anti-Pattern | Detection | Fix |
|:-------------|:----------|:----|
| Comments explaining "what" not "why" | `// set x to 5` style comments | Rewrite for intent |
| Unused using directives | `using` without references | Remove |
| Inconsistent code style within file | Mixed brace styles, spacing | Apply .editorconfig |
| TODO/FIXME/HACK without ticket reference | Grep for markers | Add ticket or resolve |
| Excessive null checks cascading | `if (x != null && x.y != null && ...)` | Null Object pattern or restructure |

## Error Handling

- [ ] No empty catch blocks — every catch either handles, logs, or rethrows
- [ ] Specific exception types caught (not bare `catch (Exception)`)
- [ ] Error paths return meaningful feedback (not silent failure)
- [ ] Network/IO operations have timeout and retry logic
- [ ] User-facing errors are localized and helpful
- [ ] Debug.LogError used for actual errors, not flow control
- [ ] `try/finally` or `using` for resource cleanup
- [ ] Async error handling: no `async void` except Unity event handlers

## Testing

### Coverage Assessment
- [ ] Test assembly definitions exist
- [ ] Critical game logic has unit tests
- [ ] Data serialization/deserialization tested
- [ ] Edge cases covered (null, empty, boundary, overflow)
- [ ] No test code in production assemblies
- [ ] Tests are deterministic (no timing/order dependencies)

### Test Quality
- [ ] Tests follow Arrange-Act-Assert pattern
- [ ] Each test verifies ONE behavior
- [ ] Test names describe the scenario, not the method
- [ ] No `Debug.Log` assertions (use NUnit Assert/Fluent)
- [ ] Mocking strategy exists for external dependencies
- [ ] Play Mode tests for async/coroutine/scene flows

## Documentation

- [ ] Public API has XML doc comments (`/// <summary>`)
- [ ] Complex algorithms have inline comments explaining "why"
- [ ] Architecture decisions documented (ADR or README)
- [ ] Breaking changes have migration notes
- [ ] README exists with setup instructions
- [ ] Inspector-visible fields have `[Tooltip("...")]`
- [ ] `[Header("Section")]` used to organize Inspector groups

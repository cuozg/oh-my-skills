# C# Code Review — PR Checklist

> Authoritative for: nullable refs, access modifiers, exception handling, logging, method/class quality, anti-patterns, documentation.
> Cross-ref: `review-logic-data.md` (data flow, concurrency), `review-architecture-patterns.md` (SOLID, coupling), `csharp-hygiene.md` (style guide)

---

## 🔴 Critical

| Name | Issue | Fix |
|------|-------|-----|
| Empty Catch Block | `catch (Exception) { }` silently swallows errors — masks bugs | Log, rethrow, or handle specifically; never swallow silently |
| Catch-All in Business Logic | `catch (Exception ex)` at every call site hides root cause | Catch specific exceptions; let unexpected ones propagate to global handler |
| Null Dereference Unguarded | Accessing `.Value`, `.Result`, or member without null check | Use `?.`, null check, or `TryGet` pattern; enable nullable reference types |
| Public Mutable Collection | `public List<T> Items` — anyone can `.Clear()`, mutate state | Return `IReadOnlyList<T>` or `ReadOnlyCollection<T>`; expose `Add/Remove` methods |
| Async Void | `async void` cannot be awaited or caught — crashes on exception | Use `async Task` always; `async void` only for Unity event handlers (Start, OnEnable) |
| Magic Strings/Numbers | Hardcoded `"PlayerTag"`, `0.5f`, `100` scattered through code | Extract to `const`, `static readonly`, `enum`, or config SO |
| BinaryFormatter Usage | `BinaryFormatter` is insecure — arbitrary code execution via deserialized data | Use JSON (Newtonsoft), MessagePack, or FlatBuffers |

## 🟡 Major — Nullable & Access

| Name | Issue | Fix |
|------|-------|-----|
| Missing `#nullable enable` | No nullable analysis — compiler won't flag null risks | Add `#nullable enable` at file or project level |
| Nullable Warning Suppressed | `null!` or `#pragma warning disable` hides real null risks | Fix the null flow; use `?? throw`, guard clause, or redesign |
| Wrong Access Modifier | `public` field/method that should be `private` or `internal` | Apply least-privilege: `private` default, `internal` for assembly, `public` for API |
| Mutable Struct Exposed | `public struct Config { public float Speed; }` — mutation bugs | Use `readonly struct` or class; make fields `init`-only |
| Missing `sealed` on Leaf Class | Non-`abstract` class without `sealed` — allows unintended inheritance | Add `sealed` unless designed for extension |
| `protected` Field | Subclass directly mutates parent state — fragile base class problem | Use `protected` property with validation, or pass via constructor |

## 🟡 Major — Exception Handling

| Name | Issue | Fix |
|------|-------|-----|
| Throwing `System.Exception` | `throw new Exception("failed")` — too generic to catch specifically | Throw specific: `InvalidOperationException`, `ArgumentException`, or custom |
| Missing Stack Trace on Rethrow | `catch (Exception ex) { throw ex; }` resets stack trace | Use `throw;` (no argument) to preserve original stack trace |
| Exception in Constructor | Constructor throws — leaves object in invalid partial state | Use factory method or `Init()` pattern; validate args before construction |
| Missing Validation on Public API | Public method accepts any input without checks | Add guard clauses: `ArgumentNullException`, `ArgumentOutOfRangeException` at entry |
| Logging Without Context | `Debug.LogError("Failed")` — no info about what, where, or why | Include method name, entity ID, and relevant state: `$"[{name}] Failed to load {id}: {ex.Message}"` |
| Excessive Try-Catch Nesting | 3+ nested try-catch blocks — unreadable flow | Extract inner blocks to methods; use early return; let exceptions propagate to single handler |

## 🟡 Major — Method & Class Quality

| Name | Issue | Fix |
|------|-------|-----|
| Long Method | Method >30 LOC — hard to test, read, and reason about | Extract logical blocks into well-named private methods |
| Too Many Parameters | Method has 5+ parameters — signals it does too much | Group into parameter object, config struct, or builder pattern |
| Boolean Parameter | `Process(data, true, false)` — unreadable at call site | Use enum, named constants, or separate methods (`ProcessFast`, `ProcessSafe`) |
| Mixed Abstraction Levels | Method mixes high-level flow with low-level details | Keep one abstraction level per method; extract details to helper methods |
| Large Class | Class >300 LOC with 3+ concerns — violates SRP | Split into focused classes; use composition over inheritance |
| Deep Nesting | 4+ levels of `if/for/while` nesting | Use guard clauses (early return), extract methods, invert conditions |
| Side Effect in Getter | Property getter modifies state or triggers I/O | Use method instead of property for operations with side effects |

## 🔵 Medium — Anti-Patterns

| Name | Issue | Fix |
|------|-------|-----|
| Feature Envy | Method uses 5+ members of another class instead of its own | Move method to the class it envies; expose behavior, not data |
| Data Clump | Same 3+ fields passed together everywhere | Extract into a value object or struct |
| Middle Man | Class delegates every call to another class without adding value | Remove middle man; call target directly or merge |
| Inappropriate Intimacy | Class accesses another class's private/internal state via reflection or tricks | Expose proper API; redesign dependency |
| Speculative Generality | Abstract class or interface with only one implementation and no plan for more | Remove abstraction until second use case exists (YAGNI) |
| Divergent Change | One class modified for 3+ unrelated reasons | Split by reason-to-change into separate classes |

## 🔵 Medium — Logging & Documentation

| Name | Issue | Fix |
|------|-------|-----|
| Missing ILogger | Using `Debug.Log` directly everywhere — can't filter, route, or disable | Use `ILogger` / `ILogHandler` abstraction; inject via DI |
| Log Level Misuse | `Debug.LogError` for info, `Debug.Log` for errors | Error=unexpected failure, Warning=recoverable issue, Log=info/flow |
| Sensitive Data in Logs | Logging passwords, tokens, PII, or secrets | Strip sensitive fields; log IDs and operation names, not values |
| Missing XML Docs on Public API | Public method/class has no `///` summary | Add `<summary>`, `<param>`, `<returns>` for all public members |
| Commented-Out Code | Dead code in `//` blocks — clutters and misleads | Delete it; version control preserves history |
| TODO Without Ticket | `// TODO: fix later` with no tracking ticket | Add ticket reference: `// TODO(PROJ-123): reason` or remove |

## 🟢 Minor

| Name | Issue | Fix |
|------|-------|-----|
| Inconsistent Naming | Mix of `_field`, `m_Field`, `field` for private fields | Follow project convention; Unity default: `_camelCase` for private, `PascalCase` for public |
| Missing `readonly` on Injected Field | DI-injected field can be reassigned accidentally | Add `readonly` to all injected/constructor-assigned fields |
| Redundant `this.` Qualifier | `this.name` when `name` is unambiguous | Remove `this.` unless disambiguating from local variable |
| Missing `nameof()` | String literal `"PropertyName"` instead of `nameof(PropertyName)` | Use `nameof()` for refactor-safe property/method name references |
| Region Abuse | `#region` used to hide complexity instead of extracting classes | Remove regions; extract to focused classes/methods instead |

---

> **Style reference:** See `csharp-hygiene.md` for naming conventions, formatting rules, and `using` organization.

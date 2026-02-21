# C# Quality Review Checklist

## Nullable Reference Types

- [ ] `<Nullable>enable</Nullable>` in .csproj
- [ ] Nullable types explicitly declared with `?`
- [ ] Non-nullable properties initialized (not left as default)
- [ ] No `!` (null-forgiving) without documented reason
- [ ] Null checks use pattern matching (`is null`, `is not null`)
- [ ] No unnecessary null checks on DI-injected dependencies

## Access Modifiers

- [ ] Fields are `private` (or `private readonly`)
- [ ] Helper classes are `internal sealed`
- [ ] Only API boundaries are `public`
- [ ] No public fields (use properties)
- [ ] `[SerializeField]` private fields for Unity inspector

## Exception Handling

### Throwing
- [ ] Exceptions thrown for error conditions (not logged-and-continued)
- [ ] `ArgumentNullException.ThrowIfNull()` for null guards
- [ ] `ArgumentException.ThrowIfNullOrEmpty()` for string guards
- [ ] `ArgumentOutOfRangeException` for range violations
- [ ] `KeyNotFoundException` for missing dictionary entries
- [ ] `InvalidOperationException` for invalid state transitions
- [ ] Custom exceptions for domain-specific errors

### Catching
- [ ] `catch (OperationCanceledException)` handled separately from general exceptions
- [ ] No empty catch blocks
- [ ] No `catch (Exception)` that swallows without re-throw
- [ ] Specific exception types caught (not bare `Exception`)
- [ ] Exception details preserved when re-throwing (`throw;` not `throw ex;`)

## Logging

### ILogger Usage
- [ ] `ILogger` used for runtime logging (injected via DI)
- [ ] No `Debug.Log` in runtime code (only `#if UNITY_EDITOR`)
- [ ] No logging in constructors
- [ ] No null-conditional on logger (`this.logger.Debug()` not `this.logger?.Debug()`)
- [ ] No manual prefixes (logger handles automatically)
- [ ] No conditional compilation guards around logger calls
- [ ] Appropriate log levels: Debug for diagnostics, Info for significant events, Warning for recoverable issues

### Log Quality
- [ ] No verbose/unnecessary logs (entering method, exiting method)
- [ ] Log messages are actionable (include relevant data)
- [ ] No sensitive data in logs (passwords, tokens, PII)
- [ ] No string concatenation in log calls (use interpolation)

## Naming Conventions

- [ ] PascalCase: types, methods, properties, constants, enum values
- [ ] camelCase with `_` prefix: private fields
- [ ] `I` prefix: interfaces
- [ ] PascalCase: local functions
- [ ] Descriptive names (no abbreviations except well-known: `id`, `url`, `ui`)
- [ ] Boolean names start with `is`, `has`, `can`, `should`
- [ ] Async methods end with `Async`

## Class Design

- [ ] Classes `sealed` unless designed for inheritance
- [ ] Fields `readonly` when set only in constructor
- [ ] One class per file (exceptions for small related types)
- [ ] File-scoped namespaces
- [ ] No partial classes (except Unity auto-generated)
- [ ] Guard clauses instead of deep nesting
- [ ] Maximum ~300 lines per class (split if larger)

## Collections

- [ ] Collections initialized (not null)
- [ ] `IReadOnlyList<T>` / `IReadOnlyCollection<T>` for read-only exposure
- [ ] Pre-sized when count is known: `new List<T>(count)`
- [ ] `Dictionary.TryGetValue()` instead of `ContainsKey` + indexer
- [ ] No `List<T>` exposed as public property (use `IReadOnlyList<T>`)

## String Handling

- [ ] String interpolation `$""` instead of concatenation
- [ ] `string.IsNullOrEmpty()` / `string.IsNullOrWhiteSpace()` for checks
- [ ] `StringComparison.Ordinal` for performance-critical comparisons
- [ ] `StringBuilder` for multiple concatenations
- [ ] Raw string literals for multi-line strings

## Modern C# Features

- [ ] Expression-bodied members for single expressions
- [ ] Null-coalescing `??`, `??=` instead of null checks
- [ ] Pattern matching `is`, `switch` expressions
- [ ] Target-typed `new()` where type is clear
- [ ] `var` for obvious types, explicit for unclear
- [ ] Using declarations (not using statements with braces)
- [ ] Collection expressions `[..]` where applicable
- [ ] Records for immutable data types

## Code Smells to Flag

### Critical
- Swallowed exceptions (empty catch)
- `Debug.Log` in runtime code
- Public mutable fields
- No null safety (nullable not enabled)

### Major
- God methods (>50 lines)
- Deep nesting (>3 levels)
- Magic numbers without constants
- Dead code (unreachable branches, unused parameters)
- Mutable static fields

### Minor
- Missing `sealed` modifier
- Missing `readonly` on constructor-set fields
- Verbose null checks (should use `??` or `?.`)
- Unused `using` statements
- TODO/HACK comments without issue tracking

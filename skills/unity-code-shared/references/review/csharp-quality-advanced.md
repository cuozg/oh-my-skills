# C# Quality Review Checklist — Advanced Topics

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

See also [csharp-quality.md](csharp-quality.md) for Nullable Types, Access Modifiers, Exception Handling, Logging, and Naming Conventions sections.

# Optimize Mode — Flutter Refactoring

Clean up code without changing behavior. Focus on rebuild reduction, dead code removal, and clarity.

## Workflow

1. **Read** — fully understand current behavior before touching anything
2. **Identify** — catalog issues: rebuilds, dead code, missing const, complex logic
3. **Refactor** — apply fixes preserving exact behavior
4. **Verify** — `lsp_diagnostics` on every changed file
5. **Report** — what changed, why, rebuild/performance impact

## Common Refactors

### Rebuild Reduction
- Extract widget subtrees into `const` child widgets (stops rebuild propagation)
- Use `ref.watch(provider.select((s) => s.field))` for granular provider reads
- Add `const` constructors to stateless widgets and value objects
- Wrap expensive subtrees in `RepaintBoundary` when justified

### Dead Code Removal
- Remove unused imports (`dart fix --apply` or manual)
- Delete unreachable methods, unused variables, commented-out blocks
- Remove empty overrides that only call `super`

### Simplification
- Flatten nested `if-else` with early returns or switch expressions
- Replace `Builder` + `setState` with proper Riverpod state management
- Collapse single-use private methods back inline if they obscure flow
- Use collection literals and spread operators over manual list building

### Provider Cleanup
- Convert manual `StateNotifierProvider` to `@riverpod` codegen
- Remove `autoDispose` wrappers (codegen handles this by default)
- Merge redundant providers that derive the same state

## Report Format

For each change:
```
- **What**: [brief description]
- **Why**: [rebuild count / dead code / readability]
- **Impact**: [fewer rebuilds / smaller bundle / clearer flow]
```

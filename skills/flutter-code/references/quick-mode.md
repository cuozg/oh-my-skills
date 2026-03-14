# Quick Mode — Single-File Flutter/Dart

Write one complete `.dart` file: widget, provider, model, utility, or service.

## Workflow

1. **Qualify** — confirm one file suffices; escalate to Deep if scope grows
2. **Discover** — read target + 1-2 nearby files for naming, imports, provider style
3. **Implement** — smallest complete change matching local style
4. **Verify** — `lsp_diagnostics` on changed file
5. **Handoff** — file path, usage example, codegen reminder if `@riverpod` used

## Patterns

### StatelessWidget
- `const` constructor with `Key? key` via `super.key`
- Extract sub-trees into methods only when reused; prefer `const` child widgets

### StatefulWidget
- Dispose controllers/subscriptions in `dispose()`
- Use `mounted` check before `setState` in async callbacks

### Provider (@riverpod codegen)
- Annotate with `@riverpod` (auto-dispose) or `@Riverpod(keepAlive: true)`
- Function provider for simple derived state; class provider (Notifier) for mutable state
- Return type explicitly annotated on the function/getter

### Data Class / Model
- `fromJson` factory + `toJson` method (or use `freezed`/`json_serializable`)
- All fields `final`; use `copyWith` for immutability
- Override `==` and `hashCode` (or use `@freezed`)

### Utility / Extension
- Top-level functions for stateless utilities
- Extensions on existing types for domain-specific helpers
- Document with `///` doc comments

## Rules

- One class per file, file name = class name in `snake_case`
- Trailing commas on all multi-line argument lists
- `const` constructors wherever possible
- Never leave `TODO`, stubs, or incomplete wiring
- Prefer `final` locals; avoid `var` for non-reassigned variables

# Deep Mode — Multi-File Flutter Features

Build complete features spanning 2+ files with proper layering and dependency order.

## Workflow

1. **Qualify** — confirm 2+ files needed; switch to Quick if single-file
2. **Discover** — read project structure, existing providers, router config, barrel files
3. **Plan** — list every file, layer (data → providers → presentation), dependency order
4. **Implement** — data layer first, then providers, then presentation
5. **Verify** — `lsp_diagnostics` per layer, then all files
6. **Handoff** — file list, architecture notes, codegen commands, testing guidance

## Layer Order (ALWAYS follow)

1. **Data** — models, DTOs, repository interfaces, data sources
2. **Providers** — Riverpod Notifier/AsyncNotifier, repository implementations
3. **Presentation** — screens, widgets, controllers

## Feature-First Structure

```
lib/features/<feature>/
  data/          # models, DTOs, repos (abstract + impl), data sources
  providers/     # @riverpod notifiers, state classes
  presentation/  # screens, reusable widgets
```

## Patterns

### Repository Pattern
- Abstract class defines contract; implementation injects data sources
- Repository provider exposes the implementation via Riverpod

### AsyncNotifier (Complex State)
- Extend `_$ClassName` (codegen); override `build()` for initial state
- Expose mutation methods; use `state = AsyncLoading()` during operations
- Handle errors with `state = AsyncError(e, st)`

### State Classes
- Prefer `freezed` unions for complex states (loading/data/error)
- Simple states: use the Notifier's `AsyncValue<T>` directly

## Rules

- Create files in dependency order (models before repos before providers)
- Run `dart run build_runner build` after adding `@riverpod` or `@freezed`
- Wire providers top-down; never create circular provider dependencies
- Each layer testable in isolation (repos mock data sources, providers mock repos)

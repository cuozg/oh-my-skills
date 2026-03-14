---
name: flutter-standards
description: >
  Use this skill as the shared reference hub for all Flutter & Dart development — coding standards,
  naming conventions, architecture patterns, state management, testing, performance, and UI guidelines.
  MUST be included in load_skills for any Flutter task delegation. Triggers automatically when writing,
  reviewing, debugging, testing, or planning Flutter/Dart code. Contains 12 reference files across
  architecture, state, UI, performance, and tooling categories that downstream skills pull on demand.
  Also use when the user says "Dart style guide," "Flutter best practices," "Riverpod patterns,"
  "feature-first structure," "Flutter performance," or any Flutter/Dart coding standards question.
metadata:
  author: kuozg
  version: "1.0"
---

# flutter-standards

Flutter & Dart shared reference hub for code, review, debug, testing, planning, and UI work.

## When This Skill Triggers

- Writing or refactoring Flutter/Dart code
- Reviewing local changes or pull requests for Flutter projects
- Debugging Flutter runtime, widget, or build issues
- Planning, testing, or documenting Flutter systems
- Any downstream flutter-* skill delegation (MUST include in load_skills)

## Usage

- Always include `flutter-standards` in `load_skills` for delegated Flutter work.
- Load only the needed reference: `read_skill_file("flutter-standards", "references/<filename>")`.

## Design Decisions

- **Style**: Google's Effective Dart — naming, formatting, null-safety
- **State Management**: Riverpod 2.x with codegen (primary); BLoC/Provider as alternatives
- **Architecture**: Feature-first folder layout, single responsibility
- **Target**: Solo developer — practical patterns, no team-coordination overhead

## Reference Catalog

### Code & Style (2)

- `dart-style-guide.md` — Effective Dart naming, formatting, linting, null-safety rules
- `code-organization.md` — Feature-first folder layout, pubspec.yaml, build flavors, barrel files

### Architecture & State (3)

- `architecture-patterns.md` — Feature-first, layered architecture, MVVM, clean arch comparison
- `state-management-guide.md` — Riverpod 2.x codegen, Notifier patterns, BLoC/Provider alternatives
- `dependency-injection.md` — Riverpod as DI, GetIt/Injectable alternatives, scoping strategies

### UI & Assets (2)

- `ui-best-practices.md` — Widget composition, const, keys, responsive layout, theming
- `asset-management.md` — Images, fonts, flutter_gen, gen_l10n, asset organization

### Async & Error Handling (2)

- `async-streams.md` — Future, Stream, StreamController, Completer, error propagation
- `error-handling.md` — Exception hierarchies, Result pattern, user-facing recovery, crash reporting

### Testing (1)

- `testing-patterns.md` — Unit, widget, golden, integration tests; AAA pattern, mocking with Mocktail

### Performance & Debug (2)

- `performance-optimization.md` — Rebuild profiling, RepaintBoundary, Impeller, memory, frame budget
- `debug-logging.md` — package:logger, DevTools, PlatformDispatcher, structured logging

## Downstream Skills (Planned)

These future skills will load references from flutter-standards:

| Skill | Domain |
|-------|--------|
| flutter-code | Write, extend, refactor Flutter/Dart code |
| flutter-ui | Build screens, widgets, responsive layouts |
| flutter-debug | Diagnose and fix Flutter bugs |
| flutter-review | Review Flutter PRs and local changes |
| flutter-test | Write unit, widget, and integration tests |
| flutter-profiler | Analyze DevTools profiler data |

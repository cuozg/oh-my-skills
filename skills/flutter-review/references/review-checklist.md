# Review Checklist

Criteria table for Flutter/Dart code review. Each criterion maps to its `flutter-standards` reference file.

## Code Review Criteria

| # | Criterion | What to Check | Reference |
|---|-----------|---------------|-----------|
| 1 | **Code Style** | Naming conventions, formatting, null-safety, import ordering, lint compliance | `dart-style-guide.md` |
| 2 | **Architecture** | Feature-first layout, layer separation, dependency direction, repository pattern | `architecture-patterns.md` |
| 3 | **State Management** | Provider/Notifier design, rebuild scope, state isolation, disposal | `state-management-guide.md` |
| 4 | **Performance** | Const constructors, unnecessary rebuilds, lazy builders, RepaintBoundary | `performance-optimization.md` |
| 5 | **Error Handling** | Exception hierarchy, Result pattern, try/catch specificity, crash reporting | `error-handling.md` |
| 6 | **Async Patterns** | Future/Stream handling, error propagation, cancellation, race conditions | `async-streams.md` |
| 7 | **Testing** | Test coverage gaps, missing edge cases, mock patterns, AAA structure | `testing-patterns.md` |

## Severity Minimum Floors

These issues must NEVER be graded below the stated severity:

| Issue | Minimum Severity |
|-------|:---:|
| `setState` in widget > 80 lines | MEDIUM |
| Missing `dispose()` for controllers, streams, subscriptions | HIGH |
| Unhandled async error (missing try/catch on Future) | HIGH |
| `!` bang operator on nullable without preceding null check | MEDIUM |
| Widget method extraction (should be separate widget class) | LOW |
| Hardcoded API key or secret in source | CRITICAL |
| Missing `const` on stateless constructor | LOW |
| `catch (e) {}` — empty catch block | HIGH |
| `dynamic` type used without justification | MEDIUM |
| Circular dependency between features | HIGH |

## Additional Checks (PR Review Only)

| Check | Condition |
|-------|-----------|
| Config review | `.yaml` files changed — check pubspec deps, analysis_options, build configs |
| Asset review | Images/fonts/l10n changed — check organization per `asset-management.md` |
| State review | New providers/notifiers/blocs added — check patterns per `state-management-guide.md` |
| Architecture review | New services/repositories added — check patterns per `architecture-patterns.md` |

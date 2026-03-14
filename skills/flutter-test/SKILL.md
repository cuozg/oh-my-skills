---
name: flutter-test
description: >
  Write Flutter tests with auto-triage across Unit, Widget, and Integration modes.
  Uses AAA (Arrange-Act-Assert) pattern, mocktail for mocking, ProviderContainer for
  Riverpod providers, and minimum 10 test cases per class. Use when the user says
  "write tests," "unit test," "widget test," "integration test," "add test coverage,"
  "test this feature," "test this provider," "test this screen," or wants automated
  verification of any Dart class, widget, or user flow. Do not use for manual QA
  test plans — use a test-case skill for that.
metadata:
  author: cuongnp
  version: "1.0"
---
# flutter-test

Detect test type, pick mode, write comprehensive tests. AAA pattern, mocktail mocking, 10+ tests per class.

## Step 1 — Detect Mode

| Signal | Mode |
|--------|------|
| Provider, service, repository, model, utility, pure logic class | **Unit** |
| Widget, screen, component, UI element, form validation display | **Widget** |
| Full app flow, navigation, multi-screen journey, end-to-end | **Integration** |

State triage: "This is [mode] — [reason]."

## Step 2 — Execute

### Unit Mode

Load `read_skill_file("flutter-test", "references/unit-mode.md")` for patterns.

1. **Read** — read the target class; identify public API, dependencies, state mutations
2. **List** — enumerate 10+ test cases: happy paths, edge cases, error paths, boundary values, null/empty inputs
3. **Mock** — create mocks with mocktail for all dependencies; load `read_skill_file("flutter-test", "references/mocking-patterns.md")`
4. **Write** — implement tests using AAA pattern; `group()` by method, `setUp`/`tearDown` for isolation
5. **Verify** — `lsp_diagnostics` on test file; confirm all imports resolve

### Widget Mode

Load `read_skill_file("flutter-test", "references/widget-mode.md")` for patterns.

1. **Read** — read the widget class; identify props, interactions, conditional rendering, provider dependencies
2. **List** — enumerate 10+ test cases: render states, tap actions, text input, error display, loading/empty states
3. **Setup** — create pump helper with `ProviderScope` overrides and `MaterialApp` wrapper
4. **Write** — implement tests with `testWidgets`, finders, `pumpAndSettle`, interaction gestures
5. **Verify** — `lsp_diagnostics` on test file

### Integration Mode

Load `read_skill_file("flutter-test", "references/integration-mode.md")` for patterns.

1. **Read** — read the app entry point, router config, and screens involved in the flow
2. **List** — enumerate test scenarios for the complete user journey
3. **Setup** — configure `IntegrationTestWidgetsFlutterBinding`, mock external services
4. **Write** — implement end-to-end tests with navigation, state changes across screens, assertions at each step
5. **Verify** — `lsp_diagnostics` on test file

## Rules

- **AAA pattern** in every test body — Arrange, Act, Assert with comments
- **mocktail only** — never use mockito; `Mock`, `Fake`, `registerFallbackValue`
- **10+ test cases** per class under test — happy paths, edge cases, error paths, boundaries
- **One assertion focus** per test — multiple related asserts OK, but keep tests atomic
- **ProviderContainer** for provider tests — `addTearDown(container.dispose)` always
- **Descriptive names** — `'returns User on success'` not `'test1'`
- **`setUp`/`tearDown`** for isolation — never share mutable state across tests
- **Mock at boundaries** — repositories, API clients, external services — not internal classes
- **Test file mirrors source** — `lib/features/auth/data/auth_repo.dart` → `test/features/auth/data/auth_repo_test.dart`
- **No `print`/`debugPrint`** in tests — use `expect` assertions only

## Escalation

| From | To | When |
|------|----|------|
| Unit | Widget | Test requires rendering UI to verify behavior |
| Widget | Unit | Widget test is testing pure logic — extract to unit test |
| Widget | Integration | Test needs navigation or multi-screen state |
| Any | Unit+Widget | Feature needs both logic and UI coverage |

Carry forward context; tell user why mode changed.

## Standards

Load on demand via `read_skill_file("flutter-standards", "references/<path>")`:

- `testing-patterns.md` — Foundation patterns for all test types
- `dependency-injection.md` — Riverpod DI patterns for testable architecture
- `state-management-guide.md` — Provider patterns relevant to test setup
- `error-handling.md` — Error types and exception testing patterns
- `code-organization.md` — Test file placement, feature-first test structure

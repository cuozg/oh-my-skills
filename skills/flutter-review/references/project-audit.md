# Project Audit Workflow

Read-only scan of a Flutter project. Grade Architecture, Code Style, Performance, Best Practices on an A-F scale. Generate HTML report.

## Steps

1. **Scope project** — list all `.dart`, `.yaml`, `analysis_options.yaml`, `pubspec.yaml` files; record counts
2. **Analyze Architecture** — feature-first layout, dependency injection, provider scoping, layer separation
   - Checklist: `flutter-standards/references/architecture-patterns.md`
   - Checklist: `flutter-standards/references/dependency-injection.md`
3. **Analyze Code Style** — Dart naming, null-safety usage, linting rules, import ordering
   - Checklist: `flutter-standards/references/dart-style-guide.md`
   - Checklist: `flutter-standards/references/code-organization.md`
4. **Analyze Performance** — widget rebuilds, const usage, RepaintBoundary, lazy builders
   - Checklist: `flutter-standards/references/performance-optimization.md`
   - Checklist: `flutter-standards/references/ui-best-practices.md`
5. **Evaluate Best Practices** — error handling, async patterns, testing coverage, asset management
   - Checklist: `flutter-standards/references/error-handling.md`
   - Checklist: `flutter-standards/references/async-streams.md`
   - Checklist: `flutter-standards/references/testing-patterns.md`
   - Checklist: `flutter-standards/references/asset-management.md`
6. **Grade each category** — apply A-F rubric below
7. **Generate HTML report** — save to `Documents/QualityAudit_{date}.html`

## Grading Rubric

### Architecture
- A: Feature-first layout, proper DI, clear layer separation, no circular imports
- B-C: Minor coupling issues; some features mixed in shared/; one God widget
- D: No clear architecture; business logic in widgets; circular dependencies
- F: All code in lib/ root; no separation; spaghetti imports

### Code Style
- A: Zero lint warnings, consistent naming, proper null-safety, organized imports
- B-C: Minor lint issues; a few dynamic types; some missing docs on public APIs
- D: Widespread `dynamic`, suppressed lint rules, inconsistent naming
- F: No analysis_options.yaml; `// ignore` everywhere; no null-safety

### Performance
- A: Const constructors everywhere possible, proper keys, lazy builders for lists
- B-C: Some missing const; occasional unnecessary rebuilds
- D: setState in large widgets; no RepaintBoundary; O(n) in build methods
- F: Rebuilding entire tree on every state change; sync IO on main thread

### Best Practices
- A: Tests present, proper error handling, Result pattern, crash reporting
- B-C: Some missing tests; sparse error handling in edge cases
- D: No tests; catch-all `catch(e){}` blocks; hardcoded strings
- F: Hardcoded credentials; no error handling; no crash reporting

## Rules

- One grade per category — do not average
- Every grade must cite >=1 evidence file path + line number
- F grade requires 3+ CRITICAL violations in that category
- A grade requires zero violations and positive evidence
- Include "Top 5 Priority Fixes" ranked by severity x frequency
- Read files only — never modify source code

## Output

HTML report saved to `Documents/QualityAudit_{date}.html` unless user specifies a different path.

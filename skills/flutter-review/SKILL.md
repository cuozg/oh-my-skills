---
name: flutter-review
description: >
  Unified Flutter review skill — reviews local changes, GitHub PRs, or full Flutter projects.
  For local changes, adds inline // REVIEW comments to .dart files. For GitHub PRs, classifies
  changed files by type (.dart, .yaml, assets), assesses change size, spawns parallel specialist
  reviews (code quality, architecture, state management, performance), aggregates findings, and
  posts APPROVE or REQUEST_CHANGES via GitHub API. For project audits, grades architecture,
  code style, performance, best practices A-F with an HTML report. Use whenever the user says
  "review my code," "review this PR," "check my changes," "review PR #123," "audit this project,"
  "code quality report," "is this ready to merge," or wants any form of Flutter code or architecture
  review. Also triggers on "check the widgets," "review state management," or "review the providers."
---

# flutter-review

Detect review target, classify changed file types and size, delegate specialist reviews to parallel subagents, aggregate findings, deliver results — inline comments for local, GitHub comments + APPROVE/REQUEST_CHANGES for PRs, HTML reports for audits.

## Step 1 — Detect Review Mode

| Signal | Mode | Reference |
|--------|------|-----------|
| PR URL/number, "PR", "pull request", "merge" | **PR Review** | `references/github-review.md` |
| "review my code", "check changes", specific file, no PR | **Local Review** | `references/local-review.md` |
| "audit project", "quality report", "tech debt", "rate codebase" | **Project Audit** | `references/project-audit.md` |

## Step 2 — Execute

### PR Review

1. **Fetch PR** — follow `references/github-review.md`
2. **Classify files** by type and spawn specialist subagents in parallel:
   - `.dart` → code review (size-aware: minor = single-pass, large = parallel subagents)
   - `.yaml` (pubspec, analysis_options, build configs) → dependency & config review
   - Asset files (images, fonts, l10n) → asset organization review
   - `.dart` with new providers/notifiers/blocs → state management review
   - `.dart` with new repositories/services/APIs → architecture review
3. **Specialist checklists** — load from `flutter-standards` via `read_skill_file("flutter-standards", "references/<file>")`:
   - `dart-style-guide.md` — naming, formatting, null-safety
   - `architecture-patterns.md` — feature-first, layered deps, repository pattern
   - `state-management-guide.md` — Riverpod patterns, notifier design
   - `performance-optimization.md` — rebuilds, const, lazy build
   - `error-handling.md` — exception hierarchy, Result pattern
   - `async-streams.md` — Future/Stream handling, error propagation
   - `testing-patterns.md` — test coverage gaps
4. **Aggregate** — deduplicate by (path, line), keep highest severity, sort file -> line
5. **Final decision** — APPROVE or REQUEST_CHANGES per `references/github-review.md` decision rules
6. **Submit** — single review POST via `gh api`, verify posted

### Local Review

Follow `references/local-review.md`:
`git diff HEAD` -> filter `.dart` files -> read full files -> spawn parallel subagents (one per criterion from `references/review-checklist.md`) -> aggregate -> insert `// -- REVIEW` comments -> apply safe fixes -> `task_create` for unfixed issues.

### Project Audit

Follow `references/project-audit.md`:
Scope `.dart` + config files -> analyze 4 categories (Architecture, Code Style, Performance, Best Practices) -> grade A-F -> generate HTML report.

## Comment Format (PR)

````
**{icon} Title** — `SEVERITY`

{what is wrong, why it matters}

```suggestion
{corrected code}
```
````

Suggestion blocks required for MEDIUM+ severity.

## Severity Scale

CRITICAL -> HIGH -> MEDIUM -> LOW -> STYLE

Minimum floors: `setState` in large widget -> MEDIUM | Missing `dispose()` for controllers/streams -> HIGH | Unhandled async error -> HIGH | `!` bang operator on nullable without check -> MEDIUM | Widget method extraction (should be class) -> LOW

## Standards

Load `flutter-standards` for all checklists via `read_skill_file("flutter-standards", "references/<path>")`:

- `dart-style-guide.md` — naming, formatting, null-safety, import ordering
- `architecture-patterns.md` — feature-first, layered architecture, repository pattern
- `state-management-guide.md` — Riverpod, BLoC, Provider patterns
- `code-organization.md` — folder layout, pubspec, barrel files
- `testing-patterns.md` — unit, widget, golden tests, AAA pattern
- `async-streams.md` — Future, Stream, error propagation
- `ui-best-practices.md` — widget composition, const, keys, responsive layout
- `performance-optimization.md` — rebuild profiling, RepaintBoundary, frame budget
- `debug-logging.md` — logging patterns, DevTools
- `dependency-injection.md` — Riverpod as DI, scoping strategies
- `asset-management.md` — images, fonts, flutter_gen, localization
- `error-handling.md` — exception hierarchies, Result pattern, crash reporting

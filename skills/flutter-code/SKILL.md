---
name: flutter-code
description: >
  Unified Flutter/Dart coding skill — write, extend, or optimize Dart code across all domains.
  Auto-triages: Quick (single-file widget, provider, model, utility, service), Deep (multi-file
  features, state machines, system builds, refactors spanning 3+ files), Optimize (simplify/clean
  up without behavior change). MUST use for ANY Flutter/Dart code request — writing widgets,
  creating providers, implementing features, building services, refactoring, cleaning up code,
  reducing rebuilds. Triggers: "write a widget," "create a provider," "build a feature,"
  "implement service," "refactor," "clean up," "simplify," "optimize this." Do not use for
  UI-focused layout work (flutter-ui), tests (flutter-test), or debugging (flutter-debug).
metadata:
  author: cuongnp
  version: "1.0"
---
# flutter-code

Detect scope, pick mode, implement. Match local patterns, verify with analyzer, deliver complete code.

## Step 1 — Detect Mode

| Signal | Mode |
|--------|------|
| One `.dart` file, single widget/provider/model/utility | **Quick** |
| 2+ files, build feature, implement service+provider+UI, refactor across classes | **Deep** |
| "Clean up," "simplify," "optimize," "reduce rebuilds," behavior unchanged | **Optimize** |

State triage: "This is [mode] — [reason]."

## Step 2 — Execute

### Quick Mode

Load `read_skill_file("flutter-code", "references/quick-mode.md")` for patterns.

1. **Qualify** — confirm one `.dart` file suffices; escalate to Deep if scope grows
2. **Discover** — read target + 1-2 nearby files for naming, import style, provider conventions
3. **Implement** — smallest complete change matching local style; use `const` constructors, proper null-safety, trailing commas
4. **Verify** — `lsp_diagnostics` on changed file
5. **Handoff** — file path, what changed, usage example, codegen reminder if `@riverpod` used

### Deep Mode

Load `read_skill_file("flutter-code", "references/deep-mode.md")` for multi-file workflow.

1. **Qualify** — confirm 2+ files needed; switch to Quick if single-file
2. **Discover** — read affected files + project structure for feature-first layout, existing providers, router config
3. **Plan** — list every file, layer (data/providers/presentation), dependency order
4. **Implement** — data layer first (models, repos) → providers (Notifier/AsyncNotifier) → presentation (screens, widgets)
5. **Verify** — `lsp_diagnostics` per layer, then all files
6. **Handoff** — changed paths, architecture notes, codegen commands (`dart run build_runner build`), testing guidance

### Optimize Mode

Load `read_skill_file("flutter-code", "references/optimize-mode.md")` for refactoring patterns.

1. **Read** — load file(s); fully understand current behavior before touching anything
2. **Identify** — dead code, unnecessary rebuilds, missing `const`, complex conditionals, duplicated logic, improper provider usage
3. **Refactor** — preserve behavior: extract widgets for rebuild isolation, add `const`, use `select()` for granular provider reads, simplify control flow, remove dead imports
4. **Verify** — `lsp_diagnostics` on every changed file
5. **Report** — what changed, why, rebuild/performance impact

## Rules

- Local style wins — project patterns trump references
- Never leave `TODO`, stubs, or partially wired code
- One class per file, file name = class name in snake_case
- Bug fixes: minimal diff, no mixed refactors
- `lsp_diagnostics` after every code change
- Riverpod codegen (`@riverpod`) is default — use manual providers only if project already does
- Always add trailing commas for multi-line argument lists
- Prefer `const` constructors wherever possible
- Ambiguity → simplest implementation; state assumption in handoff

## Escalation

| From | To | When |
|------|----|------|
| Quick | Deep | Work requires a second file or new feature layer |
| Deep | Quick | Plan reveals single-file scope |
| Any | Optimize | User pivots to cleanup-only |

Carry forward context; tell user why.

## Standards

Load on demand via `read_skill_file("flutter-standards", "references/<path>")`:

- `dart-style-guide.md` — Naming, formatting, null-safety, linting rules
- `architecture-patterns.md` — Feature-first structure, layered architecture, repository pattern
- `state-management-guide.md` — Riverpod 2.x codegen, Notifier/AsyncNotifier, provider scoping
- `code-organization.md` — Feature folder anatomy, barrel files, pubspec essentials
- `dependency-injection.md` — Riverpod as DI, service locator alternatives
- `async-streams.md` — Future/Stream patterns, error propagation, Completer usage
- `testing-patterns.md` — Testability patterns (DI-friendly, mockable design)
- `performance-optimization.md` — Rebuild profiling, RepaintBoundary, memory optimization
- `debug-logging.md` — Structured logging, DevTools integration

---
name: flutter-ui
description: >
  Unified Flutter UI skill — compose screens, widgets, themes, and responsive layouts.
  Auto-triages: Quick (single widget, one screen, layout fix, simple styling) or Deep
  (multi-screen systems, custom themes, responsive breakpoints, animations, component
  libraries). MUST use for ANY Flutter UI composition request — building screens, styling
  widgets, theming, responsive layout, design systems, onboarding flows. Triggers: "build
  a screen," "create a widget," "add dark mode," "responsive layout," "fix padding,"
  "design system," "component library," "onboarding flow." Do not use for business logic,
  state management, or services (flutter-code), tests (flutter-test), or debugging
  (flutter-debug).
metadata:
  author: cuongnp
  version: "1.0"
---
# flutter-ui

Detect scope, pick mode, compose UI. Match local patterns, verify with analyzer, deliver complete widgets.

## Step 1 — Detect Mode

| Signal | Quick | Deep |
|--------|-------|------|
| Scope | Single widget/screen | Multi-screen system |
| Complexity | Built-in widgets, simple layout | Custom theme, responsive breakpoints, animations |
| Time | <1h | 1-8h |
| Files | 1-2 | 3+ |

State triage: "This is [mode] — [reason]."

## Step 2 — Execute

### Quick Mode

Load `read_skill_file("flutter-ui", "references/quick-mode.md")` for patterns.

1. **Qualify** — confirm 1-2 files suffice; escalate to Deep if scope grows
2. **Discover** — read target + nearby widgets for spacing, theme usage, naming patterns
3. **Implement** — compose widget/screen matching local style; use `const` constructors, `AppSpacing`, trailing commas
4. **Verify** — `lsp_diagnostics` on changed file
5. **Handoff** — file path, widget preview description, usage example

### Deep Mode

Load `read_skill_file("flutter-ui", "references/deep-mode.md")` for multi-screen workflow.
Load `read_skill_file("flutter-ui", "references/theming-guide.md")` if theming is involved.
Load `read_skill_file("flutter-ui", "references/responsive-design.md")` if responsive layout is needed.

1. **Qualify** — confirm 3+ files needed; switch to Quick if single-file
2. **Discover** — read project structure, existing theme, shared widgets, spacing constants
3. **Plan** — list every file: theme config, shared widgets, screens, animations
4. **Implement** — theme/constants first → shared widgets → screens → animations
5. **Verify** — `lsp_diagnostics` on all files
6. **Handoff** — file list, architecture notes, theme usage examples, screenshot suggestions

## Rules

- Local style wins — project patterns trump references
- Never leave `TODO`, stubs, or partially wired code
- One widget class per file, file name = class name in snake_case
- `const` constructors everywhere possible
- Extract widgets into classes, not methods (methods rebuild with parent)
- Use `AppSpacing` constants — never magic numbers for padding/margins
- `build()` methods stay lean (<30 lines); extract sections into child widgets
- `lsp_diagnostics` after every code change
- Always add trailing commas for multi-line argument lists

## Escalation

| From | To | When |
|------|----|------|
| Quick | Deep | Scope grows to 3+ files, needs theme system or responsive breakpoints |
| Deep | Quick | Plan reveals single-widget scope |
| Any | flutter-code | Task involves state management, navigation, API integration, or services |

Carry forward context; tell user why.

## Standards

Load on demand via `read_skill_file("flutter-standards", "references/<path>")`:

- `ui-best-practices.md` — Widget composition, const, keys, responsive layout, theming
- `dart-style-guide.md` — Naming, formatting, null-safety, linting rules
- `performance-optimization.md` — Rebuild profiling, RepaintBoundary, memory optimization
- `asset-management.md` — Images, fonts, flutter_gen, asset organization
- `code-organization.md` — Feature folder anatomy, barrel files, pubspec essentials

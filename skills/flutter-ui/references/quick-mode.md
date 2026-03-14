# Quick Mode — Single Widget/Screen

Compose one widget or screen with proper layout, styling, and const enforcement.

## Workflow

1. **Qualify** — confirm 1-2 files suffice; escalate to Deep if scope grows
2. **Discover** — read target + nearby widgets for spacing, theme usage, naming
3. **Implement** — compose widget matching local style and spacing constants
4. **Verify** — `lsp_diagnostics` on changed file
5. **Handoff** — file path, widget preview, usage example

## Widget Extraction

- **Extract widgets into classes** — not methods. Methods rebuild the entire parent.
- Each extracted widget gets its own file if reusable, inline `const` class if local.
- Pass data via constructor, not by capturing parent scope.

## Spacing Constants

Use `AppSpacing` — never hardcode padding/margin values:

| Constant | Value | Usage |
|----------|-------|-------|
| `xs` | 4 | Tight gaps, icon padding |
| `sm` | 8 | List item spacing, chip gaps |
| `md` | 16 | Section padding, card insets |
| `lg` | 24 | Screen edge padding |
| `xl` | 32 | Large section separators |

## Layout Patterns

- **Row/Column** — `MainAxisAlignment` for primary, `CrossAxisAlignment` for cross
- **Stack** — overlapping layers with `Positioned` children
- **Wrap** — flowing chips/tags that wrap to next line
- **SizedBox** — preferred spacer via `AppSpacing.gap16` constants

## Rules

- `const` constructors on every stateless widget
- `build()` body under 30 lines — extract sections into child widgets
- One widget class per file, file name = class name in `snake_case`
- Trailing commas on all multi-line argument lists
- Access theme via context extensions: `context.textTheme`, `context.colorScheme`
- Never hardcode colors or text styles — always pull from theme

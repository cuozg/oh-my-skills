# Deep Mode — Multi-Screen UI Systems

Build complete UI systems spanning 3+ files with shared widgets, theming, and responsive layout.

## Workflow

1. **Qualify** — confirm 3+ files needed; switch to Quick if single-file
2. **Discover** — read project structure, existing theme, shared widgets, spacing constants
3. **Plan** — list every file: theme config, shared widgets, screens, animations
4. **Implement** — theme/constants first → shared widgets → screens → animations
5. **Verify** — `lsp_diagnostics` on all files
6. **Handoff** — file list, architecture notes, theme usage, screenshot suggestions

## Implementation Order (ALWAYS follow)

1. **Theme/Constants** — AppTheme, AppSpacing, color tokens, text styles
2. **Shared Widgets** — reusable components (buttons, cards, inputs, badges)
3. **Screen Sections** — composable sections (headers, footers, content areas)
4. **Screens** — full screens composed from sections and shared widgets
5. **Animations** — page transitions, hero animations, micro-interactions

## Component Library Structure

Place shared widgets in `lib/shared/widgets/`, feature widgets under `lib/features/<feature>/presentation/widgets/`. Theme files in `lib/shared/theme/`.

## Animation Patterns

- **AnimatedContainer** — property transitions (size, color, padding)
- **Hero** — shared element transitions between screens
- **PageRouteBuilder** — custom page transitions (slide, fade, scale)
- **AnimatedSwitcher** — swap widgets with cross-fade or custom transition

## Accessibility

- Wrap decorative images with `ExcludeSemantics`
- Add `Semantics(label:)` to icon buttons and custom controls
- Ensure tap targets are at least 48x48 logical pixels

## Testing Strategy

- **Widget tests** — verify layout renders, interactions trigger callbacks
- **Golden tests** — pixel-perfect snapshots for design system components

## Rules

- Create files in dependency order (theme before widgets before screens)
- Every shared widget gets a `const` constructor and `///` doc comment
- Screen widgets compose from sections — never mega-build() methods
- Use `Theme.of(context)` and extensions — never hardcode colors or text styles

# Responsive Design

Breakpoints, adaptive layout, and platform-aware widget patterns.

## Breakpoint Constants

Define as `abstract final class Breakpoints` with `mobile = 600`, `tablet = 1024`. Add `isMobile(width)`, `isTablet(width)`, `isDesktop(width)` static helpers.

## LayoutBuilder (Parent-Constrained)

Use when sizing depends on parent constraints. Switch between wide/narrow layouts based on `constraints.maxWidth` vs breakpoint.

## MediaQuery (Screen-Level)

Use `MediaQuery.sizeOf(context)` for screen-level decisions. Prefer `sizeOf` over `of` — only rebuilds on size changes, not all media query changes.

## Adaptive Widget Pattern

Build `AdaptiveScaffold` showing sidebar on desktop and bottom nav on mobile. Use `MediaQuery.sizeOf(context).width` with breakpoint constants to switch.

## OrientationBuilder

Use for orientation-dependent layout (e.g., grid columns: 2 portrait, 4 landscape).

## Platform-Adaptive Design

- Use `.adaptive` constructors: `Switch.adaptive()`, `Slider.adaptive()`
- Check `Theme.of(context).platform` for larger platform-specific differences

## Rules

- Prefer `MediaQuery.sizeOf(context)` over `MediaQuery.of(context).size`
- Define breakpoints as constants — never hardcode width checks inline
- Use `LayoutBuilder` for component-level, `MediaQuery` for screen-level
- Test at mobile (375px), tablet (768px), and desktop (1440px) widths
- Use `SafeArea` on screens with notches or system UI overlap

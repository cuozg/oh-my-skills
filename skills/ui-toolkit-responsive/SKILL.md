---
name: ui-toolkit-responsive
description: "Responsive design for Unity UI Toolkit. Covers flexbox layout, length units, safe area handling, screen adaptation, aspect ratio strategies, responsive breakpoints, and common layout patterns. Use when: (1) Building adaptive UI that works across phone/tablet/desktop, (2) Implementing safe area handling for notched devices, (3) Creating responsive grid layouts, (4) Handling portrait/landscape orientation changes, (5) Setting up flexible containers with flexbox. Triggers: 'responsive', 'flexbox', 'safe area', 'screen adaptation', 'aspect ratio', 'breakpoint', 'flex-grow', 'portrait landscape', 'adaptive layout'."
---

# UI Toolkit Responsive Design

Flexbox-based responsive layout: safe area, orientation, adaptive patterns across devices.

## Output
Responsive USS layouts and C# handlers for safe area, orientation, and multi-device adaptation.

### Dragon Crashers Responsive Patterns
DC: flexbox column default, `flex-grow: 1` for content fill, `%` widths for grids, `GeometryChangedEvent` (not Update polling), SafeAreaBorder (borderWidth), MediaQuery (aspect ratio threshold), ThemeManager (PanelSettings+TSS swap), PositionToVisualElement (3D→UI alignment).

## Responsive Layout Patterns

> **Full code**: See [Responsive Code Patterns](references/responsive-code-patterns.md)

## Dragon Crashers Project Patterns

> **DC patterns**: See [Dragon Crashers Responsive](references/dragon-crashers-responsive.md)

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Fixed `px` on containers | `%` or `flex-grow` |
| Ignoring `Screen.safeArea` | `SafeAreaHandler` on root |
| Orientation check in `Update()` | `GeometryChangedEvent` |
| `position: absolute` for layout | Overlays/modals only |
| Separate UXML per orientation | Single UXML + USS class toggle |
| Padding when border color needed | `borderWidth` + `borderColor` (DC) |

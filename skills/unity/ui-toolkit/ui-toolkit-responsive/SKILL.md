---
name: ui-toolkit-responsive
description: "Responsive design for Unity UI Toolkit. Covers flexbox layout, length units, safe area handling, screen adaptation, aspect ratio strategies, responsive breakpoints, and common layout patterns. Use when: (1) Building adaptive UI that works across phone/tablet/desktop, (2) Implementing safe area handling for notched devices, (3) Creating responsive grid layouts, (4) Handling portrait/landscape orientation changes, (5) Setting up flexible containers with flexbox. Triggers: 'responsive', 'flexbox', 'safe area', 'screen adaptation', 'aspect ratio', 'breakpoint', 'flex-grow', 'portrait landscape', 'adaptive layout'."
---

# UI Toolkit Responsive Design

<!-- OWNERSHIP: MediaQuery, SafeAreaBorder (borderWidth + padding approaches), PositionToVisualElement, flexbox deep dive, orientation handling, length units, adaptive layout patterns. -->

> **Based on**: Unity 6 (6000.0), Dragon Crashers official sample

Flexbox-based responsive layout techniques for Unity UI Toolkit. Covers layout properties, safe area, orientation handling, and adaptive patterns that scale across devices.

> Related: [ui-toolkit-master](../ui-toolkit-master/SKILL.md) | [ui-toolkit-mobile](../ui-toolkit-mobile/SKILL.md) | [ui-toolkit-architecture](../ui-toolkit-architecture/SKILL.md) | [ui-toolkit-theming](../ui-toolkit-theming/SKILL.md) | [ui-toolkit-patterns](../ui-toolkit-patterns/SKILL.md)

### Dragon Crashers Responsive Patterns
Dragon Crashers uses these responsive techniques throughout:
- **Flexbox column layout** as default direction for all screens
- **`flex-grow: 1`** on content areas to fill remaining space after fixed headers/footers
- **Percentage widths** for grid items (inventory, character select)
- **`GeometryChangedEvent`** instead of `Update()` polling for layout recalculation
- **SafeAreaBorder** using `borderWidth` (not padding) with configurable multiplier — see [SafeAreaBorder](#safeareaborder-borderwidth-approach)
- **MediaQuery** class detecting Portrait/Landscape via aspect ratio threshold — see [MediaQuery](#mediaquery-aspect-ratio-detection)
- **ThemeManager** swapping PanelSettings + TSS per orientation — see [ThemeManager](#thememanager-orientation-aware-theming)
- **PositionToVisualElement** aligning 3D GameObjects to UI elements — see [PositionToVisualElement](#positiontovisualelement-world-to-ui-alignment)

## Responsive Layout Patterns

> **Full responsive code patterns**: See [Responsive Code Patterns](references/responsive-code-patterns.md) — covers Flexbox Deep Dive (property reference, layout examples, grow/shrink rules), Length Units, Percentages vs Pixels decision rules, SafeArea API (SafeAreaHandler.cs), Screen Adaptation Strategy (OrientationHandler, PanelSettings Scale Modes), Aspect Ratio Handling, Responsive Breakpoint Pattern (ScreenSizeClassifier.cs), Breakpoint USS Classes, Common Responsive Patterns (card grid, sidebar collapse).

---

## Dragon Crashers Project Patterns

> **Dragon Crashers responsive patterns**: See [Dragon Crashers Responsive](references/dragon-crashers-responsive.md) — covers MediaQuery aspect ratio detection, SafeAreaBorder borderWidth approach, ThemeManager orientation-aware theming, GeometryChangedEvent patterns, PositionToVisualElement world-to-UI alignment.

### MediaQuery: Aspect Ratio Detection

> Moved to [Dragon Crashers Responsive](references/dragon-crashers-responsive.md#mediaquery-aspect-ratio-detection). Subscribe to `MediaQueryEvents.AspectRatioUpdated` for orientation changes.

### SafeAreaBorder: borderWidth Approach

> Moved to [Dragon Crashers Responsive](references/dragon-crashers-responsive.md#safeareaborder-borderwidth-approach). Uses `borderWidth` instead of padding for visible colored bars behind the notch.

### ThemeManager: Orientation-Aware Theming

> Moved to [Dragon Crashers Responsive](references/dragon-crashers-responsive.md#thememanager-orientation-aware-theming). Swaps entire PanelSettings + TSS per orientation.

### GeometryChangedEvent Patterns

> Moved to [Dragon Crashers Responsive](references/dragon-crashers-responsive.md#geometrychangedevent-patterns). Primary layout trigger — never `Update()` polling.

### PositionToVisualElement: World-to-UI Alignment

> Moved to [Dragon Crashers Responsive](references/dragon-crashers-responsive.md#positiontovisualelement-world-to-ui-alignment). Aligns 3D GameObjects to VisualElements across orientation changes.

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Fixed `px` width on containers | Use `%` or `flex-grow` |
| Ignoring `Screen.safeArea` | Apply `SafeAreaHandler` on root |
| Hardcoded `left`/`top` positions | Use flexbox layout instead |
| Checking orientation in `Update()` | Use `GeometryChangedEvent` |
| Pixel sizes for all spacing | Use USS custom property tokens |
| Deep nesting for layout | Flatten hierarchy, use flex properties |
| `position: absolute` for layout | Reserve for overlays/modals only |
| Separate UXML per orientation | Single UXML + USS class toggling or TSS swapping |
| Using padding when border color needed for safe area | Use `borderWidth` + `borderColor` (DC approach) |
| Not accounting for borderWidth in coordinate conversion | Add `resolvedStyle.borderLeftWidth/borderTopWidth` |
| Hardcoded camera for UI-to-world alignment | Subscribe to `ThemeEvents.CameraUpdated` |

## Shared Resources

- [Dragon Crashers Insights](../references/dragon-crashers-insights.md) — responsive patterns from the official sample
- [Code Templates](../references/code-templates.md) — production-ready UXML/USS/C# templates
- [Performance Benchmarks](../references/performance-benchmarks.md) — layout cost targets
- [Official Docs Links](../references/official-docs-links.md) — Unity 6 layout and styling docs

## Official Documentation

- [Visual Tree / Layout Engine](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-VisualTree.html) — Yoga flexbox in UI Toolkit
- [USS Length Units](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-USS-UnityVariable.html) — px, %, auto
- [PanelSettings](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-Runtime-Panel-Settings.html) — scale modes, DPI
- [Screen.safeArea](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Screen-safeArea.html) — notch handling API

---
**← Previous**: [ui-toolkit-architecture](../ui-toolkit-architecture/SKILL.md) | **Next →**: [ui-toolkit-theming](../ui-toolkit-theming/SKILL.md)

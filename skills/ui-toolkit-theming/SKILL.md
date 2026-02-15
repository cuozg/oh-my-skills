---
name: ui-toolkit-theming
description: "Theme Style Sheets (TSS) and design token architecture for Unity UI Toolkit. Covers TSS/USS cascade, semantic color tokens, typography scale, spacing systems, runtime theme switching, and theme-aware components. Use when: (1) Building a design token system for UI, (2) Creating dark/light themes, (3) Switching themes at runtime, (4) Organizing USS variables into a scalable system, (5) Debugging style cascade and specificity issues. Triggers: 'theme', 'TSS', 'design tokens', 'dark mode', 'light mode', 'USS variables', 'theme switch', 'color palette', 'style cascade'."
---

# UI Toolkit Theming

Design token architecture and theme management using TSS, USS custom properties, and runtime theme switching.

### Dragon Crashers Theming Pattern
DC uses a **compound TSS system** (7 TSS: 2 orientations × 3 seasons + 1 base). Key: **BEM utility classes** with hardcoded values (no `:root` tokens), `:root` only for font/cursor in `Common.uss`, TSS inheritance for orientation+seasonal layers, `PanelSettings` + `ThemeStyleSheet` swapped together at runtime.

## TSS Architecture

```
 PanelSettings → TSS (.tss) → @import tokens.uss → @import base.uss → @import overrides.uss
                             → Default Style Sheet (.uss, optional fallback)
```

**TSS vs USS**: `.tss` wraps and imports USS files as a theme applied to all UIDocuments under a PanelSettings. USS defines actual styles. TSS controls *which* USS files are active.

## Design Token System

Single `tokens.uss` = source of truth for colors (primary/secondary/bg/text/border/status), typography (xs–4xl), spacing (4px grid: 0–64px), radius, transitions, shadows.

> **Complete tokens.uss**: See [Theming Code Patterns](references/theming-code-patterns.md#complete-tokensuss--light-theme-default)

## Color Token Organization

Use **semantic naming** (purpose-based). Raw values (`--color-primary-500`) map to semantic tokens (`--color-bg-primary`, `--color-text-primary`). **Rule: Components only reference semantic tokens.** Theme changes only update mappings.

## Typography & Spacing

USS utility classes for font sizes (`.text-xs` through `.text-3xl`), styles, alignment — consuming `var(--font-size-*)` tokens. See [Theming Code Patterns](references/theming-code-patterns.md#typography-system-uss).

4px spacing grid: `--space-1`(4px) through `--space-16`(64px). Usage: `padding: var(--space-4); margin-bottom: var(--space-3);`

## Theme Switching at Runtime

**Dark theme**: Copy `tokens.uss` → `tokens-dark.uss`, override only changed values (backgrounds, text, borders).

**TSS files**: One `.tss` per theme (Create > UI Toolkit > TSS Theme File). Each imports token file + shared styles. See [Theming Code Patterns](references/theming-code-patterns.md#tss-file-structure).

**ThemeManager**: Singleton MonoBehaviour swapping `PanelSettings.themeStyleSheet`. Persists via `PlayerPrefs`. Exposes `ToggleTheme()`, `SetTheme(bool)`, `OnThemeChanged` event. See [Theming Code Patterns](references/theming-code-patterns.md#c-thememanager).

**UXML + base-components.uss**: See [Theming Code Patterns](references/theming-code-patterns.md#uxml-consuming-tokens).

## USS Cascading Rules

Priority (low→high): Type (`Button {}`) → Class (`.my-class`) → Multi-class (`.card.selected`) → Name (`#my-button`) → Pseudo (`:hover`) → Inline (`style.color`).

Specificity: Type=0-0-1, Class=0-1-0, Name=1-0-0. No `!important` in USS. TSS imports override in order. `:root` custom properties inherited by all descendants.

## Creating a New Theme

1. Copy `tokens.uss` → `tokens-mytheme.uss` (change values only)
2. Create `.tss` in Editor, import token + shared USS files
3. Register in ThemeManager, call `SetTheme()`

## Theme-Aware Custom Controls

Consume tokens through USS classes, never hardcode. BEM naming. `[UxmlElement]` + `[UxmlAttribute]`. See [Theming Code Patterns](references/theming-code-patterns.md#theme-aware-custom-controls).

## Dragon Crashers: Compound Theming

7 TSS files (2 orientations × 3 seasons + 1 base), BEM utilities, hardcoded values. Simpler but inflexible. See [Theming Code Patterns](references/theming-code-patterns.md#dragon-crashers-compound-theming-system), [Dragon Crashers Insights](../ui-toolkit-architecture/references/dragon-crashers-insights.md), [Project Patterns](../ui-toolkit-architecture/references/project-patterns.md).

## Common Pitfalls

| Anti-Pattern | Correct Approach |
|-------------|-----------------|
| Hardcoded colors in USS/C# | `var(--color-*)` tokens / USS classes |
| Inline styles via `element.style` | `AddToClassList()` / `RemoveFromClassList()` |
| Deep specificity chains | BEM-style flat classes: `.list-item__label` |
| Duplicating token values | Single `tokens.uss` with `@import` |
| Skipping semantic tokens | Map raw palette → semantic names |
| Switching USS at runtime | Switch TSS on PanelSettings instead |
| Magic spacing numbers | `--space-*` tokens |



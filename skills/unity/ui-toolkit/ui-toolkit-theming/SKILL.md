---
name: ui-toolkit-theming
description: "Theme Style Sheets (TSS) and design token architecture for Unity UI Toolkit. Covers TSS/USS cascade, semantic color tokens, typography scale, spacing systems, runtime theme switching, and theme-aware components. Use when: (1) Building a design token system for UI, (2) Creating dark/light themes, (3) Switching themes at runtime, (4) Organizing USS variables into a scalable system, (5) Debugging style cascade and specificity issues. Triggers: 'theme', 'TSS', 'design tokens', 'dark mode', 'light mode', 'USS variables', 'theme switch', 'color palette', 'style cascade'."
---

# UI Toolkit Theming

<!-- OWNERSHIP: ThemeManager, TSS hierarchy/cascade, compound theming (orientation+season), design tokens (USS custom properties), BEM utility classes, runtime theme switching. -->

> **Based on**: Unity 6 (6000.0), Dragon Crashers official sample

Design token architecture and theme management for Unity UI Toolkit using TSS, USS custom properties, and runtime theme switching.

### Dragon Crashers Theming Pattern
Dragon Crashers uses a **compound TSS system** with 7 theme files (2 orientations × 3 seasons + 1 base). Key techniques:
- **BEM utility classes** with hardcoded values (`.color__text--white`, `.text__size--small`, `.button-orange`) — DC does **not** use `:root` CSS custom properties for design tokens
- **`:root`** is used only for font-definition and cursor in `Common.uss` — not for color/spacing/typography tokens
- **TSS inheritance chain** for layering orientation + seasonal decoration
- **`PanelSettings` + `ThemeStyleSheet` swapped together** at runtime for orientation changes (different reference resolutions per orientation)

## TSS Architecture

```
 PanelSettings (Inspector)
 ├── Theme Style Sheet (.tss)          ← Assigned here
 │   ├── @import url("tokens.uss")     ← Design tokens (variables)
 │   ├── @import url("base.uss")       ← Component styles using var()
 │   └── @import url("overrides.uss")  ← Theme-specific value overrides
 │
 └── Default Style Sheet (.uss)        ← Fallback (optional)

 Runtime flow:
 ┌────────────┐    ┌─────────┐    ┌──────────┐    ┌──────────────┐
 │ PanelSettings│──→│  TSS    │──→│  USS     │──→│ VisualElement │
 │ .themeStyle  │   │ (theme) │   │ (tokens) │   │ resolved style│
 │  Sheet       │   │         │   │ var()    │   │               │
 └────────────┘    └─────────┘    └──────────┘    └──────────────┘
```

**TSS vs USS**: A `.tss` file is a wrapper that imports USS files and applies them as a theme to all UIDocuments under a PanelSettings. USS files define the actual styles. TSS controls *which* USS files are active for a given theme.

## Design Token System

A single `tokens.uss` file is the source of truth for all design values — colors (primary, secondary, background, text, border, status), typography (font sizes xs–4xl, weights, line-heights), spacing (4px grid: 0–64px), border radius, transitions, and shadows.

> **Complete tokens.uss (light theme default)**: See [Theming Code Patterns](references/theming-code-patterns.md#complete-tokensuss--light-theme-default) — full `:root` block with all token categories.

## Color Token Organization

Use **semantic naming** (purpose-based) rather than raw color names:

```
 RAW VALUES (don't use directly in components)
 ┌──────────────────────────────┐
 │  --color-primary-500: #2196F3│
 │  --color-primary-700: #1976D2│
 │  --color-gray-100: #F5F5F5  │
 │  --color-gray-900: #212121  │
 └──────────┬───────────────────┘
            │  mapped to
            ▼
 SEMANTIC TOKENS (use these in components)
 ┌──────────────────────────────────┐
 │  --color-bg-primary     → white  │
 │  --color-text-primary   → gray900│
 │  --color-border-focus   → pri500 │
 │  --color-status-error   → red500 │
 └──────────────────────────────────┘
```

**Rule: Components only reference semantic tokens.** When themes change, only the mapping changes — components stay untouched.

## Typography System

USS utility classes for font sizes (`.text-xs` through `.text-3xl`), font styles (`.text-bold`, `.text-italic`), alignment, and compound heading/body classes — all consuming `var(--font-size-*)` tokens.

> **Full typography.uss**: See [Theming Code Patterns](references/theming-code-patterns.md#typography-system-uss) — covers size utilities, style utilities, heading-1/heading-2, body-text, caption-text.

## Spacing Scale

The 4px grid keeps spacing consistent across all components:

| Token | Value | Usage |
|-------|-------|-------|
| `--space-1` | 4px | Icon-to-text gap, tight padding |
| `--space-2` | 8px | Default inner padding, list item spacing |
| `--space-3` | 12px | Button padding, input padding |
| `--space-4` | 16px | Card padding, section spacing |
| `--space-6` | 24px | Panel margins, group spacing |
| `--space-8` | 32px | Screen edge padding |
| `--space-12` | 48px | Section dividers |
| `--space-16` | 64px | Major layout spacing |

```css
/* Usage in component USS */
.card {
    padding: var(--space-4);
    margin-bottom: var(--space-3);
    border-radius: var(--radius-lg);
    border-width: 1px;
    border-color: var(--color-border-default);
    background-color: var(--color-bg-elevated);
}
```

## Theme Switching at Runtime

### Dark Theme Token Overrides

```css
/* tokens-dark.uss — Override only the tokens that change */
:root {
    --color-bg-primary: #121212;
    --color-bg-secondary: #1E1E1E;
    --color-bg-tertiary: #2C2C2C;
    --color-bg-elevated: #1E1E1E;
    --color-bg-overlay: rgba(0, 0, 0, 0.7);

    --color-text-primary: #E0E0E0;
    --color-text-secondary: #9E9E9E;
    --color-text-disabled: #616161;
    --color-text-inverse: #212121;

    --color-border-default: #424242;
    --color-border-focus: #64B5F6;

    --color-primary-500: #64B5F6;
    --color-primary-700: #42A5F5;

    --shadow-color: rgba(0, 0, 0, 0.3);
}
```

### TSS Files

Create one `.tss` per theme. In Unity Editor: right-click in Project > Create > UI Toolkit > TSS Theme File. Each TSS imports a token file + shared component styles.

> **Light/dark TSS file examples**: See [Theming Code Patterns](references/theming-code-patterns.md#tss-file-structure) — covers light-theme.tss and dark-theme.tss import structure.

### C# ThemeManager

Singleton MonoBehaviour that swaps `PanelSettings.themeStyleSheet` between light/dark TSS assets. Persists preference via `PlayerPrefs`. Exposes `ToggleTheme()`, `SetTheme(bool)`, and `OnThemeChanged` event.

> **Full ThemeManager implementation**: See [Theming Code Patterns](references/theming-code-patterns.md#c-thememanager) — complete C# with Inspector fields, PlayerPrefs persistence, and static event API.

### UXML Consuming Tokens

> **Full UXML + base-components.uss examples**: See [Theming Code Patterns](references/theming-code-patterns.md#uxml-consuming-tokens) — covers UXML with token classes, theme-agnostic `.screen`, `.btn`, `.btn-primary` with hover/active states.

## USS Cascading Rules

Style resolution order (lowest to highest priority):

```
 1. Type selectors          →  Button { }            ← Lowest
 2. Class selectors         →  .my-class { }
 3. Multiple classes        →  .card.selected { }
 4. Name selectors          →  #my-button { }
 5. :hover / :active        →  .btn:hover { }
 6. Inline styles (C#)      →  style.color = ...     ← Highest
```

| Rule | Specificity | Example |
|------|-------------|---------|
| Type selector | 0-0-1 | `Label { }` |
| Class selector | 0-1-0 | `.heading { }` |
| Name selector | 1-0-0 | `#player-name { }` |
| Combined | Sum | `.card > Label` = 0-1-1 |
| Inline style (C#) | Wins all | `element.style.color` |

**Key differences from CSS:**
- USS has no `!important` keyword — use higher specificity or inline styles
- TSS imports are applied in order; later imports override earlier ones
- `:root` custom properties are inherited by all descendants

## Creating a New Theme — Step by Step

1. **Copy `tokens.uss` to `tokens-mytheme.uss`** — change only the variable values
2. **Create `mytheme.tss`** in the Editor (Create > UI Toolkit > TSS Theme File)
3. **Edit the `.tss`** to import your token file + shared component styles:
   ```css
   @import url("tokens-mytheme.uss");
   @import url("typography.uss");
   @import url("base-components.uss");
   ```
4. **Register in ThemeManager** — add the `ThemeStyleSheet` asset reference
5. **Test** — call `ThemeManager.SetTheme()` or use a debug button

## Theme-Aware Custom Controls

Custom controls should consume tokens through USS classes, never hardcode colors. Use BEM naming (`status-badge`, `status-badge--success`, `status-badge__label`) and `[UxmlElement]` with `[UxmlAttribute]` for properties.

> **Full StatusBadge example (C# + USS)**: See [Theming Code Patterns](references/theming-code-patterns.md#theme-aware-custom-controls) — covers `[UxmlElement]` StatusBadge with BEM classes, enum-driven state switching, and fully theme-aware USS.

## Dragon Crashers: Compound Theming System

DC uses a **compound TSS system** (7 TSS files: 2 orientations × 3 seasons + 1 base) with BEM utility classes and hardcoded values — no `:root` custom properties. DC's approach is simpler but inflexible (no dark mode); the `:root` variable system above is better for multi-theme apps.

> **Full DC compound theming details**: See [Theming Code Patterns](references/theming-code-patterns.md#dragon-crashers-compound-theming-system) — covers 7-file TSS matrix, decoration USS, orientation USS, ThemeManager dual trigger flow, and DC vs recommended approach comparison.

> **Full DC theming details**: See [Dragon Crashers Insights](../references/dragon-crashers-insights.md) and [Project Patterns](../references/project-patterns.md)

## Common Pitfalls

| Anti-Pattern | Problem | Correct Approach |
|-------------|---------|-----------------|
| Hardcoded colors in USS | Theme switch breaks styling | Use `var(--color-*)` tokens |
| Hardcoded colors in C# | Cannot be overridden by theme | Apply USS classes, not inline styles |
| Inline styles via `element.style` | Overrides all USS, defeats theming | Use `AddToClassList()` / `RemoveFromClassList()` |
| Deep specificity chains | `.panel > .content > .list > .item > Label` is fragile | Use BEM-style flat classes: `.list-item__label` |
| Duplicating token values | Values drift across files | Single `tokens.uss` with `@import` |
| Skipping semantic tokens | Components tied to raw colors | Map raw palette to semantic names |
| Switching USS at runtime | Causes full style recalculation | Switch TSS on PanelSettings instead |
| Magic numbers for spacing | Inconsistent spacing | Use `--space-*` tokens from the scale |

## Resources & Cross-References

- **Docs**: [TSS](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-tss.html) · [USS Custom Properties](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-USS-CustomProperties.html) · [USS Selectors](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-USS-Selectors.html) · [PanelSettings API](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/UIElements.PanelSettings.html)
- **Shared**: [Dragon Crashers Insights](../references/dragon-crashers-insights.md) · [QuizU Patterns](../references/quizu-patterns.md) · [Code Templates](../references/code-templates.md) · [Performance Benchmarks](../references/performance-benchmarks.md)
- **Related Skills**: [ui-toolkit-responsive](../ui-toolkit-responsive/SKILL.md) (MediaQuery, orientation layout) · [ui-toolkit-mobile](../ui-toolkit-mobile/SKILL.md) (device orientation, safe area)

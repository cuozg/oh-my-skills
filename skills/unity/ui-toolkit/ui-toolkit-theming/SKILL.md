---
name: ui-toolkit-theming
description: "Theme Style Sheets (TSS) and design token architecture for Unity UI Toolkit. Covers TSS/USS cascade, semantic color tokens, typography scale, spacing systems, runtime theme switching, and theme-aware components. Use when: (1) Building a design token system for UI, (2) Creating dark/light themes, (3) Switching themes at runtime, (4) Organizing USS variables into a scalable system, (5) Debugging style cascade and specificity issues. Triggers: 'theme', 'TSS', 'design tokens', 'dark mode', 'light mode', 'USS variables', 'theme switch', 'color palette', 'style cascade'."
---

# UI Toolkit Theming

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

Complete `tokens.uss` file — the single source of truth for all design values:

```css
/* tokens.uss — Light theme (default) */
:root {
    /* --- Color: Primary --- */
    --color-primary-50: #E3F2FD;   --color-primary-100: #BBDEFB;
    --color-primary-500: #2196F3;  --color-primary-700: #1976D2;
    --color-primary-900: #0D47A1;
    /* --- Color: Secondary --- */
    --color-secondary-500: #FF9800; --color-secondary-700: #F57C00;
    /* --- Color: Background --- */
    --color-bg-primary: #FFFFFF;   --color-bg-secondary: #F5F5F5;
    --color-bg-tertiary: #EEEEEE;  --color-bg-elevated: #FFFFFF;
    --color-bg-overlay: rgba(0, 0, 0, 0.5);
    /* --- Color: Text --- */
    --color-text-primary: #212121;   --color-text-secondary: #757575;
    --color-text-disabled: #BDBDBD;  --color-text-inverse: #FFFFFF;
    --color-text-link: #1976D2;
    /* --- Color: Border --- */
    --color-border-default: #E0E0E0; --color-border-focus: #2196F3;
    --color-border-error: #F44336;
    /* --- Color: Status --- */
    --color-status-success: #4CAF50; --color-status-warning: #FF9800;
    --color-status-error: #F44336;   --color-status-info: #2196F3;

    /* --- Typography --- */
    --font-size-xs: 10px;  --font-size-sm: 12px;  --font-size-md: 14px;
    --font-size-lg: 16px;  --font-size-xl: 20px;  --font-size-2xl: 24px;
    --font-size-3xl: 32px; --font-size-4xl: 40px;
    --font-weight-normal: normal; --font-weight-bold: bold;
    --line-height-tight: 1.2; --line-height-normal: 1.5;

    /* --- Spacing (4px base) --- */
    --space-0: 0px;  --space-1: 4px;  --space-2: 8px;   --space-3: 12px;
    --space-4: 16px; --space-5: 20px; --space-6: 24px;  --space-8: 32px;
    --space-10: 40px; --space-12: 48px; --space-16: 64px;

    /* --- Border Radius --- */
    --radius-none: 0px; --radius-sm: 2px;  --radius-md: 4px;
    --radius-lg: 8px;   --radius-xl: 12px; --radius-full: 9999px;

    /* --- Transitions --- */
    --transition-fast: 100ms; --transition-normal: 200ms;
    --transition-slow: 400ms; --ease-default: ease-in-out;

    /* --- Shadows (via border trick — USS has no box-shadow) --- */
    --shadow-color: rgba(0, 0, 0, 0.12);
    --shadow-width-sm: 1px; --shadow-width-md: 2px; --shadow-width-lg: 4px;
}
```

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

```css
/* typography.uss */
.text-xs  { font-size: var(--font-size-xs); }
.text-sm  { font-size: var(--font-size-sm); }
.text-md  { font-size: var(--font-size-md); }
.text-lg  { font-size: var(--font-size-lg); }
.text-xl  { font-size: var(--font-size-xl); }
.text-2xl { font-size: var(--font-size-2xl); }
.text-3xl { font-size: var(--font-size-3xl); }

.text-bold   { -unity-font-style: bold; }
.text-italic { -unity-font-style: italic; }
.text-left   { -unity-text-align: middle-left; }
.text-center { -unity-text-align: middle-center; }
.text-right  { -unity-text-align: middle-right; }

.heading-1 {
    font-size: var(--font-size-3xl); -unity-font-style: bold;
    color: var(--color-text-primary); margin-bottom: var(--space-4);
}
.heading-2 {
    font-size: var(--font-size-2xl); -unity-font-style: bold;
    color: var(--color-text-primary); margin-bottom: var(--space-3);
}
.body-text    { font-size: var(--font-size-md); color: var(--color-text-primary); }
.caption-text { font-size: var(--font-size-sm); color: var(--color-text-secondary); }
```

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

Create one `.tss` per theme. In Unity Editor: right-click in Project > Create > UI Toolkit > TSS Theme File.

**light-theme.tss** contents:
```css
@import url("tokens.uss");
@import url("typography.uss");
@import url("base-components.uss");
```

**dark-theme.tss** contents:
```css
@import url("tokens-dark.uss");
@import url("typography.uss");
@import url("base-components.uss");
```

### C# ThemeManager

```csharp
using UnityEngine;
using UnityEngine.UIElements;

/// <summary>
/// Switches the active theme on all PanelSettings assets at runtime.
/// Assign light/dark TSS assets via Inspector.
/// </summary>
public class ThemeManager : MonoBehaviour
{
    [SerializeField] private PanelSettings panelSettings;
    [SerializeField] private ThemeStyleSheet lightTheme;
    [SerializeField] private ThemeStyleSheet darkTheme;

    private static ThemeManager _instance;
    private bool _isDark;

    public bool IsDark => _isDark;

    public static event System.Action<bool> OnThemeChanged;

    private void Awake()
    {
        _instance = this;
        // Load saved preference
        _isDark = PlayerPrefs.GetInt("Theme_IsDark", 0) == 1;
        ApplyTheme();
    }

    public static void ToggleTheme()
    {
        if (_instance == null) return;
        _instance._isDark = !_instance._isDark;
        _instance.ApplyTheme();
        PlayerPrefs.SetInt("Theme_IsDark", _instance._isDark ? 1 : 0);
        OnThemeChanged?.Invoke(_instance._isDark);
    }

    public static void SetTheme(bool dark)
    {
        if (_instance == null || _instance._isDark == dark) return;
        _instance._isDark = dark;
        _instance.ApplyTheme();
        PlayerPrefs.SetInt("Theme_IsDark", dark ? 1 : 0);
        OnThemeChanged?.Invoke(dark);
    }

    private void ApplyTheme()
    {
        panelSettings.themeStyleSheet = _isDark ? darkTheme : lightTheme;
    }
}
```

### UXML Consuming Tokens

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
    <ui:VisualElement class="screen">
        <ui:VisualElement class="card">
            <ui:Label class="heading-2" text="Settings" />
            <ui:Label class="body-text" text="Choose your preferred theme." />
            <ui:Button class="btn btn-primary" name="theme-toggle" text="Toggle Theme" />
        </ui:VisualElement>
    </ui:VisualElement>
</ui:UXML>
```

```css
/* base-components.uss — theme-agnostic, uses tokens only */
.screen {
    flex-grow: 1;
    background-color: var(--color-bg-primary);
    padding: var(--space-8);
}

.btn {
    padding: var(--space-2) var(--space-4);
    border-radius: var(--radius-md);
    font-size: var(--font-size-md);
    -unity-font-style: bold;
    border-width: 0;
    transition: background-color var(--transition-fast) var(--ease-default);
}

.btn-primary {
    background-color: var(--color-primary-500);
    color: var(--color-text-inverse);
}

.btn-primary:hover {
    background-color: var(--color-primary-700);
}

.btn-primary:active {
    background-color: var(--color-primary-900);
}
```

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

Custom controls should consume tokens through USS classes, never hardcode colors:

```csharp
using UnityEngine.UIElements;

[UxmlElement]
public partial class StatusBadge : VisualElement
{
    public static readonly string ussClassName = "status-badge";
    public static readonly string successClass = "status-badge--success";
    public static readonly string warningClass = "status-badge--warning";
    public static readonly string errorClass = "status-badge--error";

    private readonly Label _label;

    [UxmlAttribute]
    public string Text
    {
        get => _label.text;
        set => _label.text = value;
    }

    [UxmlAttribute]
    public StatusType Status
    {
        get => _status;
        set { _status = value; UpdateStatusClass(); }
    }
    private StatusType _status;

    public enum StatusType { Success, Warning, Error }

    public StatusBadge()
    {
        AddToClassList(ussClassName);
        _label = new Label();
        _label.AddToClassList("status-badge__label");
        Add(_label);
    }

    private void UpdateStatusClass()
    {
        RemoveFromClassList(successClass);
        RemoveFromClassList(warningClass);
        RemoveFromClassList(errorClass);

        AddToClassList(_status switch
        {
            StatusType.Success => successClass,
            StatusType.Warning => warningClass,
            StatusType.Error => errorClass,
            _ => successClass
        });
    }
}
```

```css
/* status-badge.uss — fully theme-aware */
.status-badge {
    padding: var(--space-1) var(--space-3);
    border-radius: var(--radius-full);
    align-self: flex-start;
}

.status-badge__label {
    font-size: var(--font-size-sm);
    -unity-font-style: bold;
    color: var(--color-text-inverse);
}

.status-badge--success { background-color: var(--color-status-success); }
.status-badge--warning { background-color: var(--color-status-warning); }
.status-badge--error   { background-color: var(--color-status-error); }
```

## Dragon Crashers: Compound Theming System

The Dragon Crashers project implements a **compound theme** pattern that combines **orientation** (Portrait/Landscape) with **seasonal decoration** (Default/Christmas/Halloween) into a single theme string.

### Compound Theme Name Format

Theme names follow the pattern `"{Orientation}--{Season}"`:

```
 Orientation          Season            Compound Theme Name
 ──────────── × ──────────────── = ──────────────────────────
 Landscape      Default              "Landscape--Default"
 Landscape      Christmas            "Landscape--Christmas"
 Landscape      Halloween            "Landscape--Halloween"
 Portrait       Default              "Portrait--Default"
 Portrait       Christmas            "Portrait--Christmas"
 Portrait       Halloween            "Portrait--Halloween"
```

The `--` delimiter separates the two dimensions. `ThemeManager` uses `GetPrefix`/`GetSuffix` helpers to split and recombine these parts when either dimension changes independently.

### TSS Inheritance Chain (7-File Matrix)

TSS files are layered with `@import` so each level extends the previous:
```
 Assets/UI/Themes/
 ├── RuntimeTheme-Default.tss               ← Base: Unity defaults + Decoration-Default.uss
 ├── RuntimeTheme-Landscape.tss             ← @import Default.tss + all Landscape/*.uss
 │   ├── RuntimeTheme-Landscape--Christmas.tss  ← @import Landscape.tss + Decoration-Christmas.uss
 │   └── RuntimeTheme-Landscape--Halloween.tss  ← @import Landscape.tss + Decoration-Halloween.uss
 │
 └── RuntimeTheme-Portrait.tss              ← @import Default.tss + all Portrait/*.uss
     ├── RuntimeTheme-Portrait--Christmas.tss   ← @import Portrait.tss + Decoration-Christmas.uss
     └── RuntimeTheme-Portrait--Halloween.tss   ← @import Portrait.tss + Decoration-Halloween.uss
```

Each orientation TSS imports the Default base, then all per-screen layout overrides. Seasonal variants layer a single Decoration USS on top.

**Example — `RuntimeTheme-Landscape.tss`:**
```css
@import url("RuntimeTheme-Default.tss");

@import url("/Assets/UI/Uss/ThemeStyles/Landscape/MenuBar-Landscape.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Landscape/HomeScreen-Landscape.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Landscape/CharScreen-Landscape.uss");
/* ... all 10 per-screen landscape overrides ... */

VisualElement {}
```

**Example — `RuntimeTheme-Portrait--Halloween.tss`:**
```css
@import url("RuntimeTheme-Portrait.tss");
@import url("/Assets/UI/Uss/ThemeStyles/Decoration-Halloween.uss");

VisualElement {}
```

### Decoration USS Files

Seasonal decorations use **visibility toggling** — each Decoration USS shows one season's elements and hides the others:

```
 Assets/UI/Uss/ThemeStyles/
 ├── Decoration-Default.uss      ← Shows .theme__decoration--default, hides others
 ├── Decoration-Christmas.uss    ← Shows .theme__decoration--christmas, hides others
 └── Decoration-Halloween.uss    ← Shows .theme__decoration--halloween, hides others
```

**`Decoration-Christmas.uss`:**
```css
.theme__decoration--christmas {
    opacity: 1;
    display: flex;
}
.theme__decoration--halloween {
    opacity: 0;
    display: none;
}
.theme__decoration--default {
    display: none;
    opacity: 0;
}
```

In UXML, decorate screens with elements carrying these classes. The active TSS controls which decorations are visible without any C# code.

### Per-Screen Orientation USS

Each screen has paired USS files in `Assets/UI/Uss/ThemeStyles/{Landscape,Portrait}/` (10 per orientation, 20 total): `HomeScreen`, `CharScreen`, `ShopScreen`, `SettingsScreen`, `MenuBar`, plus 5 more.

### ThemeManager Implementation

`ThemeManager` (`Assets/Scripts/UI/Themes/ThemeManager.cs`) swaps **both** `PanelSettings` and `ThemeStyleSheet` on the `UIDocument` when themes change:

```csharp
// Pairs a Theme StyleSheet with a string key and PanelSettings
[Serializable]
public struct ThemeSettings
{
    public string theme;           // e.g. "Landscape--Default"
    public ThemeStyleSheet tss;    // The TSS asset
    public PanelSettings panelSettings;  // Orientation-specific PanelSettings
}

[ExecuteInEditMode]
public class ThemeManager : MonoBehaviour
{
    [SerializeField] UIDocument m_Document;
    [SerializeField] List<ThemeSettings> m_ThemeSettings;  // All 7 theme combos
    string m_CurrentTheme;

    void OnEnable()
    {
        // Direct theme changes from Settings UI
        ThemeEvents.ThemeChanged += OnThemeChanged;
        // Orientation changes from MediaQuery
        MediaQueryEvents.AspectRatioUpdated += OnAspectRatioUpdated;
        m_CurrentTheme = m_ThemeSettings[0].theme;
    }

    // Sets both PanelSettings and TSS on the UIDocument
    public void ApplyTheme(string theme)
    {
        m_Document.panelSettings = GetPanelSettings(theme);
        m_Document.panelSettings.themeStyleSheet = GetThemeStyleSheet(theme);
        m_CurrentTheme = theme;
    }

    // When orientation changes, keep the season suffix and swap orientation prefix
    void OnAspectRatioUpdated(MediaAspectRatio mediaAspectRatio)
    {
        string suffix = GetSuffix(m_CurrentTheme, "--");  // e.g. "--Halloween"
        string newThemeName = mediaAspectRatio.ToString() + suffix;
        ApplyTheme(newThemeName);  // "Portrait--Halloween"
    }
}
```

Key design: `ThemeManager` stores a `List<ThemeSettings>` with all 7 compound theme names. Each entry maps to both a TSS and a PanelSettings asset, allowing orientation-specific PanelSettings (e.g., different reference resolutions for Portrait vs Landscape).

### SettingsScreenController — Theme Data Flow

`SettingsScreenController` (`Assets/Scripts/UI/Controllers/SettingsScreenController.cs`) constructs the compound theme from orientation + season:

```csharp
public class SettingsScreenController : MonoBehaviour
{
    GameData m_SettingsData;
    MediaAspectRatio m_MediaAspectRatio = MediaAspectRatio.Undefined;

    void OnEnable()
    {
        MediaQueryEvents.ResolutionUpdated += OnResolutionUpdated;
        SettingsEvents.UIGameDataUpdated += OnUISettingsUpdated;
    }

    void OnResolutionUpdated(Vector2 resolution) =>
        m_MediaAspectRatio = MediaQuery.CalculateAspectRatio(resolution);

    // GameData.theme stores season only: "Default", "Christmas", "Halloween"
    void UpdateTheme()
    {
        string newTheme = m_MediaAspectRatio.ToString() + "--" + m_SettingsData.theme;
        ThemeEvents.ThemeChanged(newTheme);  // e.g. "Landscape--Christmas"
    }
}
```

### SettingsView — Theme UI Controls

`SettingsView` (`Assets/Scripts/UI/UIViews/SettingsView.cs`) uses a `DropdownField` for theme selection, storing only the season part in `GameData`:

```csharp
// Query the dropdown from UXML
m_ThemeDropdown = m_TopElement.Q<DropdownField>("settings__theme-dropdown");

// Register callback
m_ThemeDropdown.RegisterValueChangedCallback(ChangeThemeDropdown);

void ChangeThemeDropdown(ChangeEvent<string> evt)
{
    // Save season name only — orientation is added by SettingsScreenController
    m_LocalUISettings.theme = evt.newValue;  // "Default", "Christmas", or "Halloween"
    SettingsEvents.UIGameDataUpdated?.Invoke(m_LocalUISettings);
}
```

### Event-Driven Theme Update Flow

Two independent triggers converge on `ThemeManager.ApplyTheme()`:

```
 Season change (user action):
   SettingsView → SettingsEvents.UIGameDataUpdated → SettingsScreenController.UpdateTheme()
     → constructs "Portrait--Halloween" → ThemeEvents.ThemeChanged → ThemeManager.ApplyTheme()

 Orientation change (device rotation):
   MediaQuery → MediaQueryEvents.AspectRatioUpdated → ThemeManager.OnAspectRatioUpdated()
     → keeps "--Halloween" suffix, swaps prefix → ApplyTheme("Landscape--Halloween")
```

**Key events** (`Assets/Scripts/UI/Events/`): `ThemeEvents.ThemeChanged` (`Action<string>`, compound theme name), `ThemeEvents.CameraUpdated` (`Action<Camera>`), `SettingsEvents.UIGameDataUpdated` / `GameDataLoaded` / `SettingsUpdated` (all `Action<GameData>`).

### Adding a New Season

To add a seasonal theme (e.g., Easter):
1. Create `Decoration-Easter.uss` — show `.theme__decoration--easter`, hide all others
2. Create `RuntimeTheme-Landscape--Easter.tss` and `RuntimeTheme-Portrait--Easter.tss` (import orientation TSS + `Decoration-Easter.uss`)
3. Add 2 entries to `ThemeManager.m_ThemeSettings`: `"Landscape--Easter"` and `"Portrait--Easter"`
4. Add `"Easter"` to the Settings UXML dropdown and `.theme__decoration--easter { display: none; opacity: 0; }` to existing Decoration USS files

## Dragon Crashers: Actual USS Organization

Dragon Crashers organizes USS into a 7-file **Base layer** of BEM utility classes, plus per-screen USS, theme decoration USS, and orientation USS. Unlike the `:root` variable approach recommended above, DC uses **hardcoded values in utility classes** — a pragmatic approach that trades design-token flexibility for simplicity.

### Base USS Files

All 7 Base USS files live in `Assets/UI/Uss/Base/` and are imported by every UXML screen:

#### Colors.uss (45 lines)
```css
/* from Assets/UI/Uss/Base/Colors.uss */

/* Text colors — BEM utility classes with hardcoded RGB values */
.color__text--white { color: rgb(255, 255, 255); }
.color__text--gray { color: rgb(189, 181, 181); }
.color__text--orange { color: rgb(243, 156, 18); }
.color__text--blue { color: rgb(243, 156, 18); }  /* ⚠️ BUG: uses orange value, not blue */
.color__text--brown { color: rgb(106, 72, 45); }
.color__text--dark-brown { color: rgb(77, 46, 24); }

/* Background colors */
.color__background--white { background-color: rgb(255, 255, 255); }
.color__background--orange { background-color: rgb(243, 156, 18); }
.color__background--blue { background-color: rgb(52, 152, 219); }

/* Border colors */
.color__border--clear { border-color: rgba(0, 0, 0, 0); }
.color__border--white { border-color: rgb(255, 255, 255); }
.color__border--light-brown { border-color: rgb(106, 72, 45); }
```

> **Pattern**: BEM naming `{category}__{property}--{value}`. Applied as additive classes in UXML: `<Label class="color__text--white text__size--large">`.

#### Text.uss (41 lines)
```css
/* from Assets/UI/Uss/Base/Text.uss */

/* Font definition — applied to all text elements */
* {
    -unity-font-definition: url('/Assets/UI/Fonts/AlfaSlabOne-Regular SDF.asset');
}

/* Text style utilities */
.text__style--bold { -unity-font-style: bold; }
.text__style--normal { -unity-font-style: normal; }

/* Text size scale — fixed pixel values, not token-based */
.text__size--small { font-size: 35px; }
.text__size--medium { font-size: 45px; }
.text__size--large { font-size: 60px; }
.text__size--extra-large { font-size: 80px; }

/* Text shadow applied to all text */
.text__style--bold { text-shadow: 2px 2px 0 rgb(0, 0, 0); }
.text__size--small { text-shadow: 1px 1px 0 rgb(0, 0, 0); }
```

#### Common.uss (118 lines)
```css
/* from Assets/UI/Uss/Base/Common.uss */

/* `:root` is used ONLY for font and cursor — not design tokens */
:root {
    -unity-font-definition: url('/Assets/UI/Fonts/AlfaSlabOne-Regular SDF.asset');
    cursor: url('/Assets/UI/Textures/Cursors/Cursor_A.png') 9 2;
}

/* Border utilities */
.border__width--0 { border-width: 0; }
.border__radius--10 { border-radius: 10px; }
.border__radius--25 { border-radius: 25px; }

/* Alignment */
.alignment--center {
    align-items: center;
    justify-content: center;
}

/* Screen anchor positions (absolute positioning helpers) */
.screen__anchor--top { position: absolute; top: 0; left: 0; right: 0; }
.screen__anchor--bottom { position: absolute; bottom: 0; left: 0; right: 0; }
.screen__anchor--top-left { position: absolute; top: 0; left: 0; }
.screen__anchor--top-right { position: absolute; top: 0; right: 0; }
.screen__anchor--bottom-left { position: absolute; bottom: 0; left: 0; }
.screen__anchor--bottom-right { position: absolute; bottom: 0; right: 0; }
.screen__anchor--fill { position: absolute; top: 0; bottom: 0; left: 0; right: 0; }

/* Tileable background images */
.tileable--horizontal {
    -unity-background-scale-mode: stretch-to-fill;
    background-repeat: repeat;
}

/* Theme decoration default state — hidden by default, shown by Decoration USS */
.theme__decoration--default { display: flex; opacity: 1; }
```

#### Buttons.uss (65 lines)
```css
/* from Assets/UI/Uss/Base/Buttons.uss */

/* Base button — transparent background, absolute positioning, transition on scale */
Button {
    background-color: rgba(0, 0, 0, 0);
    border-width: 0;
    position: absolute;
    transition: scale 0.25s;
}

Button:hover { scale: 1.1; }

/* Colored buttons use background-image tint, NOT background-color */
.button-orange {
    -unity-background-image-tint-color: rgb(243, 156, 18);
}
.button-green {
    -unity-background-image-tint-color: rgb(46, 204, 113);
}
.button-gray {
    -unity-background-image-tint-color: rgb(149, 165, 166);
}

/* Inactive state — reduced opacity, no hover effect */
.button--inactive {
    -unity-background-image-tint-color: rgb(130, 130, 130);
    opacity: 0.6;
}
.button--inactive:hover { scale: 1; }
```

> **Key pattern**: Buttons use `-unity-background-image-tint-color` for state changes, not `background-color`. The base image comes from a texture atlas, and tint color modifies the appearance. This allows a single button sprite to have many color variants.

#### Sliders.uss (54 lines)
```css
/* from Assets/UI/Uss/Base/Sliders.uss */

/* Custom slider — replaces default Unity parts with images */
.unity-base-slider__dragger {
    background-image: url('/Assets/UI/Textures/Sliders/slider_knob.png');
    width: 60px; height: 60px;
    -unity-background-image-tint-color: rgb(243, 156, 18);
}

.unity-base-slider__tracker {
    background-image: url('/Assets/UI/Textures/Sliders/slider_track.png');
    height: 20px;
}

.unity-base-slider__drag-container {
    min-height: 60px;
}
```

#### Dropdowns.uss (37 lines)
```css
/* from Assets/UI/Uss/Base/Dropdowns.uss */
/* ⚠️ NOTE: This file MUST be imported via TSS, not UXML.
   Dropdown compound element parts appear grayed out in UIBuilder Hierarchy
   when imported via UXML — they only work correctly via TSS import. */

.unity-base-dropdown__label {
    font-size: 35px;
    color: rgb(255, 255, 255);
    -unity-text-align: middle-center;
}

.unity-base-dropdown__container-inner {
    background-color: rgb(51, 35, 20);
    border-color: rgb(106, 72, 45);
    border-width: 3px;
}

.unity-base-dropdown__item:hover {
    background-color: rgb(106, 72, 45);
}
```

#### Cursors.uss (140 lines)
```css
/* from Assets/UI/Uss/Base/Cursors.uss */

/* Two-cursor system:
   Cursor_A (arrow) = non-interactive elements
   Cursor_B (pointer) = interactive/clickable elements */

/* Non-interactive elements use Cursor_A (default arrow) */
VisualElement { cursor: url('/Assets/UI/Textures/Cursors/Cursor_A.png') 9 2; }
Label { cursor: url('/Assets/UI/Textures/Cursors/Cursor_A.png') 9 2; }

/* Interactive elements use Cursor_B (pointer hand) */
Button { cursor: url('/Assets/UI/Textures/Cursors/Cursor_B.png') 9 2; }
Toggle { cursor: url('/Assets/UI/Textures/Cursors/Cursor_B.png') 9 2; }
Slider { cursor: url('/Assets/UI/Textures/Cursors/Cursor_B.png') 9 2; }
DropdownField { cursor: url('/Assets/UI/Textures/Cursors/Cursor_B.png') 9 2; }
ScrollView { cursor: url('/Assets/UI/Textures/Cursors/Cursor_B.png') 9 2; }
```

### Dragon Crashers vs Recommended Approach

| Aspect | Dragon Crashers (Actual) | Recommended (Modern) |
|---|---|---|
| **Color system** | BEM classes: `.color__text--white` with hardcoded `rgb()` | `:root` variables: `--color-text-primary` with `var()` |
| **Typography** | Fixed pixel sizes: `.text__size--small { font-size: 35px; }` | Token scale: `--font-size-sm: 12px` + `var()` |
| **Spacing** | Inline values per element | `--space-*` tokens from a 4px grid |
| **Theming** | Swap entire TSS file (7-file matrix) | Override `:root` variables per theme |
| **Strengths** | Simple, no variable indirection, easy to debug | Scalable, theme-flexible, single-source tokens |
| **Weaknesses** | Color changes require editing every class, no dark mode | Variable resolution adds debugging complexity |
| **Best for** | Fixed-theme games with orientation support | Apps needing dark/light modes or brand customization |

> **Takeaway**: DC's approach is valid for a single-theme game that needs orientation support. For multi-theme apps (dark/light, brand white-labeling), the `:root` variable approach from the earlier sections of this skill is more maintainable.

## Dragon Crashers: Real TSS File Contents

All TSS files live in `Assets/UI/Themes/`. Each ends with `VisualElement {}` — an empty rule required for TSS validity.

### RuntimeTheme-Default.tss (Base)
```css
/* from Assets/UI/Themes/RuntimeTheme-Default.tss */
@import url("unity-theme://default");

@import url("/Assets/UI/Uss/Base/ChartLibrary.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Decoration-Default.uss");
@import url("/Assets/UI/Uss/Base/Dropdowns.uss");

VisualElement {}
```

> **Note**: `@import url("unity-theme://default")` imports Unity's built-in default theme. `ChartLibrary.uss` is a third-party chart component. `Dropdowns.uss` must be in TSS (not UXML) because compound element sub-parts only resolve correctly via TSS.

### RuntimeTheme-Landscape.tss (Orientation)
```css
/* from Assets/UI/Themes/RuntimeTheme-Landscape.tss */
@import url("RuntimeTheme-Default.tss");

@import url("/Assets/UI/Uss/ThemeStyles/Landscape/MenuBar-Landscape.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Landscape/HomeScreen-Landscape.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Landscape/CharScreen-Landscape.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Landscape/ShopScreen-Landscape.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Landscape/MailScreen-Landscape.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Landscape/SettingsScreen-Landscape.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Landscape/InfoDialog-Landscape.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Landscape/LevelUpMessage-Landscape.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Landscape/Toolbar-Landscape.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Landscape/ToolbarShop-Landscape.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Landscape/Chat-Landscape.uss");

VisualElement {}
```

### RuntimeTheme-Portrait.tss (Orientation)
```css
/* from Assets/UI/Themes/RuntimeTheme-Portrait.tss */
@import url("RuntimeTheme-Default.tss");

@import url("/Assets/UI/Uss/ThemeStyles/Portrait/MenuBar-Portrait.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Portrait/HomeScreen-Portrait.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Portrait/CharScreen-Portrait.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Portrait/ShopScreen-Portrait.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Portrait/MailScreen-Portrait.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Portrait/SettingsScreen-Portrait.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Portrait/InfoDialog-Portrait.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Portrait/LevelUpMessage-Portrait.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Portrait/Toolbar-Portrait.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Portrait/ToolbarShop-Portrait.uss");
@import url("/Assets/UI/Uss/ThemeStyles/Portrait/Chat-Portrait.uss");

VisualElement {}
```

### Seasonal TSS Files
```css
/* from Assets/UI/Themes/RuntimeTheme-Landscape--Christmas.tss */
@import url("RuntimeTheme-Landscape.tss");
@import url("/Assets/UI/Uss/ThemeStyles/Decoration-Christmas.uss");

VisualElement {}
```

```css
/* from Assets/UI/Themes/RuntimeTheme-Portrait--Halloween.tss */
@import url("RuntimeTheme-Portrait.tss");
@import url("/Assets/UI/Uss/ThemeStyles/Decoration-Halloween.uss");

VisualElement {}
```

> **Pattern**: Seasonal files are 3 lines — import the orientation TSS + one Decoration USS override. Adding a new season requires only creating these small files plus the Decoration USS.

## Dragon Crashers: Orientation USS Comparison

Orientation USS files override the **same CSS classes** with different layout values. This side-by-side shows how the MenuBar and HomeScreen change between orientations:

### MenuBar — Landscape (Vertical Sidebar) vs Portrait (Horizontal Bar)

```css
/* from Assets/UI/Uss/ThemeStyles/Landscape/MenuBar-Landscape.uss */

/* Landscape: Vertical left sidebar, 13% width, full height */
.menu-bar__container {
    width: 13%;
    height: 100%;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    padding-top: 5%;
}

.menu-bar__logo {
    width: 90%;
    height: 12%;
}

.menu-bar__button-group {
    flex-direction: column;
    width: 80%;
    height: 60%;
    justify-content: space-around;
}

.menu-bar__button {
    width: 100%;
    height: 18%;
}
```

```css
/* from Assets/UI/Uss/ThemeStyles/Portrait/MenuBar-Portrait.uss */

/* Portrait: Horizontal bottom bar, full width, 13% height */
.menu-bar__container {
    width: 100%;
    height: 13%;
    flex-direction: row;              /* ← KEY CHANGE: row instead of column */
    justify-content: space-around;
    align-items: center;
    padding-top: 0;
    padding-left: 2%;
    padding-right: 2%;
}

.menu-bar__logo {
    width: 10%;                       /* ← Much smaller in portrait */
    height: 80%;
}

.menu-bar__button-group {
    flex-direction: row;              /* ← Horizontal in portrait */
    width: 80%;
    height: 90%;
    justify-content: space-around;
}

.menu-bar__button {
    width: 15%;                       /* ← Width-constrained in portrait */
    height: 90%;
}
```

> **Key pattern**: Same class names, completely different layout. Landscape uses `flex-direction: column` (vertical sidebar), Portrait uses `flex-direction: row` (horizontal bar). The TSS swap applies the correct USS file based on orientation — no C# class toggling needed.

### HomeScreen — Landscape vs Portrait

```css
/* from Assets/UI/Uss/ThemeStyles/Landscape/HomeScreen-Landscape.uss */
.home-screen__hero { width: 70%; height: 80%; }
.home-screen__sidebar { width: 25%; flex-direction: column; }
.home-screen__play-button { width: 40%; height: 15%; }
```

```css
/* from Assets/UI/Uss/ThemeStyles/Portrait/HomeScreen-Portrait.uss */
.home-screen__hero { width: 100%; height: 50%; }       /* ← Full width, half height */
.home-screen__sidebar { width: 100%; flex-direction: row; }  /* ← Below hero, horizontal */
.home-screen__play-button { width: 60%; height: 12%; }
```

## Dragon Crashers: Theme Event System

Two event files drive the theme system:

### ThemeEvents.cs
```csharp
// from Assets/Scripts/UI/Events/ThemeEvents.cs
using System;
using UnityEngine;

public static class ThemeEvents
{
    // Fired when compound theme changes (e.g. "Landscape--Christmas")
    public static Action<string> ThemeChanged;

    // Fired when the main camera reference changes (used by world-to-panel positioning)
    public static Action<Camera> CameraUpdated;
}
```

### MediaQueryEvents.cs
```csharp
// from Assets/Scripts/UI/Events/MediaQueryEvents.cs
using System;
using UnityEngine;

public static class MediaQueryEvents
{
    // Screen resolution changed
    public static Action<Vector2> ResolutionUpdated;

    // Aspect ratio classification changed (e.g. Portrait ↔ Landscape)
    public static Action<MediaAspectRatio> AspectRatioUpdated;

    // Safe area insets changed (notch, status bar)
    public static Action<Rect> SafeAreaUpdated;

    // DPI changed (display switch, settings change)
    public static Action<float> DpiUpdated;
}
```

> **Flow**: `MediaQuery` detects device changes → fires `MediaQueryEvents` → `ThemeManager` receives `AspectRatioUpdated` → swaps TSS to match new orientation → all UI elements re-resolve their styles from the new USS imports.

## Dragon Crashers Source Files

| Source File | Content |
|---|---|
| `Assets/UI/Uss/Base/Colors.uss` | BEM color utility classes (text, background, border) |
| `Assets/UI/Uss/Base/Text.uss` | Font definition, text style/size utilities |
| `Assets/UI/Uss/Base/Common.uss` | `:root` font/cursor, border/alignment/anchor/tileable utilities |
| `Assets/UI/Uss/Base/Buttons.uss` | Button type selector, hover/tint states, colored variants |
| `Assets/UI/Uss/Base/Sliders.uss` | Custom slider part styling with images |
| `Assets/UI/Uss/Base/Dropdowns.uss` | Dropdown compound element styling (TSS-only import) |
| `Assets/UI/Uss/Base/Cursors.uss` | Two-cursor system (arrow vs pointer) |
| `Assets/UI/Uss/ThemeStyles/Decoration-Default.uss` | Default season visibility toggles |
| `Assets/UI/Uss/ThemeStyles/Decoration-Christmas.uss` | Christmas season visibility toggles |
| `Assets/UI/Uss/ThemeStyles/Decoration-Halloween.uss` | Halloween season visibility toggles |
| `Assets/UI/Uss/ThemeStyles/Landscape/MenuBar-Landscape.uss` | Vertical sidebar layout (13% width, column) |
| `Assets/UI/Uss/ThemeStyles/Portrait/MenuBar-Portrait.uss` | Horizontal bottom bar layout (13% height, row) |
| `Assets/UI/Uss/ThemeStyles/Landscape/HomeScreen-Landscape.uss` | Wide hero + sidebar column layout |
| `Assets/UI/Uss/ThemeStyles/Portrait/HomeScreen-Portrait.uss` | Stacked hero + horizontal sidebar layout |
| `Assets/UI/Themes/RuntimeTheme-Default.tss` | Base TSS: Unity default + Decoration-Default + Dropdowns |
| `Assets/UI/Themes/RuntimeTheme-Landscape.tss` | Landscape TSS: Default + 11 Landscape USS imports |
| `Assets/UI/Themes/RuntimeTheme-Portrait.tss` | Portrait TSS: Default + 11 Portrait USS imports |
| `Assets/UI/Themes/RuntimeTheme-Landscape--Christmas.tss` | Seasonal: Landscape + Decoration-Christmas |
| `Assets/UI/Themes/RuntimeTheme-Portrait--Halloween.tss` | Seasonal: Portrait + Decoration-Halloween |
| `Assets/Scripts/UI/Themes/ThemeManager.cs` | Runtime theme switching (compound name, PanelSettings + TSS swap) |
| `Assets/Scripts/UI/Events/ThemeEvents.cs` | `ThemeChanged` and `CameraUpdated` static events |
| `Assets/Scripts/UI/Events/MediaQueryEvents.cs` | Resolution, aspect ratio, safe area, DPI events |
| `Assets/Scripts/UI/Controllers/SettingsScreenController.cs` | Constructs compound theme from orientation + season |
| `Assets/Scripts/UI/UIViews/SettingsView.cs` | Theme dropdown UI, stores season in GameData |

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

## Exercise: Dark/Light Theme Toggle

Create a minimal dark/light theme system with a toggle button.

1. Create `tokens.uss` with `:root` vars for `--color-bg-primary`, `--color-text-primary`, `--color-primary-500`
2. Create `tokens-dark.uss` overriding those 3 vars with dark values
3. Create `light-theme.tss` importing `tokens.uss` and `dark-theme.tss` importing `tokens-dark.uss`
4. Assign `light-theme.tss` to `PanelSettings.themeStyleSheet`
5. Create `ThemeManager.cs` that swaps TSS on button click
6. Create a simple UXML with a card + toggle button that uses `var(--color-*)` tokens

**Checklist**: ✅ Light theme renders with correct colors | ✅ Toggle swaps to dark | ✅ No hardcoded colors in USS or C# | ✅ Preference persists via `PlayerPrefs`

## Shared Resources

- [Dragon Crashers Insights](../references/dragon-crashers-insights.md) — theming patterns from the official sample
- [Code Templates](../references/code-templates.md) — production-ready UXML/USS/C# templates
- [Performance Benchmarks](../references/performance-benchmarks.md) — theme switch cost targets
- [Official Docs Links](../references/official-docs-links.md) — Unity 6 USS and TSS documentation

## Official Documentation

- [Theme Style Sheet (TSS)](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-tss.html) — creating and assigning themes
- [USS Custom Properties](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-USS-CustomProperties.html) — `var()` and `:root`
- [USS Selectors](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-USS-Selectors.html) — specificity rules
- [PanelSettings API](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/UIElements.PanelSettings.html) — runtime theme assignment

## Cross-References

- **[ui-toolkit-responsive](../ui-toolkit-responsive/SKILL.md)** — MediaQuery, aspect ratio detection, orientation-based layout switching that drives the orientation half of compound themes
- **[ui-toolkit-mobile](../ui-toolkit-mobile/SKILL.md)** — Device orientation handling, safe area, and mobile-specific PanelSettings that complement theme switching

---
**← Previous**: [ui-toolkit-responsive](../ui-toolkit-responsive/SKILL.md) | **Next →**: [ui-toolkit-databinding](../ui-toolkit-databinding/SKILL.md)

# Theming Code Patterns

> Referenced from [SKILL.md](../SKILL.md). Complete code examples for design tokens, theme switching, and theme-aware controls.

## Complete tokens.uss — Light Theme (Default)

Single source of truth for all design values:

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

## Typography System USS

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

## TSS File Structure

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

## C# ThemeManager

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

## UXML Consuming Tokens

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

## Theme-Aware Custom Controls

Custom controls should consume tokens through USS classes, never hardcode colors:

### StatusBadge C#

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

### StatusBadge USS

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

DC implements a **compound theme** combining orientation × season into 7 TSS files (2 orientations × 3 seasons + 1 base). Theme names: `"Landscape--Christmas"`, `"Portrait--Default"`, etc.

**Key techniques:**
- **BEM utility classes** with hardcoded values (`.color__text--white`, `.text__size--small`) — DC does NOT use `:root` CSS custom properties
- **7-file TSS matrix**: `Default.tss` → `Landscape.tss`/`Portrait.tss` → seasonal variants (each adds one `Decoration-*.uss`)
- **Decoration USS**: visibility toggling (`.theme__decoration--christmas { display: flex; }`, others `display: none`)
- **Orientation USS**: same class names, different `flex-direction`/`width`/`height` per orientation (20 files total, 10 per orientation)
- **ThemeManager** swaps both `PanelSettings` (different reference resolutions) and `ThemeStyleSheet` via `List<ThemeSettings>` lookup
- **Dual trigger flow**: season change (SettingsView → SettingsScreenController → ThemeEvents) and orientation change (MediaQuery → ThemeManager) both converge on `ApplyTheme()`

**DC vs Recommended approach**: DC's BEM utilities are simpler but inflexible (no dark mode). The `:root` variable system above is better for multi-theme apps. DC's compound TSS approach is ideal for orientation + decoration layering.

> ⚠️ `Dropdowns.uss` must be imported via TSS (not UXML) — compound element sub-parts only resolve correctly via TSS.

> **Full DC theming details**: See [Dragon Crashers Insights](../../references/dragon-crashers-insights.md) and [Project Patterns](../../references/project-patterns.md)

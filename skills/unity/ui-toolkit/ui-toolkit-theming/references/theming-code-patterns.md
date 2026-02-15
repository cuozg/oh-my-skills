# Theming Code Patterns

## tokens.uss — Light Theme (Default)

```css
:root {
    --color-primary-500: #2196F3; --color-primary-700: #1976D2; --color-primary-900: #0D47A1;
    --color-secondary-500: #FF9800;
    --color-bg-primary: #FFFFFF; --color-bg-secondary: #F5F5F5; --color-bg-overlay: rgba(0,0,0,0.5);
    --color-text-primary: #212121; --color-text-secondary: #757575;
    --color-text-disabled: #BDBDBD; --color-text-inverse: #FFFFFF;
    --color-border-default: #E0E0E0; --color-border-focus: #2196F3; --color-border-error: #F44336;
    --color-status-success: #4CAF50; --color-status-warning: #FF9800; --color-status-error: #F44336;
    --font-size-xs: 10px; --font-size-sm: 12px; --font-size-md: 14px;
    --font-size-lg: 16px; --font-size-xl: 20px; --font-size-2xl: 24px; --font-size-3xl: 32px;
    --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px; --space-6: 24px; --space-8: 32px;
    --radius-sm: 2px; --radius-md: 4px; --radius-lg: 8px; --radius-full: 9999px;
    --transition-fast: 100ms; --transition-normal: 200ms; --ease-default: ease-in-out;
    --shadow-color: rgba(0,0,0,0.12);
}
```

## Typography USS

```css
.text-xs { font-size: var(--font-size-xs); } .text-sm { font-size: var(--font-size-sm); }
.text-md { font-size: var(--font-size-md); } .text-lg { font-size: var(--font-size-lg); }
.text-bold { -unity-font-style: bold; } .text-center { -unity-text-align: middle-center; }
.heading-1 { font-size: var(--font-size-3xl); -unity-font-style: bold; margin-bottom: var(--space-4); }
.body-text { font-size: var(--font-size-md); color: var(--color-text-primary); }
.caption-text { font-size: var(--font-size-sm); color: var(--color-text-secondary); }
```

## TSS File Structure

**light-theme.tss**: `@import url("tokens.uss"); @import url("typography.uss"); @import url("base-components.uss");`
**dark-theme.tss**: `@import url("tokens-dark.uss"); @import url("typography.uss"); @import url("base-components.uss");`

## ThemeManager

```csharp
public class ThemeManager : MonoBehaviour {
    [SerializeField] PanelSettings panelSettings;
    [SerializeField] ThemeStyleSheet lightTheme, darkTheme;
    static ThemeManager _instance;
    bool _isDark;
    public static event System.Action<bool> OnThemeChanged;
    void Awake() {
        _instance = this;
        _isDark = PlayerPrefs.GetInt("Theme_IsDark", 0) == 1;
        ApplyTheme();
    }
    public static void ToggleTheme() {
        if (_instance == null) return;
        _instance._isDark = !_instance._isDark;
        _instance.ApplyTheme();
        PlayerPrefs.SetInt("Theme_IsDark", _instance._isDark ? 1 : 0);
        OnThemeChanged?.Invoke(_instance._isDark);
    }
    public static void SetTheme(bool dark) {
        if (_instance == null || _instance._isDark == dark) return;
        _instance._isDark = dark;
        _instance.ApplyTheme();
        PlayerPrefs.SetInt("Theme_IsDark", dark ? 1 : 0);
        OnThemeChanged?.Invoke(dark);
    }
    void ApplyTheme() => panelSettings.themeStyleSheet = _isDark ? darkTheme : lightTheme;
}
```

## Base Components USS (Token-Consuming)

```css
.screen { flex-grow: 1; background-color: var(--color-bg-primary); padding: var(--space-8); }
.btn { padding: var(--space-2) var(--space-4); border-radius: var(--radius-md); font-size: var(--font-size-md); -unity-font-style: bold; border-width: 0; transition: background-color var(--transition-fast) var(--ease-default); }
.btn-primary { background-color: var(--color-primary-500); color: var(--color-text-inverse); }
.btn-primary:hover { background-color: var(--color-primary-700); }
.btn-primary:active { background-color: var(--color-primary-900); }
```

## Theme-Aware Custom Control — StatusBadge

```csharp
[UxmlElement]
public partial class StatusBadge : VisualElement {
    readonly Label _label;
    [UxmlAttribute] public string Text { get => _label.text; set => _label.text = value; }
    [UxmlAttribute] public StatusType Status { get => _status; set { _status = value; UpdateStatusClass(); } }
    StatusType _status;
    public enum StatusType { Success, Warning, Error }
    public StatusBadge() { AddToClassList("status-badge"); _label = new Label(); Add(_label); }
    // UpdateStatusClass: remove all status-badge--* classes, add matching one via switch
}
```

```css
.status-badge { padding: var(--space-1) var(--space-3); border-radius: var(--radius-full); }
.status-badge--success { background-color: var(--color-status-success); }
.status-badge--warning { background-color: var(--color-status-warning); }
.status-badge--error { background-color: var(--color-status-error); }
```

## DC Compound Theming

DC uses compound themes: orientation × season → 7 TSS files. BEM utility classes with hardcoded values (no `:root` vars). `:root` variable system above is better for multi-theme apps.

> ⚠️ `Dropdowns.uss` must be imported via TSS, not UXML.

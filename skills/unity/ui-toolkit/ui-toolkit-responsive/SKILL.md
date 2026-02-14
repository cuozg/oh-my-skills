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

## Flexbox Deep Dive

UI Toolkit uses the Yoga flexbox engine. Every `VisualElement` is a flex container.

### Property Reference

| Property | Values | Default | Purpose |
|----------|--------|---------|---------|
| `flex-direction` | `row`, `column`, `row-reverse`, `column-reverse` | `column` | Main axis direction |
| `flex-grow` | `0+` float | `0` | How much element grows to fill space |
| `flex-shrink` | `0+` float | `1` | How much element shrinks when space is tight |
| `flex-basis` | `<length>`, `auto` | `auto` | Initial size before grow/shrink |
| `flex-wrap` | `nowrap`, `wrap` | `nowrap` | Whether children wrap to next line |
| `align-items` | `flex-start`, `center`, `flex-end`, `stretch`, `auto` | `stretch` | Cross-axis alignment of children |
| `align-self` | `flex-start`, `center`, `flex-end`, `stretch`, `auto` | `auto` | Override parent's align-items |
| `justify-content` | `flex-start`, `center`, `flex-end`, `space-between`, `space-around` | `flex-start` | Main-axis distribution |

### Flexbox Layout Examples

```xml
<!-- UXML: Header with spacer pattern -->
<ui:VisualElement class="header">
    <ui:Button class="header__back-btn" text="Back" />
    <ui:Label class="header__title" text="Settings" />
    <ui:VisualElement class="header__spacer" />
    <ui:Button class="header__action-btn" text="Save" />
</ui:VisualElement>
```

```css
/* USS: Flexbox header layout */
.header {
    flex-direction: row;
    align-items: center;
    height: 56px;
    padding: 0 var(--spacing-md);
    background-color: var(--color-bg-secondary);
}

.header__title {
    flex-grow: 0;
    margin: 0 var(--spacing-sm);
    font-size: var(--font-size-lg);
    color: var(--color-text-primary);
}

.header__spacer {
    flex-grow: 1;
}

.header__back-btn,
.header__action-btn {
    flex-shrink: 0;
    width: 44px;
    height: 44px;
}
```

### Grow vs Shrink Rules

- `flex-grow: 1` on all siblings = equal distribution of remaining space
- `flex-grow: 2` vs `flex-grow: 1` = 2:1 ratio of extra space (not total size)
- `flex-shrink: 0` = element never shrinks below its basis size
- `flex-basis: 200px` + `flex-grow: 1` = starts at 200px, grows if space available

## Length Units

| Unit | Example | When to Use |
|------|---------|-------------|
| `px` | `width: 48px;` | Fixed-size elements: icons, buttons, spacing tokens |
| `%` | `width: 50%;` | Container widths, responsive columns, relative sizing |
| `auto` | `width: auto;` | Content-sized elements, let flexbox decide |
| `none` | `max-width: none;` | Remove constraints |

> UI Toolkit does **not** support `em`, `rem`, `vw`, or `vh`. Use `%` for relative sizing and C# for viewport-relative calculations.

## Percentages vs Pixels: Decision Rules

| Context | Use | Example |
|---------|-----|---------|
| Container widths | `%` | `width: 100%;` |
| Grid columns | `%` | `width: 33.3%;` |
| Icon sizes | `px` | `width: 24px; height: 24px;` |
| Touch targets | `px` | `min-height: 44px;` |
| Spacing tokens | `px` via USS vars | `padding: var(--spacing-md);` (16px) |
| Font sizes | `px` via USS vars | `font-size: var(--font-size-body);` (16px) |
| Max content width | `px` | `max-width: 600px;` |
| Aspect-dependent | `%` | `padding-top: 56.25%;` (16:9 ratio) |

## SafeArea API

Handles notched displays (iPhone, Android punch-hole cameras).

### SafeAreaHandler.cs

```csharp
/// Applies Screen.safeArea as percentage-based padding to the root container.
/// Attach to the same GameObject as UIDocument.
[RequireComponent(typeof(UIDocument))]
public class SafeAreaHandler : MonoBehaviour
{
    private VisualElement _root;
    private Rect _lastSafeArea;

    private void OnEnable()
    {
        var doc = GetComponent<UIDocument>();
        _root = doc.rootVisualElement.Q<VisualElement>("screen-root") ?? doc.rootVisualElement;
        _root.RegisterCallback<GeometryChangedEvent>(e => ApplySafeArea());
        ApplySafeArea();
    }

    private void ApplySafeArea()
    {
        Rect sa = Screen.safeArea;
        if (sa == _lastSafeArea) return;
        _lastSafeArea = sa;

        float w = Screen.width, h = Screen.height;
        _root.style.paddingLeft = new Length(sa.x / w * 100f, LengthUnit.Percent);
        _root.style.paddingRight = new Length((w - sa.xMax) / w * 100f, LengthUnit.Percent);
        _root.style.paddingTop = new Length((h - sa.yMax) / h * 100f, LengthUnit.Percent);
        _root.style.paddingBottom = new Length(sa.y / h * 100f, LengthUnit.Percent);
    }
}
```

## Screen Adaptation Strategy

### Orientation Detection (C#)

```csharp
using UnityEngine;
using UnityEngine.UIElements;

/// <summary>
/// Toggles USS classes based on device orientation.
/// Checks on geometry change to handle runtime rotation.
/// </summary>
[RequireComponent(typeof(UIDocument))]
public class OrientationHandler : MonoBehaviour
{
    private VisualElement _root;
    private bool _wasPortrait;

    private void OnEnable()
    {
        _root = GetComponent<UIDocument>().rootVisualElement;
        _root.RegisterCallback<GeometryChangedEvent>(OnGeometryChanged);
        UpdateOrientation();
    }

    private void OnDisable()
    {
        _root?.UnregisterCallback<GeometryChangedEvent>(OnGeometryChanged);
    }

    private void OnGeometryChanged(GeometryChangedEvent evt)
    {
        UpdateOrientation();
    }

    private void UpdateOrientation()
    {
        bool isPortrait = Screen.width <= Screen.height;
        if (isPortrait == _wasPortrait && _root.ClassListContains("portrait"))
            return;

        _wasPortrait = isPortrait;
        _root.EnableInClassList("portrait", isPortrait);
        _root.EnableInClassList("landscape", !isPortrait);
    }
}
```

### Orientation-Responsive USS

```css
/* Default: portrait layout (column) */
.content-grid {
    flex-direction: column;
    flex-wrap: wrap;
}

.content-grid__item {
    width: 100%;
    padding: var(--spacing-sm);
}

/* Landscape: switch to row layout */
.landscape .content-grid {
    flex-direction: row;
}

.landscape .content-grid__item {
    width: 50%;
}

/* Landscape: sidebar becomes visible */
.sidebar {
    display: none;
    width: 280px;
    flex-shrink: 0;
}

.landscape .sidebar {
    display: flex;
}
```

### PanelSettings Scale Modes

Configure in `PanelSettings` asset for DPI-aware scaling:

| Scale Mode | Behavior | Best For |
|------------|----------|----------|
| `Constant Pixel Size` | 1:1 pixel mapping | Desktop, editor tools |
| `Constant Physical Size` | DPI-aware, consistent physical size | Mobile, cross-device |
| `Scale With Screen Size` | Scales to reference resolution | Fixed-layout games |

For mobile, use **Constant Physical Size** with `referenceDpi = 96` and `fallbackDpi = 96`.

## Aspect Ratio Handling

Common ratios: **16:9** (1920×1080, legacy), **19.5:9** (iPhone 12+), **20:9** (Galaxy S21+), **4:3** (iPad).

### Aspect-Aware USS

```css
/* Base: works for all ratios */
.game-hud { flex-grow: 1; flex-direction: column; justify-content: space-between; }
.game-hud__top-bar { flex-direction: row; justify-content: space-between; padding: var(--spacing-sm) var(--spacing-md); flex-shrink: 0; }
.game-hud__bottom-bar { flex-direction: row; justify-content: center; padding: var(--spacing-md); flex-shrink: 0; }

/* Wide phones (18:9+): extra padding */
.aspect-wide .game-hud__top-bar,
.aspect-wide .game-hud__bottom-bar { padding-left: var(--spacing-xl); padding-right: var(--spacing-xl); }

/* Tablet (4:3): constrain width */
.aspect-tablet .game-hud__content { max-width: 720px; align-self: center; width: 100%; }
```

## Responsive Breakpoint Pattern

### ScreenSizeClassifier.cs

```csharp
using UnityEngine;
using UnityEngine.UIElements;

/// <summary>
/// Adds USS classes based on screen width breakpoints and aspect ratio.
/// Classes: screen-sm, screen-md, screen-lg, screen-xl, aspect-wide, aspect-tablet
/// </summary>
[RequireComponent(typeof(UIDocument))]
public class ScreenSizeClassifier : MonoBehaviour
{
    [Header("Width Breakpoints (px)")]
    [SerializeField] private float _smallMax = 480f;
    [SerializeField] private float _mediumMax = 768f;
    [SerializeField] private float _largeMax = 1200f;

    private VisualElement _root;
    private string _currentSize;
    private string _currentAspect;

    private void OnEnable()
    {
        _root = GetComponent<UIDocument>().rootVisualElement;
        _root.RegisterCallback<GeometryChangedEvent>(OnGeometryChanged);
        Classify();
    }

    private void OnDisable()
    {
        _root?.UnregisterCallback<GeometryChangedEvent>(OnGeometryChanged);
    }

    private void OnGeometryChanged(GeometryChangedEvent evt)
    {
        Classify();
    }

    private void Classify()
    {
        float w = Screen.width;
        float h = Screen.height;

        // Size class
        string sizeClass;
        if (w <= _smallMax) sizeClass = "screen-sm";
        else if (w <= _mediumMax) sizeClass = "screen-md";
        else if (w <= _largeMax) sizeClass = "screen-lg";
        else sizeClass = "screen-xl";

        if (sizeClass != _currentSize)
        {
            _root.EnableInClassList("screen-sm", false);
            _root.EnableInClassList("screen-md", false);
            _root.EnableInClassList("screen-lg", false);
            _root.EnableInClassList("screen-xl", false);
            _root.EnableInClassList(sizeClass, true);
            _currentSize = sizeClass;
        }

        // Aspect ratio class
        float ratio = Mathf.Max(w, h) / Mathf.Min(w, h);
        string aspectClass;
        if (ratio >= 2f) aspectClass = "aspect-wide";
        else if (ratio <= 1.4f) aspectClass = "aspect-tablet";
        else aspectClass = "aspect-standard";

        if (aspectClass != _currentAspect)
        {
            _root.EnableInClassList("aspect-wide", false);
            _root.EnableInClassList("aspect-tablet", false);
            _root.EnableInClassList("aspect-standard", false);
            _root.EnableInClassList(aspectClass, true);
            _currentAspect = aspectClass;
        }
    }
}
```

### Breakpoint USS Classes

Use `ScreenSizeClassifier` classes as USS parent selectors: `screen-sm` (phones), `screen-md` (tablet portrait), `screen-lg` (tablet landscape / small desktop), `screen-xl` (large desktop). Aspect classes: `aspect-wide`, `aspect-tablet`, `aspect-standard`.

```css
.screen-sm .nav { flex-direction: column; }
.screen-lg .nav { flex-direction: row; }
.aspect-tablet .content { max-width: 720px; align-self: center; }
```

## Common Responsive Patterns

### Card Grid + Sidebar Collapse

```css
/* Responsive card grid: 1-col → 2-col → 3-col via breakpoint classes */
.card-grid { flex-direction: row; flex-wrap: wrap; padding: var(--spacing-sm); }
.card-grid__item { width: 50%; padding: var(--spacing-xs); }
.screen-sm .card-grid__item { width: 100%; }
.screen-lg .card-grid__item { width: 33.3%; }
.screen-xl .card-grid__item { width: 25%; }
.screen-xl .card-grid { max-width: 1400px; align-self: center; }

/* Two-pane layout: sidebar collapses on small screens */
.split-layout { flex-direction: row; flex-grow: 1; }
.split-layout__sidebar { width: 280px; flex-shrink: 0; }
.split-layout__main { flex-grow: 1; }
.screen-sm .split-layout { flex-direction: column; }
.screen-sm .split-layout__sidebar { width: 100%; max-height: 200px; }
```

## Dragon Crashers Project Patterns

The following sections document concrete responsive patterns from the Dragon Crashers UIToolkit demo project. All file paths are relative to the project root.

### MediaQuery: Aspect Ratio Detection

> **Source**: `Assets/Scripts/Utilities/MediaQuery.cs`, `Assets/Scripts/UI/Events/MediaQueryEvents.cs`

Dragon Crashers uses a `MediaQuery` MonoBehaviour (`[ExecuteInEditMode]`) to detect orientation changes via aspect ratio threshold (`width/height >= 1.2f`), firing static events. Uses `GeometryChangedEvent` on UIDocument root — no `Update()` polling.

```csharp
public enum MediaAspectRatio { Undefined, Landscape, Portrait }

// Static delegates (MediaQueryEvents.cs) — subscribe to track orientation
public class MediaQueryEvents
{
    public static Action<Vector2> ResolutionUpdated;
    public static Action<MediaAspectRatio> AspectRatioUpdated;
}

// Detection (MediaQuery.cs): Landscape when aspect >= 1.2
public const float k_LandscapeMin = 1.2f;
public static MediaAspectRatio CalculateAspectRatio(Vector2 resolution)
    => (resolution.x / resolution.y >= k_LandscapeMin) ? MediaAspectRatio.Landscape : MediaAspectRatio.Portrait;

// Usage: subscribe in OnEnable, unsubscribe in OnDisable
void OnEnable() => MediaQueryEvents.AspectRatioUpdated += OnAspectRatioUpdated;
void OnDisable() => MediaQueryEvents.AspectRatioUpdated -= OnAspectRatioUpdated;
```

> **Cross-ref**: [ui-toolkit-theming](../ui-toolkit-theming/SKILL.md) for how `ThemeManager` consumes these events.

### SafeAreaBorder: borderWidth Approach

> **Source**: `Assets/Scripts/Utilities/SafeAreaBorder.cs`

Dragon Crashers implements safe area using **`borderWidth`** (not `padding`), allowing visible colored bars behind the notch. Key details:

- Uses `Screen.safeArea` insets applied as `borderTopWidth`, `borderLeftWidth`, etc.
- Configurable `m_Multiplier` (`[Range(0, 1)]`) and `m_BorderColor` via Inspector
- `[ExecuteInEditMode]` — re-applies on `OnValidate()` and `GeometryChangedEvent`
- `ExtensionMethods.GetScreenCoordinate()` compensates for border widths in coordinate conversions

| Safe Area Approach | Mechanism | Use When |
|-------------------|-----------|----------|
| **borderWidth** (DC) | `borderTopWidth` + `borderColor` | Need visible colored bars behind notch |
| **padding** (generic) | `paddingTop` as percentage | Children naturally inset, no visible border |

> **Cross-ref**: [ui-toolkit-mobile](../ui-toolkit-mobile/SKILL.md) for device-specific safe area considerations. Full code in [Dragon Crashers Insights](../references/dragon-crashers-insights.md).

### ThemeManager: Orientation-Aware Theming

> **Source**: `Assets/Scripts/UI/Themes/ThemeManager.cs`

Instead of toggling USS classes, Dragon Crashers swaps **entire PanelSettings + ThemeStyleSheet (TSS)** assets per orientation. Theme naming: `{Orientation}--{Variation}` (e.g., `Portrait--Default`). On `AspectRatioUpdated`, builds new theme name and calls `ApplyTheme()` which sets both `panelSettings` and `themeStyleSheet` on the `UIDocument`. **Why swap PanelSettings?** Portrait/Landscape need different reference resolutions, scale modes, or DPI settings.

> **Cross-ref**: [ui-toolkit-theming](../ui-toolkit-theming/SKILL.md) for TSS structure, custom properties, and seasonal theme variations.

### GeometryChangedEvent Patterns

Dragon Crashers uses `GeometryChangedEvent` as the primary layout trigger — never `Update()` polling. Used by `MediaQuery` (resolution/aspect), `SafeAreaBorder` (border widths), `PositionToVisualElement` (3D repositioning).

```csharp
// Pattern: Register in OnEnable, unregister in OnDisable, run initial setup immediately
void OnEnable()
{
    m_Root = m_Document.rootVisualElement.Q<VisualElement>(m_ElementName);
    m_Root.RegisterCallback<GeometryChangedEvent>(OnGeometryChanged);
    ApplyLayout(); // Initial setup
}
void OnDisable() => m_Root?.UnregisterCallback<GeometryChangedEvent>(OnGeometryChanged);
void OnGeometryChanged(GeometryChangedEvent evt) => ApplyLayout();
```

Fires on: screen resize, orientation change, parent layout change, element added/removed, style changes affecting layout. Does **not** fire every frame.

### PositionToVisualElement: World-to-UI Alignment

> **Source**: `Assets/Scripts/Utilities/PositionToVisualElement.cs`, `Assets/Scripts/Utilities/ExtensionMethods.cs`

Aligns a 3D `GameObject` to a `VisualElement` across orientation changes. **Conversion chain**: `VisualElement.worldBound` → `GetScreenCoordinate()` (adjusts for borderWidth) → `Camera.ScreenToWorldPoint` → `transform.position`. Re-runs on `GeometryChangedEvent` and `ThemeEvents.CameraUpdated` (camera swaps on orientation change). Full code in [Dragon Crashers Insights](../references/dragon-crashers-insights.md) (section: Screen Implementations).

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

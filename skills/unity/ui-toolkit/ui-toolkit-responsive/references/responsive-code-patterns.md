# Responsive Code Patterns

> Extracted from [SKILL.md](../SKILL.md) — flexbox deep dive, length units, safe area, screen adaptation, aspect ratio, breakpoints, and common responsive patterns.

---

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

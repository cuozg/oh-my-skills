---
name: ui-toolkit-responsive
description: "Responsive design for Unity UI Toolkit. Covers flexbox layout, length units, safe area handling, screen adaptation, aspect ratio strategies, responsive breakpoints, and common layout patterns. Use when: (1) Building adaptive UI that works across phone/tablet/desktop, (2) Implementing safe area handling for notched devices, (3) Creating responsive grid layouts, (4) Handling portrait/landscape orientation changes, (5) Setting up flexible containers with flexbox. Triggers: 'responsive', 'flexbox', 'safe area', 'screen adaptation', 'aspect ratio', 'breakpoint', 'flex-grow', 'portrait landscape', 'adaptive layout'."
---

# UI Toolkit Responsive Design

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
using UnityEngine;
using UnityEngine.UIElements;

/// <summary>
/// Applies Screen.safeArea as percentage-based padding to the root container.
/// Attach to the same GameObject as UIDocument.
/// </summary>
[RequireComponent(typeof(UIDocument))]
public class SafeAreaHandler : MonoBehaviour
{
    private VisualElement _root;
    private Rect _lastSafeArea;

    private void OnEnable()
    {
        var doc = GetComponent<UIDocument>();
        _root = doc.rootVisualElement.Q<VisualElement>("screen-root");
        if (_root == null)
            _root = doc.rootVisualElement;

        _root.RegisterCallback<GeometryChangedEvent>(OnGeometryChanged);
        ApplySafeArea();
    }

    private void OnDisable()
    {
        _root?.UnregisterCallback<GeometryChangedEvent>(OnGeometryChanged);
    }

    private void OnGeometryChanged(GeometryChangedEvent evt)
    {
        ApplySafeArea();
    }

    private void ApplySafeArea()
    {
        Rect safeArea = Screen.safeArea;
        if (safeArea == _lastSafeArea)
            return;

        _lastSafeArea = safeArea;

        float screenW = Screen.width;
        float screenH = Screen.height;

        // Convert safe area to percentage-based padding
        float left = safeArea.x / screenW * 100f;
        float right = (screenW - safeArea.xMax) / screenW * 100f;
        float top = (screenH - safeArea.yMax) / screenH * 100f;
        float bottom = safeArea.y / screenH * 100f;

        // Apply as percentage padding
        _root.style.paddingLeft = new Length(left, LengthUnit.Percent);
        _root.style.paddingRight = new Length(right, LengthUnit.Percent);
        _root.style.paddingTop = new Length(top, LengthUnit.Percent);
        _root.style.paddingBottom = new Length(bottom, LengthUnit.Percent);
    }
}
```

> **Usage**: Add `SafeAreaHandler` to the same GameObject as `UIDocument`. It targets `name="screen-root"` or falls back to the root element.

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

### Responsive Card Grid

```xml
<ui:VisualElement class="card-grid">
    <ui:VisualElement class="card-grid__item">
        <ui:VisualElement class="card">
            <ui:VisualElement class="card__image" />
            <ui:Label class="card__title" text="Item Name" />
        </ui:VisualElement>
    </ui:VisualElement>
</ui:VisualElement>
```
```css
.card-grid { flex-direction: row; flex-wrap: wrap; padding: var(--spacing-sm); }
.card-grid__item { width: 50%; padding: var(--spacing-xs); }
.card { flex-grow: 1; background-color: var(--color-bg-secondary); border-radius: 8px; }
.card__image { width: 100%; height: 120px; }
.card__title { font-size: var(--font-size-md); padding: var(--spacing-sm); }
.screen-sm .card-grid__item { width: 100%; }
.screen-lg .card-grid__item { width: 33.3%; }
.screen-xl .card-grid__item { width: 25%; }
.screen-xl .card-grid { max-width: 1400px; align-self: center; }
```

### Sidebar Collapse + Action Bar

```css
/* Two-pane layout */
.split-layout { flex-direction: row; flex-grow: 1; }
.split-layout__sidebar { width: 280px; flex-shrink: 0; }
.split-layout__main { flex-grow: 1; }
.screen-sm .split-layout { flex-direction: column; }
.screen-sm .split-layout__sidebar { width: 100%; max-height: 200px; }

/* Action bar: row on wide, column on narrow */
.action-bar { flex-direction: row; justify-content: space-between; padding: var(--spacing-md); }
.screen-sm .action-bar { flex-direction: column; }
.screen-sm .action-bar__btn { width: 100%; margin-bottom: var(--spacing-sm); }
```

## Dragon Crashers Project Patterns

The following sections document concrete responsive patterns from the Dragon Crashers UIToolkit demo project. All file paths are relative to the project root.

### MediaQuery: Aspect Ratio Detection

> **Source**: `Assets/Scripts/Utilities/MediaQuery.cs`, `Assets/Scripts/UI/Events/MediaQueryEvents.cs`

Dragon Crashers uses a `MediaQuery` MonoBehaviour (`[ExecuteInEditMode]`) to detect orientation changes via aspect ratio threshold (`width/height >= 1.2f`), firing static events. Uses `GeometryChangedEvent` on UIDocument root — no `Update()` polling. Also hooks `SceneManager.sceneLoaded` for scene transitions.

```csharp
public enum MediaAspectRatio { Undefined, Landscape, Portrait }

// Static delegates (Assets/Scripts/UI/Events/MediaQueryEvents.cs)
public class MediaQueryEvents
{
    public static Action<Vector2> ResolutionUpdated;
    public static Action<MediaAspectRatio> AspectRatioUpdated;
    public static Action CameraResized;
    public static Action SafeAreaApplied;
}

// Detection logic (MediaQuery.cs)
public const float k_LandscapeMin = 1.2f;

public static MediaAspectRatio CalculateAspectRatio(Vector2 resolution)
{
    if (Math.Abs(resolution.y) < float.Epsilon)
        return MediaAspectRatio.Undefined;
    float aspectRatio = resolution.x / resolution.y;
    return (aspectRatio >= k_LandscapeMin) ? MediaAspectRatio.Landscape : MediaAspectRatio.Portrait;
}
```

**Subscribing to orientation changes:**
```csharp
void OnEnable() => MediaQueryEvents.AspectRatioUpdated += OnAspectRatioUpdated;
void OnDisable() => MediaQueryEvents.AspectRatioUpdated -= OnAspectRatioUpdated;

void OnAspectRatioUpdated(MediaAspectRatio ratio)
{
    bool isLandscape = ratio == MediaAspectRatio.Landscape;
    // Adapt layout, swap cameras, reposition elements, etc.
}
```

> **Cross-ref**: [ui-toolkit-theming](../ui-toolkit-theming/SKILL.md) for how `ThemeManager` consumes these events.

### SafeAreaBorder: borderWidth Approach

> **Source**: `Assets/Scripts/Utilities/SafeAreaBorder.cs`

Dragon Crashers implements safe area using **`borderWidth`** — not `padding`. Key distinction:

| Approach | How It Works | When to Use |
|----------|-------------|-------------|
| **borderWidth** (this project) | `borderTopWidth`, `borderLeftWidth`, etc. + `borderColor` | Need visible colored bars behind notch |
| **padding** (generic approach above) | `paddingTop`, `paddingLeft`, etc. (percentage-based) | Children should naturally inset, no visible border |

```csharp
// SafeAreaBorder.cs — [ExecuteInEditMode], configurable via Inspector
// m_Element: target named element (or rootVisualElement if empty)
// m_Multiplier: 0–1 Range slider for adjusting safe area inset
// m_BorderColor: configurable border color (default black)

void ApplySafeArea()
{
    Rect safeArea = Screen.safeArea;

    float leftBorder   = safeArea.x;
    float rightBorder  = Screen.width - safeArea.xMax;
    float topBorder    = Screen.height - safeArea.yMax;
    float bottomBorder = safeArea.y;

    // Apply as borderWidth (NOT padding) with multiplier
    m_Root.style.borderTopWidth    = topBorder * m_Multiplier;
    m_Root.style.borderBottomWidth = bottomBorder * m_Multiplier;
    m_Root.style.borderLeftWidth   = leftBorder * m_Multiplier;
    m_Root.style.borderRightWidth  = rightBorder * m_Multiplier;

    // Visible border color (e.g., black bars behind notch)
    m_Root.style.borderBottomColor = m_BorderColor;
    m_Root.style.borderTopColor    = m_BorderColor;
    m_Root.style.borderLeftColor   = m_BorderColor;
    m_Root.style.borderRightColor  = m_BorderColor;
}

// OnValidate re-applies when Inspector values change
void OnValidate() => ApplySafeArea();
```

**Important**: `ExtensionMethods.GetScreenCoordinate()` adds `resolvedStyle.borderLeftWidth/borderTopWidth` when converting UI positions to screen coordinates, so click/position calculations remain accurate with safe area borders applied.

> **Cross-ref**: [ui-toolkit-mobile](../ui-toolkit-mobile/SKILL.md) for device-specific safe area considerations.

### ThemeManager: Orientation-Aware Theming

> **Source**: `Assets/Scripts/UI/Themes/ThemeManager.cs`

Instead of toggling USS classes, Dragon Crashers swaps **entire PanelSettings + ThemeStyleSheet (TSS)** assets per orientation. This allows different reference resolutions, scale modes, and style hierarchies.

**Theme naming convention**: `{Orientation}--{Variation}` (e.g., `Portrait--Default`, `Landscape--Christmas`). The `ThemeSettings` struct pairs a theme string key with a `ThemeStyleSheet` and `PanelSettings` asset.

```csharp
// ThemeManager listens to MediaQuery orientation changes
void OnEnable()
{
    ThemeEvents.ThemeChanged += OnThemeChanged;
    MediaQueryEvents.AspectRatioUpdated += OnAspectRatioUpdated;
}

// Build theme name from orientation + current variation suffix
void OnAspectRatioUpdated(MediaAspectRatio mediaAspectRatio)
{
    string suffix = GetSuffix(m_CurrentTheme, "--");  // e.g., "--Default"
    string newThemeName = mediaAspectRatio.ToString() + suffix;  // "Portrait--Default"
    ApplyTheme(newThemeName);
}

// Swap both PanelSettings AND ThemeStyleSheet on the UIDocument
public void ApplyTheme(string theme)
{
    SetPanelSettings(theme);    // m_Document.panelSettings = matched PanelSettings
    SetThemeStyleSheet(theme);  // m_Document.panelSettings.themeStyleSheet = matched TSS
}
```

**Why swap PanelSettings?** Portrait and Landscape may need different reference resolutions (1080×1920 vs 1920×1080), scale modes, or DPI settings. Swapping the entire asset handles all at once.

> **Cross-ref**: [ui-toolkit-theming](../ui-toolkit-theming/SKILL.md) for TSS structure, custom properties, and seasonal theme variations.

### GeometryChangedEvent Patterns

Dragon Crashers uses `GeometryChangedEvent` as the primary trigger for layout-dependent initialization — never `Update()` polling.

| Component | What It Does on GeometryChanged |
|-----------|--------------------------------|
| `MediaQuery` | Re-checks resolution and aspect ratio |
| `SafeAreaBorder` | Re-applies border widths |
| `PositionToVisualElement` | Repositions 3D objects to match UI |

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

> **Cross-ref**: [ui-toolkit-patterns](../ui-toolkit-patterns/SKILL.md) for full event handling patterns.

### PositionToVisualElement: World-to-UI Alignment

> **Source**: `Assets/Scripts/Utilities/PositionToVisualElement.cs`, `Assets/Scripts/Utilities/ExtensionMethods.cs`

Aligns a 3D `GameObject` to a `VisualElement`. Used when 3D characters must stay anchored to UI slots across orientation changes.

**Conversion chain**: `VisualElement.worldBound` → `GetScreenCoordinate()` (adjusts for borderWidth) → `ScreenPosToWorldPos()` (`Camera.ScreenToWorldPoint`) → `GameObject.transform.position`

```csharp
public void MoveToElement()
{
    // 1. Get UI element center in UI Toolkit coordinates
    Rect worldBound = m_TargetElement.worldBound;
    Vector2 centerPosition = new Vector2(
        worldBound.x + worldBound.width / 2,
        worldBound.y + worldBound.height / 2);

    // 2. Convert to screen pixels (adjusts for SafeAreaBorder borderWidths)
    Vector2 screenPos = centerPosition.GetScreenCoordinate(m_Document.rootVisualElement);

    // 3. Convert screen position to 3D world position
    Vector3 worldPosition = screenPos.ScreenPosToWorldPos(m_Camera, m_Depth);
    m_ObjectToMove.transform.position = worldPosition;
}

// Camera updates on orientation change via ThemeEvents
void OnEnable()
{
    ThemeEvents.CameraUpdated += OnCameraUpdated;
    m_TargetElement.RegisterCallback<GeometryChangedEvent>(OnGeometryChanged);
}

void OnCameraUpdated(Camera camera) { m_Camera = camera; MoveToElement(); }
void OnGeometryChanged(GeometryChangedEvent evt) => MoveToElement();
```

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Fixed `px` width on containers | Doesn't adapt to screen size | Use `%` or `flex-grow` |
| Ignoring `Screen.safeArea` | Content hidden behind notch | Apply `SafeAreaHandler` on root |
| Hardcoded `left`/`top` positions | Breaks on different resolutions | Use flexbox layout instead |
| Checking orientation in `Update()` | Wastes CPU every frame | Use `GeometryChangedEvent` |
| Pixel sizes for all spacing | Inconsistent across DPI | Use USS custom property tokens |
| Deep nesting for layout | Performance cost, hard to maintain | Flatten hierarchy, use flex properties |
| `position: absolute` for layout | Overlaps on different sizes | Reserve for overlays/modals only |
| Separate UXML per orientation | Double maintenance cost | Single UXML + USS class toggling or TSS swapping |
| Using padding for safe area when border color needed | Can't show colored bars behind notch | Use `borderWidth` + `borderColor` (Dragon Crashers approach) |
| Not accounting for borderWidth in screen coordinate conversion | Click positions offset by safe area borders | Add `resolvedStyle.borderLeftWidth/borderTopWidth` before normalizing |
| Hardcoded camera reference for UI-to-world alignment | Breaks on orientation change when camera swaps | Subscribe to `ThemeEvents.CameraUpdated` to receive new camera |

## Exercise: Responsive Product Card Grid

Build a product card grid that adapts from 1 column (phone) to 2 columns (tablet) to 3 columns (desktop).

**ProductGrid.uxml**
```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
    <ui:VisualElement name="screen-root" class="root">
        <ui:Label class="page-title" text="Shop" />
        <ui:VisualElement class="product-grid">
            <ui:VisualElement class="product-grid__item">
                <ui:VisualElement class="product-card">
                    <ui:VisualElement class="product-card__img" />
                    <ui:Label class="product-card__name" text="Sword" />
                    <ui:Label class="product-card__price" text="100g" />
                </ui:VisualElement>
            </ui:VisualElement>
            <!-- Duplicate product-grid__item 5 more times -->
        </ui:VisualElement>
    </ui:VisualElement>
</ui:UXML>
```

**ProductGrid.uss**
```css
.root { flex-grow: 1; padding: 8px; }
.page-title { font-size: 24px; -unity-font-style: bold; margin-bottom: 8px; }
.product-grid { flex-direction: row; flex-wrap: wrap; }
.product-grid__item { width: 100%; padding: 4px; }
.product-card { background-color: #2A2A2A; border-radius: 8px; padding: 8px; }
.product-card__img { width: 100%; height: 80px; background-color: #444; border-radius: 4px; }
.product-card__name { font-size: 14px; margin-top: 4px; }
.product-card__price { font-size: 12px; color: #FFD700; }

/* Tablet: 2 columns */
.screen-md .product-grid__item { width: 50%; }
/* Desktop: 3 columns */
.screen-lg .product-grid__item { width: 33.3%; }
.screen-xl .product-grid__item { width: 25%; }
```

**Checklist**: ✅ Cards stack on phone | ✅ 2-col on tablet | ✅ 3-col on desktop | ✅ Uses `flex-wrap` | ✅ Breakpoint classes from `ScreenSizeClassifier`

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

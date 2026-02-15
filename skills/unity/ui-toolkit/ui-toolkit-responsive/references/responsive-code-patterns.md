# Responsive Code Patterns

## Flexbox Quick Ref

Key properties: `flex-direction` (row/column), `flex-grow` (fill space), `flex-shrink` (shrink when tight), `flex-wrap` (wrap), `align-items` (cross-axis), `justify-content` (main-axis distribution).

### Header with Spacer Pattern

```xml
<ui:VisualElement class="header">
    <ui:Button class="header__back-btn" text="Back" />
    <ui:Label class="header__title" text="Settings" />
    <ui:VisualElement class="header__spacer" />
    <ui:Button class="header__action-btn" text="Save" />
</ui:VisualElement>
```

```css
.header { flex-direction: row; align-items: center; height: 56px; }
.header__spacer { flex-grow: 1; }
.header__back-btn, .header__action-btn { flex-shrink: 0; width: 44px; height: 44px; }
```

## Length Units

`px` for fixed sizes. `%` for container widths. `auto` for content-sized. No `em`/`rem`/`vw`/`vh`.

## SafeAreaHandler

```csharp
[RequireComponent(typeof(UIDocument))]
public class SafeAreaHandler : MonoBehaviour {
    VisualElement _root; Rect _lastSafeArea;
    void OnEnable() {
        var doc = GetComponent<UIDocument>();
        _root = doc.rootVisualElement.Q<VisualElement>("screen-root") ?? doc.rootVisualElement;
        _root.RegisterCallback<GeometryChangedEvent>(e => ApplySafeArea());
        ApplySafeArea();
    }
    void ApplySafeArea() {
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

## Orientation Detection

```csharp
// MonoBehaviour: listen GeometryChangedEvent, toggle root classes "portrait"/"landscape"
// based on Screen.width <= Screen.height. Cache _wasPortrait to skip redundant updates.
```

```css
.landscape .content-grid { flex-direction: row; }
.landscape .content-grid__item { width: 50%; }
.sidebar { display: none; }
.landscape .sidebar { display: flex; width: 280px; }
```

PanelSettings: `Constant Pixel Size` (desktop), `Constant Physical Size` (mobile, `referenceDpi=96`), `Scale With Screen Size` (fixed-layout games).

## ScreenSizeClassifier (Breakpoints)

```csharp
[RequireComponent(typeof(UIDocument))]
public class ScreenSizeClassifier : MonoBehaviour {
    [SerializeField] float _smallMax = 480f, _mediumMax = 768f, _largeMax = 1200f;
    VisualElement _root; string _currentSize, _currentAspect;
    void OnEnable() {
        _root = GetComponent<UIDocument>().rootVisualElement;
        _root.RegisterCallback<GeometryChangedEvent>(e => Classify());
        Classify();
    }
    void OnDisable() => _root?.UnregisterCallback<GeometryChangedEvent>(e => Classify());
    void Classify() {
        float w = Screen.width, h = Screen.height;
        string sizeClass = w <= _smallMax ? "screen-sm" : w <= _mediumMax ? "screen-md" : w <= _largeMax ? "screen-lg" : "screen-xl";
        if (sizeClass != _currentSize) {
            foreach (var c in new[] { "screen-sm", "screen-md", "screen-lg", "screen-xl" }) _root.EnableInClassList(c, c == sizeClass);
            _currentSize = sizeClass;
        }
        float ratio = Mathf.Max(w, h) / Mathf.Min(w, h);
        string aspectClass = ratio >= 2f ? "aspect-wide" : ratio <= 1.4f ? "aspect-tablet" : "aspect-standard";
        if (aspectClass != _currentAspect) {
            foreach (var c in new[] { "aspect-wide", "aspect-tablet", "aspect-standard" }) _root.EnableInClassList(c, c == aspectClass);
            _currentAspect = aspectClass;
        }
    }
}
```

Classes: `screen-sm`/`screen-md`/`screen-lg`/`screen-xl`. Aspect: `aspect-wide`/`aspect-tablet`/`aspect-standard`.

## Common Responsive Patterns

```css
/* Card grid: 1-col → 2-col → 3-col */
.card-grid { flex-direction: row; flex-wrap: wrap; }
.card-grid__item { width: 50%; }
.screen-sm .card-grid__item { width: 100%; }
.screen-lg .card-grid__item { width: 33.3%; }
.screen-xl .card-grid__item { width: 25%; }

/* Two-pane: sidebar collapses on small */
.split-layout { flex-direction: row; flex-grow: 1; }
.split-layout__sidebar { width: 280px; flex-shrink: 0; }
.split-layout__main { flex-grow: 1; }
.screen-sm .split-layout { flex-direction: column; }
.screen-sm .split-layout__sidebar { width: 100%; max-height: 200px; }
```

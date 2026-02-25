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


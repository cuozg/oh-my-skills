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

See [responsive-code-patterns-advanced.md](responsive-code-patterns-advanced.md) for common responsive CSS patterns.

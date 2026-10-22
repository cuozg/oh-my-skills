# UI Toolkit Performance

## Element Visibility Cost

| Method | Layout | Render | Memory | Use Case |
|--------|--------|--------|--------|----------|
| `visibility: hidden` | Kept | Skipped | Kept | Frequently toggled UI |
| `opacity: 0` | Kept | Vertex cost remains | Kept | Fade animations |
| `display: none` | Removed (relayout on toggle) | Skipped | Kept | Hidden for longer periods |
| `RemoveFromHierarchy()` + drop refs | Removed | None | GC-freed | Rarely shown; re-creation is costly |

**Rule**: Pre-create and toggle with `visibility` for frequent changes; remove
elements only when they are rarely needed. Source: Manual `UIE-best-practices-for-managing-elements`.

## Element Pooling

```csharp
using UnityEngine.Pool;

private ObjectPool<VisualElement> _pool;

void InitPool(VisualElement parent)
{
    _pool = new ObjectPool<VisualElement>(
        createFunc: () => { var e = new VisualElement(); e.AddToClassList("list-item"); return e; },
        actionOnGet: e => parent.Add(e),
        actionOnRelease: e => e.RemoveFromHierarchy());
}
```

## ListView (Built-in Pooling)

```csharp
// ListView auto-pools - only visible items exist in hierarchy
var listView = root.Q<ListView>("item-list");
listView.itemsSource = items;
listView.makeItem = () => new Label();
listView.bindItem = (element, index) =>
    ((Label)element).text = items[index].name;
listView.RefreshItems();   // after items change
```

## USS Selector Performance

- **Cost formula**: N1 (classes on element) x N2 (USS files loaded)
- BEM single-class selectors: `.button--primary` -> O(1)
- Deep selectors: `.panel > .list > .item:hover` -> N1xN2 per mouse move
- `:hover` on deep hierarchies triggers re-style on every `PointerMoveEvent`
- Prefer USS files over inline styles - inline styles allocate per-element memory

## UsageHints

```csharp
element.usageHints = UsageHints.DynamicTransform;  // frequently moving elements
element.usageHints = UsageHints.GroupTransform;     // complex content grouping
```

## UQuery Caching & Memory Leaks

```csharp
// BAD: traverses hierarchy every call
void OnClick() => root.Q<Label>("status").text = "Done";

// GOOD: cache in OnEnable
private Label _status;
void OnEnable() => _status = root.Q<Label>("status");
void OnClick() => _status.text = "Done";

// GOOD Always unregister in OnDisable
void OnDisable() {
    _button.clicked -= OnButtonClicked;
    _slider.UnregisterValueChangedCallback(OnSliderChanged);
}
```

## Profiler Markers

| Marker | Measures | Fix |
|--------|----------|-----|
| `UpdateStyling` | USS selector application | Simplify selectors, reduce USS files |
| `Layout` | Flexbox computation | Reduce nesting, avoid frequent display toggles |
| `RenderChain` | Mesh tessellation + batching | Use UsageHints, reduce dynamic elements |

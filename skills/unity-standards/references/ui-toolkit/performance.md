# UI Toolkit Performance

## Element Visibility Cost

| Method | CPU | GPU | Memory | Use Case |
|--------|-----|-----|--------|----------|
| `visibility: hidden` | ✅ Low | ✅ No render | ✅ Freed | Frequently toggled UI |
| `opacity: 0` | ✅ Low | ⚠️ GPU processes | ✅ Freed | Fade animations |
| `display: none` | ⚠️ Layout reflow | ✅ No render | ✅ Freed | Permanent removal |
| `RemoveFromHierarchy()` | ⚠️ Recreate cost | ✅ Freed | ✅ Freed | One-time hide |

**Rule**: Use `visibility: hidden` for toggled UI. Use `display: none` only for permanent changes.

## Element Pooling

```csharp
private readonly List<VisualElement> _pool = new();

void InitPool(VisualElement parent, int count)
{
    for (int i = 0; i < count; i++)
    {
        var item = new VisualElement();
        item.AddToClassList("list-item");
        item.style.visibility = Visibility.Hidden;
        parent.Add(item);
        _pool.Add(item);
    }
}

VisualElement GetFromPool() =>
    _pool.FirstOrDefault(e => e.style.visibility == Visibility.Hidden)
         is { } item ? (item.style.visibility = Visibility.Visible, item).item : null;
```

## ListView (Built-in Pooling)

```csharp
// ListView auto-pools — only visible items exist in hierarchy
var listView = root.Q<ListView>("item-list");
listView.itemsSource = items;
listView.makeItem = () => new Label();
listView.bindItem = (element, index) =>
    ((Label)element).text = items[index].name;
```

## USS Selector Performance

- **Cost formula**: N1 (classes on element) × N2 (USS files loaded)
- BEM single-class selectors: `.button--primary` → O(1)
- Deep selectors: `.panel > .list > .item:hover` → N1×N2 per mouse move
- `:hover` on deep hierarchies triggers re-style on every `PointerMoveEvent`

## UsageHints

```csharp
element.usageHints = UsageHints.DynamicTransform;  // frequently moving elements
element.usageHints = UsageHints.GroupTransform;     // complex content grouping
```

## UQuery Caching & Memory Leaks

```csharp
// ✗ BAD: traverses hierarchy every call
void OnClick() => root.Q<Label>("status").text = "Done";

// ✓ GOOD: cache in OnEnable
private Label _status;
void OnEnable() => _status = root.Q<Label>("status");
void OnClick() => _status.text = "Done";

// ✗ Captures 'this' — entire MonoBehaviour stays alive
button.clicked += () => this.UpdateUI();
// ✓ Capture specific element reference
var label = root.Q<Label>("output");
button.clicked += () => label.text = "Updated";

// ✓ Always unregister in OnDisable
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

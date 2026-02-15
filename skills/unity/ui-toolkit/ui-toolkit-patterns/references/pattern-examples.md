# UI Toolkit Pattern Examples

> Code patterns for all 10 UI patterns. See [SKILL.md](../SKILL.md) for overview.

## 1. Tabbed Navigation

UXML: Tab bar with `tab-bar__tab` buttons + `tab-bar__indicator` + content pages (display:none toggled).

```css
.tab-bar { flex-direction: row; }
.tab-bar__tab { flex-grow: 1; padding: 12px 0; border-width: 0; color: var(--tab-idle); transition: color 0.2s; }
.tab-bar__tab--active { color: var(--tab-active); }
.tab-bar__indicator { position: absolute; bottom: 0; height: 3px; width: 33.33%; background-color: var(--tab-active); transition: translate 0.25s ease-out; }
```

```csharp
public class TabViewController {
    readonly List<Button> _tabs; readonly List<VisualElement> _pages;
    readonly VisualElement _indicator; int _activeIndex;
    public TabViewController(VisualElement root) {
        _tabs = root.Query<Button>(className: "tab-bar__tab").ToList();
        _pages = root.Query<VisualElement>(className: "tab-view__page").ToList();
        _indicator = root.Q(className: "tab-bar__indicator");
        for (int i = 0; i < _tabs.Count; i++) { int idx = i; _tabs[i].clicked += () => SelectTab(idx); }
    }
    public void SelectTab(int index) {
        _tabs[_activeIndex].RemoveFromClassList("tab-bar__tab--active");
        _pages[_activeIndex].style.display = DisplayStyle.None;
        _activeIndex = index;
        _tabs[_activeIndex].AddToClassList("tab-bar__tab--active");
        _pages[_activeIndex].style.display = DisplayStyle.Flex;
        _indicator.style.translate = new Translate(new Length(100f * index, LengthUnit.Percent), 0);
    }
}
```

## 2. Inventory Grid

`<ListView name="inventory-grid" fixed-item-height="90" selection-type="Single"/>` with detail panel.

```csharp
public class InventoryGridController {
    public InventoryGridController(VisualElement root, List<ItemData> items) {
        var grid = root.Q<ListView>("inventory-grid");
        grid.makeItem = () => { /* card with icon + qty label */ };
        grid.bindItem = (el, i) => {
            el.Q("icon").style.backgroundImage = new StyleBackground(items[i].Icon);
            el.Q<Label>("qty").text = items[i].Quantity > 1 ? $"x{items[i].Quantity}" : "";
        };
        grid.itemsSource = items;
        grid.selectionChanged += sel => { /* update detail panel */ };
    }
}
```

DC uses `ScrollView` + `VisualTreeAsset.Instantiate()` (no virtualization). Use `ListView` for 50+ items, `ScrollView` for small fixed sets.

## 3. Modal / Popup Dialog

Overlay with backdrop click-to-close, animated via `translate` + `opacity` class toggles.

```csharp
public class ModalController {
    readonly VisualElement _overlay, _backdrop, _dialog; Action _onConfirm;
    public ModalController(VisualElement root) {
        _overlay = root.Q("modal-overlay"); _backdrop = root.Q(className: "modal-backdrop");
        _dialog = root.Q(className: "modal-dialog");
        _backdrop.RegisterCallback<ClickEvent>(_ => Hide());
        root.Q<Button>("btn-cancel").clicked += Hide;
        root.Q<Button>("btn-confirm").clicked += () => { _onConfirm?.Invoke(); Hide(); };
    }
    public void Show(string title, string body, Action onConfirm) {
        _overlay.Q<Label>(className: "modal__title").text = title;
        _overlay.Q<Label>(className: "modal__body").text = body;
        _onConfirm = onConfirm;
        _overlay.style.display = DisplayStyle.Flex;
        _overlay.schedule.Execute(() => {
            _backdrop.AddToClassList("modal-backdrop--visible");
            _dialog.AddToClassList("modal-dialog--visible");
        });
    }
    public void Hide() {
        _backdrop.RemoveFromClassList("modal-backdrop--visible");
        _dialog.RemoveFromClassList("modal-dialog--visible");
        _dialog.schedule.Execute(() => _overlay.style.display = DisplayStyle.None).ExecuteLater(300);
    }
}
```

Key USS: `.modal-backdrop--visible { opacity: 1; }`, `.modal-dialog--visible { translate: 0 0; opacity: 1; }`.

## 4. Stateful Buttons

```css
.btn-primary { transition: background-color 0.15s, scale 0.1s; }
.btn-primary:hover { scale: 1.03; }
.btn-primary:active { scale: 0.97; }
.btn-primary:disabled { background-color: #37474F; }
.btn-primary.btn--loading .btn__label { visibility: hidden; }
.btn-primary.btn--loading .btn__spinner { display: flex; }
```

```csharp
public void SetLoading(bool loading) {
    _button.SetEnabled(!loading);
    _button.EnableInClassList("btn--loading", loading);
    if (loading) {
        float angle = 0f;
        _spinAnim = _button.schedule.Execute(() => {
            angle = (angle + 15f) % 360f;
            _spinner.style.rotate = new Rotate(angle);
        }).Every(16);
    } else { _spinAnim?.Pause(); _spinAnim = null; }
}
```

## 5. Message List (Mail/Chat)

`<ListView name="message-list" fixed-item-height="72"/>` with read/unread + swipe-to-dismiss.

```csharp
// Swipe gesture in makeItem
float startX = 0;
row.RegisterCallback<PointerDownEvent>(e => startX = e.position.x);
row.RegisterCallback<PointerUpEvent>(e => {
    if (startX - e.position.x > 80) row.AddToClassList("msg-row--swiped");
});
// In bindItem: read/unread state
el.EnableInClassList("msg-row--unread", !msg.IsRead);
```

## 6. Scroll View with Snap

Horizontal carousel with page snapping and indicator dots.

```csharp
public class SnapCarouselController {
    readonly ScrollView _scroll; readonly List<VisualElement> _dots = new();
    int _pageCount, _currentPage;
    public SnapCarouselController(VisualElement root, int pageCount) {
        _pageCount = pageCount; _scroll = root.Q<ScrollView>("carousel-scroll");
        var dotsContainer = root.Q("carousel-dots");
        for (int i = 0; i < pageCount; i++) {
            var dot = new VisualElement(); dot.AddToClassList("dot");
            int idx = i; dot.RegisterCallback<ClickEvent>(_ => SnapToPage(idx));
            dotsContainer.Add(dot); _dots.Add(dot);
        }
        _scroll.horizontalScroller.valueChanged += v => {
            float pw = _scroll.contentContainer.resolvedStyle.width / _pageCount;
            if (pw > 0) { int n = Mathf.Clamp(Mathf.RoundToInt(v / pw), 0, _pageCount - 1); if (n != _currentPage) UpdateDots(n); }
        };
    }
    public void SnapToPage(int i) { _scroll.scrollOffset = new Vector2(_scroll.contentContainer.resolvedStyle.width / _pageCount * i, 0); UpdateDots(i); }
    void UpdateDots(int a) { _dots[_currentPage].RemoveFromClassList("dot--active"); _currentPage = a; _dots[a].AddToClassList("dot--active"); }
}
```

## 7. Async Task Animation (Non-MonoBehaviour)

UIView classes (plain C#) use `async Task`. Fire-and-forget: `_ = MethodAsync()` — wrap in `try/catch`.

```csharp
// Typewriter — Task.Delay ignores timeScale
async Task TypewriterRoutine(Label label, string text) {
    label.text = ""; foreach (char c in text) { label.text += c; await Task.Delay(20); }
}
// Progress bar — Stopwatch + Yield for frame-independent timing
async Task UpdateLevelAsync(float target, float lerpTime) {
    float start = m_LevelProgress; var sw = System.Diagnostics.Stopwatch.StartNew();
    while (sw.Elapsed.TotalSeconds < lerpTime) { float t = (float)(sw.Elapsed.TotalSeconds / lerpTime); m_ProgressBar.style.width = new Length(Mathf.Lerp(start, target, t) * 100f, LengthUnit.Percent); await Task.Yield(); }
}
```

| Strategy | timeScale | Best For |
|---|---|---|
| `Task.Delay(ms)` | Ignores | Typewriter, fixed-rate |
| `Stopwatch+Yield` | Ignores | Progress bars |

## 8. Experimental Animation API

```csharp
// Position — slide marker. Requires coordinate conversion.
void AnimateMarkerToTarget(VisualElement target, int ms = 200) {
    Vector2 world = target.parent.LocalToWorld(target.layout.position);
    Vector3 local = m_MenuMarker.parent.WorldToLocal(world);
    m_MenuMarker.experimental.animation.Position(local - new Vector3(m_MenuMarker.resolvedStyle.width / 2f, 0, 0), ms);
}
// Scale — pop-in: element.transform.scale = Vector3(0.1f,0.1f,1f); element.experimental.animation.Scale(1f, 200);
```

## 9. GeometryChangedEvent & Composite View

- **GeometryChangedEvent**: `resolvedStyle` returns zero until layout. Register → fire once → unregister. See [responsive](../../ui-toolkit-responsive/SKILL.md).
- **Composite View**: Split complex screens into parent + child UIViews. Parent injects containers via `Q()`. 2 levels max. See [architecture](../../ui-toolkit-architecture/SKILL.md).

## 10. World-to-Panel Positioning

```csharp
void UpdateHealthBarPosition(VisualElement element, Vector3 worldPos, Vector2 worldSize) {
    if (element.panel == null) return;
    Rect rect = RuntimePanelUtils.CameraTransformWorldToPanelRect(element.panel, worldPos, worldSize, Camera.main);
    element.transform.position = rect.position;
    element.style.width = rect.width; element.style.height = rect.height;
}
// Call every frame via Update() or schedule.Execute().Every(16). Check element.panel != null.
```

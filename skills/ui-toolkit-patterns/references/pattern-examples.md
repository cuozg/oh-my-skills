# UI Toolkit Pattern Examples (Part 1)

> Code patterns for patterns 1-3. See [SKILL.md](../SKILL.md) for overview.

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

See [pattern-examples-advanced.md](pattern-examples-advanced.md) for patterns 4–10.

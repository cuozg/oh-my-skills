---
name: ui-toolkit-patterns
description: "Common UI patterns implemented in Unity UI Toolkit with complete UXML/USS/C# examples. Covers tabbed navigation, inventory grids, modal dialogs, stateful buttons, message lists, and scroll snapping. Use when: (1) Building tabbed interfaces, (2) Creating inventory or card grid layouts, (3) Implementing modal popups with backdrop, (4) Adding button states and loading spinners, (5) Building chat or mail list views, (6) Implementing horizontal scroll with page snap. Triggers: 'tab bar', 'inventory grid', 'modal popup', 'dialog overlay', 'button states', 'message list', 'scroll snap', 'UI pattern'."
---

# UI Toolkit Common Patterns

> **Based on**: Unity 6 (6000.0), [Dragon Crashers](../references/dragon-crashers-insights.md) official sample

Production-ready patterns with complete UXML, USS, and C#. Follows [architecture](../ui-toolkit-architecture/SKILL.md) principles: UXML=structure, USS=style, C#=behavior. All animations use transform properties (`translate`, `scale`, `opacity`, `rotate`) to avoid layout cost — see [ui-toolkit-performance](../ui-toolkit-performance/SKILL.md).

---

## 1. Tabbed Navigation

Tab bar with content switching and sliding indicator. Based on the [Dragon Crashers](../references/dragon-crashers-insights.md) pattern.

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
  <ui:VisualElement class="tab-view">
    <ui:VisualElement class="tab-bar">
      <ui:Button class="tab-bar__tab tab-bar__tab--active" name="tab-inventory" text="Inventory"/>
      <ui:Button class="tab-bar__tab" name="tab-skills" text="Skills"/>
      <ui:Button class="tab-bar__tab" name="tab-stats" text="Stats"/>
      <ui:VisualElement class="tab-bar__indicator"/>
    </ui:VisualElement>
    <ui:VisualElement class="tab-view__content">
      <ui:VisualElement name="content-inventory" class="tab-view__page"/>
      <ui:VisualElement name="content-skills" class="tab-view__page" style="display:none;"/>
      <ui:VisualElement name="content-stats" class="tab-view__page" style="display:none;"/>
    </ui:VisualElement>
  </ui:VisualElement>
</ui:UXML>
```

```css
:root { --tab-active: #4FC3F7; --tab-idle: #90A4AE; }
.tab-bar { flex-direction: row; border-bottom-width: 2px; border-bottom-color: rgba(255,255,255,0.1); }
.tab-bar__tab {
  flex-grow: 1; padding: 12px 0; background-color: rgba(0,0,0,0);
  border-width: 0; color: var(--tab-idle); font-size: 14px;
  -unity-font-style: bold; transition: color 0.2s;
}
.tab-bar__tab:hover { color: #fff; }
.tab-bar__tab--active { color: var(--tab-active); }
.tab-bar__indicator {
  position: absolute; bottom: 0; height: 3px; width: 33.33%;
  background-color: var(--tab-active); transition: translate 0.25s ease-out;
}
.tab-view__content { flex-grow: 1; }
.tab-view__page { flex-grow: 1; }
```

```csharp
public class TabViewController
{
    readonly List<Button> _tabs;
    readonly List<VisualElement> _pages;
    readonly VisualElement _indicator;
    int _activeIndex;

    public TabViewController(VisualElement root)
    {
        _tabs = root.Query<Button>(className: "tab-bar__tab").ToList();
        _pages = root.Query<VisualElement>(className: "tab-view__page").ToList();
        _indicator = root.Q(className: "tab-bar__indicator");
        for (int i = 0; i < _tabs.Count; i++)
        {
            int idx = i;
            _tabs[i].clicked += () => SelectTab(idx);
        }
        SelectTab(0);
    }

    public void SelectTab(int index)
    {
        _tabs[_activeIndex].RemoveFromClassList("tab-bar__tab--active");
        _pages[_activeIndex].style.display = DisplayStyle.None;
        _activeIndex = index;
        _tabs[_activeIndex].AddToClassList("tab-bar__tab--active");
        _pages[_activeIndex].style.display = DisplayStyle.Flex;
        _indicator.style.translate = new Translate(new Length(100f * index, LengthUnit.Percent), 0);
    }
}
```

### Dragon Crashers Implementation — Two Tab Approaches

Dragon Crashers uses **two contrasting tab implementations**, which is a great study in reusability vs simplicity tradeoffs.

#### Approach A: Reusable Convention-Based Controller (`TabbedMenuController`)

Used by Mail and Character screens. Maps tab → content by suffix convention: element named `{id}-tab` activates `{id}-content`.

```csharp
// from Assets/Scripts/UI/Controllers/TabbedMenuController.cs
public class TabbedMenuController
{
    const string k_TabClassName = "tab";
    const string k_SelectedTabClassName = "selected-tab";
    const string k_UnselectedTabClassName = "unselected-tab";
    const string k_TabNameSuffix = "-tab";
    const string k_ContentNameSuffix = "-content";

    readonly VisualElement m_Root;

    public TabbedMenuController(VisualElement root)
    {
        m_Root = root;
        // Find all elements with "tab" USS class and wire up click handlers
        var tabs = GetAllTabs();
        foreach (var tab in tabs)
        {
            tab.RegisterCallback<ClickEvent>(OnTabClicked);
        }
    }

    void OnTabClicked(ClickEvent evt)
    {
        if (evt.currentTarget is not VisualElement clickedTab) return;
        if (TabIsCurrentlySelected(clickedTab)) return;

        // Deselect all tabs, select clicked one
        GetAllTabs().Where(tab => tab != clickedTab && TabIsCurrentlySelected(tab))
            .ForEach(UnselectTab);
        SelectTab(clickedTab);
    }

    // Convention: tab named "inbox-tab" → content named "inbox-content"
    void SelectTab(VisualElement tab)
    {
        tab.RemoveFromClassList(k_UnselectedTabClassName);
        tab.AddToClassList(k_SelectedTabClassName);
        var content = FindContent(tab);
        content.RemoveFromClassList("unselected-content");
    }

    void UnselectTab(VisualElement tab)
    {
        tab.RemoveFromClassList(k_SelectedTabClassName);
        tab.AddToClassList(k_UnselectedTabClassName);
        var content = FindContent(tab);
        content.AddToClassList("unselected-content");
    }

    // Name convention mapping: "inbox-tab" → "inbox-content"
    VisualElement FindContent(VisualElement tab)
    {
        string tabName = tab.name;
        string contentName = tabName.Replace(k_TabNameSuffix, k_ContentNameSuffix);
        return m_Root.Q(contentName);
    }

    static bool TabIsCurrentlySelected(VisualElement tab) =>
        tab.ClassListContains(k_SelectedTabClassName);

    UQueryBuilder<VisualElement> GetAllTabs() =>
        m_Root.Query<VisualElement>(className: k_TabClassName);
}
```

**Key insight**: No hardcoded tab names — works for ANY screen with properly named UXML elements. Reuse by wrapping in `TabbedMenu.cs`:

```csharp
// from Assets/Scripts/UI/Components/TabbedMenu.cs
// Wrapper that creates controller from any VisualElement with tabs
public class TabbedMenu
{
    TabbedMenuController m_Controller;

    public TabbedMenu(VisualElement root)
    {
        m_Controller = new TabbedMenuController(root);
    }
}
```

#### Approach B: Manual Per-Screen Tab Implementation (`ShopView`)

Used by Shop screen. Trades reusability for fine-grained control — each tab fires a specific domain event.

```csharp
// from Assets/Scripts/UI/UIViews/ShopView.cs
const string k_TabClass = "shoptab";
const string k_SelectedTabClass = "selected-shoptab";

Button m_GoldTabButton;
Button m_GemTabButton;
Button m_PotionTabButton;

public override void Initialize()
{
    base.Initialize();

    m_GoldTabButton = m_TopElement.Q<Button>("shop__gold-tab-button");
    m_GemTabButton = m_TopElement.Q<Button>("shop__gem-tab-button");
    m_PotionTabButton = m_TopElement.Q<Button>("shop__potion-tab-button");

    // Each tab fires a domain-specific event
    m_GoldTabButton.RegisterCallback<ClickEvent>(SelectGoldTab);
    m_GemTabButton.RegisterCallback<ClickEvent>(SelectGemTab);
    m_PotionTabButton.RegisterCallback<ClickEvent>(SelectPotionTab);
}

void SelectGoldTab(ClickEvent evt)
{
    ClickTabButton(evt);
    ShopEvents.GoldSelected?.Invoke();
}

// CSS class toggle — manual select/unselect
void ClickTabButton(ClickEvent evt)
{
    UnselectTab(m_GoldTabButton);
    UnselectTab(m_GemTabButton);
    UnselectTab(m_PotionTabButton);
    SelectTab(evt.currentTarget as VisualElement);
}

void SelectTab(VisualElement tab) => tab.AddToClassList(k_SelectedTabClass);
void UnselectTab(VisualElement tab) => tab.RemoveFromClassList(k_SelectedTabClass);
```

#### When to Use Each Approach

| Criteria | `TabbedMenuController` (Reusable) | Manual per-screen |
|----------|-----------------------------------|-------------------|
| **Tab count** | Any (auto-discovered) | Fixed, known at compile time |
| **Tab → action** | Generic (show/hide content) | Domain-specific events per tab |
| **Reusability** | Drop into any UXML with naming convention | One-off per screen |
| **Coupling** | None — pure CSS class toggle | Tight — each tab knows its domain event |
| **Best for** | Mail, Settings, Character screens | Shop, Inventory with filter logic |

---

## 2. Inventory Grid

ListView-backed grid with item cards, selection state, and detail panel. See [ui-toolkit-performance](../ui-toolkit-performance/SKILL.md) for large-list virtualization.

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
  <ui:VisualElement class="inventory">
    <ui:ListView name="inventory-grid" class="inventory__grid"
                 fixed-item-height="90" selection-type="Single"/>
    <ui:VisualElement name="detail-panel" class="inventory__detail">
      <ui:VisualElement class="detail__icon"/>
      <ui:Label class="detail__name"/>
      <ui:Label class="detail__desc"/>
    </ui:VisualElement>
  </ui:VisualElement>
</ui:UXML>
```

```css
.inventory { flex-direction: row; flex-grow: 1; }
.inventory__grid { width: 65%; }
.item-card {
  width: 80px; height: 80px; margin: 4px; border-radius: 8px;
  background-color: rgba(255,255,255,0.06); align-items: center;
  justify-content: center; transition: scale 0.15s, background-color 0.15s;
}
.item-card:hover { scale: 1.05; background-color: rgba(255,255,255,0.12); }
.item-card--selected { border-width: 2px; border-color: #4FC3F7; background-color: rgba(79,195,247,0.15); }
.item-card__icon { width: 48px; height: 48px; }
.item-card__qty { position: absolute; bottom: 4px; right: 6px; font-size: 11px; color: #ccc; }
.inventory__detail { width: 35%; padding: 16px; background-color: rgba(0,0,0,0.3); }
```

```csharp
public class InventoryGridController
{
    readonly ListView _grid;
    readonly VisualElement _detail;
    List<ItemData> _items;

    public InventoryGridController(VisualElement root, List<ItemData> items)
    {
        _items = items;
        _grid = root.Q<ListView>("inventory-grid");
        _detail = root.Q("detail-panel");
        _grid.makeItem = () =>
        {
            var card = new VisualElement { name = "card" };
            card.AddToClassList("item-card");
            var icon = new VisualElement { name = "icon" };
            icon.AddToClassList("item-card__icon");
            var qty = new Label { name = "qty" };
            qty.AddToClassList("item-card__qty");
            card.Add(icon);
            card.Add(qty);
            return card;
        };
        _grid.bindItem = (el, i) =>
        {
            el.Q("icon").style.backgroundImage = new StyleBackground(_items[i].Icon);
            el.Q<Label>("qty").text = _items[i].Quantity > 1 ? $"x{_items[i].Quantity}" : "";
        };
        _grid.itemsSource = _items;
        _grid.selectionChanged += sel =>
        {
            if (sel.FirstOrDefault() is not ItemData item) return;
            _detail.Q<Label>(className: "detail__name").text = item.Name;
            _detail.Q<Label>(className: "detail__desc").text = item.Description;
            _detail.Q(className: "detail__icon").style.backgroundImage = new StyleBackground(item.Icon);
        };
    }
}
```

### Dragon Crashers Implementation — ScrollView + VisualTreeAsset (Not ListView)

> **Key difference**: Dragon Crashers does NOT use `ListView` for its inventory grid. It uses a `ScrollView` with manual `VisualTreeAsset.Instantiate()` loops. This means no virtualization — simpler code but higher memory for large lists. Choose `ListView` for 100+ items, `ScrollView` for smaller fixed sets.

#### Item Instantiation Pattern (`InventoryView`)

```csharp
// from Assets/Scripts/UI/UIViews/InventoryView.cs
VisualTreeAsset m_GearItemAsset;   // assigned from Resources or SerializedField
ScrollView m_InventoryScrollView;

// Called when filtered gear list changes
void ShowGearItems(List<GearData> gearToShow)
{
    // 1. Clear existing items
    m_InventoryScrollView.Clear();

    // 2. Instantiate from VisualTreeAsset template for each item
    foreach (var gearData in gearToShow)
    {
        // Clone the UXML template
        TemplateContainer gearUIElement = m_GearItemAsset.Instantiate();
        gearUIElement.AddToClassList("gear-item-spacing");

        // Create component wrapper, bind data, register callbacks
        GearItemComponent gearItem = new GearItemComponent(gearData);
        gearItem.SetVisualElements(gearUIElement);
        gearItem.SetGameData(gearUIElement);
        gearItem.RegisterButtonCallbacks();

        // Add to scroll container
        m_InventoryScrollView.Add(gearUIElement);
    }
}
```

**Pattern breakdown**:
1. `VisualTreeAsset.Instantiate()` — clones the UXML template (returns `TemplateContainer`)
2. Component wrapper class (`GearItemComponent`) — bridges data ↔ visual elements
3. `SetVisualElements()` — queries child elements by name
4. `SetGameData()` — binds data values to labels/images
5. `RegisterButtonCallbacks()` — wires click handlers

#### Filtering via DropdownField (`InventoryView`)

```csharp
// from Assets/Scripts/UI/UIViews/InventoryView.cs
DropdownField m_InventoryRarityDropdown;
DropdownField m_InventoryTypeDropdown;

public override void Initialize()
{
    base.Initialize();

    m_InventoryRarityDropdown = m_TopElement.Q<DropdownField>("inventory__rarity-dropdown");
    m_InventoryTypeDropdown = m_TopElement.Q<DropdownField>("inventory__type-dropdown");

    // DropdownField fires ChangeEvent<string> on selection
    m_InventoryRarityDropdown.RegisterValueChangedCallback(UpdateFilters);
    m_InventoryTypeDropdown.RegisterValueChangedCallback(UpdateFilters);
}

void UpdateFilters(ChangeEvent<string> evt)
{
    // Parse string back to enum
    Rarity rarity = Enum.Parse<Rarity>(m_InventoryRarityDropdown.value);
    EquipmentType gearType = Enum.Parse<EquipmentType>(m_InventoryTypeDropdown.value);

    // Fire event → controller filters → event back → view refreshes
    InventoryEvents.GearFiltered?.Invoke(rarity, gearType);
}
```

#### Controller-Side LINQ Filtering (`InventoryScreenController`)

```csharp
// from Assets/Scripts/UI/Controllers/InventoryScreenController.cs
void FilterGearList(Rarity rarity, EquipmentType gearType)
{
    List<GearData> filteredGear = m_AllGear
        .Where(g => rarity == Rarity.All || g.rarity == rarity)
        .Where(g => gearType == EquipmentType.All || g.equipmentType == gearType)
        .ToList();

    SortGearList(filteredGear);
}

void SortGearList(List<GearData> gearToSort)
{
    List<GearData> sortedGear = gearToSort
        .OrderBy(g => g.rarity)
        .ThenBy(g => g.equipmentType)
        .ToList();

    // Fire event back to view to refresh the grid
    InventoryEvents.InventoryUpdated?.Invoke(sortedGear);
}
```

#### Event Flow Diagram

```
DropdownField.ChangeEvent<string>
    → InventoryView.UpdateFilters()
        → InventoryEvents.GearFiltered?.Invoke(rarity, type)
            → InventoryScreenController.FilterGearList()
                → LINQ Where().OrderBy()
                    → InventoryEvents.InventoryUpdated?.Invoke(filteredList)
                        → InventoryView.ShowGearItems(filteredList)
                            → ScrollView.Clear() + Instantiate loop
```

> **ListView vs ScrollView tradeoff**: Use `ListView` (as in the generic pattern above) when you have 100+ items and need virtualization. Use `ScrollView` + `Instantiate()` (Dragon Crashers pattern) when items are fewer and you need full control over the item lifecycle.

---

## 3. Modal / Popup Dialog

Overlay with backdrop click-to-close and animated show/hide via `translate` + `opacity`.

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
  <ui:VisualElement name="modal-overlay" class="modal-overlay" style="display:none;">
    <ui:VisualElement class="modal-backdrop"/>
    <ui:VisualElement class="modal-dialog">
      <ui:Label class="modal__title" text="Confirm"/>
      <ui:Label class="modal__body" text="Are you sure?"/>
      <ui:VisualElement class="modal__actions">
        <ui:Button name="btn-cancel" class="modal__btn modal__btn--secondary" text="Cancel"/>
        <ui:Button name="btn-confirm" class="modal__btn modal__btn--primary" text="OK"/>
      </ui:VisualElement>
    </ui:VisualElement>
  </ui:VisualElement>
</ui:UXML>
```

```css
.modal-overlay {
  position: absolute; left: 0; top: 0; right: 0; bottom: 0;
  align-items: center; justify-content: center;
}
.modal-backdrop {
  position: absolute; left: 0; top: 0; right: 0; bottom: 0;
  background-color: rgba(0,0,0,0.5); opacity: 0; transition: opacity 0.2s;
}
.modal-backdrop--visible { opacity: 1; }
.modal-dialog {
  width: 360px; padding: 24px; border-radius: 12px; background-color: #263238;
  translate: 0 30px; opacity: 0; transition: translate 0.25s ease-out, opacity 0.2s;
}
.modal-dialog--visible { translate: 0 0; opacity: 1; }
.modal__title { font-size: 20px; -unity-font-style: bold; margin-bottom: 8px; }
.modal__body { font-size: 14px; color: #B0BEC5; margin-bottom: 20px; white-space: normal; }
.modal__actions { flex-direction: row; justify-content: flex-end; }
.modal__btn { padding: 8px 20px; border-radius: 6px; border-width: 0; margin-left: 8px; }
.modal__btn--secondary { background-color: #455A64; color: #CFD8DC; }
.modal__btn--primary { background-color: #4FC3F7; color: #0D1B2A; }
```

```csharp
public class ModalController
{
    readonly VisualElement _overlay, _backdrop, _dialog;
    Action _onConfirm;

    public ModalController(VisualElement root)
    {
        _overlay = root.Q("modal-overlay");
        _backdrop = root.Q(className: "modal-backdrop");
        _dialog = root.Q(className: "modal-dialog");
        _backdrop.RegisterCallback<ClickEvent>(_ => Hide());
        root.Q<Button>("btn-cancel").clicked += Hide;
        root.Q<Button>("btn-confirm").clicked += () => { _onConfirm?.Invoke(); Hide(); };
    }

    public void Show(string title, string body, Action onConfirm)
    {
        _overlay.Q<Label>(className: "modal__title").text = title;
        _overlay.Q<Label>(className: "modal__body").text = body;
        _onConfirm = onConfirm;
        _overlay.style.display = DisplayStyle.Flex;
        _overlay.schedule.Execute(() =>
        {
            _backdrop.AddToClassList("modal-backdrop--visible");
            _dialog.AddToClassList("modal-dialog--visible");
        });
    }

    public void Hide()
    {
        _backdrop.RemoveFromClassList("modal-backdrop--visible");
        _dialog.RemoveFromClassList("modal-dialog--visible");
        _dialog.schedule.Execute(() => _overlay.style.display = DisplayStyle.None).ExecuteLater(300);
    }
}
```

### Dragon Crashers Implementation — Modal vs Overlay Navigation

Dragon Crashers implements **two distinct navigation patterns** in `UIManager.cs` — a true modal (replaces current view) and an overlay (shows on top, restores previous).

#### Modal Navigation Pattern (`UIManager`)

Hides the current view entirely, shows the new one. Saves previous view for back-navigation.

```csharp
// from Assets/Scripts/UI/UIViews/UIManager.cs
UIView m_CurrentView;
UIView m_PreviousView;

// Modal: only one view visible at a time
void ShowModalView(UIView newView)
{
    // Hide whatever is currently shown
    m_CurrentView?.Hide();

    // Save for back-navigation
    m_PreviousView = m_CurrentView;

    // Show new view
    m_CurrentView = newView;
    m_CurrentView?.Show();
}
```

#### Overlay Pattern (`UIManager`)

Overlays keep the previous view alive (just hidden). Used for Settings and Inventory which can be dismissed to return to the previous screen.

```csharp
// from Assets/Scripts/UI/UIViews/UIManager.cs
// Settings overlay — shows on top, restores previous on close
void OnSettingsScreenShown()
{
    m_PreviousView = m_CurrentView;
    m_SettingsView.Show();
}

void OnSettingsScreenHidden()
{
    m_SettingsView.Hide();
    m_PreviousView?.Show();
    m_CurrentView = m_PreviousView;
}

// Inventory overlay — same pattern, different view
void OnInventoryScreenShown()
{
    m_PreviousView = m_CurrentView;
    m_InventoryView.Show();
}

void OnInventoryScreenHidden()
{
    m_InventoryView.Hide();
    m_PreviousView?.Show();
    m_CurrentView = m_PreviousView;
}
```

#### Scale Animation on Show (`InventoryView`)

Dragon Crashers uses the **experimental animation API** (not USS transitions) for a pop-in scale effect when opening the inventory.

```csharp
// from Assets/Scripts/UI/UIViews/InventoryView.cs
public override void Show()
{
    base.Show();

    // Start at 10% scale, animate to 100% over 200ms
    m_InventoryPanel.transform.scale = new Vector3(0.1f, 0.1f, 1f);
    m_InventoryPanel.experimental.animation.Scale(1f, 200);
}
```

> ⚠️ **Note**: `experimental.animation` is a convenience API but lacks easing control. For production, prefer USS transitions (`transition: scale 0.2s ease-out`) which give you easing curves and are declared in stylesheets rather than C#. See [ui-toolkit-performance](../ui-toolkit-performance/SKILL.md) for animation cost comparison.

#### Modal vs Overlay Decision Guide

| Behavior | Modal (`ShowModalView`) | Overlay |
|----------|------------------------|---------|
| **Previous view** | Hidden via `Hide()` | Saved in `m_PreviousView`, restored on close |
| **Navigation stack** | Single `m_PreviousView` (1 level) | Single `m_PreviousView` (1 level) |
| **Use case** | Screen transitions (Home → Mail → Shop) | Temporary panels (Settings, Inventory popover) |
| **Animation** | View's own `Show()`/`Hide()` | View's own `Show()`/`Hide()` |

---

## 4. Stateful Buttons

USS pseudo-classes for normal/hover/active/disabled + loading spinner via class toggle.

```css
.btn-primary {
  padding: 10px 24px; border-radius: 8px; border-width: 0;
  background-color: #4FC3F7; color: #0D1B2A; font-size: 14px;
  -unity-font-style: bold; transition: background-color 0.15s, scale 0.1s;
}
.btn-primary:hover { background-color: #29B6F6; scale: 1.03; }
.btn-primary:active { background-color: #0288D1; scale: 0.97; }
.btn-primary:disabled { background-color: #37474F; color: #607D8B; }
.btn-primary.btn--loading { background-color: #37474F; }
.btn-primary.btn--loading .btn__label { visibility: hidden; }
.btn-primary.btn--loading .btn__spinner { display: flex; }
.btn__spinner {
  display: none; position: absolute; width: 20px; height: 20px;
  border-width: 3px; border-color: rgba(255,255,255,0.3);
  border-top-color: #fff; border-radius: 50%;
}
```

```csharp
public class StatefulButton
{
    readonly Button _button;
    readonly VisualElement _spinner;
    IVisualElementScheduledItem _spinAnim;

    public StatefulButton(Button button)
    {
        _button = button;
        _button.AddToClassList("btn-primary");
        _button.Q<Label>()?.AddToClassList("btn__label");
        _spinner = new VisualElement();
        _spinner.AddToClassList("btn__spinner");
        _button.Add(_spinner);
    }

    public void SetLoading(bool loading)
    {
        _button.SetEnabled(!loading);
        _button.EnableInClassList("btn--loading", loading);
        if (loading)
        {
            float angle = 0f;
            _spinAnim = _button.schedule.Execute(() =>
            {
                angle = (angle + 15f) % 360f;
                _spinner.style.rotate = new Rotate(angle);
            }).Every(16);
        }
        else { _spinAnim?.Pause(); _spinAnim = null; }
    }
}
```

### Dragon Crashers Implementation — Button State via CSS Class Toggle

Dragon Crashers doesn't use a generic `StatefulButton` wrapper — instead it manages button state through direct CSS class toggling and fires audio feedback via a centralized `AudioManager`.

#### Tab Button State Toggle (`ShopView`)

```csharp
// from Assets/Scripts/UI/UIViews/ShopView.cs
const string k_SelectedTabClass = "selected-shoptab";

// Select: add CSS class for visual state
void SelectTab(VisualElement tab) => tab.AddToClassList(k_SelectedTabClass);

// Unselect: remove CSS class
void UnselectTab(VisualElement tab) => tab.RemoveFromClassList(k_SelectedTabClass);

// On click: unselect all, select clicked, fire domain event
void ClickTabButton(ClickEvent evt)
{
    UnselectTab(m_GoldTabButton);
    UnselectTab(m_GemTabButton);
    UnselectTab(m_PotionTabButton);
    SelectTab(evt.currentTarget as VisualElement);
}
```

USS for the tab states (conceptual — based on Dragon Crashers conventions):

```css
/* from Assets/UI/Uss/Screens/ShopScreen.uss (conceptual) */
.shoptab {
    background-color: rgba(255, 255, 255, 0.05);
    color: #90A4AE;
    transition: background-color 0.15s, color 0.15s;
}

.selected-shoptab {
    background-color: rgba(79, 195, 247, 0.2);
    color: #4FC3F7;
    border-bottom-width: 2px;
    border-bottom-color: #4FC3F7;
}
```

#### Audio Feedback Pattern

Dragon Crashers fires button sounds through a centralized `AudioManager` rather than per-button:

```csharp
// from Assets/Scripts/UI/UIViews/ShopView.cs
void SelectGoldTab(ClickEvent evt)
{
    ClickTabButton(evt);
    AudioManager.PlayDefaultButtonSound();  // centralized audio
    ShopEvents.GoldSelected?.Invoke();
}
```

> **Pattern**: Separate visual state (CSS class toggle) from audio (centralized manager) from domain logic (events). Each concern handled by a different system.

---

## 5. Message List (Mail/Chat)

ListView with read/unread states, swipe gesture, and badge counter.

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
  <ui:VisualElement class="mail-view">
    <ui:VisualElement class="mail-header">
      <ui:Label class="mail-header__title" text="Inbox"/>
      <ui:VisualElement class="mail-header__badge">
        <ui:Label name="badge-count" class="badge__text" text="3"/>
      </ui:VisualElement>
    </ui:VisualElement>
    <ui:ListView name="message-list" fixed-item-height="72"/>
  </ui:VisualElement>
</ui:UXML>
```

```css
.mail-header { flex-direction: row; align-items: center; padding: 12px 16px; }
.mail-header__title { font-size: 22px; -unity-font-style: bold; flex-grow: 1; }
.mail-header__badge {
  width: 24px; height: 24px; border-radius: 12px; background-color: #EF5350;
  align-items: center; justify-content: center;
}
.badge__text { font-size: 12px; color: #fff; -unity-font-style: bold; }
.msg-row {
  flex-direction: row; padding: 12px 16px; align-items: center;
  border-bottom-width: 1px; border-bottom-color: rgba(255,255,255,0.06);
  transition: translate 0.2s, opacity 0.2s;
}
.msg-row--unread { background-color: rgba(79,195,247,0.08); }
.msg-row--swiped { translate: -100% 0; opacity: 0; }
.msg__dot { width: 8px; height: 8px; border-radius: 4px; background-color: #4FC3F7; margin-right: 12px; }
.msg__dot--read { opacity: 0; }
.msg__sender { font-size: 14px; -unity-font-style: bold; }
.msg__preview { font-size: 12px; color: #90A4AE; margin-top: 2px; }
.msg__time { font-size: 11px; color: #607D8B; }
```

```csharp
public class MessageListController
{
    readonly ListView _list;
    readonly Label _badge;
    List<MessageData> _messages;

    public MessageListController(VisualElement root, List<MessageData> messages)
    {
        _messages = messages;
        _list = root.Q<ListView>("message-list");
        _badge = root.Q<Label>("badge-count");
        _list.makeItem = () =>
        {
            var row = new VisualElement();
            row.AddToClassList("msg-row");
            var dot = new VisualElement(); dot.AddToClassList("msg__dot"); row.Add(dot);
            var content = new VisualElement(); content.AddToClassList("msg__content");
            content.Add(new Label { name = "sender", classList = { "msg__sender" } });
            content.Add(new Label { name = "preview", classList = { "msg__preview" } });
            row.Add(content);
            var time = new Label { name = "time" }; time.AddToClassList("msg__time"); row.Add(time);
            float startX = 0;
            row.RegisterCallback<PointerDownEvent>(e => startX = e.position.x);
            row.RegisterCallback<PointerUpEvent>(e =>
            {
                if (startX - e.position.x > 80) row.AddToClassList("msg-row--swiped");
            });
            return row;
        };
        _list.bindItem = (el, i) =>
        {
            var msg = _messages[i];
            el.Q<Label>("sender").text = msg.Sender;
            el.Q<Label>("preview").text = msg.Preview;
            el.Q<Label>("time").text = msg.TimeAgo;
            el.EnableInClassList("msg-row--unread", !msg.IsRead);
            el.Q(className: "msg__dot").EnableInClassList("msg__dot--read", msg.IsRead);
        };
        _list.itemsSource = _messages;
        int unread = _messages.Count(m => !m.IsRead);
        _badge.text = unread.ToString();
        _badge.parent.style.display = unread > 0 ? DisplayStyle.Flex : DisplayStyle.None;
    }
}
```

### Dragon Crashers Implementation — Composite Mail System

Dragon Crashers' mail system is significantly more sophisticated than the generic pattern above. It uses a **composite view** (parent managing 3 child views), **tabbed inbox/deleted switching**, **LINQ sorting**, and a **static event bus** for decoupled communication.

#### Composite View Architecture (`MailView`)

```csharp
// from Assets/Scripts/UI/UIViews/MailView.cs
// Parent view creates and manages 3 independent child views
public class MailView : UIView
{
    MailTabView m_MailTabView;
    MailboxView m_MailboxView;
    MailContentView m_MailContentView;

    public override void Initialize()
    {
        base.Initialize();

        // Each child view owns a section of the parent's UXML
        m_MailTabView = new MailTabView(m_TopElement.Q("mail__tabs-container"));
        m_MailboxView = new MailboxView(m_TopElement.Q("mail__mailbox-container"));
        m_MailContentView = new MailContentView(m_TopElement.Q("mail__content-container"));
    }

    public override void Dispose()
    {
        base.Dispose();
        m_MailboxView.Dispose();
        m_MailContentView.Dispose();
        m_MailTabView.Dispose();
    }
}
```

#### Controller: Inbox/Deleted Switching + LINQ Sort (`MailScreenController`)

```csharp
// from Assets/Scripts/UI/Controllers/MailScreenController.cs
List<MailMessageData> m_InboxMessages;
List<MailMessageData> m_DeletedMessages;

void OnInboxTabSelected()
{
    // Sort by date descending, fire event to update view
    var sorted = m_InboxMessages
        .OrderByDescending(m => m.date)
        .ToList();

    MailEvents.MailboxUpdated?.Invoke(sorted);
}

void OnDeletedTabSelected()
{
    var sorted = m_DeletedMessages
        .OrderByDescending(m => m.date)
        .ToList();

    MailEvents.MailboxUpdated?.Invoke(sorted);
}

void OnMailDeleted(MailMessageData message)
{
    // Move from inbox to deleted
    m_InboxMessages.Remove(message);
    m_DeletedMessages.Add(message);

    // Refresh the current tab
    MailEvents.MailboxUpdated?.Invoke(
        m_InboxMessages.OrderByDescending(m => m.date).ToList()
    );
}

void OnMailRead(MailMessageData message)
{
    message.isRead = true;
    // View will reflect read state on next refresh
}
```

#### Event Bus (`MailEvents`)

```csharp
// from Assets/Scripts/UI/Events/MailEvents.cs
// 11 static Action delegates for complete mail lifecycle
public static class MailEvents
{
    public static Action InboxTabSelected;       // tab switching
    public static Action DeletedTabSelected;
    public static Action<List<MailMessageData>> MailboxUpdated;  // list refresh
    public static Action<MailMessageData> MailSelected;          // detail view
    public static Action<MailMessageData> MailDeleted;           // CRUD
    public static Action<MailMessageData> MailUndeleted;
    public static Action<MailMessageData> MailRead;
    public static Action MailContentShown;       // UI state
    public static Action MailContentHidden;
    public static Action MailScreenShown;
    public static Action MailScreenHidden;
}
```

#### Event Flow: Tab Switch → Sort → Refresh

```
User clicks Inbox tab
    → MailTabView fires: MailEvents.InboxTabSelected?.Invoke()
        → MailScreenController.OnInboxTabSelected()
            → LINQ OrderByDescending(m => m.date)
                → MailEvents.MailboxUpdated?.Invoke(sortedList)
                    → MailboxView refreshes display
```

#### Event Flow: Delete Mail

```
User clicks Delete button on mail
    → MailContentView fires: MailEvents.MailDeleted?.Invoke(message)
        → MailScreenController.OnMailDeleted(message)
            → Remove from inbox list, add to deleted list
                → MailEvents.MailboxUpdated?.Invoke(updatedInbox)
                    → MailboxView refreshes display
```

> **Key insight**: Dragon Crashers splits what would be one monolithic mail view into 3 independent sub-views (`MailTabView`, `MailboxView`, `MailContentView`), each with its own responsibility. This is the **Composite View Pattern** — see Pattern 7 below for the generalized version.

---

## 6. Scroll View with Snap

Horizontal carousel with page snapping and indicator dots.

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
  <ui:VisualElement class="snap-carousel">
    <ui:ScrollView name="carousel-scroll" class="carousel__scroll"
                   mode="Horizontal" horizontal-scroller-visibility="Hidden"
                   vertical-scroller-visibility="Hidden"/>
    <ui:VisualElement name="carousel-dots" class="carousel__dots"/>
  </ui:VisualElement>
</ui:UXML>
```

```css
.carousel__scroll { flex-grow: 1; }
.carousel__scroll #unity-content-container { flex-direction: row; flex-wrap: nowrap; }
.carousel__page { width: 100%; flex-shrink: 0; align-items: center; justify-content: center; padding: 24px; }
.carousel__dots { flex-direction: row; justify-content: center; padding: 12px; }
.dot { width: 8px; height: 8px; border-radius: 4px; background-color: rgba(255,255,255,0.3); margin: 0 4px; transition: background-color 0.2s, scale 0.15s; }
.dot--active { background-color: #4FC3F7; scale: 1.3; }
```

```csharp
public class SnapCarouselController
{
    readonly ScrollView _scroll;
    readonly List<VisualElement> _dots = new();
    int _pageCount, _currentPage;

    public SnapCarouselController(VisualElement root, int pageCount)
    {
        _pageCount = pageCount;
        _scroll = root.Q<ScrollView>("carousel-scroll");
        var dotsContainer = root.Q("carousel-dots");
        for (int i = 0; i < pageCount; i++)
        {
            var page = new VisualElement(); page.AddToClassList("carousel__page");
            _scroll.contentContainer.Add(page);
            var dot = new VisualElement(); dot.AddToClassList("dot");
            int idx = i;
            dot.RegisterCallback<ClickEvent>(_ => SnapToPage(idx));
            dotsContainer.Add(dot); _dots.Add(dot);
        }
        _scroll.RegisterCallback<GeometryChangedEvent>(_ => SnapToPage(0));
        _scroll.horizontalScroller.valueChanged += v =>
        {
            float pw = _scroll.contentContainer.resolvedStyle.width / _pageCount;
            if (pw <= 0) return;
            int nearest = Mathf.Clamp(Mathf.RoundToInt(v / pw), 0, _pageCount - 1);
            if (nearest != _currentPage) UpdateDots(nearest);
        };
        UpdateDots(0);
    }

    public VisualElement GetPage(int i) => _scroll.contentContainer.ElementAt(i);

    public void SnapToPage(int index)
    {
        float pw = _scroll.contentContainer.resolvedStyle.width / _pageCount;
        _scroll.scrollOffset = new Vector2(pw * index, 0);
        UpdateDots(index);
    }

    void UpdateDots(int active)
    {
        _dots[_currentPage].RemoveFromClassList("dot--active");
        _currentPage = active;
        _dots[_currentPage].AddToClassList("dot--active");
    }
}
```

### Dragon Crashers Note

Dragon Crashers does not implement a snap carousel. However, `ShopView` and `InventoryView` both use `ScrollView` for item grids — see Pattern 2's Dragon Crashers section for the `ScrollView` + `VisualTreeAsset.Instantiate()` pattern. The generic snap carousel above can be combined with that instantiation pattern for a snapping item browser.

---

## 7. Async Task Animation Patterns

Dragon Crashers UIView classes are **non-MonoBehaviour** (plain C# inheriting `UIView`), so they use `async Task` instead of coroutines. Three distinct timing strategies emerge:

### Fire-and-Forget Pattern

All async UI animations use the discard pattern to avoid blocking callers:

```csharp
// Discard the Task — animation runs independently, caller continues
_ = ChatRoutine(chatData);           // ChatView
_ = HandleFundsUpdatedAsync(data);   // OptionsBarView
_ = UpdateLevelAsync(progress, 1f);  // LevelMeterView
_ = ClaimRewardRoutineAsync();       // MailContentView
```

> ⚠️ Fire-and-forget swallows exceptions. Wrap body in `try/catch` or use a central error handler.

### 7a. Typewriter Text — `Task.Delay(ms)`

Fixed-interval character reveal. Simplest pattern — good for chat bubbles and dialog text.

```csharp
// from Assets/Scripts/UI/UIViews/ChatView.cs
async Task TypewriterRoutine(Label label, string fullText)
{
    label.text = "";
    foreach (char c in fullText)
    {
        label.text += c;
        await Task.Delay(20);  // ~50 chars/sec
    }
}
```

### 7b. Counter Lerp — Frame-Synced `Task.Delay`

Smooth value interpolation synced to Unity's frame rate. Used for currency/score counters.

```csharp
// from Assets/Scripts/UI/UIViews/OptionsBarView.cs
async Task LerpCounterAsync(Label label, int startVal, int endVal, float duration)
{
    float elapsed = 0f;
    while (elapsed < duration)
    {
        elapsed += Time.deltaTime;
        float t = Mathf.Clamp01(elapsed / duration);
        int current = (int)Mathf.Lerp(startVal, endVal, t);
        label.text = current.ToString();
        await Task.Delay(TimeSpan.FromSeconds(Time.deltaTime));
    }
    label.text = endVal.ToString();  // ensure final value
}
```

### 7c. Progress Bar — `Stopwatch` + `Task.Yield`

Frame-independent timing via `System.Diagnostics.Stopwatch`. Most precise approach — immune to `Time.timeScale`.

```csharp
// from Assets/Scripts/UI/UIViews/LevelMeterView.cs
async Task UpdateLevelAsync(float targetProgress, float lerpTime)
{
    float startProgress = m_LevelProgress;
    var sw = new System.Diagnostics.Stopwatch();
    sw.Start();

    while (sw.Elapsed.TotalSeconds < lerpTime)
    {
        float t = (float)(sw.Elapsed.TotalSeconds / lerpTime);
        m_LevelProgress = Mathf.Lerp(startProgress, targetProgress, t);
        m_ProgressBar.style.width = new Length(m_LevelProgress * 100f, LengthUnit.Percent);
        await Task.Yield();  // resume next frame
    }

    m_LevelProgress = targetProgress;
    m_ProgressBar.style.width = new Length(m_LevelProgress * 100f, LengthUnit.Percent);
}
```

### Timing Strategy Decision

| Strategy | Timing | `Time.timeScale` | Best For |
|----------|--------|-------------------|----------|
| `Task.Delay(ms)` | Wall-clock fixed | Ignores | Typewriter, fixed-rate effects |
| `Task.Delay(TimeSpan.FromSeconds(Time.deltaTime))` | Frame-synced | Respects | Counter lerps, game-synced anims |
| `Stopwatch` + `Task.Yield()` | Wall-clock smooth | Ignores | Progress bars, precise transitions |

---

## 8. Experimental Animation API & Coordinate Conversion

### `experimental.animation.Position()` — Sliding Markers

Used to animate UI indicators (tab markers, active frames) to follow selection targets. Requires coordinate conversion between element spaces.

```csharp
// from Assets/Scripts/UI/UIViews/MenuBarView.cs
void AnimateMarkerToTarget(VisualElement targetElement, int durationMs = 200)
{
    // Convert target position through coordinate spaces
    Vector2 targetInWorldSpace = targetElement.parent.LocalToWorld(targetElement.layout.position);
    Vector3 targetInRootSpace = m_MenuMarker.parent.WorldToLocal(targetInWorldSpace);

    Vector3 offset = new Vector3(m_MenuMarker.resolvedStyle.width / 2f, 0, 0);
    m_MenuMarker.experimental.animation.Position(targetInRootSpace - offset, durationMs);
}
```

```csharp
// from Assets/Scripts/UI/UIViews/CharStatsView.cs — same pattern for skill icon marker
void AnimateFrameToSkillIcon(VisualElement targetIcon, int durationMs = 250)
{
    Vector2 worldPos = targetIcon.parent.LocalToWorld(targetIcon.layout.position);
    Vector3 rootPos = m_ActiveFrame.parent.WorldToLocal(worldPos);

    Vector3 offset = new Vector3(m_ActiveFrame.resolvedStyle.width / 2f, 0, 0);
    m_ActiveFrame.experimental.animation.Position(rootPos - offset, durationMs);
}
```

> **Coordinate flow**: `target.parent.LocalToWorld()` → absolute panel coords → `marker.parent.WorldToLocal()` → marker's local space. This two-step conversion is required when the marker and target have different parents.

### `experimental.animation.Scale()` — Pop-In Effects

Already covered in [Section 3 — InventoryView Scale Animation](#scale-animation-on-show-inventoryview). Summary:

```csharp
// from Assets/Scripts/UI/UIViews/InventoryView.cs
element.transform.scale = new Vector3(0.1f, 0.1f, 1f);  // start small
element.experimental.animation.Scale(1f, 200);            // animate to full
```

### Click Cooldown Guard

Prevents rapid-fire clicks from queueing multiple animations:

```csharp
// from Assets/Scripts/UI/UIViews/CharStatsView.cs
float m_TimeToNextClick = 0f;
const float k_ClickCooldown = 0.2f;

void OnSkillIconClicked(ClickEvent evt)
{
    if (Time.time < m_TimeToNextClick) return;
    m_TimeToNextClick = Time.time + k_ClickCooldown;

    // proceed with animation...
}
```

---

## 9. GeometryChangedEvent for Deferred Initialization

`layout.position` and `resolvedStyle` return zero until the element has been laid out. Use `GeometryChangedEvent` to run initialization that depends on resolved geometry.

```csharp
// from Assets/Scripts/UI/UIViews/MenuBarView.cs
public override void Initialize()
{
    base.Initialize();
    // Marker position depends on resolved layout — defer until geometry is ready
    m_MenuMarker.RegisterCallback<GeometryChangedEvent>(OnGeometryChangedEvent);
}

void OnGeometryChangedEvent(GeometryChangedEvent evt)
{
    // Unregister immediately — one-shot initialization
    m_MenuMarker.UnregisterCallback<GeometryChangedEvent>(OnGeometryChangedEvent);

    // Now safe to read layout.position and animate
    AnimateMarkerToTarget(m_DefaultTab);
}
```

```csharp
// from Assets/Scripts/UI/UIViews/CharStatsView.cs — same one-shot pattern
m_SkillIcons[0].RegisterCallback<GeometryChangedEvent>(InitializeSkillMarker);

void InitializeSkillMarker(GeometryChangedEvent evt)
{
    m_SkillIcons[0].UnregisterCallback<GeometryChangedEvent>(InitializeSkillMarker);
    AnimateFrameToSkillIcon(m_SkillIcons[0], durationMs: 0);  // instant position, no animation
}
```

**Pattern**: Register → fire once → unregister. Always unregister in the callback to avoid repeated initialization on window resize.

---

## 10. World-to-Panel Positioning

Attach UI elements to 3D world objects (health bars, name plates, damage numbers).

```csharp
// from Assets/Scripts/UI/Controllers/HealthBarController.cs
void UpdateHealthBarPosition(VisualElement element, Vector3 worldPosition, Vector2 worldSize)
{
    if (element.panel == null) return;

    // Convert 3D world position + size to panel-space rect
    Rect rect = RuntimePanelUtils.CameraTransformWorldToPanelRect(
        element.panel,
        worldPosition,
        worldSize,
        Camera.main
    );

    element.transform.position = rect.position;
    element.style.width = rect.width;
    element.style.height = rect.height;
}
```

> **Key API**: `RuntimePanelUtils.CameraTransformWorldToPanelRect()` handles camera projection + panel DPI scaling in one call. Must be called every frame (e.g., in `Update()` or via `schedule.Execute().Every(16)`). Check `element.panel != null` before use — panels are null when elements are detached.

---

## 11. Composite View Pattern (Parent + Child UIViews)

When a screen has distinct sub-regions (tabs panel, list panel, detail panel), Dragon Crashers splits them into separate `UIView`-derived classes. The **parent** view creates children by injecting container elements from its own UXML, then delegates lifecycle methods.

### MailView — 3 Child Views

```csharp
// from Assets/Scripts/UI/UIViews/MailView.cs
public class MailView : UIView
{
    MailTabView m_MailTabView;
    MailboxView m_MailboxView;
    MailContentView m_MailContentView;

    public override void Initialize()
    {
        base.Initialize();

        // Each child receives a container element from the parent's UXML
        m_MailTabView = new MailTabView(m_TopElement.Q("mail__tabs-container"));
        m_MailboxView = new MailboxView(m_TopElement.Q("mail__mailbox-container"));
        m_MailContentView = new MailContentView(m_TopElement.Q("mail__content-container"));
    }

    public override void Dispose()
    {
        base.Dispose();
        // Parent delegates disposal to all children
        m_MailboxView?.Dispose();
        m_MailContentView?.Dispose();
        m_MailTabView?.Dispose();
    }
}
```

### CharView — Embedded CharStatsView

```csharp
// from Assets/Scripts/UI/UIViews/CharView.cs
// CharView embeds CharStatsView as a child for the stats/skills/bio panel
CharStatsView m_CharStatsView;

public override void Initialize()
{
    base.Initialize();

    // Inject the stats container element into the child view
    m_CharStatsView = new CharStatsView(m_TopElement.Q("char__stats-container"));
}

public override void Dispose()
{
    base.Dispose();
    m_CharStatsView?.Dispose();
}
```

### Architecture Diagram

```
┌─ MailView (parent UIView) ─────────────────────────┐
│                                                     │
│  ┌─ MailTabView ─────┐  ┌─ MailboxView ──────────┐  │
│  │ mail__tabs-       │  │ mail__mailbox-          │  │
│  │ container         │  │ container               │  │
│  │                   │  │                         │  │
│  │ Inbox | Deleted   │  │ [message list]          │  │
│  └───────────────────┘  └─────────────────────────┘  │
│                                                     │
│  ┌─ MailContentView ─────────────────────────────┐  │
│  │ mail__content-container                        │  │
│  │                                                │  │
│  │ [selected message detail + actions]            │  │
│  └────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

### Generic Composite Template

```csharp
// Reusable composite pattern — apply to any multi-panel screen
public class CompositeScreenView : UIView
{
    ChildViewA m_ChildA;
    ChildViewB m_ChildB;

    public override void Initialize()
    {
        base.Initialize();
        // Rule 1: Inject containers, don't let children query the parent
        m_ChildA = new ChildViewA(m_TopElement.Q("panel-a-container"));
        m_ChildB = new ChildViewB(m_TopElement.Q("panel-b-container"));
    }

    public override void Show()
    {
        base.Show();
        // Rule 2: Parent delegates lifecycle — children don't self-activate
        m_ChildA.Show();
        m_ChildB.Show();
    }

    public override void Hide()
    {
        m_ChildA.Hide();
        m_ChildB.Hide();
        base.Hide();
    }

    public override void Dispose()
    {
        // Rule 3: Always null-check — child might fail initialization
        m_ChildA?.Dispose();
        m_ChildB?.Dispose();
        base.Dispose();
    }
}
```

**Key rules:**
1. **Container injection** — parent passes container elements via `Q()`, children never query the parent's UXML
2. **Lifecycle delegation** — parent calls `Show()`/`Hide()`/`Dispose()` on children; children don't self-manage visibility
3. **Flat composition** — avoid deep nesting (parent → child → grandchild); keep to 2 levels
4. **Null-check in Dispose** — children might fail initialization; always `?.Dispose()`

---

## 12. Category Filtering with LINQ (Shop Pattern)

Dragon Crashers' shop uses a **pre-cached filtering** strategy: LINQ queries run once at load time per category, and tab clicks select from pre-built lists.

### Controller: Pre-Cached Category Lists (`ShopScreenController`)

```csharp
// from Assets/Scripts/UI/Controllers/ShopScreenController.cs
List<ShopItemData> m_AllShopItems;
List<ShopItemData> m_GoldItems;
List<ShopItemData> m_GemItems;
List<ShopItemData> m_PotionItems;

void LoadShopData()
{
    // Pre-cache filtered + sorted lists at load time — no per-frame LINQ
    m_GoldItems = m_AllShopItems
        .Where(item => item.shopItemType == ShopItemType.Gold)
        .OrderBy(item => item.cost)
        .ToList();

    m_GemItems = m_AllShopItems
        .Where(item => item.shopItemType == ShopItemType.Gem)
        .OrderBy(item => item.cost)
        .ToList();

    m_PotionItems = m_AllShopItems
        .Where(item => item.shopItemType == ShopItemType.Potion)
        .OrderBy(item => item.cost)
        .ToList();

    // Default to gold tab
    ShopEvents.ShopUpdated?.Invoke(m_GoldItems);
}

// Tab click → fire pre-cached list
void OnGoldSelected() => ShopEvents.ShopUpdated?.Invoke(m_GoldItems);
void OnGemSelected() => ShopEvents.ShopUpdated?.Invoke(m_GemItems);
void OnPotionSelected() => ShopEvents.ShopUpdated?.Invoke(m_PotionItems);
```

### View: Rebuild Grid from Filtered List (`ShopView`)

```csharp
// from Assets/Scripts/UI/UIViews/ShopView.cs
VisualTreeAsset m_ShopItemAsset;
ScrollView m_ContentContainer;

void OnShopUpdated(List<ShopItemData> shopItems)
{
    // 1. Clear all existing items
    m_ContentContainer.Clear();

    // 2. Instantiate new items from template
    foreach (var shopItem in shopItems)
    {
        CreateShopItemElement(shopItem);
    }
}

void CreateShopItemElement(ShopItemData shopItemData)
{
    // Clone UXML template
    TemplateContainer shopItemElement = m_ShopItemAsset.Instantiate();

    // Create component wrapper + bind data + wire events
    ShopItemComponent shopItem = new ShopItemComponent(shopItemData);
    shopItem.SetVisualElements(shopItemElement);
    shopItem.SetGameData(shopItemElement);
    shopItem.RegisterButtonCallbacks();

    // Add to scroll container
    m_ContentContainer.Add(shopItemElement);
}
```

### Event Flow

```
Tab click (GoldTabButton)
    → ShopView.SelectGoldTab()
        → AudioManager.PlayDefaultButtonSound()
        → ShopEvents.GoldSelected?.Invoke()
            → ShopScreenController.OnGoldSelected()
                → ShopEvents.ShopUpdated?.Invoke(m_GoldItems)  // pre-cached
                    → ShopView.OnShopUpdated(goldItems)
                        → Clear() + foreach CreateShopItemElement()
```

### Event Bus (`ShopEvents`)

```csharp
// from Assets/Scripts/UI/Events/ShopEvents.cs
public static class ShopEvents
{
    public static Action GoldSelected;
    public static Action GemSelected;
    public static Action PotionSelected;
    public static Action<List<ShopItemData>> ShopUpdated;
    public static Action<ShopItemData> ShopItemSelected;
    public static Action<ShopItemData> ShopItemBought;
    public static Action ShopScreenShown;
    public static Action ShopScreenHidden;
    public static Action ShopOpened;
    public static Action ShopClosed;
    public static Action<ShopItemData> ShopItemClicked;
    public static Action<string> ShopMessageShown;
}
```

### Decision Guide: When to Use This Pattern

| Aspect | Pre-Cached (Dragon Crashers) | On-Demand LINQ |
|--------|------------------------------|----------------|
| **Data size** | < 200 items | Any size |
| **Filter complexity** | Simple Where + OrderBy | Complex multi-field queries |
| **Data mutability** | Mostly static | Frequently changing |
| **Memory** | Higher (N lists in memory) | Lower (one source list) |
| **CPU per tab click** | O(1) — list lookup | O(n) — LINQ re-evaluation |
| **Best for** | Shop categories, fixed sets | Inventory with dynamic filters |

---

## 13. Circular Navigation & Gear Slot Management

Dragon Crashers' character screen combines **circular index wrapping** for character selection with **gear slot management** that prevents equipment type duplicates.

### Circular Character Selection (`CharScreenController`)

```csharp
// from Assets/Scripts/UI/Controllers/CharScreenController.cs
int m_CurrentIndex;
List<CharacterData> m_CharacterDataList;

void SelectNextCharacter()
{
    m_CurrentIndex++;
    if (m_CurrentIndex >= m_CharacterDataList.Count)
        m_CurrentIndex = 0;  // wrap to first

    CharEvents.CharacterShown?.Invoke(m_CharacterDataList[m_CurrentIndex]);
}

void SelectLastCharacter()
{
    m_CurrentIndex--;
    if (m_CurrentIndex < 0)
        m_CurrentIndex = m_CharacterDataList.Count - 1;  // wrap to last

    CharEvents.CharacterShown?.Invoke(m_CharacterDataList[m_CurrentIndex]);
}
```

### Gear Equip with Duplicate Prevention (`CharScreenController`)

```csharp
// from Assets/Scripts/UI/Controllers/CharScreenController.cs
GearData[] m_EquippedGear = new GearData[4];  // 4 gear slots

void OnGearSelected(GearData gearData)
{
    // 1. Unequip any existing gear in the target slot
    int slotIndex = (int)gearData.gearSlot;
    if (m_EquippedGear[slotIndex] != null)
    {
        CharEvents.GearUnequipped?.Invoke(m_EquippedGear[slotIndex]);
    }

    // 2. Remove any OTHER slot with the same equipment type (prevents duplicates)
    RemoveGearType(gearData.equipmentType);

    // 3. Equip the new gear
    m_EquippedGear[slotIndex] = gearData;
    CharEvents.GearEquipped?.Invoke(gearData);
}

void RemoveGearType(EquipmentType equipmentType)
{
    for (int i = 0; i < m_EquippedGear.Length; i++)
    {
        if (m_EquippedGear[i] != null && m_EquippedGear[i].equipmentType == equipmentType)
        {
            CharEvents.GearUnequipped?.Invoke(m_EquippedGear[i]);
            m_EquippedGear[i] = null;
        }
    }
}

void OnGearUnequipped()
{
    // Unequip ALL slots
    for (int i = 0; i < m_EquippedGear.Length; i++)
    {
        if (m_EquippedGear[i] != null)
        {
            CharEvents.GearUnequipped?.Invoke(m_EquippedGear[i]);
            m_EquippedGear[i] = null;
        }
    }
}
```

### View: Gear Slot Visual Update (`CharView`)

```csharp
// from Assets/Scripts/UI/UIViews/CharView.cs
VisualElement[] m_GearSlots = new VisualElement[4];
VisualElement[] m_GearSlotSymbols = new VisualElement[4];

void OnGearSlotUpdated(GearData gearData, bool equipped)
{
    int slotIndex = (int)gearData.gearSlot;

    if (equipped)
    {
        // Show gear icon
        m_GearSlots[slotIndex].style.backgroundImage = new StyleBackground(gearData.icon);
        m_GearSlotSymbols[slotIndex].style.display = DisplayStyle.None;
    }
    else
    {
        // Show empty slot with type symbol
        m_GearSlots[slotIndex].style.backgroundImage = StyleKeyword.None;
        m_GearSlotSymbols[slotIndex].style.display = DisplayStyle.Flex;
    }
}
```

### Level-Up Button State Control (`CharView`)

Triple-state button control using CSS class + `SetEnabled()` + `pickingMode`:

```csharp
// from Assets/Scripts/UI/UIViews/CharView.cs
const string k_LevelUpButtonActiveClass = "levelup-button--active";
const string k_LevelUpButtonInactiveClass = "levelup-button--inactive";

void SetLevelUpButtonState(bool canLevelUp)
{
    if (canLevelUp)
    {
        m_LevelUpButton.RemoveFromClassList(k_LevelUpButtonInactiveClass);
        m_LevelUpButton.AddToClassList(k_LevelUpButtonActiveClass);
        m_LevelUpButton.SetEnabled(true);
        m_LevelUpButton.pickingMode = PickingMode.Position;  // clickable
    }
    else
    {
        m_LevelUpButton.RemoveFromClassList(k_LevelUpButtonActiveClass);
        m_LevelUpButton.AddToClassList(k_LevelUpButtonInactiveClass);
        m_LevelUpButton.SetEnabled(false);
        m_LevelUpButton.pickingMode = PickingMode.Ignore;  // not clickable
    }
}
```

> **Why triple-state?** `SetEnabled(false)` greys the button via `:disabled` pseudo-class but doesn't always prevent clicks in all Unity versions. `pickingMode = Ignore` is a belt-and-suspenders approach that guarantees no click events reach the element.

### Event Bus (`CharEvents`)

```csharp
// from Assets/Scripts/UI/Events/CharEvents.cs
// 18 static Action delegates — the largest event bus in Dragon Crashers
public static class CharEvents
{
    // Navigation
    public static Action NextCharacterSelected;
    public static Action LastCharacterSelected;
    public static Action<CharacterData> CharacterShown;

    // Gear management
    public static Action<GearData> GearSelected;
    public static Action<GearData> GearEquipped;
    public static Action<GearData> GearUnequipped;
    public static Action GearAllUnequipped;
    public static Action<GearData> GearAutoEquipped;
    public static Action AutoEquipToggled;

    // Level & progression
    public static Action LevelUpClicked;
    public static Action<CharacterData> LevelUpdated;
    public static Action<bool> LevelUpButtonEnabled;

    // Display
    public static Action<int> SkillSelected;
    public static Action StatsTabSelected;
    public static Action SkillsTabSelected;
    public static Action BioTabSelected;

    // Screen lifecycle
    public static Action CharScreenShown;
    public static Action CharScreenHidden;
}
```

### Event Flow: Character Navigation + Gear Equip

```
User clicks Next arrow
    → CharView fires: CharEvents.NextCharacterSelected?.Invoke()
        → CharScreenController.SelectNextCharacter()
            → m_CurrentIndex++ (wrap at Count → 0)
            → CharEvents.CharacterShown?.Invoke(characterData)
                → CharView updates portrait, name, stats
                → CharStatsView updates skill icons, bio

User clicks gear item in inventory
    → InventoryView fires: CharEvents.GearSelected?.Invoke(gearData)
        → CharScreenController.OnGearSelected(gearData)
            → Unequip existing slot → RemoveGearType (prevent duplicates)
            → m_EquippedGear[slot] = gearData
            → CharEvents.GearEquipped?.Invoke(gearData)
                → CharView.OnGearSlotUpdated(gearData, equipped: true)
                    → Show gear icon, hide empty symbol
```

---

## Quick Reference

| Pattern | Key Classes / API | Animation | DC Example |
|---------|-------------------|-----------|------------|
| Tabs | `tab-bar__tab--active`, indicator | `transition: translate` | `TabbedMenuController`, `ShopView` |
| Inventory | `item-card--selected`, ListView | `transition: scale` | `InventoryView` ScrollView + Instantiate |
| Modal | `--visible` class toggle | `translate + opacity` | `UIManager.ShowModalView()` |
| Buttons | `:hover/:active/:disabled`, `.btn--loading` | `transition: scale, bg-color` | `ShopView` tab toggle |
| Messages | `msg-row--unread/--swiped` | `translate + opacity` | `MailView` composite + `MailScreenController` |
| Carousel | `dot--active`, scrollOffset | programmatic snap | — (generic pattern) |
| Async Anims | `async Task`, `_ = Method()` | `Task.Delay`, `Stopwatch` | `ChatView`, `OptionsBarView`, `LevelMeterView` |
| Experimental API | `experimental.animation.Position/Scale` | C# programmatic | `MenuBarView`, `CharStatsView`, `InventoryView` |
| GeometryChanged | `GeometryChangedEvent`, one-shot init | deferred | `MenuBarView`, `CharStatsView` marker init |
| World-to-Panel | `RuntimePanelUtils.CameraTransformWorldToPanelRect` | per-frame update | `HealthBarController` |
| Composite View | Parent `UIView` + child `UIView`s via container injection | — | `MailView` → 3 children, `CharView` → `CharStatsView` |
| Category Filter | LINQ `Where/OrderBy`, pre-cached lists, `Clear()` + Instantiate | — | `ShopScreenController` + `ShopView` |
| Circular Nav | Index wrap, gear slot array, duplicate prevention | — | `CharScreenController` + `CharView` |

## Exercise: Notification Toast

Build a self-dismissing toast notification that slides in from the top:

1. Create `Toast.uxml` — overlay container with icon + message label + close button
2. Create `Toast.uss` — position absolute, top, translate-based slide animation, auto-fade via opacity
3. Create `ToastController.cs` — `Show(string msg, float duration)` adds toast, schedules `Hide()` after duration
4. Use element pooling (see [performance](../ui-toolkit-performance/SKILL.md)) to avoid GC from repeated toast creation

**Checklist**: ✅ Uses `translate` animation (no layout cost) · ✅ Auto-dismisses via `schedule.Execute().ExecuteLater()` · ✅ Pools toast elements · ✅ Accessible (min 44×44 close button)

## Related Skills

- [UI Toolkit Architecture](../ui-toolkit-architecture/SKILL.md) — UIView base class, event bus pattern, view lifecycle that underpins all patterns above
- [UI Toolkit Performance](../ui-toolkit-performance/SKILL.md) — animation cost comparison (USS transitions vs `experimental.animation` vs `async Task`), virtualization for large lists
- [UI Toolkit Mobile](../ui-toolkit-mobile/SKILL.md) — touch-specific patterns, safe area, and gesture handling

## Shared Resources

- [Code Templates](../references/code-templates.md) — boilerplate for new patterns
- [Dragon Crashers Insights](../references/dragon-crashers-insights.md) — production pattern examples
- [Performance Benchmarks](../references/performance-benchmarks.md) — animation and draw call targets
- [Official Docs Links](../references/official-docs-links.md) — Unity 6 documentation index

## Official Documentation

- [UI Toolkit Manual](https://docs.unity3d.com/6000.0/Documentation/Manual/UIElements.html)
- [USS Transitions](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-Transitions.html)
- [ListView](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-ListView.html)
- [Custom Controls](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-create-custom-controls.html)

---

**← Previous**: [Data Binding](../ui-toolkit-databinding/SKILL.md) | **Next →**: [Performance](../ui-toolkit-performance/SKILL.md)

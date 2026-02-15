---
name: ui-toolkit-architecture
description: "Component-based architecture for Unity UI Toolkit. Covers UXML/USS/C# separation, custom controls with [UxmlElement], reusable templates, MVC/MVP patterns, and scalable project structure. Use when: (1) Designing UI component hierarchies, (2) Creating reusable custom controls, (3) Implementing MVC/MVP for UI screens, (4) Structuring large-scale UI projects, (5) Building inventory, character, or menu systems. Triggers: 'UI architecture', 'custom control', 'UxmlElement', 'reusable component', 'UI MVC', 'component hierarchy'."

# UI Toolkit Architecture

Component-based design patterns for scalable, maintainable UI Toolkit projects.

## Core Principles

1. **Separation**: UXML (structure), USS (style), C# (behavior) — never cross
2. **Component isolation**: Each component owns its UXML, USS, and C# controller
3. **Data down, events up**: Parents pass data via properties/binding; children dispatch events
4. **Composition over inheritance**: Compose VisualElements, avoid deep class hierarchies

## Custom Controls with [UxmlElement]

Unity 6 uses `[UxmlElement]` (replaces `UxmlFactory`/`UxmlTraits`). Must use `partial class`.

```csharp
[UxmlElement]
public partial class StatBar : VisualElement
{
    public static readonly string ussClassName = "stat-bar";
    [UxmlAttribute] public string Label { get => _label?.text; set { if (_label != null) _label.text = value; } }
    [UxmlAttribute] public float Value { get => _value; set { _value = Mathf.Clamp01(value); UpdateFill(); } }
    float _value; Label _label; VisualElement _fill, _track;

    public StatBar()
    {
        AddToClassList(ussClassName);
        _label = new Label(); _label.AddToClassList($"{ussClassName}__label"); Add(_label);
        _track = new VisualElement(); _track.AddToClassList($"{ussClassName}__track"); Add(_track);
        _fill = new VisualElement(); _fill.AddToClassList($"{ussClassName}__fill"); _track.Add(_fill);
    }
    void UpdateFill() => _fill.style.scale = new Scale(new Vector3(_value, 1f, 1f));
}
// UXML: <StatBar label="Health" value="0.75" />
```

## UXML Template Composition

```xml
<!-- Components/Header.uxml -->
<ui:UXML xmlns:ui="UnityEngine.UIElements">
    <ui:VisualElement class="header">
        <ui:Button name="btn-back" class="btn-icon" />
        <ui:Label name="title" class="header__title" />
        <ui:Button name="btn-settings" class="btn-icon" />
    </ui:VisualElement>
</ui:UXML>

<!-- Screens/InventoryScreen.uxml — uses Template/Instance -->
<ui:UXML xmlns:ui="UnityEngine.UIElements">
    <ui:Template src="Components/Header.uxml" name="Header" />
    <ui:VisualElement class="screen">
        <ui:Instance template="Header" />
        <ui:ListView name="item-list" />
    </ui:VisualElement>
</ui:UXML>
```

## MVC Pattern

Controller (MonoBehaviour) queries View elements, listens to events, updates Model. Model (ScriptableObject) holds data. Events flow up via static event bus.

```csharp
[RequireComponent(typeof(UIDocument))]
public class InventoryScreenController : MonoBehaviour
{
    [SerializeField] InventoryDataSource _inventoryData;
    [SerializeField] VisualTreeAsset _itemTemplate;
    ListView _itemList;

    void OnEnable()
    {
        var root = GetComponent<UIDocument>().rootVisualElement;
        _itemList = root.Q<ListView>("item-list");  // Cache — never Q() per-frame
        _itemList.itemsSource = _inventoryData.Items;
        _itemList.fixedItemHeight = 64;
        _itemList.makeItem = () => _itemTemplate.Instantiate();
        _itemList.bindItem = (e, i) => e.Q<Label>("item-name").text = _inventoryData.Items[i].Name;
    }
}
```

## Dragon Crashers Architecture

> See [Architecture DC Patterns](references/architecture-dc-patterns.md) — UIView base class, HomeView, HomeScreenController, TabbedMenuController, HealthBarComponent, SlideToggle, BEM naming, Composite View, Dynamic UI Generation, Button.userData, UIManager navigation.

## Scaling Guidelines

| Size | Strategy |
|------|----------|
| Small (1-5 screens) | Single UIDocument, screen toggling |
| Medium (5-15) | UIDocument per screen, ScreenManager |
| Large (15+) | Module-based, lazy loading, screen pooling |

Large: group by module (Shop/, Inventory/, Social/), shared `Common/` folder, central `UIScreenManager`, lazy-load UXML on first access.

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| God Screen Controller (500+ lines) | Split into sub-controllers per panel |
| Inline styles in UXML | Always use USS classes |
| Deep inheritance chains | Composition with interfaces |
| Missing `partial` on [UxmlElement] | Source gen fails — always `partial class` |
| Q() in bindItem | Cache element refs in makeItem |
| No OnDisable cleanup | Unregister events in OnDisable |



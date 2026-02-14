---
name: ui-toolkit-architecture
description: "Component-based architecture for Unity UI Toolkit. Covers UXML/USS/C# separation, custom controls with [UxmlElement], reusable templates, MVC/MVP patterns, and scalable project structure. Use when: (1) Designing UI component hierarchies, (2) Creating reusable custom controls, (3) Implementing MVC/MVP for UI screens, (4) Structuring large-scale UI projects, (5) Building inventory, character, or menu systems. Triggers: 'UI architecture', 'custom control', 'UxmlElement', 'reusable component', 'UI MVC', 'component hierarchy'."
---

# UI Toolkit Architecture

<!-- OWNERSHIP: UIView base class, UIManager, event bus architecture, Controller+View MVC pattern, custom controls ([UxmlElement]/UxmlFactory), TabbedMenuController, template composition, Two UIDocument strategy. -->

Component-based design patterns for scalable, maintainable UI Toolkit projects.

> **Based on**: Unity 6 (6000.0), Dragon Crashers official sample, and production mobile game patterns.

## Core Architecture Principles

1. **Separation of concerns**: UXML (structure), USS (style), C# (behavior) — never cross boundaries
2. **Component isolation**: Each component owns its UXML template, USS styles, and C# controller
3. **Data flows down**: Parent passes data to children via properties or binding
4. **Events flow up**: Children dispatch events, parents listen and coordinate
5. **Composition over inheritance**: Prefer composing VisualElements over deep class hierarchies

## Component Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Screen (Full-screen view)                               │
│  ┌─────────────────────┐  ┌──────────────────────────┐  │
│  │  Header Component   │  │  Content Area            │  │
│  │  ┌───┐ ┌────┐ ┌──┐ │  │  ┌────────────────────┐  │  │
│  │  │←  │ │Title│ │⚙ │ │  │  │  Card Component    │  │  │
│  │  └───┘ └────┘ └──┘ │  │  │  ┌──────┐ ┌──────┐ │  │  │
│  └─────────────────────┘  │  │  │ Icon │ │ Text │ │  │  │
│  ┌─────────────────────┐  │  │  └──────┘ └──────┘ │  │  │
│  │  TabBar Component   │  │  └────────────────────┘  │  │
│  │  [Tab1][Tab2][Tab3] │  └──────────────────────────┘  │
│  └─────────────────────┘                                 │
└─────────────────────────────────────────────────────────┘
```

## Custom Controls with [UxmlElement]

Unity 6 uses `[UxmlElement]` attribute (replaces legacy `UxmlFactory`/`UxmlTraits`):

```csharp
[UxmlElement]
public partial class StatBar : VisualElement
{
    public static readonly string ussClassName = "stat-bar";

    [UxmlAttribute] public string Label { get => _label?.text; set { if (_label != null) _label.text = value; } }
    [UxmlAttribute] public float Value { get => _value; set { _value = Mathf.Clamp01(value); UpdateFill(); } }
    [UxmlAttribute] public Color BarColor { get; set; }

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
// UXML: <StatBar label="Health" value="0.75" bar-color="#FF4444" />
```

## UXML Template Composition

Break screens into reusable templates:

```xml
<!-- Components/Header.uxml -->
<ui:UXML xmlns:ui="UnityEngine.UIElements">
    <ui:VisualElement class="header">
        <ui:Button name="btn-back" class="btn-icon" />
        <ui:Label name="title" class="header__title" />
        <ui:Button name="btn-settings" class="btn-icon" />
    </ui:VisualElement>
</ui:UXML>

<!-- Screens/InventoryScreen.uxml -->
<ui:UXML xmlns:ui="UnityEngine.UIElements">
    <ui:Template src="Components/Header.uxml" name="Header" />
    <ui:VisualElement class="screen">
        <ui:Instance template="Header" />
        <ui:VisualElement class="content">
            <ui:ListView name="item-list" />
            <ui:VisualElement name="item-detail" class="detail-panel" />
        </ui:VisualElement>
    </ui:VisualElement>
</ui:UXML>
```

## MVC Pattern for UI Screens

```
Controller (MonoBehaviour)         View (UXML + USS)
  - Queries elements from View       - Layout structure
  - Listens to View events           - Visual styles
  - Updates Model / Refreshes View
       ↓                                ↑
    Model (ScriptableObject)    Events flow up
  - Data (items, selection)     via static event bus
```

```csharp
[RequireComponent(typeof(UIDocument))]
public class InventoryScreenController : MonoBehaviour
{
    [SerializeField] InventoryDataSource _inventoryData;
    [SerializeField] VisualTreeAsset _itemTemplate;

    ListView _itemList; Label _detailName, _detailDesc;

    void OnEnable()
    {
        var root = GetComponent<UIDocument>().rootVisualElement;
        _itemList = root.Q<ListView>("item-list");  // Cache queries — never Q() per-frame
        _detailName = root.Q("item-detail").Q<Label>("detail-name");

        _itemList.itemsSource = _inventoryData.Items;
        _itemList.fixedItemHeight = 64;
        _itemList.makeItem = () => _itemTemplate.Instantiate();
        _itemList.bindItem = (e, i) => e.Q<Label>("item-name").text = _inventoryData.Items[i].Name;
        _itemList.selectedIndicesChanged += OnItemSelected;
    }
}
```

## Dragon Crashers — Architecture in Practice

> **Full Dragon Crashers architecture patterns**: See [Architecture DC Patterns](references/architecture-dc-patterns.md) — covers UIView base class (Template Method), HomeView concrete view, HomeScreenController (thin coordinator), TabbedMenuController (reusable tabs), HealthBarComponent (deprecated UxmlFactory), SlideToggle (BaseField), BEM naming, Composite View (MailView), Dynamic UI Generation (ShopView), Button.userData patterns, UIManager single-document navigation.

## Scaling Guidelines

| Project Size | Screens | Strategy |
|-------------|---------|----------|
| Small (1-5) | HUD, menu, settings | Single UIDocument, screen toggling |
| Medium (5-15) | RPG menus, shop, inventory | UIDocument per screen, ScreenManager |
| Large (15+) | Full game UI | Module-based, lazy loading, screen pooling |

**For large projects:**
- Group related screens into modules (Shop, Inventory, Social)
- Each module has its own folder with UXML/USS/C#
- Shared components live in a `Common/` folder
- Use a central `UIScreenManager` for navigation
- Lazy-load screen UXML on first access

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| God Screen Controller | 500+ line controller | Split into sub-controllers per panel |
| Inline styles in UXML | Cannot theme, cascade, or override | Always use USS classes |
| Deep inheritance chains | Fragile, hard to modify | Composition with interfaces |
| Singleton UI references | Tight coupling, test-unfriendly | Dependency injection or events |
| Rebuilding entire UI on change | Expensive, flickers | Bind or update specific elements |
| Missing `partial` keyword on [UxmlElement] | Compile error — source gen fails | Always use `partial class` |
| Q() calls inside bindItem | Allocates per recycled item | Cache element refs in makeItem |
| Forgetting OnDisable cleanup | Memory leaks, stale callbacks | Unregister events in OnDisable |

## Related Skills

- **[ui-toolkit-patterns](../ui-toolkit-patterns/SKILL.md)** — Animation, transition, and interaction patterns (hover effects, USS transitions, click feedback)
- **[ui-toolkit-responsive](../ui-toolkit-responsive/SKILL.md)** — Responsive layout, flex-grow/shrink, media queries, safe area handling
- **[ui-toolkit-master](../ui-toolkit-master/SKILL.md)** — Top-level orchestrator skill for all UI Toolkit work

## Shared Resources

- [Dragon Crashers Insights](../references/dragon-crashers-insights.md) — architecture patterns from Unity's sample
- [QuizU Patterns](../references/quizu-patterns.md) — UIScreen stack navigation, EventRegistry, non-MonoBehaviour base class, Presenter pattern
- [Code Templates](../references/code-templates.md) — base screen, custom control, screen manager templates
- [Official Docs Links](../references/official-docs-links.md) — curated Unity 6 documentation

## Official Documentation

- [Custom Controls](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-create-custom-controls.html)
- [UxmlElement Attribute](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/UIElements.UxmlElementAttribute.html)
- [UXML Templates](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-reuse-uxml-files.html)
- [VisualElement](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-VisualTree.html)
- [Event System](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-Events.html)

**← Previous**: [ui-toolkit-master](../ui-toolkit-master/SKILL.md) | **Next →**: [ui-toolkit-responsive](../ui-toolkit-responsive/SKILL.md)

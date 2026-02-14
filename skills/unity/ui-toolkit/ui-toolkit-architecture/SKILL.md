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

Dragon Crashers separates concerns with a clear layered architecture. Below are **real code examples** from the project.

### UIView Base Class — Template Method Pattern

Every screen inherits from `UIView` (plain C# class, NOT MonoBehaviour):

```csharp
// from Assets/Scripts/UI/UIViews/UIView.cs
public class UIView : IDisposable
{
    protected bool m_HideOnAwake = true;
    protected bool m_IsOverlay;
    protected VisualElement m_TopElement;

    public UIView(VisualElement topElement)
    {
        m_TopElement = topElement ?? throw new ArgumentNullException(nameof(topElement));
        Initialize();
    }

    // Template Method: Hide → SetVisualElements (cache Q()) → RegisterButtonCallbacks (wire events)
    public virtual void Initialize()
    {
        if (m_HideOnAwake) Hide();
        SetVisualElements();
        RegisterButtonCallbacks();
    }

    protected virtual void SetVisualElements() { }
    protected virtual void RegisterButtonCallbacks() { }
    public virtual void Show() => m_TopElement.style.display = DisplayStyle.Flex;
    public virtual void Hide() => m_TopElement.style.display = DisplayStyle.None;
    public virtual void Dispose() { }
}
```

### Concrete View — HomeView

Views follow the UIView template: cache Q() calls in `SetVisualElements()`, register events in `RegisterButtonCallbacks()`, compose sub-views in constructor, unsubscribe in `Dispose()`. Views fire static events (e.g., `HomeEvents.PlayButtonClicked?.Invoke()`) — never contain business logic.

> Full code: [Dragon Crashers Insights](../references/dragon-crashers-insights.md) (section: Architecture Components)

### Screen Controller — Thin Coordinator

Controllers are MonoBehaviours that coordinate between game systems and UI via static events:

```csharp
// from Assets/Scripts/UI/Controllers/HomeScreenController.cs
public class HomeScreenController : MonoBehaviour
{
    [SerializeField] LevelSO m_LevelData;

    void OnEnable() => HomeEvents.PlayButtonClicked += OnPlayGameLevel;
    void OnDisable() => HomeEvents.PlayButtonClicked -= OnPlayGameLevel;
    void Start() => HomeEvents.LevelInfoShown?.Invoke(m_LevelData);

    public void OnPlayGameLevel()
    {
        HomeEvents.MainMenuExited?.Invoke();
        SceneManager.LoadSceneAsync(m_LevelData.sceneName);
    }
}
```

**Key separation**: Controller knows `LevelSO` + `SceneManager`. View knows `VisualElement` + `Label`. They communicate only through `HomeEvents` static events.

### Reusable Sub-Controller — TabbedMenuController

A configurable tabbed menu system as plain C# (not MonoBehaviour), reusable across multiple screens:

```csharp
// Config struct — maps tab elements to content panels by naming convention
[System.Serializable]
public struct TabbedMenuIDs
{
    public string tabClassName;              // USS class for tabs (e.g., "chartab")
    public string selectedTabClassName;      // USS class for active tab
    public string unselectedContentClassName;// USS class to hide content
    public string tabNameSuffix;             // e.g., "-chartab"
    public string contentNameSuffix;         // e.g., "-content"
}

// from Assets/Scripts/UI/Controllers/TabbedMenuController.cs
public class TabbedMenuController
{
    readonly VisualElement m_Root;
    readonly TabbedMenuIDs m_IDs;

    public TabbedMenuController(VisualElement root, TabbedMenuIDs ids) { m_Root = root; m_IDs = ids; }

    public void RegisterTabCallbacks() =>
        m_Root.Query<VisualElement>(className: m_IDs.tabClassName).ForEach(t => t.RegisterCallback<ClickEvent>(OnTabClick));

    void OnTabClick(ClickEvent evt)
    {
        var clicked = evt.currentTarget as VisualElement;
        if (clicked.ClassListContains(m_IDs.selectedTabClassName)) return;
        // Deselect all, select clicked — CSS class toggling drives ALL visual state
        m_Root.Query<VisualElement>(className: m_IDs.tabClassName)
            .Where(t => t != clicked && t.ClassListContains(m_IDs.selectedTabClassName))
            .ForEach(t => { t.RemoveFromClassList(m_IDs.selectedTabClassName);
                            m_Root.Q(t.name.Replace(m_IDs.tabNameSuffix, m_IDs.contentNameSuffix))
                                  .AddToClassList(m_IDs.unselectedContentClassName); });
        clicked.AddToClassList(m_IDs.selectedTabClassName);
        m_Root.Q(clicked.name.Replace(m_IDs.tabNameSuffix, m_IDs.contentNameSuffix))
              .RemoveFromClassList(m_IDs.unselectedContentClassName);
    }
}
```

**Key design:** Tab ↔ content mapping is convention-based (suffix replacement). Same controller serves Mail, Char, Shop screens by changing `TabbedMenuIDs` in Inspector. A `TabbedMenu` MonoBehaviour wires this to a `UIDocument` element.

### Custom Controls — HealthBarComponent (⚠️ Deprecated UxmlFactory Pattern)

Dragon Crashers uses the **pre-2023.2 `UxmlFactory`/`UxmlTraits` pattern**. This is deprecated in Unity 6.

```csharp
// from Assets/Scripts/UI/Components/HealthBarComponent.cs
public class HealthBarComponent : VisualElement
{
    // ⚠️ DEPRECATED — replace with [UxmlElement] + [UxmlAttribute] in Unity 6
    public new class UxmlFactory : UxmlFactory<HealthBarComponent, UxmlTraits> { }
    public new class UxmlTraits : VisualElement.UxmlTraits
    {
        readonly UxmlIntAttributeDescription _currentHealth = new() { name = "currentHealth", defaultValue = 0 };
        readonly UxmlIntAttributeDescription _maximumHealth = new() { name = "MaximumHealth", defaultValue = 100 };
        readonly UxmlStringAttributeDescription _healthBarTitle = new() { name = "HealthBarTitle" };

        public override void Init(VisualElement ve, IUxmlAttributes bag, CreationContext cc)
        {
            base.Init(ve, bag, cc);
            var hb = (HealthBarComponent)ve;
            hb.CurrentHealth = _currentHealth.GetValueFromBag(bag, cc);
            hb.MaximumHealth = _maximumHealth.GetValueFromBag(bag, cc);
            hb.HealthBarTitle = _healthBarTitle.GetValueFromBag(bag, cc);
        }
    }

    private int _currentHealth, _maximumHealth;
    private readonly Label _titleLabel, _healthStat;
    private VisualElement _progress;

    // Constructor builds visual tree programmatically with BEM class names
    public HealthBarComponent()
    {
        AddToClassList("health-bar__container");
        var titleBg = new VisualElement(); titleBg.AddToClassList("health-bar__title_background"); Add(titleBg);
        _titleLabel = new Label(); _titleLabel.AddToClassList("health-bar__title"); titleBg.Add(_titleLabel);
        var bg = new VisualElement(); bg.AddToClassList("health-bar__background"); Add(bg);
        _progress = new VisualElement(); _progress.AddToClassList("health-bar__progress"); bg.Add(_progress);
        _healthStat = new Label(); _healthStat.AddToClassList("health-bar__label"); _progress.Add(_healthStat);
    }

    private void SetHealth(int cur, int max) {
        _healthStat.text = $"{cur}/{max}";
        if (max > 0) _progress.style.width = new StyleLength(Length.Percent(Mathf.Clamp((float)cur / max * 100, 0f, 100f)));
    }
}
```

**✅ Modern equivalent:** Add `[UxmlElement]`, make class `partial`, replace `UxmlFactory`/`UxmlTraits` with `[UxmlAttribute]` on properties. Constructor code stays identical.

### Custom Controls — SlideToggle (⚠️ Deprecated + BaseField)

SlideToggle derives from `BaseField<bool>` instead of `VisualElement` for automatic `ChangeEvent<bool>`, label support, and data binding:

```csharp
// from Assets/Scripts/UI/Components/SlideToggle.cs (namespace: MyUILibrary)
public class SlideToggle : BaseField<bool>
{
    public new class UxmlFactory : UxmlFactory<SlideToggle, UxmlTraits> { }   // ⚠️ DEPRECATED
    public new class UxmlTraits : BaseFieldTraits<bool, UxmlBoolAttributeDescription> { }

    public static readonly new string ussClassName = "slide-toggle";
    public static readonly string inputKnobUssClassName = "slide-toggle__input-knob";
    public static readonly string inputCheckedUssClassName = "slide-toggle__input--checked";

    VisualElement m_Input, m_Knob;

    public SlideToggle(string label = null) : base(label, null)
    {
        AddToClassList(ussClassName);
        m_Input = this.Q(className: BaseField<bool>.inputUssClassName);
        m_Knob = new(); m_Knob.AddToClassList(inputKnobUssClassName); m_Input.Add(m_Knob);

        // Three input methods: click, keyboard, gamepad
        RegisterCallback<ClickEvent>(evt => { ToggleValue(); evt.StopPropagation(); });
        RegisterCallback<KeyDownEvent>(evt => OnKeydownEvent(evt));
        RegisterCallback<NavigationSubmitEvent>(evt => OnSubmit(evt));
    }

    void ToggleValue() => value = !value;

    // BaseField<bool> calls this on value change — toggle CSS class
    public override void SetValueWithoutNotify(bool newValue)
    {
        base.SetValueWithoutNotify(newValue);
        m_Input.EnableInClassList(inputCheckedUssClassName, newValue);
    }
}
```

**Why `BaseField<bool>`:** Auto `ChangeEvent<bool>` dispatch, built-in label, `INotifyValueChanged<bool>` for data binding, `SerializedProperty` compatible.

### BEM Naming Convention

Dragon Crashers uses BEM (Block__Element--Modifier): `.health-bar__container`, `.health-bar__progress`, `.slide-toggle__input--checked`. Tab state: `.selected-tab` / `.unselected-content { display: none; }`.

### Composite View Pattern — MailView

Parent views own and manage sub-view lifecycles: query containers in `SetVisualElements()`, create sub-views in `Initialize()` AFTER base completes, cascade `Dispose()` to children. Example: `MailView` creates `MailTabView`, `MailboxView`, `MailContentView` from their respective container elements.

> Full code: [Dragon Crashers Insights](../references/dragon-crashers-insights.md) (section: Architecture Components)

### Dynamic UI Generation — VisualTreeAsset.Instantiate()

Dragon Crashers generates shop items dynamically from a template instead of using ListView:

```csharp
// from Assets/Scripts/UI/UIViews/ShopView.cs
public class ShopView : UIView
{
    VisualTreeAsset m_ShopItemAsset;  // loaded via Resources.Load<VisualTreeAsset>("ShopItem")

    public void OnShopUpdated(List<ShopItemSO> shopItems)
    {
        m_ShopScrollView.Clear();  // remove all existing items
        foreach (ShopItemSO item in shopItems) CreateShopItemElement(item, m_ShopScrollView);
    }

    void CreateShopItemElement(ShopItemSO data, VisualElement parent)
    {
        TemplateContainer elem = m_ShopItemAsset.Instantiate();  // 1. Clone template
        var controller = new ShopItemComponent(m_GameIconsData, data); // 2. Create controller
        controller.SetVisualElements(elem);  // 3. Query + populate
        controller.SetGameData(elem);
        controller.RegisterCallbacks();
        parent.Add(elem);  // 4. Add to parent
    }
}
```

**When to use:** `VisualTreeAsset.Instantiate()` for small lists (<50), complex interactions, varying sizes. `ListView` with virtualization for large lists (100+), uniform height, scroll performance.

### Button.userData + StopImmediatePropagation Patterns

`ShopItemComponent` demonstrates two important patterns:

```csharp
// from Assets/Scripts/UI/Components/ShopItemComponent.cs
public void RegisterCallbacks()
{
    m_BuyButton.userData = m_ShopItemData;  // Store SO reference — no closures needed
    m_BuyButton.RegisterCallback<ClickEvent>(BuyAction);
    m_BuyButton.RegisterCallback<PointerMoveEvent>(evt => evt.StopImmediatePropagation()); // Prevent ScrollView drag
}

void BuyAction(ClickEvent evt)
{
    ShopItemSO data = (evt.currentTarget as VisualElement).userData as ShopItemSO;  // Retrieve without closure
    ShopEvents.ShopItemClicked?.Invoke(data, screenPos);
}
```

- **`userData`**: Avoids allocation per item, works with recycled elements, no captured variable staleness
- **`StopImmediatePropagation()`**: Prevents `PointerMoveEvent` from reaching parent ScrollView (which would interpret as drag). Use on any interactive element inside ScrollView.

### UIManager — Single-Document Navigation

All screens exist in one UXML document — views are subtrees shown/hidden via `DisplayStyle`:

```csharp
// from Assets/Scripts/UI/UIViews/UIManager.cs
[RequireComponent(typeof(UIDocument))]
public class UIManager : MonoBehaviour
{
    UIView m_CurrentView, m_PreviousView;
    List<UIView> m_AllViews = new List<UIView>();

    void SetupViews()
    {
        var root = m_MainMenuDocument.rootVisualElement;
        m_HomeView = new HomeView(root.Q<VisualElement>("HomeScreen"));
        m_ShopView = new ShopView(root.Q<VisualElement>("ShopScreen"));
        m_MailView = new MailView(root.Q<VisualElement>("MailScreen"));
        // all views added to m_AllViews for lifecycle management
    }

    void ShowModalView(UIView newView)  // Modal: replace current view
    {
        m_CurrentView?.Hide();
        m_PreviousView = m_CurrentView;
        m_CurrentView = newView;
        m_CurrentView?.Show();
    }

    void OnSettingsScreenShown()  // Overlay: stack on top, restore on close
    {
        m_PreviousView = m_CurrentView;
        m_SettingsView.Show();  // doesn't hide current
    }

    void OnDisable() { foreach (var v in m_AllViews) v.Dispose(); }
}
```

**Patterns:** Single UIDocument with subtree views. Modal replaces current; overlay stacks. `m_AllViews` ensures centralized lifecycle disposal.

> **DC source file listing**: [Dragon Crashers Insights](../references/dragon-crashers-insights.md) (section: DC Source Files Reference)

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

# Project Architecture Patterns — UI Toolkit

> **PURPOSE**: Documents the 16 architectural patterns found in Dragon Crashers — what the DC project actually does.
> For **ready-to-copy templates** for your own projects (Unity 6+ APIs), see [code-templates.md](code-templates.md).

16 production-grade patterns from Dragon Crashers (idle RPG) + 7 patterns from QuizU (quiz app). Each includes source file, code example, and when to use it.

> **Two reference projects**: Dragon Crashers (DC) patterns #1–16 below. QuizU patterns in [quizu-patterns.md](quizu-patterns.md) — single UIDocument + stack navigation, EventRegistry, Presenter pattern.
> See the comparison table in quizu-patterns.md for architectural differences.

---

## 1. Event Bus (Static Action Delegates)

**Source**: `Assets/Scripts/UI/Events/` (10 event classes)

All inter-module communication uses static `System.Action` delegates — no UnityEvents, no C# events with custom EventArgs.

```csharp
// CharEvents.cs
public static class CharEvents
{
    public static Action CharScreenShown;
    public static Action<CharacterData> CharSelected;
    public static Action<int> GoldUpdated;
}
```

**When to use**: Any cross-module communication (UI ↔ gameplay, view ↔ controller, screen ↔ screen).

**Event classes**: `CharEvents`, `ShopEvents`, `HomeEvents`, `MailEvents`, `InventoryEvents`, `SettingsEvents`, `GameplayEvents`, `MainMenuUIEvents`, `MediaQueryEvents`, `ThemeEvents`

---

## 2. MVC-like Architecture (Controller + View + ScriptableObject)

**Source**: All `Controllers/` and `UIViews/` files

Controllers are `MonoBehaviour`s that own the lifecycle. Views are plain C# classes (not MonoBehaviours) that manage UI elements.

```csharp
// Controller (MonoBehaviour, in scene)
public class HomeScreenController : MonoBehaviour
{
    [SerializeField] UIDocument m_Document;
    HomeView m_HomeView;

    void OnEnable()
    {
        m_HomeView = new HomeView(m_Document.rootVisualElement);
        HomeEvents.HomeScreenShown?.Invoke();
    }

    void OnDisable()
    {
        m_HomeView.Dispose();
    }
}

// View (plain C# class)
public class HomeView
{
    VisualElement m_Root;
    Label m_GoldLabel;

    public HomeView(VisualElement root)
    {
        m_Root = root;
        m_GoldLabel = root.Q<Label>("home-gold-label");
        CharEvents.GoldUpdated += OnGoldUpdated;
    }

    void OnGoldUpdated(int gold) => m_GoldLabel.text = gold.ToString();

    public void Dispose()
    {
        CharEvents.GoldUpdated -= OnGoldUpdated;
    }
}
```

**When to use**: Every screen in the game. Controller handles lifecycle + data loading. View handles UI element manipulation.

---

## 3. Two UIDocument Strategy

**Source**: `HomeScreenController.cs`, `HealthBarController.cs`

Menu screens share a single `UIDocument`. Gameplay HUD elements (e.g., health bars) get separate `UIDocument` instances.

```
Scene Hierarchy:
├── MainMenuUIManager (UIDocument for all menu screens)
│   ├── HomeScreenController
│   ├── ShopScreenController
│   └── SettingsScreenController
└── HealthBar (separate UIDocument per gameplay element)
```

**When to use**: Separate UIDocuments when gameplay UI must overlay independently or use different PanelSettings (e.g., world-space vs screen-space).

---

## 4. Compound Theming ("{Orientation}--{Season}")

**Source**: `ThemeManager.cs`, `SettingsScreenController.cs`

Theme names combine orientation and season with `--` delimiter. 7 TSS files form an inheritance chain.

```csharp
// SettingsScreenController.cs
string themeName = m_MediaAspectRatio.ToString() + "--" + m_SettingsData.theme;
// Result: "Landscape--Halloween", "Portrait--Default", etc.

// ThemeManager.cs
public void SetTheme(string themeName)
{
    var settings = m_ThemeSettings.Find(x => x.theme == themeName);
    m_Document.panelSettings = settings.panelSettings;
    m_Document.panelSettings.themeStyleSheet = settings.tss;
}
```

**TSS hierarchy**: `Default.tss` → `{Orientation}.tss` → `{Orientation}--{Season}.tss`

**When to use**: Projects needing both responsive (orientation) and aesthetic (theme/season) styling simultaneously.

---

## 5. Custom Controls (UxmlFactory / UxmlTraits) — Legacy Pattern

**Source**: `SlideToggle.cs`, `HealthBarComponent.cs`

> ⚠️ **Legacy API**: Dragon Crashers uses the pre-Unity 6 `UxmlFactory`/`UxmlTraits` pattern shown below.
> For **Unity 6+ projects**, prefer the `[UxmlElement]`/`[UxmlAttribute]` attribute-based API — see [code-templates.md → Custom Control Template](code-templates.md#custom-control-template).

Project uses the pre-Unity 6 pattern with `UxmlFactory` and `UxmlTraits` (not `[UxmlElement]`).

```csharp
// SlideToggle.cs — custom toggle extending BaseField<bool>
public class SlideToggle : BaseField<bool>
{
    public new class UxmlFactory : UxmlFactory<SlideToggle, UxmlTraits> { }
    public new class UxmlTraits : BaseFieldTraits<bool, UxmlBoolAttributeDescription>
    {
        public override void Init(VisualElement ve, IUxmlAttributes bag, CreationContext cc)
        {
            base.Init(ve, bag, cc);
            // Custom attribute initialization
        }
    }
    // ...
}
```

**When to use**: Reusable UI components that need UXML support in the UI Builder.

---

## 6. Async/Await in Views (Fire-and-Forget)

**Source**: `OptionsBarView.cs`, `ChatView.cs`, `MailView.cs`

Views use `async Task` methods for animations. Fire-and-forget via `_ = MethodAsync()`.

```csharp
// OptionsBarView.cs
public void ShowOptionsBar()
{
    _ = ShowOptionsBarTask(); // Fire-and-forget
}

async Task ShowOptionsBarTask()
{
    m_OptionsBarElement.style.display = DisplayStyle.Flex;
    await Task.Delay(10);
    m_OptionsBarElement.AddToClassList(k_OptionsBarActiveClass);
    await Task.Delay(300); // Wait for CSS transition
}
```

**Three async timing approaches in this project**:

| Approach | Use Case | Source |
|----------|----------|--------|
| `Task.Delay(ms)` | Fixed delay (CSS transition timing) | `OptionsBarView` |
| `Task.Delay(TimeSpan.FromSeconds(Time.deltaTime))` | Frame-synced delay | `ChatView` |
| `Task.Yield()` + `Stopwatch` | Smooth frame-independent animation | `HomeView` |

**When to use**: UI animations in non-MonoBehaviour views where coroutines aren't available.

---

## 7. Composite View Pattern (Sub-View Management)

**Source**: `MailView.cs`

A parent view manages the lifecycle of multiple child views, delegating setup and disposal.

```csharp
// MailView.cs
public class MailView
{
    MailboxView m_MailboxView;
    MailContentView m_MailContentView;
    MailRewardView m_MailRewardView;

    public MailView(VisualElement root)
    {
        m_MailboxView = new MailboxView(root);
        m_MailContentView = new MailContentView(root);
        m_MailRewardView = new MailRewardView(root);
    }

    public void Dispose()
    {
        m_MailboxView.Dispose();
        m_MailContentView.Dispose();
        m_MailRewardView.Dispose();
    }
}
```

**When to use**: Complex screens with logically distinct UI regions that share a root VisualElement.

---

## 8. Dynamic UI Generation (VisualTreeAsset.Instantiate)

**Source**: `InventoryView.cs`, `ShopView.cs`

For lists under ~20 items, the project uses `VisualTreeAsset.Instantiate()` rather than `ListView`.

```csharp
// ShopView.cs
void FillShopItems(List<ShopItemSO> items, VisualTreeAsset template, VisualElement container)
{
    container.Clear();
    foreach (var item in items)
    {
        VisualElement shopItem = template.Instantiate();
        shopItem.Q<Label>("shop-item__title").text = item.itemName;
        shopItem.Q<Label>("shop-item__cost").text = item.cost.ToString();
        container.Add(shopItem);
    }
}
```

**When to use**: Small lists (<20 items). For larger lists, prefer `ListView` with virtualization.

---

## 9. World-to-Panel Coordinate Conversion

**Source**: `PositionToVisualElement.cs`, `HealthBarController.cs`

Align UI elements to 3D world objects using `RuntimePanelUtils`.

```csharp
// PositionToVisualElement.cs
public class PositionToVisualElement : MonoBehaviour
{
    void LateUpdate()
    {
        Rect rect = RuntimePanelUtils.CameraTransformWorldToPanelRect(
            m_Panel, m_WorldTransform.position, m_WorldSize, m_Camera);

        m_TargetElement.style.left = rect.x;
        m_TargetElement.style.top = rect.y;
        m_TargetElement.style.width = rect.width;
        m_TargetElement.style.height = rect.height;
    }
}
```

**When to use**: Health bars, name tags, damage numbers — any UI that tracks a 3D object.

---

## 10. CSS Class Toggling for State Management

**Source**: Most view files

UI state transitions use CSS class toggling rather than direct style property changes.

```csharp
// Tab selection
m_TabElements[i].AddToClassList("tab--active");
m_TabElements[prevIndex].RemoveToClassList("tab--active");

// Screen transitions
m_ScreenElement.AddToClassList("screen--visible");
m_ScreenElement.RemoveToClassList("screen--hidden");

// Toggle with EnableInClassList
m_Element.EnableInClassList("item--selected", isSelected);
```

**When to use**: Any visual state change. Keeps styling in USS, logic in C#.

---

## 11. experimental.animation API

**Source**: `OptionsBarView.cs`, `HomeView.cs`

Position and scale tweening using the experimental animation API.

```csharp
// OptionsBarView.cs — position animation
m_Element.experimental.animation
    .Start(new Vector2(0, 100), Vector2.zero, 300)
    .Ease(Easing.OutQuad)
    .OnValueChanged(v => m_Element.style.translate = new Translate(v.x, v.y));

// HomeView.cs — scale animation
m_Element.experimental.animation
    .Start(0f, 1f, 200)
    .OnValueChanged(v => m_Element.style.scale = new Scale(new Vector3(v, v, 1)));
```

**When to use**: Simple tweens where DOTween or USS transitions aren't suitable. Good for programmatic one-shot animations.

---

## 12. GeometryChangedEvent (Deferred Initialization)

**Source**: `HomeView.cs`, `MailView.cs`

Run layout-dependent logic after the visual tree is fully laid out.

```csharp
m_ScrollView.RegisterCallback<GeometryChangedEvent>(OnGeometryChanged);

void OnGeometryChanged(GeometryChangedEvent evt)
{
    m_ScrollView.UnregisterCallback<GeometryChangedEvent>(OnGeometryChanged);
    // Safe to read layout properties now
    float scrollHeight = m_ScrollView.resolvedStyle.height;
}
```

**When to use**: One-time initialization that depends on resolved layout values (element size, position).

---

## 13. Button.userData for Data Storage

**Source**: `ShopView.cs`, `CharView.cs`

Store `ScriptableObject` references on buttons using the `userData` property.

```csharp
// Store data
button.userData = shopItemSO;

// Retrieve on click
void OnShopItemClicked(ClickEvent evt)
{
    var button = evt.currentTarget as Button;
    var itemData = button.userData as ShopItemSO;
    ShopEvents.ShopItemSelected?.Invoke(itemData);
}
```

**When to use**: Dynamic lists where each button maps to a data object. Avoids closures and lambda captures.

---

## 14. StopImmediatePropagation

**Source**: `ShopItemComponent.cs`

Prevent parent `ScrollView` from capturing drag events meant for child interactive elements.

```csharp
m_ChildElement.RegisterCallback<PointerDownEvent>(evt =>
{
    evt.StopImmediatePropagation();
    // Handle child-specific interaction
}, TrickleDown.TrickleDown);
```

**When to use**: Interactive elements inside `ScrollView` where drag conflicts occur.

---

## 15. SafeAreaBorder (borderWidth Approach)

**Source**: `SafeAreaBorder.cs`, `Assets/Scripts/Utilities/`

Uses `borderWidth` (not `padding`) to apply safe area insets. This preserves the content layout area.

```csharp
// SafeAreaBorder.cs
void ApplySafeArea()
{
    Rect safeArea = Screen.safeArea;
    float left = safeArea.x / Screen.width * m_PanelWidth;
    float right = (Screen.width - safeArea.xMax) / Screen.width * m_PanelWidth;
    float top = (Screen.height - safeArea.yMax) / Screen.height * m_PanelHeight;
    float bottom = safeArea.y / Screen.height * m_PanelHeight;

    m_Root.style.borderLeftWidth = left;
    m_Root.style.borderRightWidth = right;
    m_Root.style.borderTopWidth = top;
    m_Root.style.borderBottomWidth = bottom;
    m_Root.style.borderBottomColor = Color.clear; // Invisible borders
}
```

**When to use**: Any mobile UI that needs notch/punch-hole avoidance. The borderWidth approach is superior to padding because it doesn't affect child element positioning calculations.

---

## 16. PositionToVisualElement (3D-to-UI Alignment)

**Source**: `PositionToVisualElement.cs`

Aligns a 3D GameObject's position to a UI Toolkit `VisualElement` — for cases where UI drives the position of world objects (inverse of pattern #9).

```csharp
// PositionToVisualElement.cs
void UpdatePosition()
{
    Vector2 panelPos = new Vector2(
        m_TargetElement.resolvedStyle.left + m_TargetElement.resolvedStyle.width / 2,
        m_TargetElement.resolvedStyle.top + m_TargetElement.resolvedStyle.height / 2);

    Vector2 screenPos = RuntimePanelUtils.ScreenToPanel(m_Panel, panelPos);
    Vector3 worldPos = m_Camera.ScreenToWorldPoint(new Vector3(screenPos.x, screenPos.y, m_Depth));
    transform.position = worldPos;
}
```

**When to use**: Particle effects, 3D decorations, or character models that should align with UI element positions.

---

## Pattern Selection Guide

| Need | Pattern | # |
|------|---------|---|
| Cross-module communication | Event Bus | 1 |
| Screen lifecycle management | MVC-like | 2 |
| Overlapping UI layers | Two UIDocument | 3 |
| Orientation + theme support | Compound Theming | 4 |
| Reusable UXML components | Custom Controls | 5 |
| Animation in non-MonoBehaviour | Async/Await | 6 |
| Complex screen with regions | Composite View | 7 |
| Small dynamic lists | VisualTreeAsset.Instantiate | 8 |
| UI tracking 3D objects | World-to-Panel | 9 |
| Visual state transitions | CSS Class Toggling | 10 |
| Programmatic tweens | experimental.animation | 11 |
| Layout-dependent init | GeometryChangedEvent | 12 |
| Data on UI elements | Button.userData | 13 |
| ScrollView child interaction | StopImmediatePropagation | 14 |
| Mobile notch/safe area | SafeAreaBorder | 15 |
| 3D objects tracking UI | PositionToVisualElement | 16 |

---

## Related References

- **[quizu-patterns.md](quizu-patterns.md)** — 7 QuizU patterns (stack navigation, EventRegistry, Presenter)
- **[dragon-crashers-insights.md](dragon-crashers-insights.md)** — DC project structure and key insights

## Related Skills

- **[ui-toolkit-architecture](../ui-toolkit-architecture/SKILL.md)** — MVC, event bus, custom controls in depth
- **[ui-toolkit-patterns](../ui-toolkit-patterns/SKILL.md)** — Animation, coordinate conversion, class toggling
- **[ui-toolkit-responsive](../ui-toolkit-responsive/SKILL.md)** — MediaQuery, SafeArea, orientation
- **[ui-toolkit-mobile](../ui-toolkit-mobile/SKILL.md)** — Touch, safe area, mobile performance
- **[ui-toolkit-performance](../ui-toolkit-performance/SKILL.md)** — Async cost, virtualization, caching
- **[ui-toolkit-theming](../ui-toolkit-theming/SKILL.md)** — TSS matrix, compound theme names

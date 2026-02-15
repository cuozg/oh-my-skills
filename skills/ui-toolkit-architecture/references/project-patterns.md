# Project Architecture Patterns — UI Toolkit

> DC patterns #1–16. For Unity 6+ templates, see [code-templates.md](code-templates.md). QuizU patterns in [quizu-patterns.md](quizu-patterns.md).

## 1. Event Bus (Static Action Delegates)

**Source**: `Assets/Scripts/UI/Events/` (10 event classes: CharEvents, ShopEvents, HomeEvents, MailEvents, InventoryEvents, SettingsEvents, GameplayEvents, MainMenuUIEvents, MediaQueryEvents, ThemeEvents)

```csharp
public static class CharEvents
{
    public static Action CharScreenShown;
    public static Action<CharacterData> CharSelected;
    public static Action<int> GoldUpdated;
}
```

Use: Any cross-module communication (UI ↔ gameplay, view ↔ controller).

## 2. MVC-like (Controller + View + ScriptableObject)

Controllers = `MonoBehaviour` (lifecycle). Views = plain C# (UI manipulation).

```csharp
// Controller — OnEnable creates view, OnDisable disposes
public class HomeScreenController : MonoBehaviour
{
    [SerializeField] UIDocument m_Document;
    HomeView m_HomeView;
    void OnEnable() { m_HomeView = new HomeView(m_Document.rootVisualElement); }
    void OnDisable() { m_HomeView.Dispose(); }
}
// View — subscribes in ctor, unsubscribes in Dispose
public class HomeView
{
    public HomeView(VisualElement root) { CharEvents.GoldUpdated += OnGoldUpdated; }
    void OnGoldUpdated(int gold) => m_GoldLabel.text = gold.ToString();
    public void Dispose() { CharEvents.GoldUpdated -= OnGoldUpdated; }
}
```

## 3. Two UIDocument Strategy

Menu screens share one `UIDocument`. Gameplay HUD (health bars) gets separate `UIDocument` instances. Separate when overlaying independently or using different PanelSettings.

## 4. Compound Theming ("{Orientation}--{Season}")

```csharp
string themeName = m_MediaAspectRatio + "--" + m_SettingsData.theme; // "Landscape--Halloween"
// ThemeManager swaps BOTH panelSettings and TSS atomically
m_Document.panelSettings = settings.panelSettings;
m_Document.panelSettings.themeStyleSheet = settings.tss;
```

TSS hierarchy: `Default.tss` → `{Orientation}.tss` → `{Orientation}--{Season}.tss`

## 5. Custom Controls (UxmlFactory/UxmlTraits — Legacy)

> For Unity 6+, use `[UxmlElement]` — see [code-templates.md #3](code-templates.md#custom-control-template).

```csharp
public class SlideToggle : BaseField<bool>
{
    public new class UxmlFactory : UxmlFactory<SlideToggle, UxmlTraits> { }
    public new class UxmlTraits : BaseFieldTraits<bool, UxmlBoolAttributeDescription> { }
}
```

## 6. Async/Await in Views (Fire-and-Forget)

```csharp
_ = ShowOptionsBarTask(); // Fire-and-forget
async Task ShowOptionsBarTask()
{
    m_Element.style.display = DisplayStyle.Flex;
    await Task.Delay(10); // Let layout resolve
    m_Element.AddToClassList(k_ActiveClass);
    await Task.Delay(300); // CSS transition duration
}
```

Timing: `Task.Delay(ms)` for fixed, `Task.Delay(TimeSpan.FromSeconds(Time.deltaTime))` for frame-synced, `Task.Yield()` + `Stopwatch` for smooth animation.

## 7. Composite View (Sub-View Management)

Parent view creates/disposes child views: `MailView` → `MailboxView`, `MailContentView`, `MailRewardView`. Use for complex screens with distinct UI regions sharing a root.

## 8. Dynamic UI Generation (VisualTreeAsset.Instantiate)

For small lists (<20 items). `container.Clear()` then loop `template.Instantiate()`. For larger lists use `ListView`.

## 9. World-to-Panel Coordinate Conversion

```csharp
void LateUpdate() // Must be LateUpdate, after camera
{
    Rect rect = RuntimePanelUtils.CameraTransformWorldToPanelRect(m_Panel, m_WorldTransform.position, m_WorldSize, m_Camera);
    m_TargetElement.style.left = rect.x; m_TargetElement.style.top = rect.y;
}
```

## 10. CSS Class Toggling for State

```csharp
m_Tab.AddToClassList("tab--active");          // Add state
m_Element.EnableInClassList("selected", true); // Toggle state
```

Keeps styling in USS, logic in C#.

## 11. experimental.animation API

```csharp
m_Element.experimental.animation.Start(new Vector2(0, 100), Vector2.zero, 300)
    .Ease(Easing.OutQuad)
    .OnValueChanged(v => m_Element.style.translate = new Translate(v.x, v.y));
```

## 12. GeometryChangedEvent (Deferred Init)

Register one-shot callback to read layout values after first layout pass. Unregister immediately in handler.

## 13. Button.userData for Data Storage

Store `ScriptableObject` on buttons via `userData`. Retrieve in click handler: `(evt.currentTarget as Button).userData as ShopItemSO`. Avoids closures.

## 14. StopImmediatePropagation

Prevent `ScrollView` from capturing child drag/click events. Register on `TrickleDown` phase.

## 15. SafeAreaBorder (borderWidth Approach)

Uses `borderWidth` (not padding) for safe area insets — doesn't affect child layout calculations. Set `borderColor = Color.clear`.

## 16. PositionToVisualElement (3D-to-UI)

Inverse of #9. Reads UI element position via `resolvedStyle`, converts to screen coords, then `Camera.ScreenToWorldPoint`. For particle effects/3D decorations aligned to UI.

## Pattern Selection Guide

| Need | Pattern # |
|------|-----------|
| Cross-module communication | 1 |
| Screen lifecycle | 2 |
| Overlapping UI layers | 3 |
| Orientation + theme | 4 |
| Reusable UXML components | 5 |
| Animation in non-MonoBehaviour | 6 |
| Complex screen with regions | 7 |
| Small dynamic lists | 8 |
| UI tracking 3D objects | 9 |
| Visual state transitions | 10 |
| Programmatic tweens | 11 |
| Layout-dependent init | 12 |
| Data on UI elements | 13 |
| ScrollView child interaction | 14 |
| Mobile safe area | 15 |
| 3D tracking UI | 16 |

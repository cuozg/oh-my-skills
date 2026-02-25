# Project Architecture Patterns — UI Toolkit

> DC patterns #1–8. For patterns #9–16, see [project-patterns-advanced.md](project-patterns-advanced.md). For Unity 6+ templates, see [code-templates.md](code-templates.md). QuizU patterns in [quizu-patterns.md](quizu-patterns.md).

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

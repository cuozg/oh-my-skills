# QuizU — UI Toolkit Architecture Patterns

7 production patterns extracted from Unity's official QuizU demo project. QuizU demonstrates a simpler single-UIDocument approach compared to Dragon Crashers' multi-controller architecture.

**Project path**: `Assets/Unity Technologies/QuizU - A UI Toolkit demo/`

---

## 1. Single UIDocument + UIScreen Stack

**Source**: `UIManager.cs`, `UIScreens.uxml`

All screens live in one root UXML via Template/Instance. A `Stack<UIScreen>` manages navigation history.

```xml
<!-- UIScreens.uxml — all 8 screens layered via Templates -->
<ui:UXML>
    <ui:Template name="StartScreen" src="StartScreen.uxml" />
    <ui:Template name="MainMenuScreen" src="MainMenuScreen.uxml" />
    <!-- ... 6 more templates ... -->
    <ui:Instance template="StartScreen" name="StartScreen"
        picking-mode="Ignore" style="position: absolute; width: 100%; height: 100%;" />
    <!-- All instances absolutely positioned, full-size, toggled via USS classes -->
</ui:UXML>
```

```csharp
// UIManager.cs — Stack-based navigation
public class UIManager : MonoBehaviour
{
    [SerializeField] UIDocument m_Document;
    Stack<UIScreen> m_History = new();
    UIScreen m_CurrentScreen;

    public void Show(UIScreen screen, bool keepInHistory = true)
    {
        if (m_CurrentScreen != null)
        {
            if (keepInHistory) m_History.Push(m_CurrentScreen);
            m_CurrentScreen.Hide();
        }
        screen.Show();
        m_CurrentScreen = screen;
    }

    public void GoBack()
    {
        if (m_History.Count == 0) return;
        m_CurrentScreen.Hide();
        m_CurrentScreen = m_History.Pop();
        m_CurrentScreen.Show();
    }
}
```

**When to use**: Apps with linear/stack-based navigation (quiz, onboarding, wizard flows).

---

## 2. UIScreen Base Class (Non-MonoBehaviour)

**Source**: `UIScreen.cs`

Abstract base class — plain C#, not MonoBehaviour. Uses USS class toggling for transitions. Provides `Coroutines` helper for coroutine access.

```csharp
public abstract class UIScreen
{
    protected VisualElement m_RootElement;
    protected UIManager m_UIManager;
    protected VisualElement m_Screen;

    const string k_ScreenVisibleClass = "screen-visible";
    const string k_ScreenHiddenClass = "screen-hidden";

    public UIScreen(VisualElement rootElement)
    {
        m_RootElement = rootElement;
        Initialize();
    }

    protected abstract void Initialize();

    public virtual void Show()
    {
        m_Screen.RemoveFromClassList(k_ScreenHiddenClass);
        m_Screen.AddToClassList(k_ScreenVisibleClass);
    }

    public virtual void Hide()
    {
        m_Screen.RemoveFromClassList(k_ScreenVisibleClass);
        m_Screen.AddToClassList(k_ScreenHiddenClass);
    }
}
```

**When to use**: Any screen system where views don't need MonoBehaviour lifecycle.

---

## 3. Static Action Event Bus

**Source**: `Events/` directory (5 classes: UIEvents, GameEvents, SceneEvents, SettingsEvents, LevelSelectionEvents)

Same pattern as Dragon Crashers — static `System.Action` delegates organized by domain.

```csharp
// UIEvents.cs — screen navigation events
public static class UIEvents
{
    public static Action ScreenClosed;
    public static Action<UIScreen, bool> ScreenShown;
    public static Action<List<string>> ResponseButtonsEnabled;
}

// GameEvents.cs — gameplay events (3 regions)
public static class GameEvents
{
    // Gameplay: QuestionUpdated, AnswerSelected, CorrectlyAnswered, ...
    // Statistics: TotalQuestionsSetup, StreakActivated, LivesUpdated, ...
    // State: GameStarted, GamePaused, GameWon, GameLost, ...
}

// SettingsEvents.cs — MVP bidirectional flow
public static class SettingsEvents
{
    // Presenter→View: MasterSliderSet, SFXSliderSet, MusicSliderSet
    // View→Presenter: MasterSliderChanged, SFXSliderChanged, MusicSliderChanged
    // Model→Presenter: ModelMasterVolumeChanged, ModelSFXVolumeChanged, ...
}
```

**When to use**: Cross-module communication without tight coupling.

---

## 4. EventRegistry (IDisposable Event Cleanup)

**Source**: `UI/Utilities/EventRegistry.cs`

Utility that tracks all event registrations for batch cleanup. Implements `IDisposable` for deterministic unsubscription.

```csharp
public class EventRegistry : IDisposable
{
    List<Action> m_Unsubscribers = new();

    public void Register<T>(Action<T> handler, ref Action<T> eventDelegate)
    {
        eventDelegate += handler;
        m_Unsubscribers.Add(() => eventDelegate -= handler);
    }

    public void RegisterCallback<TEvent>(VisualElement element,
        EventCallback<TEvent> callback) where TEvent : EventBase<TEvent>, new()
    {
        element.RegisterCallback(callback);
        m_Unsubscribers.Add(() => element.UnregisterCallback(callback));
    }

    public void Dispose()
    {
        foreach (var unsub in m_Unsubscribers)
            unsub?.Invoke();
        m_Unsubscribers.Clear();
    }
}
```

**When to use**: Any UIScreen/view to prevent event subscription leaks. Eliminates manual `+=`/`-=` tracking.

---

## 5. USS Class Toggling for Screen Transitions

**Source**: `MenuScreens.uss`, `UIScreen.cs`

Transitions via CSS classes rather than C# style property changes. GPU-friendly, designer-editable.

```css
/* MenuScreens.uss */
.screen-visible {
    transition-property: all;
    transition-duration: 0.5s;
    transition-timing-function: ease-in-out;
    position: absolute;
}

.screen-hidden {
    transition-property: all;
    opacity: 0;
    transition-duration: 0.5s;
    transition-timing-function: ease;
    bottom: 100%;  /* Slides up off-screen */
    position: absolute;
}
```

**When to use**: Any animated show/hide transitions. Keeps animation definitions in USS (designer-friendly) while C# only toggles classes.

---

## 6. Composition Pattern (Sub-Display Components)

**Source**: `GameScreen.cs`

GameScreen creates 5 specialized display components that each own a section of the screen.

```csharp
public class GameScreen : UIScreen
{
    QuestionDisplay m_QuestionDisplay;
    ResponsePanel m_ResponsePanel;
    ProgressDisplay m_ProgressDisplay;
    TimerDisplay m_TimerDisplay;
    ScoreDisplay m_ScoreDisplay;

    protected override void Initialize()
    {
        m_QuestionDisplay = new QuestionDisplay(m_Screen);
        m_ResponsePanel = new ResponsePanel(m_Screen);
        m_ProgressDisplay = new ProgressDisplay(m_Screen);
        m_TimerDisplay = new TimerDisplay(m_Screen);
        m_ScoreDisplay = new ScoreDisplay(m_Screen);
    }
}
```

**When to use**: Complex screens with logically distinct regions. Each component owns its own element queries and event subscriptions.

---

## 7. Presenter Pattern (Bidirectional Data Flow)

**Source**: `SettingsScreen.cs`, `SettingsEvents.cs`

SettingsScreen acts as Presenter — connects UI sliders (View) to audio volumes (Model) via events.

```csharp
public class SettingsScreen : UIScreen
{
    Slider m_MasterSlider;

    protected override void Initialize()
    {
        m_MasterSlider = m_Screen.Q<Slider>("settings__master-slider");

        // View→Presenter: user moves slider
        m_MasterSlider.RegisterValueChangedCallback(evt =>
            SettingsEvents.MasterSliderChanged?.Invoke(evt.newValue));

        // Presenter→View: programmatic update
        SettingsEvents.MasterSliderSet += value =>
            m_MasterSlider.SetValueWithoutNotify(value);
    }
}
```

**Key detail**: `SetValueWithoutNotify()` prevents infinite loops when updating slider value from code.

**When to use**: Settings screens, forms, any bidirectional data flow between UI and model.

---

## QuizU vs Dragon Crashers — Key Differences

| Aspect | QuizU | Dragon Crashers |
|--------|-------|-----------------|
| UIDocument strategy | Single UIDocument, all screens | Shared + separate per gameplay element |
| Screen base class | `UIScreen` (plain C#) | `UIView` (plain C#) |
| Navigation | Stack-based (`Stack<UIScreen>`) | Tab-based + modals |
| Screen transitions | USS class toggling | CSS class toggling + async/await |
| Event cleanup | `EventRegistry` utility | Manual `Dispose()` |
| Theming | Simple USS | Compound TSS (orientation × season) |
| Custom controls | None | `SlideToggle`, `HealthBarComponent` |
| Data binding | Event-driven (static Actions) | Event-driven (static Actions) |
| Complexity | Simple (quiz app) | Complex (idle RPG) |

---

## Related Skills

- **[ui-toolkit-architecture](../ui-toolkit-architecture/SKILL.md)** — MVC, event bus, controller patterns
- **[ui-toolkit-patterns](../ui-toolkit-patterns/SKILL.md)** — Screen transitions, composition, CSS toggling
- **[project-patterns.md](project-patterns.md)** — Dragon Crashers patterns (16 patterns)
- **[common-bugs-and-fixes.md](common-bugs-and-fixes.md)** — Event leak fixes, transition bugs

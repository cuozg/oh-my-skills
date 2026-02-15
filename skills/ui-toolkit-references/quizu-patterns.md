# QuizU — UI Toolkit Architecture Patterns

7 production patterns from Unity's QuizU demo. Simpler single-UIDocument approach vs DC's multi-controller architecture.

## 1. Single UIDocument + UIScreen Stack

```csharp
public class UIManager : MonoBehaviour {
    [SerializeField] UIDocument m_Document;
    Stack<UIScreen> m_History = new();
    UIScreen m_CurrentScreen;
    public void Show(UIScreen screen, bool keepInHistory = true) {
        if (m_CurrentScreen != null) {
            if (keepInHistory) m_History.Push(m_CurrentScreen);
            m_CurrentScreen.Hide();
        }
        screen.Show(); m_CurrentScreen = screen;
    }
    public void GoBack() {
        if (m_History.Count == 0) return;
        m_CurrentScreen.Hide(); m_CurrentScreen = m_History.Pop(); m_CurrentScreen.Show();
    }
}
```

All screens in one root UXML via Template/Instance. Stack-based navigation for linear flows.

## 2. UIScreen Base Class

```csharp
public abstract class UIScreen {
    protected VisualElement m_RootElement, m_Screen;
    protected UIManager m_UIManager;
    const string k_ScreenVisibleClass = "screen-visible";
    const string k_ScreenHiddenClass = "screen-hidden";
    public UIScreen(VisualElement rootElement) { m_RootElement = rootElement; Initialize(); }
    protected abstract void Initialize();
    public virtual void Show() { m_Screen.RemoveFromClassList(k_ScreenHiddenClass); m_Screen.AddToClassList(k_ScreenVisibleClass); }
    public virtual void Hide() { m_Screen.RemoveFromClassList(k_ScreenVisibleClass); m_Screen.AddToClassList(k_ScreenHiddenClass); }
}
```

## 3. Static Action Event Bus

Same as DC — static `System.Action` delegates per domain (UIEvents, GameEvents, SceneEvents, SettingsEvents, LevelSelectionEvents).

```csharp
public static class SettingsEvents {
    // Presenter→View: MasterSliderSet, SFXSliderSet, MusicSliderSet
    // View→Presenter: MasterSliderChanged, SFXSliderChanged, MusicSliderChanged
}
```

## 4. EventRegistry (IDisposable Cleanup)

Tracks all event registrations for batch cleanup:

```csharp
public class EventRegistry : IDisposable {
    List<Action> m_Unsubscribers = new();
    public void Register<T>(Action<T> handler, ref Action<T> eventDelegate) {
        eventDelegate += handler;
        m_Unsubscribers.Add(() => eventDelegate -= handler);
    }
    public void RegisterCallback<TEvent>(VisualElement element,
        EventCallback<TEvent> callback) where TEvent : EventBase<TEvent>, new() {
        element.RegisterCallback(callback);
        m_Unsubscribers.Add(() => element.UnregisterCallback(callback));
    }
    public void Dispose() { foreach (var unsub in m_Unsubscribers) unsub?.Invoke(); m_Unsubscribers.Clear(); }
}
```

Eliminates manual `+=`/`-=` tracking. Use in any UIScreen/view.

## 5. USS Class Toggling for Transitions

```css
.screen-visible { transition-property: all; transition-duration: 0.5s; transition-timing-function: ease-in-out; position: absolute; }
.screen-hidden { transition-property: all; opacity: 0; transition-duration: 0.5s; bottom: 100%; position: absolute; }
```

Animation in USS (designer-friendly), C# only toggles classes.

## 6. Composition (Sub-Display Components)

```csharp
public class GameScreen : UIScreen {
    QuestionDisplay m_QuestionDisplay; ResponsePanel m_ResponsePanel;
    ProgressDisplay m_ProgressDisplay; TimerDisplay m_TimerDisplay; ScoreDisplay m_ScoreDisplay;
    protected override void Initialize() {
        m_QuestionDisplay = new QuestionDisplay(m_Screen);
        m_ResponsePanel = new ResponsePanel(m_Screen);
        m_ProgressDisplay = new ProgressDisplay(m_Screen);
        m_TimerDisplay = new TimerDisplay(m_Screen);
        m_ScoreDisplay = new ScoreDisplay(m_Screen);
    }
}
```

Each component owns its element queries and event subscriptions.

## 7. Presenter Pattern (Bidirectional)

```csharp
public class SettingsScreen : UIScreen {
    Slider m_MasterSlider;
    protected override void Initialize() {
        m_MasterSlider = m_Screen.Q<Slider>("settings__master-slider");
        m_MasterSlider.RegisterValueChangedCallback(evt => SettingsEvents.MasterSliderChanged?.Invoke(evt.newValue));
        SettingsEvents.MasterSliderSet += value => m_MasterSlider.SetValueWithoutNotify(value);
    }
}
```

`SetValueWithoutNotify()` prevents infinite loops. Use for settings, forms, bidirectional data flow.

## QuizU vs Dragon Crashers

| Aspect | QuizU | Dragon Crashers |
|--------|-------|-----------------|
| Navigation | Stack-based | Tab-based + modals |
| Transitions | USS class toggling | CSS + async/await |
| Event cleanup | `EventRegistry` utility | Manual `Dispose()` |
| Theming | Simple USS | Compound TSS (orientation × season) |
| Complexity | Simple (quiz app) | Complex (idle RPG) |



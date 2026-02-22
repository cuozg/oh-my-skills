# QuizU — UI Toolkit Architecture Patterns (Advanced)

> See [quizu-patterns.md](quizu-patterns.md) for UIManager stack, UIScreen base class, and event bus basics.

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

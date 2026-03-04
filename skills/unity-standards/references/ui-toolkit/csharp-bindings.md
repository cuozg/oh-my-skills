# C# Bindings

## UIDocument Controller Pattern

```csharp
using UnityEngine;
using UnityEngine.UIElements;

public class MainMenuController : MonoBehaviour
{
    private Button _playButton;
    private Button _settingsButton;

    private void OnEnable()
    {
        var root = GetComponent<UIDocument>().rootVisualElement;
        _playButton = root.Q<Button>("play-btn");       // Cache queries
        _settingsButton = root.Q<Button>("settings-btn");
        _playButton.clicked += OnPlayClicked;
        _settingsButton.clicked += OnSettingsClicked;
    }

    private void OnDisable()
    {
        _playButton.clicked -= OnPlayClicked;            // Always unregister
        _settingsButton.clicked -= OnSettingsClicked;
    }

    private void OnPlayClicked() => Debug.Log("Play");
    private void OnSettingsClicked() => Debug.Log("Settings");
}
```

## UQuery Patterns

```csharp
// Single element by name
var btn = root.Q<Button>("submit-btn");

// Single element by class
var primary = root.Q<Button>(className: "button--primary");

// Multiple elements
List<Button> buttons = root.Query<Button>(className: "button").ToList();

// Filtered query
var active = root.Query<VisualElement>(className: "card")
    .Where(e => e.ClassListContains("card--active"))
    .ToList();
```

## Event Callbacks

```csharp
button.clicked += OnClick;                                           // Button shorthand
element.RegisterCallback<PointerDownEvent>(OnPointerDown);           // Pointer events
parent.RegisterCallback<PointerDownEvent>(OnDown, TrickleDown.TrickleDown); // Parent-first
slider.RegisterValueChangedCallback(evt => Apply(evt.newValue));     // Value change
element.UnregisterCallback<PointerDownEvent>(OnPointerDown);         // Always pair
```

## Closure Safety

```csharp
// ✗ BAD: captures 'this'
button.clicked += () => this.DoSomething();
// ✓ GOOD: capture specific element
var label = root.Q<Label>("status");
button.clicked += () => label.text = "Done";
```

## Data Binding (Unity 6.3+)

```csharp
// Bind UI element to C# property
var nameLabel = root.Q<Label>("player-name");
nameLabel.SetBinding("text", new DataBinding {
    dataSourcePath = new PropertyPath(nameof(PlayerData.Name)),
    bindingMode = BindingMode.OneWayToTarget  // C# → UI only
});
// Modes: OneWayToTarget (display), TwoWay (editable), OneWayFromTarget (user-driven)
// Triggers: OnValueChange (default), OnFocusOut (debounced)
```

## Focus & Visibility

```csharp
// Focus on next frame (avoids conflicts)
root.schedule.Execute(() => textField.Focus());
element.tabIndex = 0;    // tab order (-1 to skip)
element.focusable = true;

// Hide: visibility (cheap, keeps layout) vs display (reflows)
element.style.visibility = Visibility.Hidden;   // ✓ cheapest
element.style.display = DisplayStyle.None;      // layout reflow

// State via USS classes
element.ToggleInClassList("card--selected");
```

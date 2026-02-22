# Data Binding — Advanced Patterns (Unity 6)

> See [databinding-code-patterns.md](databinding-code-patterns.md) for Dragon Crashers event-driven approach (data flow, event bus, controller lifecycle, complete example).

## IDataSource Implementation

```csharp
[CreateAssetMenu(menuName = "Data/PlayerData")]
public class PlayerData : ScriptableObject, INotifyBindablePropertyChanged {
    public event EventHandler<BindablePropertyChangedEventArgs> propertyChanged;
    [CreateProperty]
    public int Health {
        get => _health;
        set { if (_health == value) return; _health = Mathf.Clamp(value, 0, MaxHealth); Notify(nameof(Health)); }
    }
    [SerializeField] int _health = 100;
    void Notify(string property) => propertyChanged?.Invoke(this, new BindablePropertyChangedEventArgs(property));
}
```

## Bindings in C#

```csharp
[RequireComponent(typeof(UIDocument))]
public class HUDController : MonoBehaviour {
    [SerializeField] PlayerData _playerData;
    void OnEnable() {
        var root = GetComponent<UIDocument>().rootVisualElement;
        root.dataSource = _playerData; // children inherit
        root.Q<Label>("player-name").SetBinding("text", new DataBinding {
            dataSourcePath = new PropertyPath("PlayerName"), bindingMode = BindingMode.OneWay
        });
        root.Q<ProgressBar>("health-bar").SetBinding("value", new DataBinding {
            dataSourcePath = new PropertyPath("Health"), bindingMode = BindingMode.OneWay
        });
    }
}
```

Per-element override: `shopPanel.dataSource = _shopData;`

## Bindings in UXML

```xml
<ui:VisualElement data-source-type="PlayerData">
    <ui:Label binding-path="PlayerName" />
    <ui:ProgressBar name="health-bar">
        <Bindings>
            <ui:DataBinding property="value" data-source-path="Health" binding-mode="OneWay" />
        </Bindings>
    </ui:ProgressBar>
    <ui:Slider name="volume-slider" low-value="0" high-value="1">
        <Bindings>
            <ui:DataBinding property="value" data-source-path="Volume" binding-mode="TwoWay" />
        </Bindings>
    </ui:Slider>
</ui:VisualElement>
```

Set object reference in C#: `root.dataSource = _playerData;`

## Type Converters

```csharp
[ConverterGroup("GameUI")]
public static class GameUIConverters {
    [Converter] public static string IntToHealthString(ref int value) => $"{value} HP";
    [Converter] public static string FloatToPercentString(ref float value) => $"{value * 100f:F0}%";
}
```

Register: `binding.converterGroup = "GameUI";` or UXML: `source-to-ui-converters="GameUI"`

## Binding Modes

```csharp
labelBinding.bindingMode = BindingMode.OneWay;          // read-only display
sliderBinding.bindingMode = BindingMode.TwoWay;         // settings slider
inputBinding.bindingMode = BindingMode.OneWayToSource;  // input writes to model
```

## Performance Notes

Bindings polled each panel update — keep count reasonable. Prefer `OneWay` over `TwoWay`. For 60fps updates, use direct assignment. See [ui-toolkit-performance](../../ui-toolkit-performance/SKILL.md).

<!-- See also: databinding-code-patterns-advanced-complete-example.md -->

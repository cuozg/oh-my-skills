# Data Binding — Code Patterns & Examples

> **Parent skill**: [ui-toolkit-databinding](../SKILL.md)

## Dragon Crashers Event-Driven Approach

### Data Flow Architecture

```
User Input ──(static Action)──▶ Controller (MonoBehaviour) ──(method call)──▶ View (UIView)
                                  ▲ OnEnable: += / OnDisable: -=                 Q<Label>().text = val
Manager (GameData) ◀──(static Action)──┘                                         
    │                                                                       
SaveManager ── JsonUtility.ToJson() / FromJsonOverwrite() ── GameData ↔ savegame.dat
    └── SaveManager.GameDataLoaded (static event) ──▶ Views
```

### Event Bus — Static Action Delegates

Each screen domain has a dedicated static event class in `Assets/Scripts/UI/Events/`:

```csharp
public static class ShopEvents {
    public static Action GoldSelected;
    public static Action<ShopItemSO, Vector2> ShopItemPurchasing;
    public static Action<GameData> FundsUpdated;
}
```

10 event classes: CharEvents, ShopEvents, HomeEvents, MailEvents, InventoryEvents, SettingsEvents, GameplayEvents, MainMenuUIEvents, MediaQueryEvents, ThemeEvents. Pattern: `public static Action<T>` delegates, null-conditional invoke (`?.Invoke()`), one class per domain.

### Controller Subscription Lifecycle

```csharp
void OnEnable()  { ShopEvents.ShopItemClicked += OnTryBuyItem; }
void OnDisable() { ShopEvents.ShopItemClicked -= OnTryBuyItem; }
void Start()     { LoadShopData(); ShopEvents.ShopUpdated?.Invoke(m_GoldShopItems); }
```

`OnEnable`/`OnDisable` for MonoBehaviours; Constructor/`Dispose()` for UIView subclasses. Every `+=` must have matching `-=`.

### View Data Update

Views extend `UIView`. Pattern: cache Q() in `SetVisualElements()`, subscribe events in constructor, unsubscribe in `Dispose()`, update via direct property assignment.

### Complete Data Flow — Shop Purchase

User click → `ShopItemComponent` fires `ShopEvents.ShopItemClicked` → `ShopScreenController.OnTryBuyItem()` → fires `ShopItemPurchasing` → `GameDataManager.OnPurchaseItem()` → checks funds → YES: fires `TransactionProcessed`, `FundsUpdated`, `PotionsUpdated` → views update; NO: fires `TransactionFailed`.

## Unity 6 Declarative Binding

### IDataSource Implementation

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

### Bindings in C#

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

### Bindings in UXML

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

### Type Converters

```csharp
[ConverterGroup("GameUI")]
public static class GameUIConverters {
    [Converter] public static string IntToHealthString(ref int value) => $"{value} HP";
    [Converter] public static string FloatToPercentString(ref float value) => $"{value * 100f:F0}%";
}
```

Register: `binding.converterGroup = "GameUI";` or UXML: `source-to-ui-converters="GameUI"`

### Binding Modes

```csharp
labelBinding.bindingMode = BindingMode.OneWay;          // read-only display
sliderBinding.bindingMode = BindingMode.TwoWay;         // settings slider
inputBinding.bindingMode = BindingMode.OneWayToSource;  // input writes to model
```

### Performance Notes

Bindings polled each panel update — keep count reasonable. Prefer `OneWay` over `TwoWay`. For 60fps updates, use direct assignment. See [ui-toolkit-performance](../../ui-toolkit-performance/SKILL.md).

### Complete Example — HUDScreenController

```csharp
[RequireComponent(typeof(UIDocument))]
public class HUDScreenController : MonoBehaviour {
    [SerializeField] PlayerData _data;
    void OnEnable() {
        var root = GetComponent<UIDocument>().rootVisualElement;
        root.dataSource = _data;
        Bind(root, "player-name", "text", "PlayerName", BindingMode.OneWay);
        Bind(root, "health-bar", "value", "Health", BindingMode.OneWay);
        Bind(root, "gold-label", "text", "Gold", BindingMode.OneWay, "GameUI");
    }
    static void Bind(VisualElement root, string elemName, string prop,
                     string path, BindingMode mode, string converter = null) {
        var binding = new DataBinding { dataSourcePath = new PropertyPath(path), bindingMode = mode };
        if (converter != null) binding.converterGroup = converter;
        root.Q(elemName).SetBinding(prop, binding);
    }
}
```
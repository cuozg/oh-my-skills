# Data Binding — Code Patterns & Examples

> **Parent skill**: [ui-toolkit-databinding](../SKILL.md)

---

## Dragon Crashers Event-Driven Approach

### Data Flow Architecture

```
┌──────────────┐   static Action    ┌──────────────────┐   method call    ┌──────────────┐
│  User Input  │ ─────────────────▶ │   Controller     │ ───────────────▶ │    View      │
│  (ClickEvent)│                    │  (MonoBehaviour)  │                  │  (UIView)    │
└──────────────┘                    │                   │                  │              │
                                    │ OnEnable:         │                  │ Q<Label>()   │
┌──────────────┐   static Action    │  Event += Handler │  static Action   │ .text = val  │
│  Manager     │ ◀─────────────────│ OnDisable:        │ ◀─────────────── │ .style.x = y │
│ (GameData    │                    │  Event -= Handler │                  │              │
│  Manager)    │ ─────────────────▶ │                   │                  │              │
└──────────────┘   static Action    └──────────────────┘                  └──────────────┘
       │                                                                         │
       ▼                                                                         │
┌──────────────┐                                                                 │
│ SaveManager  │   JsonUtility.ToJson() / FromJsonOverwrite()                    │
│ (persistence)│   GameData ↔ savegame.dat                                       │
└──────────────┘                                                                 │
       │                                                                         │
       └─── SaveManager.GameDataLoaded (static event) ──────────────────────────┘
```

### Event Bus — Static Action Delegates

Each screen domain has a dedicated static event class in `Assets/Scripts/UI/Events/`. All 10 event classes follow the same pattern:

```csharp
// Assets/Scripts/UI/Events/ShopEvents.cs — representative example
public static class ShopEvents
{
    public static Action GoldSelected;                              // parameterless
    public static Action<ShopItemSO, Vector2> ShopItemPurchasing;   // typed payload
    public static Action<GameData> FundsUpdated;                    // data model payload
}
```

10 event classes exist in `Assets/Scripts/UI/Events/` (CharEvents, ShopEvents, HomeEvents, MailEvents, InventoryEvents, SettingsEvents, GameplayEvents, MainMenuUIEvents, MediaQueryEvents, ThemeEvents). Pattern: `public static Action<T>` delegates (never C# `event`), null-conditional invoke (`?.Invoke()`), one class per screen domain.

> Full event class listing: [Dragon Crashers Insights](../../references/dragon-crashers-insights.md) (section: Architecture Components)

### Controller Subscription Lifecycle

> **Full controller/view architecture**: See [ui-toolkit-architecture](../../ui-toolkit-architecture/SKILL.md) for UIView base class, UIManager, and screen lifecycle. Examples below focus on the **data flow aspect** only.

Controllers are `MonoBehaviour`s that subscribe in `OnEnable` and unsubscribe in `OnDisable`:

```csharp
// Assets/Scripts/UI/Controllers/ShopScreenController.cs — pattern
void OnEnable()  { ShopEvents.ShopItemClicked += OnTryBuyItem; /* ... */ }
void OnDisable() { ShopEvents.ShopItemClicked -= OnTryBuyItem; /* ... */ }
void Start()     { LoadShopData(); ShopEvents.ShopUpdated?.Invoke(m_GoldShopItems); }
```

**Key conventions**: `OnEnable`/`OnDisable` for MonoBehaviours; Constructor/`Dispose()` for UIView subclasses. Every `+=` must have matching `-=`.

### View Data Update — Direct Q() + Property Assignment

Views extend `UIView` (a non-MonoBehaviour base class). Pattern: cache Q() queries in `SetVisualElements()`, subscribe events in constructor, unsubscribe in `Dispose()`, update UI via direct property assignment (`label.text = value`, `element.style.backgroundImage = ...`).

> Full HomeView/ShopView code: [Dragon Crashers Insights](../../references/dragon-crashers-insights.md) (section: Screen Implementations)

**Dynamic list rendering** — ShopView clears and rebuilds from `VisualTreeAsset.Instantiate()` templates (see [ui-toolkit-architecture](../../ui-toolkit-architecture/SKILL.md) for full pattern).

### ScriptableObject as Data Source

ScriptableObjects (`ShopItemSO`, `EquipmentSO`, `CharacterBaseSO`, `LevelSO`, `ChatSO`, `MailMessageSO`, `GameIconsSO`) are loaded via `Resources.LoadAll<T>(path)` and pushed to views through static events.

### GameData Persistence

`GameData` (`Assets/Scripts/Data/GameData.cs`) is a `[Serializable]` plain class (not ScriptableObject) for mutable player state (gold, gems, potions, settings). Persistence: `JsonUtility.ToJson()` / `FromJsonOverwrite()` via `SaveManager` → `FileManager`. UI notified via `SaveManager.GameDataLoaded?.Invoke(gameData)`.

### Complete Data Flow — Shop Purchase

User click → `ShopItemComponent` fires `ShopEvents.ShopItemClicked` → `ShopScreenController.OnTryBuyItem()` → fires `ShopItemPurchasing` → `GameDataManager.OnPurchaseItem()` → checks funds → YES: `PayTransaction()` + fires `TransactionProcessed`, `FundsUpdated`, `PotionsUpdated` → views update labels/animations; NO: fires `TransactionFailed`. SaveManager auto-saves on quit.

---

## Unity 6 Declarative Binding — Code Patterns

### IDataSource Implementation

Data sources must implement `IDataSource` and `INotifyBindablePropertyChanged` to participate in the binding system. `ScriptableObject` and `MonoBehaviour` already implement `IDataSource`.

```csharp
[CreateAssetMenu(menuName = "Data/PlayerData")]
public class PlayerData : ScriptableObject, INotifyBindablePropertyChanged
{
    public event EventHandler<BindablePropertyChangedEventArgs> propertyChanged;

    [CreateProperty]
    public int Health
    {
        get => _health;
        set { if (_health == value) return; _health = Mathf.Clamp(value, 0, MaxHealth); Notify(nameof(Health)); }
    }

    // Same pattern for PlayerName (string), MaxHealth (int) — guard, set, notify
    [SerializeField] int _health = 100;

    void Notify(string property) =>
        propertyChanged?.Invoke(this, new BindablePropertyChangedEventArgs(property));
}
```

### PropertyPath Examples

`PropertyPath` identifies which property on the data source maps to which property on the UI element.

```csharp
// Simple property
var path = new PropertyPath("Health");

// Nested property (if data source has a nested object)
var path = new PropertyPath("Stats.Strength");

// Array/list element
var path = new PropertyPath("Inventory[0].Name");

// In UXML, use dot notation as data-source-path
// data-source-path="Stats.Strength"
```

### Setting Up Bindings in C#

#### Basic binding

```csharp
using UnityEngine.UIElements;

[RequireComponent(typeof(UIDocument))]
public class HUDController : MonoBehaviour
{
    [SerializeField] PlayerData _playerData;

    void OnEnable()
    {
        var root = GetComponent<UIDocument>().rootVisualElement;

        // Set data source on a container — children inherit it
        root.dataSource = _playerData;

        // Bind label text to PlayerName
        var nameLabel = root.Q<Label>("player-name");
        nameLabel.SetBinding("text", new DataBinding
        {
            dataSourcePath = new PropertyPath("PlayerName"),
            bindingMode = BindingMode.OneWay
        });

        // Bind health bar value
        var healthBar = root.Q<ProgressBar>("health-bar");
        healthBar.SetBinding("value", new DataBinding
        {
            dataSourcePath = new PropertyPath("Health"),
            bindingMode = BindingMode.OneWay
        });
    }
}
```

#### Per-element data source override

```csharp
// Child element can override inherited data source
var shopPanel = root.Q("shop-panel");
shopPanel.dataSource = _shopData; // different source for this subtree
```

#### DataBinding properties

```csharp
var binding = new DataBinding
{
    dataSource = _playerData,               // optional: override inherited source
    dataSourcePath = new PropertyPath("Health"),
    bindingMode = BindingMode.TwoWay,       // direction
};
element.SetBinding("value", binding);
```

### Setting Up Bindings in UXML

Bindings can be declared directly in UXML markup:

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
    <ui:VisualElement data-source-type="PlayerData">

        <!-- Bind text to PlayerName property -->
        <ui:Label binding-path="PlayerName" />

        <!-- Bind with explicit data-source-path -->
        <ui:ProgressBar name="health-bar">
            <Bindings>
                <ui:DataBinding property="value"
                                data-source-path="Health"
                                binding-mode="OneWay" />
            </Bindings>
        </ui:ProgressBar>

        <!-- Two-way binding on a slider -->
        <ui:Slider name="volume-slider" low-value="0" high-value="1">
            <Bindings>
                <ui:DataBinding property="value"
                                data-source-path="Volume"
                                binding-mode="TwoWay" />
            </Bindings>
        </ui:Slider>

    </ui:VisualElement>
</ui:UXML>
```

The `data-source` and `data-source-type` attributes on a parent element are inherited by all children. Set the actual object reference in C#:

```csharp
root.dataSource = _playerData;
```

### Type Converters

#### Custom type converter

When you need formatting (e.g., `100` → `"100 HP"`):

```csharp
using Unity.Properties;
using UnityEngine.UIElements;

[ConverterGroup("GameUI")]
public static class GameUIConverters
{
    [Converter]
    public static string IntToHealthString(ref int value)
    {
        return $"{value} HP";
    }

    [Converter]
    public static string FloatToPercentString(ref float value)
    {
        return $"{value * 100f:F0}%";
    }
}
```

Register the converter group on a binding:

```csharp
var binding = new DataBinding
{
    dataSourcePath = new PropertyPath("Health"),
    bindingMode = BindingMode.OneWay,
    converterGroup = "GameUI"
};
nameLabel.SetBinding("text", binding);
```

Or in UXML:

```xml
<ui:Label name="health-text">
    <Bindings>
        <ui:DataBinding property="text"
                        data-source-path="Health"
                        binding-mode="OneWay"
                        source-to-ui-converters="GameUI" />
    </Bindings>
</ui:Label>
```

### Binding Mode Code Examples

```csharp
// Display label — read-only
labelBinding.bindingMode = BindingMode.OneWay;

// Settings slider — bidirectional
sliderBinding.bindingMode = BindingMode.TwoWay;

// Text input that only writes to model
inputBinding.bindingMode = BindingMode.OneWayToSource;
```

### Binding Lifecycle

#### When bindings update

The binding system processes updates during the **panel update phase**, not immediately on property change:

1. Property setter fires `NotifyPropertyChanged()`
2. Binding system marks the binding as dirty
3. On next panel update, dirty bindings resolve and push values to UI elements

#### Manual refresh

Force an immediate binding update when needed:

```csharp
// Refresh all bindings on an element
element.ClearBinding("text");
element.SetBinding("text", binding);
```

#### Performance considerations

- Bindings are polled each panel update — keep data source count reasonable
- Prefer `OneWay` over `TwoWay` when writes are not needed
- Group related properties in a single data source to minimize source lookups
- For high-frequency updates (60fps score counter), consider direct assignment over binding:

```csharp
// Direct assignment for per-frame updates — more efficient than binding
void UpdateScore(int score)
{
    _scoreLabel.text = score.ToString();
}
```

- Use binding for data that changes infrequently (player name, settings, inventory)
- See [ui-toolkit-performance](../../ui-toolkit-performance/SKILL.md) for broader optimization

### Complete Example — HUDScreenController

Uses the `PlayerData` ScriptableObject from the IDataSource section above, extended with a `Gold` property.

```csharp
// Controller — HUDScreenController.cs
[RequireComponent(typeof(UIDocument))]
public class HUDScreenController : MonoBehaviour
{
    [SerializeField] PlayerData _data;

    void OnEnable()
    {
        var root = GetComponent<UIDocument>().rootVisualElement;
        root.dataSource = _data;

        Bind(root, "player-name", "text", "PlayerName", BindingMode.OneWay);
        Bind(root, "health-bar", "value", "Health", BindingMode.OneWay);
        Bind(root, "gold-label", "text", "Gold", BindingMode.OneWay, "GameUI");
    }

    static void Bind(VisualElement root, string elemName, string prop,
                     string path, BindingMode mode, string converter = null)
    {
        var binding = new DataBinding
        {
            dataSourcePath = new PropertyPath(path),
            bindingMode = mode
        };
        if (converter != null) binding.converterGroup = converter;
        root.Q(elemName).SetBinding(prop, binding);
    }
}

// Converter — GameUIConverters.cs
[ConverterGroup("GameUI")]
public static class GameUIConverters
{
    [Converter]
    public static string IntToFormattedString(ref int value) => value.ToString("N0");
}
```

---

## Cross-References

- **[ui-toolkit-architecture](../../ui-toolkit-architecture/SKILL.md)** — UIView base class, screen lifecycle, controller/view separation
- **[ui-toolkit-patterns](../../ui-toolkit-patterns/SKILL.md)** — event subscription patterns, template instantiation, USS class toggling
- **[ui-toolkit-performance](../../ui-toolkit-performance/SKILL.md)** — binding vs direct assignment benchmarks

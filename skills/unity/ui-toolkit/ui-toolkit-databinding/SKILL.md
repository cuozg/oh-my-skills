---
name: ui-toolkit-databinding
description: "Unity 6 runtime data binding for UI Toolkit. Covers IDataSource, INotifyBindablePropertyChanged, [CreateProperty], PropertyPath, DataBinding class, UXML binding attributes, type converters, and binding modes. Use when: (1) Binding data models to UI elements, (2) Implementing reactive UI updates without manual callbacks, (3) Creating data sources with change notification, (4) Setting up two-way bindings for input fields, (5) Writing custom type converters for bindings. Triggers: 'data binding', 'dataSource', 'CreateProperty', 'INotifyBindablePropertyChanged', 'binding mode', 'type converter', 'PropertyPath'."
---

# UI Toolkit Data Binding

> **Based on**: Unity 6 (6000.0), Dragon Crashers official sample

This skill covers **two approaches** to UI data binding in UI Toolkit:

| | Dragon Crashers Approach | Unity 6 Approach |
|---|---|---|
| **Mechanism** | Static `Action` event bus + direct property assignment | `IDataSource` + `DataBinding` class |
| **Used in project?** | ✅ Yes — all screens | ❌ Not used |
| **When to use** | Existing codebase, pre-Unity 6, explicit control | New projects targeting Unity 6+, declarative binding |

> ⚠️ **This project does NOT use Unity 6 runtime data binding** (`IDataSource`, `[CreateProperty]`, `DataBinding` class). All UI updates flow through the event-driven pattern documented below. The Unity 6 section is retained as reference for future migration.

---

## Dragon Crashers Approach (Event-Driven)

The project uses a **manual event-driven data flow** pattern: static `Action` delegates serve as an event bus, controllers subscribe/unsubscribe in `OnEnable`/`OnDisable`, and views update UI via direct `Q<T>()` queries and property assignment.

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

### 1. Event Bus — Static Action Delegates

Each screen domain has a dedicated static event class in `Assets/Scripts/UI/Events/`. All 10 event classes follow the same pattern:

```csharp
// Assets/Scripts/UI/Events/ShopEvents.cs
public static class ShopEvents
{
    public static Action GoldSelected;                              // parameterless
    public static Action<ShopItemSO, Vector2> ShopItemPurchasing;   // typed payload
    public static Action<List<ShopItemSO>> ShopUpdated;             // collection payload
    public static Action<GameData> FundsUpdated;                    // data model payload
    public static Action<ShopItemSO, Vector2> TransactionProcessed; // success result
    public static Action<ShopItemSO> TransactionFailed;             // failure result
}
```

**All 10 event classes** (`Assets/Scripts/UI/Events/`):

| Event Class | Domain | Key Delegates |
|-------------|--------|---------------|
| `CharEvents` | Character screen | `CharacterShown(CharacterData)`, `LevelPotionUsed(CharacterData)`, `GearSlotUpdated(EquipmentSO, int)` |
| `ShopEvents` | Shop/purchasing | `ShopItemPurchasing(ShopItemSO, Vector2)`, `TransactionProcessed`, `FundsUpdated(GameData)` |
| `HomeEvents` | Home screen | `LevelInfoShown(LevelSO)`, `PlayButtonClicked`, `ChatWindowShown(List<ChatSO>)` |
| `MailEvents` | Mail system | `RewardClaimed(MailMessageSO, Vector2)` |
| `InventoryEvents` | Inventory | Gear selection/equipment events |
| `SettingsEvents` | Settings | `SettingsUpdated(GameData)`, `PlayerFundsReset` |
| `GameplayEvents` | Gameplay | `SettingsUpdated(GameData)` |
| `MainMenuUIEvents` | Main menu | `HomeScreenShown` |
| `MediaQueryEvents` | Responsive layout | Screen size/orientation events |
| `ThemeEvents` | Theming | Theme change events |

**Pattern rules**:
- Delegates are `public static Action` or `public static Action<T>` — never C# `event` keyword
- Invocation always uses null-conditional: `ShopEvents.FundsUpdated?.Invoke(m_GameData);`
- One static class per screen domain — keeps event discoverability clear

### 2. Controller Subscription Lifecycle

Controllers are `MonoBehaviour`s that subscribe in `OnEnable` and unsubscribe in `OnDisable`:

```csharp
// Assets/Scripts/UI/Controllers/ShopScreenController.cs
public class ShopScreenController : MonoBehaviour
{
    List<ShopItemSO> m_ShopItems = new List<ShopItemSO>();

    void OnEnable()
    {
        ShopEvents.ShopItemClicked += OnTryBuyItem;
        ShopEvents.GoldSelected += OnGoldSelected;
        ShopEvents.GemSelected += OnGemSelected;
        ShopEvents.PotionSelected += OnPotionSelected;
    }

    void OnDisable()
    {
        ShopEvents.ShopItemClicked -= OnTryBuyItem;
        ShopEvents.GoldSelected -= OnGoldSelected;
        ShopEvents.GemSelected -= OnGemSelected;
        ShopEvents.PotionSelected -= OnPotionSelected;
    }

    void Start()
    {
        LoadShopData();  // Resources.LoadAll<ShopItemSO>(path)
        ShopEvents.ShopUpdated?.Invoke(m_GoldShopItems);  // push to view
    }
}
```

**Key conventions**:
- `OnEnable`/`OnDisable` for MonoBehaviour controllers and managers
- Constructor/`Dispose()` for UIView subclasses (not MonoBehaviours)
- Every `+=` must have a matching `-=` — no exceptions

### 3. View Data Update — Direct Q() + Property Assignment

Views extend `UIView` (a non-MonoBehaviour base class). They query elements once and update properties directly:

```csharp
// Assets/Scripts/UI/UIViews/HomeView.cs
public class HomeView : UIView
{
    Label m_LevelNumber;
    Label m_LevelLabel;
    VisualElement m_LevelThumbnail;

    public HomeView(VisualElement topElement) : base(topElement)
    {
        HomeEvents.LevelInfoShown += OnShowLevelInfo;  // subscribe in constructor
    }

    protected override void SetVisualElements()
    {
        m_LevelNumber = m_TopElement.Q<Label>("home-play__level-number");
        m_LevelLabel = m_TopElement.Q<Label>("home-play__level-name");
        m_LevelThumbnail = m_TopElement.Q("home-play__background");
    }

    public override void Dispose()
    {
        base.Dispose();
        HomeEvents.LevelInfoShown -= OnShowLevelInfo;  // unsubscribe in Dispose
    }

    void OnShowLevelInfo(LevelSO levelData)
    {
        m_LevelNumber.text = "Level " + levelData.levelNumber;    // direct assignment
        m_LevelLabel.text = levelData.levelLabel;                  // direct assignment
        m_LevelThumbnail.style.backgroundImage =
            new StyleBackground(levelData.thumbnail);              // style assignment
    }
}
```

**Dynamic list rendering** — ShopView clears and rebuilds from templates:

```csharp
// Assets/Scripts/UI/UIViews/ShopView.cs
public void OnShopUpdated(List<ShopItemSO> shopItems)
{
    parentTab.Clear();
    foreach (ShopItemSO shopItem in shopItems)
    {
        TemplateContainer elem = m_ShopItemAsset.Instantiate();  // UXML template
        ShopItemComponent controller = new ShopItemComponent(m_GameIconsData, shopItem);
        controller.SetVisualElements(elem);
        controller.SetGameData(elem);      // direct property assignment inside
        controller.RegisterCallbacks();
        parentElement.Add(elem);
    }
}
```

### 4. ScriptableObject as Data Source

ScriptableObjects serve as read-only data sources loaded via `Resources`:

```csharp
// Assets/Scripts/UI/Controllers/ShopScreenController.cs — loading
m_ShopItems.AddRange(Resources.LoadAll<ShopItemSO>(m_ResourcePath));
m_GoldShopItems = m_ShopItems.Where(c => c.contentType == ShopItemType.Gold).ToList();

// Assets/Scripts/UI/Controllers/HomeScreenController.cs — loading
m_ChatData.AddRange(Resources.LoadAll<ChatSO>(m_ChatResourcePath));
```

Data types used as ScriptableObject sources: `ShopItemSO`, `EquipmentSO`, `CharacterBaseSO`, `LevelSO`, `ChatSO`, `MailMessageSO`, `GameIconsSO`.

### 5. GameData Serialization with JsonUtility

`GameData` is a `[Serializable]` plain class (not a ScriptableObject) for mutable player state:

```csharp
// Assets/Scripts/Data/GameData.cs
[System.Serializable]
public class GameData
{
    public uint gold = 500;
    public uint gems = 50;
    public uint healthPotions = 6;
    public uint levelUpPotions = 80;
    public string username;
    public float musicVolume;
    public float sfxVolume;

    public string ToJson() => JsonUtility.ToJson(this);

    public void LoadJson(string json) => JsonUtility.FromJsonOverwrite(json, this);
}
```

Persistence flow in `SaveManager` (`Assets/Scripts/Managers/SaveManager.cs`):

```
SaveGame: GameData.ToJson() → FileManager.WriteToFile("savegame.dat", json)
LoadGame: FileManager.LoadFromFile("savegame.dat") → GameData.LoadJson(json)
          → SaveManager.GameDataLoaded?.Invoke(gameData)  // notify UI
```

### 6. Complete Data Flow Example — Shop Purchase

```
User clicks "Buy" on shop item
    ↓
ShopItemComponent fires ShopEvents.ShopItemClicked(shopItemSO, screenPos)
    ↓
ShopScreenController.OnTryBuyItem() receives event
    → fires ShopEvents.ShopItemPurchasing(shopItemSO, screenPos)
    ↓
GameDataManager.OnPurchaseItem() receives event
    → HasSufficientFunds(shopItem)?
    ├─ YES: PayTransaction() → ReceivePurchasedGoods()
    │       → ShopEvents.TransactionProcessed?.Invoke(shopItem, screenPos)
    │       → ShopEvents.FundsUpdated?.Invoke(m_GameData)     // update currency display
    │       → ShopEvents.PotionsUpdated?.Invoke(m_GameData)   // update potion counts
    └─ NO:  ShopEvents.TransactionFailed?.Invoke(shopItem)
    ↓
OptionsBarView receives FundsUpdated → updates gold/gem labels
PopUpText receives TransactionProcessed → shows "+100 Gold" animation
SaveManager auto-saves on settings update or OnApplicationQuit
```

### Cross-References

- **[ui-toolkit-architecture](../ui-toolkit-architecture/SKILL.md)** — UIView base class, screen lifecycle, controller/view separation
- **[ui-toolkit-patterns](../ui-toolkit-patterns/SKILL.md)** — event subscription patterns, template instantiation, USS class toggling

---

## Unity 6 Approach (Declarative Data Binding)

> The following sections document Unity 6's `DataBinding` API. This project does **not** use this approach, but it is the recommended path for new Unity 6+ projects that want automatic, declarative UI updates.

## Binding Architecture

```
┌─────────────────────┐      PropertyPath       ┌────────────────────────┐
│    DataSource        │ ─────────────────────▶  │    VisualElement       │
│  (IDataSource +      │                         │                        │
│   INotifyBindable    │      DataBinding         │  .dataSource = src     │
│   PropertyChanged)   │ ◀────────────────────── │  .SetBinding(...)      │
│                      │                         │                        │
│  [CreateProperty]    │   ┌──────────────────┐  │  text ◀─── "health"   │
│  int Health { .. }   │   │  Type Converter  │  │  value ◀── "volume"   │
│  string Name { .. }  │   │  int → string    │  │                        │
│                      │   └──────────────────┘  │  Binding Mode:         │
└─────────────────────┘                          │  OneWay / TwoWay /     │
        │                                        │  OneWayToSource        │
        │  NotifyPropertyChanged()               └────────────────────────┘
        ▼
  Binding system polls changed properties → updates bound elements
```

## IDataSource Interface

Data sources must implement `IDataSource` and `INotifyBindablePropertyChanged` to participate in the binding system. `ScriptableObject` and `MonoBehaviour` already implement `IDataSource`.

```csharp
using System;
using Unity.Properties;
using UnityEngine;
using UnityEngine.UIElements;

[CreateAssetMenu(menuName = "Data/PlayerData")]
public class PlayerData : ScriptableObject, INotifyBindablePropertyChanged
{
    public event EventHandler<BindablePropertyChangedEventArgs> propertyChanged;

    [CreateProperty]
    public string PlayerName
    {
        get => _playerName;
        set
        {
            if (_playerName == value) return;
            _playerName = value;
            Notify(nameof(PlayerName));
        }
    }

    [CreateProperty]
    public int Health
    {
        get => _health;
        set
        {
            if (_health == value) return;
            _health = Mathf.Clamp(value, 0, MaxHealth);
            Notify(nameof(Health));
        }
    }

    [CreateProperty]
    public int MaxHealth
    {
        get => _maxHealth;
        set
        {
            if (_maxHealth == value) return;
            _maxHealth = Mathf.Max(1, value);
            Notify(nameof(MaxHealth));
        }
    }

    [SerializeField] string _playerName = "Hero";
    [SerializeField] int _health = 100;
    [SerializeField] int _maxHealth = 100;

    void Notify(string property)
    {
        propertyChanged?.Invoke(this, new BindablePropertyChangedEventArgs(property));
    }
}
```

## [CreateProperty] Attribute

`[CreateProperty]` from `Unity.Properties` exposes a property to the binding system. Without it, the binding system cannot discover the property.

**Setter pattern** — always guard against redundant sets and fire notification:

```csharp
[CreateProperty]
public float Volume
{
    get => _volume;
    set
    {
        if (Mathf.Approximately(_volume, value)) return; // change guard
        _volume = Mathf.Clamp01(value);
        Notify(nameof(Volume));                           // notify binding system
    }
}
```

**Read-only properties** — omit the setter or make it private:

```csharp
[CreateProperty]
public string HealthDisplay => $"{Health} / {MaxHealth}"; // computed, read-only
```

**Fields vs Properties**: `[CreateProperty]` works on properties only. Use `[SerializeField]` on the backing field for Inspector visibility.

## PropertyPath

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

## Setting Up Bindings in C#

### Basic binding

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

### Per-element data source override

```csharp
// Child element can override inherited data source
var shopPanel = root.Q("shop-panel");
shopPanel.dataSource = _shopData; // different source for this subtree
```

### DataBinding properties

```csharp
var binding = new DataBinding
{
    dataSource = _playerData,               // optional: override inherited source
    dataSourcePath = new PropertyPath("Health"),
    bindingMode = BindingMode.TwoWay,       // direction
};
element.SetBinding("value", binding);
```

## Setting Up Bindings in UXML

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

## Type Converters

The binding system automatically converts between compatible types.

### Built-in converters

| Source Type | Target Type | Notes |
|------------|-------------|-------|
| `int` | `string` | For Label.text |
| `float` | `string` | For Label.text |
| `bool` | `string` | "True" / "False" |
| `int` | `float` | ProgressBar.value |
| `float` | `int` | Rounds to nearest |
| `enum` | `string` | Enum name |

### Custom type converter

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

## Binding Modes

| Mode | Direction | Use Case |
|------|-----------|----------|
| `OneWay` | Source → UI | Display-only: labels, health bars, icons |
| `TwoWay` | Source ↔ UI | Input fields, sliders, toggles |
| `OneWayToSource` | UI → Source | UI-only input that writes back to model |

**Default is `TwoWay`** — explicitly set `OneWay` for display-only elements to avoid accidental writes.

```csharp
// Display label — read-only
labelBinding.bindingMode = BindingMode.OneWay;

// Settings slider — bidirectional
sliderBinding.bindingMode = BindingMode.TwoWay;

// Text input that only writes to model
inputBinding.bindingMode = BindingMode.OneWayToSource;
```

## Binding Lifecycle

### When bindings update

The binding system processes updates during the **panel update phase**, not immediately on property change:

1. Property setter fires `NotifyPropertyChanged()`
2. Binding system marks the binding as dirty
3. On next panel update, dirty bindings resolve and push values to UI elements

### Manual refresh

Force an immediate binding update when needed:

```csharp
// Refresh all bindings on an element
element.ClearBinding("text");
element.SetBinding("text", binding);
```

### Performance considerations

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
- See [ui-toolkit-performance](../ui-toolkit-performance/SKILL.md) for broader optimization

## Complete Example

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

## Common Pitfalls

| Anti-Pattern | Problem | Correct Approach |
|-------------|---------|-----------------|
| Missing `[CreateProperty]` | Binding silently fails, no error | Add `[CreateProperty]` to every bound property |
| No change guard in setter | Infinite notification loops | Always `if (field == value) return;` before set |
| Forgetting `NotifyPropertyChanged` | UI never updates after data changes | Call `Notify()` after every field mutation |
| Binding in `Update()` | Recreates binding every frame, GC pressure | Bind once in `OnEnable()` |
| Using `TwoWay` for labels | Labels don't write back; unnecessary overhead | Use `BindingMode.OneWay` for display elements |
| Binding per-frame data | Binding overhead exceeds direct assignment | Use direct `label.text = value` for 60fps data |
| Deep nested `PropertyPath` | Fragile, hard to debug | Flatten data sources or use intermediate sources |
| Not implementing `INotifyBindablePropertyChanged` | Bindings never detect changes | Implement the interface and wire up the event |

## Shared Resources

- [Code Templates](../references/code-templates.md) — data source, converter, binding controller templates
- [Dragon Crashers Insights](../references/dragon-crashers-insights.md) — binding patterns from the official sample
- [Performance Benchmarks](../references/performance-benchmarks.md) — binding vs direct assignment cost
- [Official Docs Links](../references/official-docs-links.md) — Unity 6 data binding docs

## Official Documentation

- [Runtime Binding](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-runtime-binding.html) — DataBinding class, PropertyPath
- [Data Binding Overview](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-data-binding.html) — concepts and setup
- [CreateProperty](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Unity.Properties.CreatePropertyAttribute.html) — attribute reference
- [Type Converters](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-runtime-binding-type-conversion.html) — custom converter groups

## Key Project File References

| File | Role |
|------|------|
| `Assets/Scripts/UI/Events/*.cs` (10 files) | Static Action delegate event bus |
| `Assets/Scripts/UI/Controllers/*Controller.cs` | MonoBehaviour controllers — subscribe/unsubscribe in OnEnable/OnDisable |
| `Assets/Scripts/UI/UIViews/*View.cs` | UIView subclasses — subscribe in constructor, unsubscribe in Dispose |
| `Assets/Scripts/Data/GameData.cs` | Serializable player state, JsonUtility persistence |
| `Assets/Scripts/Managers/GameDataManager.cs` | Central state manager, purchase logic, fund management |
| `Assets/Scripts/Managers/SaveManager.cs` | Load/save via JsonUtility + FileManager |

---
**← Previous**: [ui-toolkit-theming](../ui-toolkit-theming/SKILL.md) | **Next →**: [ui-toolkit-patterns](../ui-toolkit-patterns/SKILL.md)

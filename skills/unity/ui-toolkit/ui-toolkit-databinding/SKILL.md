---
name: ui-toolkit-databinding
description: "Unity 6 runtime data binding for UI Toolkit. Covers IDataSource, INotifyBindablePropertyChanged, [CreateProperty], PropertyPath, DataBinding class, UXML binding attributes, type converters, and binding modes. Use when: (1) Binding data models to UI elements, (2) Implementing reactive UI updates without manual callbacks, (3) Creating data sources with change notification, (4) Setting up two-way bindings for input fields, (5) Writing custom type converters for bindings. Triggers: 'data binding', 'dataSource', 'CreateProperty', 'INotifyBindablePropertyChanged', 'binding mode', 'type converter', 'PropertyPath'."
---

# UI Toolkit Data Binding

<!-- OWNERSHIP: Unity 6 DataBinding API (IDataSource, [CreateProperty], DataBinding class, PropertyPath, binding modes, type converters), event-driven binding comparison, DC event bus data flow. -->

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
// Assets/Scripts/UI/Events/ShopEvents.cs — representative example
public static class ShopEvents
{
    public static Action GoldSelected;                              // parameterless
    public static Action<ShopItemSO, Vector2> ShopItemPurchasing;   // typed payload
    public static Action<GameData> FundsUpdated;                    // data model payload
}
```

10 event classes exist in `Assets/Scripts/UI/Events/` (CharEvents, ShopEvents, HomeEvents, MailEvents, InventoryEvents, SettingsEvents, GameplayEvents, MainMenuUIEvents, MediaQueryEvents, ThemeEvents). Pattern: `public static Action<T>` delegates (never C# `event`), null-conditional invoke (`?.Invoke()`), one class per screen domain.

> Full event class listing: [Dragon Crashers Insights](../references/dragon-crashers-insights.md) (section: Architecture Components)

### 2. Controller Subscription Lifecycle

> **Full controller/view architecture**: See [ui-toolkit-architecture](../ui-toolkit-architecture/SKILL.md) for UIView base class, UIManager, and screen lifecycle. Examples below focus on the **data flow aspect** only.

Controllers are `MonoBehaviour`s that subscribe in `OnEnable` and unsubscribe in `OnDisable`:

```csharp
// Assets/Scripts/UI/Controllers/ShopScreenController.cs — pattern
void OnEnable()  { ShopEvents.ShopItemClicked += OnTryBuyItem; /* ... */ }
void OnDisable() { ShopEvents.ShopItemClicked -= OnTryBuyItem; /* ... */ }
void Start()     { LoadShopData(); ShopEvents.ShopUpdated?.Invoke(m_GoldShopItems); }
```

**Key conventions**: `OnEnable`/`OnDisable` for MonoBehaviours; Constructor/`Dispose()` for UIView subclasses. Every `+=` must have matching `-=`.

### 3. View Data Update — Direct Q() + Property Assignment

Views extend `UIView` (a non-MonoBehaviour base class). Pattern: cache Q() queries in `SetVisualElements()`, subscribe events in constructor, unsubscribe in `Dispose()`, update UI via direct property assignment (`label.text = value`, `element.style.backgroundImage = ...`).

> Full HomeView/ShopView code: [Dragon Crashers Insights](../references/dragon-crashers-insights.md) (section: Screen Implementations)

**Dynamic list rendering** — ShopView clears and rebuilds from `VisualTreeAsset.Instantiate()` templates (see [ui-toolkit-architecture](../ui-toolkit-architecture/SKILL.md) for full pattern).

### 4. ScriptableObject as Data Source

ScriptableObjects (`ShopItemSO`, `EquipmentSO`, `CharacterBaseSO`, `LevelSO`, `ChatSO`, `MailMessageSO`, `GameIconsSO`) are loaded via `Resources.LoadAll<T>(path)` and pushed to views through static events.

### 5. GameData Persistence

`GameData` (`Assets/Scripts/Data/GameData.cs`) is a `[Serializable]` plain class (not ScriptableObject) for mutable player state (gold, gems, potions, settings). Persistence: `JsonUtility.ToJson()` / `FromJsonOverwrite()` via `SaveManager` → `FileManager`. UI notified via `SaveManager.GameDataLoaded?.Invoke(gameData)`.

### 6. Complete Data Flow — Shop Purchase

User click → `ShopItemComponent` fires `ShopEvents.ShopItemClicked` → `ShopScreenController.OnTryBuyItem()` → fires `ShopItemPurchasing` → `GameDataManager.OnPurchaseItem()` → checks funds → YES: `PayTransaction()` + fires `TransactionProcessed`, `FundsUpdated`, `PotionsUpdated` → views update labels/animations; NO: fires `TransactionFailed`. SaveManager auto-saves on quit.

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

## [CreateProperty] Attribute

`[CreateProperty]` from `Unity.Properties` exposes a property to the binding system. Without it, the binding system cannot discover the property. Setter pattern: guard → set → `Notify()` (shown in PlayerData above). Read-only: `[CreateProperty] public string HealthDisplay => $"{Health} / {MaxHealth}";`. `[CreateProperty]` works on properties only — use `[SerializeField]` on backing fields for Inspector.

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
- [QuizU Patterns](../references/quizu-patterns.md) — Presenter pattern for data binding separation
- [Performance Benchmarks](../references/performance-benchmarks.md) — binding vs direct assignment cost
- [Official Docs Links](../references/official-docs-links.md) — Unity 6 data binding docs

## Official Documentation

- [Runtime Binding](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-runtime-binding.html) — DataBinding class, PropertyPath
- [Data Binding Overview](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-data-binding.html) — concepts and setup
- [CreateProperty](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Unity.Properties.CreatePropertyAttribute.html) — attribute reference
- [Type Converters](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-runtime-binding-type-conversion.html) — custom converter groups

> **DC source file listing**: [Dragon Crashers Insights](../references/dragon-crashers-insights.md) (section: DC Source Files Reference)

---
**← Previous**: [ui-toolkit-theming](../ui-toolkit-theming/SKILL.md) | **Next →**: [ui-toolkit-patterns](../ui-toolkit-patterns/SKILL.md)

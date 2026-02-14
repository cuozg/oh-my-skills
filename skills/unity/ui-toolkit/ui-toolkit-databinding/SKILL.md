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

> **Full data flow diagram, event bus code, controller lifecycle code, and shop purchase walkthrough**: See [databinding-code-patterns.md](references/databinding-code-patterns.md#dragon-crashers-event-driven-approach)

**Key components**:

1. **Event Bus** — 10 static event classes in `Assets/Scripts/UI/Events/` (CharEvents, ShopEvents, HomeEvents, MailEvents, InventoryEvents, SettingsEvents, GameplayEvents, MainMenuUIEvents, MediaQueryEvents, ThemeEvents). Pattern: `public static Action<T>` delegates (never C# `event`), null-conditional invoke (`?.Invoke()`), one class per screen domain. Full listing: [Dragon Crashers Insights](../references/dragon-crashers-insights.md).

2. **Controller Subscription** — `MonoBehaviour`s subscribe in `OnEnable`, unsubscribe in `OnDisable`. UIView subclasses use Constructor/`Dispose()`. Every `+=` must have matching `-=`. See [ui-toolkit-architecture](../ui-toolkit-architecture/SKILL.md) for full controller/view architecture.

3. **View Data Update** — Views extend `UIView`. Cache `Q()` queries in `SetVisualElements()`, update via direct property assignment (`label.text = value`). Dynamic lists clear and rebuild from `VisualTreeAsset.Instantiate()` templates.

4. **ScriptableObject as Data Source** — SOs (`ShopItemSO`, `EquipmentSO`, `CharacterBaseSO`, etc.) loaded via `Resources.LoadAll<T>(path)` and pushed to views through static events.

5. **GameData Persistence** — `GameData` is a `[Serializable]` plain class for mutable player state. Persistence via `JsonUtility.ToJson()` / `FromJsonOverwrite()` through `SaveManager` → `FileManager`. UI notified via `SaveManager.GameDataLoaded?.Invoke(gameData)`.

6. **Shop Purchase Flow** — User click → `ShopItemComponent` fires `ShopEvents.ShopItemClicked` → `ShopScreenController.OnTryBuyItem()` → `GameDataManager.OnPurchaseItem()` → checks funds → fires `TransactionProcessed`/`FundsUpdated` or `TransactionFailed`.

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

Data sources must implement `IDataSource` and `INotifyBindablePropertyChanged` to participate in the binding system. `ScriptableObject` and `MonoBehaviour` already implement `IDataSource`. Pattern: `[CreateProperty]` on properties, guard → set → `Notify()` in setter, `EventHandler<BindablePropertyChangedEventArgs>` event.

> **Full PlayerData implementation**: See [databinding-code-patterns.md](references/databinding-code-patterns.md#idatasource-implementation)

## [CreateProperty] Attribute

`[CreateProperty]` from `Unity.Properties` exposes a property to the binding system. Without it, the binding system cannot discover the property. Setter pattern: guard → set → `Notify()` (shown in PlayerData above). Read-only: `[CreateProperty] public string HealthDisplay => $"{Health} / {MaxHealth}";`. `[CreateProperty]` works on properties only — use `[SerializeField]` on backing fields for Inspector.

## PropertyPath

`PropertyPath` identifies which property on the data source maps to which property on the UI element. Supports simple (`"Health"`), nested (`"Stats.Strength"`), and indexed (`"Inventory[0].Name"`) paths. In UXML, use dot notation as `data-source-path`.

> **PropertyPath code examples**: See [databinding-code-patterns.md](references/databinding-code-patterns.md#propertypath-examples)

## Setting Up Bindings in C#

Pattern: Set `root.dataSource` on a container (children inherit), then `element.SetBinding("property", new DataBinding { ... })` for each bound element. Child elements can override with their own `dataSource`. Key `DataBinding` properties: `dataSource` (optional override), `dataSourcePath` (PropertyPath), `bindingMode`.

> **Full C# binding examples** (HUDController, per-element override, DataBinding properties): See [databinding-code-patterns.md](references/databinding-code-patterns.md#setting-up-bindings-in-c)

## Setting Up Bindings in UXML

Bindings can be declared in UXML using `data-source-type`, `binding-path`, and `<Bindings>` elements. Parent `data-source` attributes are inherited by children. Set the actual object reference in C# (`root.dataSource = _playerData`).

> **Full UXML binding examples** (Label, ProgressBar, Slider): See [databinding-code-patterns.md](references/databinding-code-patterns.md#setting-up-bindings-in-uxml)

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

> **Full custom converter code (C# + UXML registration)**: See [databinding-code-patterns.md](references/databinding-code-patterns.md#type-converters) — `[ConverterGroup]`, `[Converter]` methods, and `source-to-ui-converters` UXML attribute.

## Binding Modes

| Mode | Direction | Use Case |
|------|-----------|----------|
| `OneWay` | Source → UI | Display-only: labels, health bars, icons |
| `TwoWay` | Source ↔ UI | Input fields, sliders, toggles |
| `OneWayToSource` | UI → Source | UI-only input that writes back to model |

**Default is `TwoWay`** — explicitly set `OneWay` for display-only elements to avoid accidental writes. See [databinding-code-patterns.md](references/databinding-code-patterns.md#binding-mode-code-examples) for usage examples.

## Binding Lifecycle

> **Full lifecycle details, manual refresh, and performance considerations**: See [databinding-code-patterns.md](references/databinding-code-patterns.md#binding-lifecycle) — update timing, manual refresh pattern, and when to use direct assignment vs binding.

Key points: Bindings update during **panel update phase** (not immediately). Prefer `OneWay` for display-only. Use direct assignment (`label.text = value`) for 60fps data. See [ui-toolkit-performance](../ui-toolkit-performance/SKILL.md) for broader optimization.

## Complete Example

> **Full HUDScreenController + GameUIConverters code**: See [databinding-code-patterns.md](references/databinding-code-patterns.md#complete-example--hudscreencontroller) — complete controller with helper `Bind()` method and `[ConverterGroup]` converter.

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

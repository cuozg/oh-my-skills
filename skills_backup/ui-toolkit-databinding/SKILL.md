---
name: ui-toolkit-databinding
description: "Unity 6 runtime data binding for UI Toolkit. Covers IDataSource, INotifyBindablePropertyChanged, [CreateProperty], PropertyPath, DataBinding class, UXML binding attributes, type converters, and binding modes. Use when: (1) Binding data models to UI elements, (2) Implementing reactive UI updates without manual callbacks, (3) Creating data sources with change notification, (4) Setting up two-way bindings for input fields, (5) Writing custom type converters for bindings. Triggers: 'data binding', 'dataSource', 'CreateProperty', 'INotifyBindablePropertyChanged', 'binding mode', 'type converter', 'PropertyPath'."
---

# UI Toolkit Data Binding

**Two approaches**: DC uses static `Action` event bus + direct property assignment (all screens). Unity 6 offers `IDataSource` + `DataBinding` (declarative, not used in DC).

## Output
Production-ready C# data binding code using either event-driven or Unity 6 declarative patterns above.

## Dragon Crashers Approach (Event-Driven)

Manual event-driven data flow: static `Action` delegates as event bus, controllers subscribe in `OnEnable`/unsubscribe in `OnDisable`, views update via `Q<T>()` + property assignment.

> **Full data flow, event bus, controller lifecycle, shop purchase walkthrough**: See [databinding-code-patterns.md](references/databinding-code-patterns.md#dragon-crashers-event-driven-approach)

**Key components**: (1) **Event Bus** — 10 static event classes (`CharEvents`, `ShopEvents`, etc.), `Action<T>` delegates, null-conditional invoke. (2) **Controller Subscription** — `+=` in OnEnable, `-=` in OnDisable. (3) **View Updates** — cache `Q()` in `SetVisualElements()`, direct assignment. (4) **SO Data Sources** — `Resources.LoadAll<T>()` pushed via events. (5) **GameData** — `[Serializable]` class, `JsonUtility` persistence via `SaveManager`. (6) **Shop Flow** — click → `ShopItemClicked` → `OnTryBuyItem` → check funds → `TransactionProcessed`/`TransactionFailed`.

Cross-refs: ui-toolkit-architecture · ui-toolkit-patterns

## Unity 6 Declarative Data Binding

> DC does **not** use this. Reference for new Unity 6+ projects.

### Architecture

DataSource (`IDataSource` + `INotifyBindablePropertyChanged`) → PropertyPath → DataBinding → VisualElement. `[CreateProperty]` exposes properties. Setter: guard → set → `Notify()`. `ScriptableObject`/`MonoBehaviour` already implement `IDataSource`.

> **Full implementations**: See [databinding-code-patterns.md](references/databinding-code-patterns.md#idatasource-implementation)

### PropertyPath

Simple (`"Health"`), nested (`"Stats.Strength"`), indexed (`"Inventory[0].Name"`). UXML: dot notation as `data-source-path`.

### Bindings in C# / UXML

Set `root.dataSource` on container (children inherit), then `element.SetBinding("property", new DataBinding { ... })`. UXML: `data-source-type`, `binding-path`, `<Bindings>` elements. Set object ref in C#.

> **Full examples**: [databinding-code-patterns.md](references/databinding-code-patterns.md#bindings-in-c) · [UXML bindings](references/databinding-code-patterns.md#bindings-in-uxml)

### Type Converters

Built-in: int/float/bool/enum → string, int ↔ float. Custom: `[ConverterGroup]` + `[Converter]` methods. See [databinding-code-patterns.md](references/databinding-code-patterns.md#type-converters).

### Binding Modes

| Mode | Direction | Use Case |
|------|-----------|----------|
| `OneWay` | Source → UI | Labels, health bars (default is TwoWay — set explicitly) |
| `TwoWay` | Source ↔ UI | Input fields, sliders, toggles |
| `OneWayToSource` | UI → Source | UI-only input writing back |

Bindings update during **panel update phase** (not immediately). Use direct assignment for 60fps data.

> **Complete example**: [databinding-code-patterns.md](references/databinding-code-patterns.md#complete-example--hudscreencontroller)

## Common Pitfalls

| Anti-Pattern | Fix |
|-------------|-----|
| Missing `[CreateProperty]` | Binding silently fails |
| No change guard in setter | Infinite notification loops |
| Forgetting `NotifyPropertyChanged` | UI never updates |
| Binding in `Update()` | GC pressure — bind once in OnEnable |
| `TwoWay` for labels | Use `OneWay` for display elements |
| Binding per-frame data | Direct `label.text = value` instead |
| Deep nested PropertyPath | Flatten or use intermediate sources |



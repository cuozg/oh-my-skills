# UI Toolkit Skills — Master Test Prompts Document

> **45 test prompts** across **9 sub-skills** (5 per skill).
> Generated 2026-02-13. Use these to validate each skill's coverage, accuracy, and depth.

---

## Table of Contents

1. [UI Toolkit Master](#1-ui-toolkit-master) — Prompts 1–5
2. [UI Toolkit Architecture](#2-ui-toolkit-architecture) — Prompts 6–10
3. [UI Toolkit Data Binding](#3-ui-toolkit-data-binding) — Prompts 11–15
4. [UI Toolkit Debugging](#4-ui-toolkit-debugging) — Prompts 16–20
5. [UI Toolkit Mobile](#5-ui-toolkit-mobile) — Prompts 21–25
6. [UI Toolkit Theming](#6-ui-toolkit-theming) — Prompts 26–30
7. [UI Toolkit Patterns](#7-ui-toolkit-patterns) — Prompts 31–35
8. [UI Toolkit Performance](#8-ui-toolkit-performance) — Prompts 36–40
9. [UI Toolkit Responsive](#9-ui-toolkit-responsive) — Prompts 41–45

---

## 1. UI Toolkit Master

**Skill file:** `ui-toolkit-master/SKILL.md`
**Covers:** UXML/USS/C# triad, project structure, Dragon Crashers patterns, PanelSettings, SafeArea, UIView/UIManager, event bus, async patterns, 3D-to-UI bridge

---

### Prompt 1 — UXML/USS/C# Triad Separation Audit

**Prompt:**
> "I have a Unity 6 project where UI is implemented entirely in C# code — elements are created via `new VisualElement()`, styles are set inline (`element.style.backgroundColor = ...`), and everything is in a single 800-line MonoBehaviour. Refactor this main menu into proper UXML/USS/C# separation. The menu has: a title label, three navigation buttons (Play, Shop, Settings), a gold counter in the top bar, and a version label at the bottom. Show me the correct file structure, UXML document, USS stylesheet, and C# controller."

**Skill Areas Tested:**
- Correct UXML structure with no inline styles and semantic class/name attributes
- USS file with proper selectors, design-token-ready custom properties, and no layout hierarchy logic
- C# controller that queries elements in `OnEnable`, caches references, registers/unregisters callbacks in `OnEnable`/`OnDisable`
- `[RequireComponent(typeof(UIDocument))]` pattern
- Adherence to the "Separation rules" (UXML: no styling, no logic; USS: no hierarchy, no behavior; C#: no hardcoded styles)

**Expected Outcome:**
- Three clean files: `MainMenu.uxml`, `MainMenu.uss`, `MainMenuController.cs`
- UXML uses `class` attributes for styling (no `style=""` attributes)
- USS uses `.class` and `#name` selectors, no C#-side `element.style.*`
- C# caches Q() results in fields, registers `ClickEvent` callbacks, unregisters in `OnDisable`
- Should recommend the project structure: `Assets/UI/Documents/Screens/`, `Assets/UI/Styles/`, `Assets/Scripts/UI/Screens/`
- Should mention PanelSettings configuration (ScaleWithScreenSize, reference resolution)

---

### Prompt 2 — Dragon Crashers–Style Multi-Screen Architecture

**Prompt:**
> "I'm building a mobile RPG with 6 screens: Home, Heroes, Inventory, Shop, Guild, and Settings. I want navigation via a bottom tab bar. Settings should appear as an overlay on top of the current screen (not replace it). The game also has an in-match HUD with health bars that exists independently. Design the full architecture: UIDocument strategy, UIView base class, UIManager navigation logic, event bus pattern, and folder structure. Follow the Dragon Crashers patterns from the UI Toolkit Master skill."

**Skill Areas Tested:**
- Single UIDocument + UIView pattern (one master UXML with all screens as branches, toggled via `DisplayStyle.Flex/None`)
- Dual UIDocument strategy (menu UIDocument for persistent screens + separate gameplay UIDocuments for HUD)
- UIView base class with template method pattern: `Initialize → SetVisualElements → RegisterButtonCallbacks`, `IDisposable`
- Modal vs Overlay navigation distinction (`ShowModalView` hides current; overlay shows on top without hiding)
- Static event bus pattern with per-feature event classes
- Correct event subscription lifecycle: controllers in `OnEnable`/`OnDisable`, views in constructor/`Dispose()`

**Expected Outcome:**
- `UIManager.cs` with single `UIDocument`, `SetupViews()` querying branches, `ShowModalView()` and overlay methods
- `UIView.cs` base class matching the Dragon Crashers template method pattern
- At least one concrete view example showing cached Q() calls, event subscription/disposal
- Static event bus classes grouped by feature
- Settings shown as overlay (not modal)
- Separate UIDocument recommendation for in-match health bars
- Folder structure following the recommended layout

---

### Prompt 3 — Safe Area, Orientation, and PanelSettings Configuration for Mobile

**Prompt:**
> "We're shipping a UI Toolkit game on iPhone 15 Pro and Samsung Galaxy S24. The game supports both portrait and landscape orientation. I need: (1) PanelSettings configured correctly for both orientations, (2) safe area handling that works with the iPhone Dynamic Island and Samsung punch-hole camera, (3) orientation-aware USS that changes layout between portrait (vertical stack) and landscape (side-by-side panels). How does Dragon Crashers handle this? Should I use CSS media queries or the TSS-swapping approach?"

**Skill Areas Tested:**
- PanelSettings asset creation: `ScaleWithScreenSize`, reference resolution, screen match mode
- SafeAreaBorder borderWidth approach (not padding) — the Dragon Crashers technique
- Understanding that UI Toolkit does NOT have CSS media queries — TSS swapping is required
- TSS orientation × theme matrix (Dragon Crashers uses 7 TSS files)
- ThemeManager pattern that swaps TSS/PanelSettings based on `Screen.orientation`
- Routing to sub-skills: `ui-toolkit-responsive`, `ui-toolkit-mobile`, `ui-toolkit-theming`

**Expected Outcome:**
- Clear explanation that TSS swapping is the correct approach (not media queries)
- SafeAreaBorder implementation using `borderWidth` with explanation of why borderWidth > padding
- PanelSettings configuration with portrait and landscape variants
- USS override file organization matching Dragon Crashers
- ThemeManager-like script that swaps TSS based on orientation
- References to sub-skills for deeper coverage

---

### Prompt 4 — Performance Anti-Pattern Code Review

**Prompt:**
> "Review this UI Toolkit code for performance issues and common mistakes. This is a leaderboard screen that updates every second with 500 player entries:
>
> ```csharp
> public class LeaderboardScreen : MonoBehaviour
> {
>     void Update()
>     {
>         var root = GetComponent<UIDocument>().rootVisualElement;
>         var container = root.Q<ScrollView>("leaderboard-container");
>         container.Clear();
>         foreach (var player in GameManager.Instance.GetLeaderboard())
>         {
>             var row = new VisualElement();
>             row.style.flexDirection = FlexDirection.Row;
>             row.style.height = 60;
>             row.style.backgroundColor = new Color(0.1f, 0.1f, 0.2f);
>             var nameLabel = new Label(player.Name);
>             nameLabel.style.fontSize = 16;
>             nameLabel.style.color = Color.white;
>             nameLabel.style.width = new Length(60, LengthUnit.Percent);
>             var scoreLabel = new Label($"Score: {player.Score}");
>             scoreLabel.style.fontSize = 14;
>             scoreLabel.style.color = new Color(0.7f, 0.7f, 0.7f);
>             row.Add(nameLabel);
>             row.Add(scoreLabel);
>             container.Add(row);
>         }
>     }
> }
> ```
> What's wrong and how should I fix it?"

**Skill Areas Tested:**
- Identifying ALL common mistakes: Q() every frame, ScrollView for 500 items, inline styles, Clear+recreate every frame, string concatenation per frame, missing `[RequireComponent]`
- Correct fix: `ListView` with `makeItem`/`bindItem`, virtualization, cached references, USS classes
- Performance rules: cache Q(), use ListView, animate transforms not layout, set UsageHints

**Expected Outcome:**
- Itemized list of every anti-pattern (at least 5-6 issues)
- Complete rewrite using `ListView` with virtualization
- USS stylesheet replacing inline styles
- Cached Q() calls in `OnEnable`
- Data-driven update (only update changed entries)
- Reference to `ui-toolkit-performance` sub-skill

---

### Prompt 5 — Async UI Animation + 3D-to-UI Bridge in Plain C# Views

**Prompt:**
> "I have a character selection screen built with the UIView pattern (plain C# class, not MonoBehaviour). When the player selects a hero card, I need to: (1) animate the selected card scaling up with a bounce effect using USS transitions, (2) lerp the hero's stats labels (HP, ATK, DEF) from old values to new values over 0.5 seconds, and (3) position a 3D character model behind the selected UI card so it aligns with the card's screen position. The character model needs to stay aligned when the device orientation changes. How do I implement all three in a UIView subclass that can't use coroutines?"

**Skill Areas Tested:**
- USS transition usage for card scale (transform-based, GPU-accelerated)
- Async/await fire-and-forget pattern: `_ = AsyncMethod()` with try/catch
- Unity 6: `await Awaitable.NextFrameAsync()` instead of `Task.Delay`
- PositionToVisualElement pattern: `worldBound` → screen → world position
- GeometryChangedEvent callback for orientation changes
- UsageHints.DynamicTransform on animated elements
- Proper event cleanup in `Dispose()`

**Expected Outcome:**
- USS with `transition: scale 0.3s ease-out-back` (not C#-side width/height animation)
- C# async method with `_ = LerpStatsAsync(...)`, try/catch wrapper, `Awaitable.NextFrameAsync()` loop
- PositionToVisualElement-style code converting card's `worldBound` center → screen → world position
- `GeometryChangedEvent` registration on the card element
- `Dispose()` implementation unregistering all callbacks
- Mention of `UsageHints.DynamicTransform`
- Explanation of why coroutines aren't available (UIView is not MonoBehaviour)

---

## 2. UI Toolkit Architecture

**Skill file:** `ui-toolkit-architecture/SKILL.md`
**Covers:** [UxmlElement] custom controls, MVC/MVP patterns, UXML template composition, composite views, UIView base class, BEM naming, reusable components

---

### Prompt 6 — Guild Roster Screen — Full MVC with Custom Controls and ListView

**Prompt:**
> "Build a Guild Roster screen for a mobile RPG using UI Toolkit. The screen should display a list of guild members using a virtualized `ListView`. Each row is a custom `[UxmlElement]` control called `GuildMemberCard` that shows the member's avatar, name, role (Officer/Member/Recruit), and online status indicator. The screen follows MVC: a `GuildRosterModel` ScriptableObject holds `List<GuildMemberData>`, a `GuildRosterView` (plain C# class inheriting a UIView base) caches all Q() calls in `SetVisualElements()` and fires events through a static `GuildRosterEvents` bus, and a `GuildRosterController` MonoBehaviour coordinates between the model and view. Include UXML, USS (with BEM naming), and all C# files. The screen has a header with a back button and member count label, plus a search filter TextField."

**Expected Outcome:**
- `GuildMemberCard` uses `[UxmlElement]` + `partial class` with `[UxmlAttribute]` for Name, Role, IsOnline
- Constructor builds visual tree with BEM class names (`guild-member-card__avatar`, `guild-member-card__name`, `guild-member-card--online`)
- `GuildRosterView` extends UIView base, caches Q() in `SetVisualElements()`, fires static events
- `GuildRosterController` is a thin MonoBehaviour that listens to static events and updates the model
- ListView uses `makeItem`/`bindItem`/`unbindItem` correctly — no Q() calls inside `bindItem`
- USS uses CSS custom properties and BEM naming throughout
- UXML uses `<ui:Template>` composition for header if applicable

---

### Prompt 7 — Equipment Loadout — Composite View with Sub-Views and UXML Template Composition

**Prompt:**
> "Create an Equipment Loadout screen for a fantasy RPG. The screen is composed of three distinct panels: (1) a character model area with 6 equipment slots arranged around a silhouette, (2) an inventory list panel showing available items filtered by the selected slot, and (3) a stat comparison panel that shows before/after stats when hovering over an inventory item. Follow the Dragon Crashers composite view pattern where the parent `EquipmentView` creates and manages the lifecycles of `EquipmentSlotsView`, `InventoryListView`, and `StatComparisonView` as sub-views. Each sub-view has its own UXML template composed via `<ui:Template>` and `<ui:Instance>`. Communication between sub-views must go through a static event bus — sub-views never reference each other directly. Include proper Dispose() cascading."

**Expected Outcome:**
- `EquipmentView` follows the MailView composite pattern: queries containers in `SetVisualElements()`, creates sub-views in `Initialize()`, cascades `Dispose()`
- Three separate UXML templates composed via `<ui:Template>` and `<ui:Instance>`
- Static event bus (`EquipmentEvents`) with events like `SlotSelected`, `ItemHovered`, `ItemEquipped`
- Data flows down: parent passes data to children via properties
- Each sub-view has its own USS file with BEM naming, no style leakage
- `EquipmentSlotControl` is a `[UxmlElement]` custom control with attributes for SlotType, ItemIcon, IsEmpty
- Proper event subscription in constructors and unsubscription in `Dispose()`

---

### Prompt 8 — Reusable Tabbed Content System with Convention-Based Mapping

**Prompt:**
> "Implement a reusable tabbed content system inspired by Dragon Crashers' `TabbedMenuController`, but modernized for Unity 6. The system should work across at least 3 different screens: a Hero screen (tabs: Stats, Skills, Equipment), a Social screen (tabs: Friends, Guild, Chat), and a Shop screen (tabs: Featured, Gems, Bundles). The tab controller must be a plain C# class that takes a configuration struct defining tab/content naming conventions. Create a `TabbedMenuConfig` struct, the `TabbedMenuController` class, a `TabbedMenu` MonoBehaviour wrapper, and demonstrate UXML for at least one screen. The tab system should support keyboard/gamepad navigation via `NavigationMoveEvent`, and use USS class toggling for ALL visual state — no inline style changes."

**Expected Outcome:**
- `TabbedMenuConfig` struct with `tabClassName`, `selectedTabClassName`, `unselectedContentClassName`, `tabNameSuffix`, `contentNameSuffix`
- `TabbedMenuController` is a plain C# class, takes root VisualElement + config
- Tab ↔ content mapping is convention-based via suffix string replacement
- Same controller serves all 3 screens — only config changes
- `TabbedMenu` MonoBehaviour wraps the controller with UIDocument access
- `NavigationMoveEvent` handler for gamepad/keyboard tab cycling
- ALL visual state driven by CSS class add/remove — never inline style

---

### Prompt 9 — Custom BaseField Control — Star Rating with Data Binding

**Prompt:**
> "Create a `StarRating` custom control that derives from `BaseField<int>` for a game review system. The control should display 5 clickable stars that fill based on the current value (1-5). It must support: (1) `[UxmlElement]` registration with `[UxmlAttribute]` for MaxStars and ReadOnly, (2) three input methods — click, keyboard arrows, and `NavigationSubmitEvent` for gamepad, (3) automatic `ChangeEvent<int>` dispatch via BaseField, (4) USS-driven visual states using class toggling (`star--filled`, `star--empty`, `star--hover`), (5) data binding compatibility with a ScriptableObject data source. Also create the USS file and show integration in a ReviewScreen UXML."

**Expected Outcome:**
- `StarRating` extends `BaseField<int>`, is `[UxmlElement] partial class`
- Constructor creates 5 star VisualElements with BEM classes
- Overrides `SetValueWithoutNotify()` to update star USS classes
- `[UxmlAttribute] public int MaxStars` and `[UxmlAttribute] public bool ReadOnly`
- Hover effect via `PointerEnterEvent`/`PointerLeaveEvent`
- Inherits `INotifyValueChanged<int>` from BaseField — no manual event dispatch
- USS file with transitions for smooth fill animation
- UXML shows `<StarRating max-stars="5" />` in a form layout

---

### Prompt 10 — Screen Navigation Architecture — Stack-Based Manager with Lazy Loading

**Prompt:**
> "Design and implement a production-grade `UIScreenManager` for a mobile game with 12+ screens. Requirements: (1) Stack-based navigation with Push/Pop/Replace operations, (2) Lazy loading — screen UXML is instantiated only on first access, cached thereafter, (3) Modal screens that replace current view, and Overlay screens that stack on top, (4) Screen lifecycle hooks — `OnScreenShown`, `OnScreenHidden`, `OnScreenCreated`, `OnScreenDestroyed`, (5) A base `UIScreen` abstract class following UIView template method pattern, (6) Back navigation that knows whether to Pop a modal or dismiss an overlay. Show the architecture with the manager, base class, two concrete screens (SettingsScreen as overlay, InventoryScreen as modal), their UXML/USS files, and a static `NavigationEvents` bus."

**Expected Outcome:**
- `UIScreen` base class with `Initialize()` → `SetVisualElements()` → `RegisterButtonCallbacks()`, `Show()`/`Hide()`, `Dispose()`
- `UIScreenManager` with `Stack<ScreenEntry>` where `ScreenEntry` tracks type (Modal/Overlay)
- `Push()` hides current + shows new, `Pop()` reverses, `Replace()` clears stack
- Lazy instantiation: dictionaries for templates and cached instances
- Overlay push doesn't hide current screen
- `NavigationEvents` static event bus
- `SettingsScreen` demonstrates overlay, `InventoryScreen` demonstrates modal
- `OnDisable` cascades `Dispose()` to all cached screens

---

## 3. UI Toolkit Data Binding

**Skill file:** `ui-toolkit-databinding/SKILL.md`
**Covers:** IDataSource, INotifyBindablePropertyChanged, [CreateProperty], BindingMode, PropertyPath, type converters, UXML declarative bindings, performance boundaries

---

### Prompt 11 — Multiplayer Lobby — Player Stats HUD with IDataSource and Mixed Binding Modes

**Prompt:**
> "I'm building a multiplayer lobby screen in Unity 6. I need a data source for the local player that tracks: `DisplayName` (string), `ReadyStatus` (bool), `Rank` (int), `WinRate` (float 0–1), and `SelectedCharacter` (enum `CharacterClass { Warrior, Mage, Archer, Healer }`). The HUD has: a Label showing display name (read-only), a Toggle for ready status (user can toggle, must write back), a Label showing rank as 'Rank #5' format, a ProgressBar showing win rate, a DropdownField for character selection. Create the full data source class, controller with all bindings, and type converters. Explain why you chose each BindingMode."

**Expected Outcome:**
- `INotifyBindablePropertyChanged` class with `[CreateProperty]` on all 5 properties
- Change guards in every setter, `Mathf.Approximately` for float
- `OneWay` for DisplayName, Rank, WinRate; `TwoWay` for ReadyStatus, SelectedCharacter
- `[ConverterGroup]` with rank → "Rank #N" converter
- Explanation of why `OneWayToSource` was NOT used here

---

### Prompt 12 — Settings Screen — Two-Way Bindings with Real-Time Persistence

**Prompt:**
> "I need a game settings screen using Unity 6 data binding. Settings model: `MasterVolume` (float 0–1), `MusicVolume` (float 0–1), `SFXVolume` (float 0–1), `ScreenShake` (bool), `Language` (enum), and a computed `IsMuted` (true when MasterVolume < 0.01). UI has three Sliders, a Toggle, a DropdownField, and a Label showing 'MUTED' based on IsMuted. Requirements: all sliders TwoWay bound, IsMuted auto-updates when MasterVolume changes, data source is a plain C# class (not ScriptableObject), include UXML with declarative `<Bindings>` blocks, add a type converter formatting floats as '75%'."

**Expected Outcome:**
- Non-ScriptableObject class implementing BOTH `IDataSource` and `INotifyBindablePropertyChanged` manually
- `MasterVolume` setter notifies both `nameof(MasterVolume)` AND `nameof(IsMuted)` — dependent property notification
- UXML with `<ui:DataBinding>` elements specifying `binding-mode="TwoWay"` for sliders
- `IsMuted` as a getter-only `[CreateProperty]` (computed property)
- `Mathf.Approximately()` in float setters

---

### Prompt 13 — Inventory System — Per-Element Data Source Override + ListView Binding

**Prompt:**
> "I'm building an RPG inventory system. The main screen has a ListView on the left and a detail panel on the right. Two data sources: `InventoryData` (Items list, Gold, CarryWeight, MaxCarryWeight) and `SelectedItemData` (ItemName, Description, Rarity enum, Attack, Defense, Value). The root container uses `InventoryData`, but the detail panel should OVERRIDE with `SelectedItemData`. When the user selects an item, `SelectedItemData` properties update and bindings react. Show both data source classes, the per-element override pattern, PropertyPath with nested properties, and a type converter mapping ItemRarity to a color-coded string like '★★★ Epic'. Explain the binding lifecycle — when does the detail panel actually reflect changes?"

**Expected Outcome:**
- Two separate data source classes with `INotifyBindablePropertyChanged`
- Root `dataSource = InventoryData`, detail panel overrides via `detailPanel.dataSource = _selectedItemData`
- Gold label with converter formatting as "1,234 G"
- SelectedItemData updated via property setters so notifications fire
- Explanation of panel update phase: binding marks dirty → resolves on next panel update → pushes to UI
- `[ConverterGroup("Inventory")]` with ItemRarity → star-rated string converter
- `PropertyPath("Items[0].Name")` acknowledged but flattened sources recommended

---

### Prompt 14 — Migrating Dragon Crashers Shop Screen from Event-Driven to Data Binding

**Prompt:**
> "Our project uses the Dragon Crashers event-driven pattern (static Action delegates, controller subscribes in OnEnable/OnDisable, views update via Q<Label>().text = value). I want to migrate the shop screen's currency display to Unity 6 runtime data binding. Currently `GameDataManager` fires `ShopEvents.FundsUpdated`, `OptionsBarView` subscribes and manually sets goldLabel.text and gemLabel.text. I want to: (1) Create a CurrencyDataSource wrapping GameData fields as [CreateProperty] properties, (2) Bind gold/gem/potion labels with OneWay bindings, (3) Keep existing ShopEvents for non-currency updates, (4) Add converters with thousands separators. Show the migration step by step. What are the pitfalls of mixing event-driven with data binding?"

**Expected Outcome:**
- `CurrencyDataSource` implementing `INotifyBindablePropertyChanged`
- Discussion of synchronization approach
- Controller setting `root.dataSource = _currencyData`
- `[ConverterGroup("Currency")]` with uint → formatted string converter
- Acknowledgment of anti-pattern table: "Missing [CreateProperty] → binding silently fails"
- Pitfall discussion: dual data flow risks state desynchronization
- No modification to existing `ShopEvents` — additive change only

---

### Prompt 15 — Real-Time Combat HUD — Performance Boundaries + OneWayToSource

**Prompt:**
> "I'm building a real-time combat HUD showing: CurrentHP (changes multiple times/second), MaxHP, Mana, ComboCount (resets frequently), DPS (computed), HealthPercent (computed). A TextField for quick-chat should ONLY write to the data model (never read back). Questions: (1) Which properties should use binding vs direct assignment for performance? (2) Implement the data source with [CreateProperty] for ALL but demonstrate binding the 'slow' properties and direct assignment for 'fast' ones. (3) Use OneWayToSource for the quick-chat TextField. (4) Show getter-only [CreateProperty] for computed properties with dependent notifications. (5) What happens if I use TwoWay on a Label?"

**Expected Outcome:**
- Data source with all properties using `[CreateProperty]`
- `CurrentHP` setter notifies BOTH `nameof(CurrentHP)` AND `nameof(HealthPercent)`
- Controller demonstrates: `OneWay` for MaxHP/Mana, direct `label.text` for CurrentHP/ComboCount/DPS, `OneWayToSource` for TextField
- Anti-pattern explanation for `TwoWay` on Labels
- Performance guidance: bindings polled each panel update
- `Mathf.Approximately()` for float comparisons, change guards on every setter

---

## 4. UI Toolkit Debugging

**Skill file:** `ui-toolkit-debugging/SKILL.md`
**Covers:** UI Toolkit Debugger, Event Debugger, Frame Debugger, Profiler UI Details, Memory Profiler, common pitfalls, diagnostic utilities

---

### Prompt 16 — Invisible Inventory Grid — Element Visibility & Layout Diagnosis

**Prompt:**
> "I have an inventory screen built with UI Toolkit. The `InventoryGridView` uses a ScrollView containing a VisualElement with `flex-wrap: wrap` to display item slots. After a recent refactor, the entire grid is invisible — the screen shows the header and footer but the grid area is blank. The UXML and USS files haven't changed. I added the grid items programmatically in `OnEnable()` and confirmed via Debug.Log that 24 items are being added. The container's background color is also not visible. No errors in the console. How do I systematically debug this?"

**Expected Outcome:**
- Open UI Toolkit Debugger, select the runtime panel
- Use Pick Mode to locate the grid container
- Check the Debugger Checklist: `display`, `visibility`, `opacity`, and Layout section for zero width/height
- Identify root cause — parent has `display: none` inline, or grid container has zero size due to missing `flex-grow: 1`
- Check `resolvedStyle` vs inline styles
- Should NOT suggest trial-and-error CSS changes — insist on reading computed state first

---

### Prompt 17 — Button Click Events Swallowed by Parent Container

**Prompt:**
> "I have a CharacterDetailPanel overlay with three action buttons: 'Equip', 'Upgrade', and 'Dismiss'. The 'Dismiss' button works fine, but 'Equip' and 'Upgrade' do nothing when clicked. All three are created identically in UXML and registered with `RegisterCallback<ClickEvent>`. I confirmed all Q<Button>() calls return non-null. Why do only some buttons respond?"

**Expected Outcome:**
- Direct to Event Debugger: filter for `ClickEvent` and `PointerDownEvent`
- Click broken buttons and observe propagation path — look for `StopPropagation` on a parent
- Identify likely cause: parent container has `RegisterCallback<ClickEvent>` that calls `evt.StopPropagation()`, or parent has `pickingMode: Position` intercepting pointer events
- Check `pickingMode` on buttons and all ancestors
- Reference event propagation phases (TrickleDown → Target → BubbleUp)
- Should NOT recommend removing and re-adding callbacks as first step

---

### Prompt 18 — Memory Leak After Repeated Screen Navigation

**Prompt:**
> "Our mobile game has 5 tabs. QA reports that after navigating between tabs ~50 times, memory climbs from 180MB to 320MB and never drops. Each tab is a UIView subclass with Initialize()/Dispose(). We use the Dragon Crashers UIManager ShowModalView() pattern. Dispose() calls UnregisterCallback for all event handlers. What's the debugging approach to find the leak?"

**Expected Outcome:**
- Memory Profiler snapshot comparison workflow: Snapshot A → navigate → Snapshot B → Compare → filter by VisualElement
- Check Common Leak Sources: unregistered callbacks (lambda closures capturing `this`), static references, bindings not unbound, VisualElements in static collections
- Specifically mention Dragon Crashers patterns: verify `UIView.Dispose()` calls `base.Dispose()`, check `OnDisable` unsubscribes from static event bus, verify fire-and-forget async methods
- Recommend `UIDebugUtils.ValidateBindings()` for orphaned bindings
- Must give specific snapshot-compare-filter workflow, not just "use a profiler"

---

### Prompt 19 — Theme Not Switching on Orientation Change with Profiler Verification

**Prompt:**
> "We implemented a theme system with ThemeManager having 6 compound themes (Landscape/Portrait × Default/Dark/Holiday). The first rotation works, but subsequent rotations stop applying the theme — UI stays stuck. ThemeEvents.ThemeChanged IS firing. Additionally, after 3-4 rotations, we see UIR.Layout spikes of 3-4ms in the Profiler. Debug both the theme sticking issue and the performance regression."

**Expected Outcome:**
- Theme debugging: enable `m_Debug` flag, trace compound name construction, check `ThemeSettings` list completeness, verify TSS/PanelSettings asset references, check `[ExecuteInEditMode]` caveat, use Debugger "Matching USS Selectors"
- Performance debugging: Profiler > UI Details module, check `UIR.Layout` call count, identify if `SetPanelSettings()` triggers full visual tree rebuild, check `GeometryChangedEvent` cascading

---

### Prompt 20 — Data Binding Failures with Silent Async Errors in Mail Screen

**Prompt:**
> "We're building a mail/inbox screen. Problems: (1) Timestamp Label always shows 'Jan 1, 0001' despite correct DateTime values in data source, (2) 'Claim Reward' button disables but reward animation freezes mid-state with no console errors, (3) After opening 15+ mail items, scrolling becomes janky. Binding UXML: `binding-path='dataSource.FormattedTimestamp'`. Data source has `[CreateProperty] public string FormattedTimestamp => ReceivedAt.ToString('MMM d, yyyy')`. Claim reward uses `_ = ClaimRewardRoutineAsync()`. Debug all three."

**Expected Outcome:**
- Issue 1: Check binding path warnings, verify case-sensitive path, use `UIDebugUtils.ValidateBindings()`, confirm `[CreateProperty]` applied and computed property fires notification
- Issue 2: Explain fire-and-forget silent exception swallowing, wrap in try/catch, register `TaskScheduler.UnobservedTaskException`, check for null references mid-animation
- Issue 3: Profiler > UI Details, verify `fixedItemHeight` on ListView, check for layout thrashing in `bindItem`, use Frame Debugger for draw call count, verify `unbindItem` cleanup

---

## 5. UI Toolkit Mobile

**Skill file:** `ui-toolkit-mobile/SKILL.md`
**Covers:** Touch input (44px targets), gesture detection, safe areas, orientation, virtual keyboard, mobile performance budgets, battery-conscious patterns, haptic feedback, platform detection, 3D-to-UI alignment

---

### Prompt 21 — Mobile E-Commerce Product Browser

**Prompt:**
> "I'm building a mobile game shop screen using UI Toolkit. The screen needs: a scrollable grid of product cards (3 columns portrait, 4 columns landscape), each card with image/name/price/Buy button, bottom navigation bar with 3 tabs, safe areas on notched devices, touch press feedback (scale + color shift), ListView virtualization for 200+ products. Target iOS and Android. Must stay under 15 draw calls, 200 visible elements. All interactive elements at least 44×44px."

**Expected Outcome:**
- UXML with `screen-root` → `content-area` + `bottom-nav` structure
- USS with 44×44px touch targets, `:active` scale/color transitions, bottom-nav in thumb zone with safe area padding
- C# with SafeAreaBorder (borderWidth approach), `[ExecuteInEditMode]`
- ListView virtualization pattern, NOT 200 instantiated elements
- USS selectors max 2-3 levels deep, `UsageHints.DynamicTransform` on animations
- Platform detection via `MobilePlatform.ApplyPlatformClasses()`
- Performance commentary referencing mobile budget table

---

### Prompt 22 — Swipe-to-Delete Notification Center with Haptics

**Prompt:**
> "I need a notification center panel for my mobile RPG. Requirements: vertical list of notifications, swipe right to dismiss with slide-out animation, long-press for context menu (Mark as Read, Delete All, Mute), tap to navigate, haptic feedback (light for tap, medium for swipe, heavy for delete-all), panel slides in from bottom and snaps back on swipe-down. I want the GestureDetector Manipulator pattern."

**Expected Outcome:**
- Full `GestureDetector` Manipulator with `OnSwipe`, `OnLongPress`, `OnTap` events — pointer capture/release, thresholds
- Long-press via `schedule.Execute().StartingIn()` pattern
- `HapticFeedback` static class with iOS/Android native calls
- USS transitions using transform-only properties (`translate`, `scale`, `opacity`)
- Touch targets ≥ 44px on all items
- Bottom-anchored panel following thumb zone principles

---

### Prompt 23 — Mobile Login/Registration Form with Virtual Keyboard

**Prompt:**
> "Our game needs a login/registration screen with username, email, password fields (with show/hide toggle), Login/Register tab switching, a Submit button at the bottom, and virtual keyboard handling so the focused field scrolls into view. Must work on phones and tablets. Support swipe-left/right to switch tabs. The keyboard keeps covering my input fields on Android."

**Expected Outcome:**
- `VirtualKeyboardHandler` with `FocusInEvent`/`FocusOutEvent`, `ScrollToField()` with 300ms delay
- `GetKeyboardHeight()` using `TouchScreenKeyboard.area.height` with platform guards
- Dynamic `paddingBottom` on ScrollView matching keyboard height
- Tab switching with `GestureDetector.OnSwipe` for horizontal gesture
- All inputs meeting 44×44px minimum
- Tablet centering: `.platform--tablet .content-column { max-width: 720px; }`
- No hover-dependent UI (skill explicitly warns against this on mobile)

---

### Prompt 24 — Orientation-Adaptive Character Select with 3D-to-UI Alignment

**Prompt:**
> "Build a character select screen: Portrait mode has character preview (3D model) at top, info+stats below, abilities at bottom. Landscape mode has preview left (40%), info panel right (60%), abilities along bottom. A 3D character model must align to a VisualElement panel via PositionToVisualElement. When device rotates, layout transitions smoothly and 3D model repositions. Safe area on all edges for iPhone 15 Pro and Galaxy S24. Use MediaQuery + ThemeEvents event-driven approach, not polling."

**Expected Outcome:**
- `MediaQuery` with `GeometryChangedEvent`, `k_LandscapeMin = 1.2f`, `MediaAspectRatio` enum
- `OrientationHandler` toggling `.orientation--portrait`/`.orientation--landscape` classes
- USS rules: portrait = `flex-direction: column`, landscape = `flex-direction: row`
- `PositionToVisualElement` with `worldBound` → screen → world position pipeline
- `SafeAreaBorder` with borderWidth approach, `[ExecuteInEditMode]`, configurable multiplier
- Safe area on ALL four edges (critical for landscape side notches)
- All interactive elements ≥ 44×44px

---

### Prompt 25 — Battery-Conscious Live Dashboard with Performance Monitoring

**Prompt:**
> "I need a real-time dashboard showing player stats, event countdown timers, friend activity feed, and a toggleable FPS counter. Critical: when on battery, throttle to 30fps and reduce animation complexity. On charger, run at 60fps. Use OLED-friendly dark theme with pure black backgrounds. Friend feed uses ListView virtualization (100+ items). Timers should NOT trigger layout recalculations. Add platform-specific styling. I want the FpsCounter pattern from Dragon Crashers and the battery management strategy."

**Expected Outcome:**
- `FpsCounter` with ring buffer (50 frames), `Application.targetFrameRate`, `SettingsEvents` wiring
- Battery management: `Application.targetFrameRate = onBattery ? 30 : 60`
- OLED USS: pure black backgrounds `rgb(0,0,0)`, cards at `rgb(18,18,18)`
- `UsageHints.DynamicTransform` on timer elements and XP bar
- `element.visible = false` vs `DisplayStyle.None` distinction
- ListView virtualization for friend feed
- Performance budget: <15 draw calls, <200 visible elements, <8MB texture
- `MobilePlatform.ApplyPlatformClasses()` with tablet/mobile overrides

---

## 6. UI Toolkit Theming

**Skill file:** `ui-toolkit-theming/SKILL.md`
**Covers:** TSS/USS cascade, design tokens, semantic color tokens, typography scale, spacing systems, runtime theme switching, compound themes, BEM naming, multi-panel synchronization

---

### Prompt 26 — Full Design Token System with Dark/Light Theme Toggle

**Prompt:**
> "Build a complete design token architecture for a Settings screen. Include: `tokens.uss` with full `:root` variable palette (primary, secondary, background, text, border, status colors), 4px spacing scale, typography scale, border radius tokens. Create `tokens-dark.uss` overriding semantic color mappings. Build `light-theme.tss` and `dark-theme.tss` importing shared USS but differing in token file. Implement ThemeManager that swaps `PanelSettings.themeStyleSheet`, persists via PlayerPrefs, exposes OnThemeChanged event. Create Settings UXML with theme toggle — all styled exclusively with `var(--color-*)` and `var(--space-*)` tokens. No hardcoded colors anywhere."

**Expected Outcome:**
- `tokens.uss` with 30+ `:root` custom properties
- `tokens-dark.uss` overriding ~15 semantic color tokens
- Two TSS files importing shared USS + respective token file
- `ThemeManager.cs` with `ToggleTheme()`, `SetTheme()`, `PlayerPrefs` persistence, `OnThemeChanged` event
- `settings-panel.uxml` consuming only semantic token classes
- Zero hardcoded color/spacing values in any file

---

### Prompt 27 — Dragon Crashers–Style Compound Theme System (Orientation × Season)

**Prompt:**
> "Implement the Dragon Crashers compound theming pattern for a lobby screen supporting 2 orientations × 3 seasonal decorations = 6 compound themes. Create the full TSS inheritance chain: base RuntimeTheme-Default.tss, orientation TSS files importing per-screen USS, seasonal variant TSS files layering Decoration USS. Implement Decoration USS with visibility toggling. Build ThemeManager with List<ThemeSettings> mapping compound names to TSS+PanelSettings assets. Wire to ThemeEvents.ThemeChanged and MediaQueryEvents.AspectRatioUpdated, preserving season suffix on orientation change and vice versa. Include SettingsScreenController constructing compound theme string."

**Expected Outcome:**
- 7 TSS files with correct `@import` inheritance chain
- 3 Decoration USS files with mutual visibility exclusion
- 6 orientation USS files (3 screens × 2 orientations) with layout axis swap
- `ThemeSettings` struct with `theme`, `tss`, and `panelSettings` fields
- `ThemeManager.cs` handling both event sources, splitting/recombining compound names with `"--"` delimiter
- Event flow documented for both season change and orientation change

---

### Prompt 28 — Theme-Aware Custom Control Library with BEM Naming and USS Cascade

**Prompt:**
> "Build a library of 3 theme-aware custom controls using [UxmlElement]: StatusBadge (Success/Warning/Error), ThemeCard (header/body/footer), ToggleSwitch (custom track colors). Follow BEM naming, all visuals from USS var() tokens, static readonly string class constants. Include [UxmlAttribute] properties. Create companion USS files. Demonstrate USS cascade/specificity showing how a parent's theme class overrides child defaults without exceeding 2-class specificity. Verify theme switching re-resolves all var() without C# intervention."

**Expected Outcome:**
- 3 C# files with `[UxmlElement]`, BEM class constants, `[UxmlAttribute]` properties
- `StatusBadge` with `AddToClassList`/`RemoveFromClassList` pattern
- `ThemeCard` composing child elements with BEM sub-element classes
- `ToggleSwitch` with custom track/thumb elements, click-toggling USS class
- 3 USS files using exclusively `var()` token references
- Specificity demonstration with comment explaining cascade resolution

---

### Prompt 29 — Runtime Theme Extension — High-Contrast Accessibility Theme

**Prompt:**
> "Extend an existing light/dark theme system to support a third High Contrast accessibility theme. Create tokens-high-contrast.uss with WCAG AAA values: pure black backgrounds, white text, 3px borders, bright yellow focus indicators, enlarged font sizes. Build high-contrast-theme.tss. Extend ThemeManager to enum-based ThemeMode { Light, Dark, HighContrast }, update PlayerPrefs to int key. Create a ThemeSelector [UxmlElement] custom control with 3 radio-style buttons that is itself theme-aware (subscribes to OnThemeChanged and updates its own USS class)."

**Expected Outcome:**
- `tokens-high-contrast.uss` with WCAG AAA overrides
- `high-contrast-theme.tss` with correct `@import` chain
- Updated `ThemeManager.cs` with `ThemeMode` enum, 3-way switch, `Action<ThemeMode>` event
- `ThemeSelector` custom control with `AttachToPanelEvent`/`DetachFromPanelEvent` lifecycle
- Demonstration that existing components resolve tokens correctly under high-contrast without code changes

---

### Prompt 30 — Multi-Panel Theme Synchronization with Per-Panel Overrides

**Prompt:**
> "Design theming for a game using multiple PanelSettings — a main HUD panel and a separate overlay/popup panel. Both share the same base theme but the overlay adds overrides: semi-transparent background, elevated shadow widths, blur-hint class. Create two PanelSettings with different sortingOrder. Build MultiPanelThemeManager that synchronizes theme switches across both. Overlay uses dedicated overlay-theme-light/dark.tss importing base + overlay-overrides.uss. Implement a ModalDialog [UxmlElement] on the overlay panel. Show that theme changes mid-modal correctly update both backdrop and content."

**Expected Outcome:**
- 4 TSS files: `main-light.tss`, `main-dark.tss`, `overlay-light.tss`, `overlay-dark.tss`
- `overlay-overrides.uss` with overlay-specific token overrides
- `MultiPanelThemeManager.cs` synchronizing 2 PanelSettings simultaneously
- `ModalDialog` custom control with backdrop using `var(--color-bg-overlay)`
- `ShowModal()`/`HideModal()` methods
- Demonstration: open modal → toggle theme → both update → close modal

---

## 7. UI Toolkit Patterns

**Skill file:** `ui-toolkit-patterns/SKILL.md`
**Covers:** Tabbed navigation, inventory grids, modal/popup dialogs, stateful buttons, message lists, scroll snapping, async task animation, experimental animation API, world-to-panel positioning, composite view pattern, category filtering

*Note: These prompts were generated from the SKILL.md content to replace unrecoverable session data.*

---

### Prompt 31 — Tabbed Navigation with Dragon Crashers Convention-Based Mapping

**Prompt:**
> "I'm building a hero detail screen for a mobile RPG with 4 tabs: Overview, Skills, Equipment, and Lore. I want to use the Dragon Crashers tabbed navigation pattern where tab buttons and content panels are linked by naming convention (e.g., `skills-tab` maps to `skills-content` via suffix replacement). The selected tab should have an active state with a bottom highlight bar, and unselected content panels should use `display: none`. Requirements: (1) Use `TabbedMenuController` as a plain C# class with a `TabbedMenuConfig` struct for suffix/class configuration, (2) Support two approaches — the UXML inline class approach and the TabbedMenuController approach — and explain when to use each, (3) Include keyboard/gamepad navigation via `NavigationMoveEvent`, (4) All visual state must be driven by USS class toggling, no inline styles."

**Skill Areas Tested:**
- Dragon Crashers TabbedMenuController pattern with convention-based suffix replacement
- `TabbedMenuConfig`/`TabbedMenuIDs` struct with `tabClassName`, `selectedTabClassName`, `unselectedContentClassName`, `tabNameSuffix`, `contentNameSuffix`
- Two tab approaches: inline UXML classes vs programmatic controller
- `NavigationMoveEvent` handling for gamepad/keyboard
- USS class toggling for all visual state

**Expected Outcome:**
- `TabbedMenuConfig` struct with all 5 configuration fields
- `TabbedMenuController` plain C# class with `RegisterTabCallbacks()`, tab click handler performing suffix replacement to find matching content
- USS for selected/unselected tab states (`.tab--selected { border-bottom-color: ... }`) and content visibility (`.content--hidden { display: none; }`)
- `NavigationMoveEvent` handler cycling through tabs
- UXML demonstrating consistent `*-tab` / `*-content` naming convention
- No inline style changes in C# — all via `AddToClassList`/`RemoveFromClassList`

---

### Prompt 32 — Inventory Grid with ListView Virtualization vs ScrollView Instantiation

**Prompt:**
> "I need to build an inventory grid for a mobile RPG that can hold up to 500 items. Each item slot shows an icon, rarity border color, quantity badge, and an equipped indicator. I want you to show me BOTH approaches from the Patterns skill: (1) ListView with `makeItem`/`bindItem`/`unbindItem` virtualization, and (2) ScrollView + manual instantiation with `VisualTreeAsset.Instantiate()`. For each approach, provide complete UXML, USS, and C# code. Then give me a clear recommendation on which to use and why, referencing the performance trade-offs (draw calls, instantiation cost, memory). The grid should be 5 columns wide and support item selection with a highlight border. Clicking an item should fire a static `InventoryEvents.ItemSelected` event."

**Skill Areas Tested:**
- ListView virtualization pattern: `makeItem` creates empty templates, `bindItem` populates data, `unbindItem` cleans up
- ScrollView + instantiation approach: `VisualTreeAsset.Instantiate()` in a loop, manual cleanup
- Performance comparison: ListView recycles (~20 visible items regardless of data size) vs ScrollView instantiates all 500
- Grid layout in USS: `flex-wrap: wrap` with fixed-width items
- Static event bus pattern for item selection
- `fixedItemHeight` for ListView performance

**Expected Outcome:**
- Complete code for BOTH approaches with UXML, USS, C#
- ListView approach using `makeItem` that creates `VisualTreeAsset.Instantiate()`, `bindItem` that populates icon/rarity/quantity, `unbindItem` that clears state
- ScrollView approach using a loop with `Instantiate()` and manual `Add()` to a flex-wrap container
- Clear recommendation: ListView for 500+ items (virtualization reduces visible elements from 500 to ~20), ScrollView acceptable for <50 static items
- Performance numbers: draw call impact, memory comparison
- `InventoryEvents.ItemSelected` static event fired on click
- Item selection highlight via USS class toggle

---

### Prompt 33 — Modal Dialog System with Backdrop, Animation, and Focus Trapping

**Prompt:**
> "Implement a reusable modal dialog system for a mobile game. The system should support: (1) A semi-transparent backdrop that blocks interaction with elements behind the dialog, (2) Dialog content slides in from the bottom with a CSS transition, (3) Dismissal by tapping the backdrop or pressing a close button, (4) Focus trapping — keyboard/gamepad navigation stays within the dialog, (5) A `ModalManager` that supports stacking (opening a confirmation dialog on top of an existing dialog). Show the complete UXML for a 'Quit Confirmation' dialog, USS with animation transitions, and C# ModalManager with `ShowModal(VisualTreeAsset dialogTemplate)` and `DismissModal()` methods. The backdrop should use the async task animation pattern for a fade-in effect."

**Skill Areas Tested:**
- Modal/Popup Dialog pattern from the skill with backdrop and content separation
- USS transitions on transform properties (`translate`, `opacity`) for slide-in animation
- Backdrop interaction blocking via `pickingMode: Position` on a full-screen VisualElement
- Focus trapping using `NavigationMoveEvent` and `focusController`
- Async task animation: `_ = FadeInBackdropAsync()` with fire-and-forget pattern
- Dialog stacking with a Stack data structure
- `VisualTreeAsset.Instantiate()` for dialog template creation

**Expected Outcome:**
- `ModalManager` C# class with `Stack<ModalEntry>`, `ShowModal()` instantiating templates, `DismissModal()` popping stack
- Backdrop VisualElement with `pickingMode: Position`, click handler calling `DismissModal()`
- USS: `.modal-backdrop { background-color: rgba(0,0,0,0.5); }`, `.modal-content { transition: translate 0.3s ease-out; }`
- Async fade-in using `_ = FadeInAsync()` with try/catch, manipulating `opacity` via USS class toggle
- Focus trapping: `NavigationMoveEvent` handler preventing focus from leaving dialog
- UXML for quit confirmation with title, message, Confirm/Cancel buttons
- Proper cleanup: event unregistration on dismiss, backdrop removal

---

### Prompt 34 — Stateful Button System with Loading Spinner and Cooldown

**Prompt:**
> "Create a reusable stateful button system for a mobile game's ability bar. Each ability button has 4 states: (1) Normal — ready to use, (2) Cooldown — shows a radial countdown overlay and remaining seconds, (3) Loading — shows a spinner animation while the server processes the ability, (4) Disabled — grayed out when requirements not met (e.g., insufficient mana). Implement this as a `[UxmlElement]` custom control called `AbilityButton` with a `ButtonState` enum and `[UxmlAttribute]` for icon, cooldown duration, and mana cost. All visual states must be driven by USS classes (`.ability-btn--cooldown`, `.ability-btn--loading`, `.ability-btn--disabled`). The cooldown timer must NOT cause layout recalculation — use transform-only updates. The loading spinner should use the Dragon Crashers async timing strategy with `Awaitable.NextFrameAsync()`. Include USS with transition animations between states."

**Skill Areas Tested:**
- Stateful button pattern with multiple visual states
- `[UxmlElement]` custom control with `[UxmlAttribute]` properties
- USS class-driven state management (no inline styles)
- Transform-only animations (no layout thrashing) using `UsageHints.DynamicTransform`
- Dragon Crashers async timing: `_ = CooldownAsync()` with `Awaitable.NextFrameAsync()` loop
- Transition timing strategies from the skill (Approach 2: `Awaitable.NextFrameAsync()` loop for frame-accurate timing)

**Expected Outcome:**
- `AbilityButton` `[UxmlElement]` with `ButtonState` enum, state transition methods
- `SetState(ButtonState)` using `EnableInClassList` for each state class
- Cooldown async method using `Awaitable.NextFrameAsync()` loop, updating a `Label.text` for remaining time
- `UsageHints.DynamicTransform` on the cooldown overlay element
- Loading spinner via USS `rotate` transition or async rotation
- USS with `.ability-btn--cooldown`, `.ability-btn--loading`, `.ability-btn--disabled` state classes
- Transition animations between states using `transition` property on `opacity`, `scale`
- Proper `Dispose()` or cancellation for running async methods

---

### Prompt 35 — Chat Message List with Composite View and Scroll-to-Bottom

**Prompt:**
> "Build a real-time chat/message list screen following the Dragon Crashers Mail screen composite view pattern. The screen has: (1) a header with channel name and online count, (2) a virtualized message list where each message shows sender avatar, name, timestamp, and message body, (3) a message input area at the bottom with a TextField and Send button, (4) auto-scroll to bottom when new messages arrive (but NOT when the user has scrolled up to read history), (5) different visual styling for own messages vs others (WhatsApp-style left/right alignment). Implement using the composite view pattern where `ChatView` manages `ChatHeaderView`, `ChatMessageListView`, and `ChatInputView` as sub-views. Use `ListView` for the message list. Communication between sub-views goes through a static `ChatEvents` bus. Include the scroll-to-bottom logic using `ScrollView.scrollOffset` and `GeometryChangedEvent`."

**Skill Areas Tested:**
- Composite view pattern from Dragon Crashers (parent manages sub-view lifecycles)
- ListView with `makeItem`/`bindItem` for message items
- Message list scroll behavior: auto-scroll on new message, pause auto-scroll when user scrolls up
- `GeometryChangedEvent` for scroll-to-bottom after content size changes
- `ScrollView.scrollOffset` manipulation
- Static event bus (`ChatEvents`) for sub-view communication
- BEM naming for own-message vs other-message styling
- Sub-view lifecycle with `Dispose()` cascading

**Expected Outcome:**
- `ChatView` following composite view pattern: creates and manages 3 sub-views, cascades `Dispose()`
- `ChatMessageListView` with ListView, `makeItem` creating message bubble template, `bindItem` populating and toggling `.message--own` / `.message--other` classes
- Auto-scroll logic: track `isScrolledToBottom` flag, on new message call `schedule.Execute(() => scrollView.scrollOffset = new Vector2(0, float.MaxValue))` only if flag is true
- `GeometryChangedEvent` on the ListView content container to detect content size changes
- `ChatEvents` static class with `MessageSent`, `MessageReceived`, `ChannelSwitched` events
- USS with left/right alignment for own vs other messages using `flex-direction` and `align-self`
- `ChatInputView` with TextField and Button, firing `ChatEvents.MessageSent` on click/Enter key

---

## 8. UI Toolkit Performance

**Skill file:** `ui-toolkit-performance/SKILL.md`
**Covers:** Transform vs layout animations, UsageHints, ListView virtualization, draw call optimization, element pooling, GC-free patterns, profiling workflow, Dragon Crashers FPS counter, world-to-panel cost, async/await tradeoffs

*Note: These prompts were generated from the SKILL.md content to replace unrecoverable session data.*

---

### Prompt 36 — Transform vs Layout Animation Audit

**Prompt:**
> "I have a card-flipping animation for a memory matching game. When the player taps a card, it currently animates by changing `width` from 120px to 0px and back (to simulate a flip), changes `backgroundColor` through 3 colors, and repositions using `left`/`top`. Each animation is done with inline C# style changes in a coroutine. There are 20 cards on screen. After 10 card flips, the game stutters noticeably on a mid-range Android phone. Review this approach and rewrite it using only transform-based, GPU-accelerated properties. Explain which CSS properties trigger layout recalculation vs which are transform-only. Set appropriate `UsageHints` on animated elements. Show the before/after profiler impact."

**Skill Areas Tested:**
- Transform vs layout animation distinction: `translate`, `rotate`, `scale`, `opacity` are GPU-accelerated; `width`, `height`, `left`, `top`, `margin`, `padding` trigger layout recalculation
- `UsageHints.DynamicTransform` for elements animated via transform properties
- `UsageHints.DynamicColor` for elements with frequently changing colors
- USS `transition` property for declarative animation
- Profiling workflow: Profiler > UI Details module, checking `UIR.Layout` vs `UIR.TransformUpdate` markers
- Inline style elimination in favor of USS class toggling

**Expected Outcome:**
- Replace `width` animation with `scale: 1 0 1` (scaleX 1→0→1) for flip effect
- Replace `left`/`top` with `translate` for repositioning
- Replace inline `backgroundColor` with USS class toggle (`.card--state-1`, `.card--state-2`, `.card--state-3`)
- Set `UsageHints.DynamicTransform` on all card elements
- USS with `transition: scale 0.2s ease-in-out, translate 0.3s ease-out`
- Profiler comparison: before shows `UIR.Layout` spikes per card flip, after shows only `UIR.TransformUpdate` (much cheaper)
- Explanation: layout properties invalidate the layout tree causing O(n) recalculation; transform properties modify the render mesh only

---

### Prompt 37 — ListView Virtualization Performance Deep Dive

**Prompt:**
> "I have a leaderboard screen that displays 10,000 player entries. Currently using a ScrollView with 10,000 instantiated VisualElements — each with a rank Label, name Label, score Label, and avatar Image. The initial load takes 3 seconds and scrolling stutters. Rewrite using ListView with virtualization. But I also need: (1) Variable item heights (top 3 players have larger cards), (2) Click-to-select with highlight, (3) Lazy loading of avatar textures (only load when item becomes visible in `bindItem`), (4) Proper cleanup in `unbindItem` to cancel pending texture loads. Show the complete implementation, explain how virtualization works internally (item pool, recycling), and provide the performance metrics to expect."

**Skill Areas Tested:**
- ListView virtualization architecture: item pool, `makeItem`/`bindItem`/`unbindItem` lifecycle
- `fixedItemHeight` for optimal performance vs dynamic height trade-offs
- `unbindItem` for cleanup (cancelling async operations, clearing textures)
- Lazy resource loading in `bindItem` — scheduling texture loads, handling recycled items
- Performance expectations: ~20 visible items regardless of data size, near-zero instantiation cost after initial pool
- Dragon Crashers `Instantiate` vs `ListView` comparison from the skill

**Expected Outcome:**
- ListView setup with `fixedItemHeight` set to standard row height (explain that variable height requires `fixedItemHeight = -1` but has performance cost)
- `makeItem` creating a row template with rank/name/score labels and avatar Image
- `bindItem` populating data, initiating async texture load with cancellation token
- `unbindItem` cancelling pending texture loads and clearing avatar texture to avoid visual artifacts on recycled items
- Selection handling via `ListView.selectionChanged` event (not per-item click handlers)
- Performance comparison: ScrollView with 10,000 elements (~300MB, 3s load) vs ListView (~20 visible, <50ms, <5MB)
- Explanation of internal recycling: ListView maintains a pool of ~20-30 items, calls `unbindItem` → `bindItem` when scrolling

---

### Prompt 38 — Draw Call Optimization and Batching

**Prompt:**
> "Our game's main HUD has 47 draw calls according to the Frame Debugger, and we need to get it under 15 for mobile. The HUD has: a top bar with currency icons (4 different sprites), health/mana bars with gradient fills, 5 ability buttons with unique icons, a minimap overlay, damage number popups that appear and fade, and a chat bubble indicator. Using the Performance skill's draw call optimization guidelines, audit this setup and provide specific steps to reduce draw calls. Explain what breaks batching in UI Toolkit and how to fix each case."

**Skill Areas Tested:**
- Draw call optimization: texture atlasing, same-material batching, render order
- What breaks UI Toolkit batching: different textures, stencil/mask changes, different materials, overlapping opaque/transparent
- Frame Debugger workflow for counting and analyzing draw calls
- Sprite atlas strategy for UI icons
- `UsageHints.MaskContainer` implications for stencil draw calls
- Reducing overdraw with opaque backgrounds

**Expected Outcome:**
- Pack all currency icons + ability icons into a single Sprite Atlas → reduces draw calls from 9 separate textures to 1
- Health/mana gradient fills: use a single gradient texture atlas or procedural USS gradient
- Damage number popups: element pooling instead of creating/destroying (each unique element is a draw call during creation frame)
- Chat bubble: ensure it uses the same atlas as other icons
- Minimap: if using RenderTexture, it's always a separate draw call — accept this
- Stencil analysis: ScrollView/mask elements add 2 extra draw calls each (stencil push/pop)
- Target architecture: 1 (atlas) + 1 (minimap RT) + 2 (scrollview stencil) + 2-3 (text) = ~7-9 draw calls
- Frame Debugger step-by-step: Window > Analysis > Frame Debugger > filter for UIR

---

### Prompt 39 — Element Pooling and GC-Free Patterns

**Prompt:**
> "Our mobile game has a combat system that creates floating damage numbers, status effect icons, and buff/debuff timers on the HUD. Currently, each damage number creates a new Label with `new Label()`, adds it to the visual tree, runs an async fade-out animation, then calls `RemoveFromHierarchy()`. During intense combat, this creates 30-50 elements per second, causing GC spikes of 2-3ms every few seconds. Implement an element pool system that pre-allocates elements and recycles them. Also audit the code for other GC allocation patterns: string concatenation in damage display (`$"{damage}"` vs `StringBuilder`), boxing in event callbacks, and LINQ usage in hot paths. Reference the GC-free patterns from the Performance skill."

**Skill Areas Tested:**
- Element pooling pattern: `Stack<VisualElement>` pool, `Get()`/`Return()` API
- Pre-allocation: create pool elements in `Initialize()`, hide with `display: none` or `visible = false`
- GC-free string formatting: `StringBuilderPool` or cached `StringBuilder` vs string interpolation
- Boxing avoidance: `ChangeEvent<int>.value` boxing in callbacks
- LINQ in hot paths: `.Where().ToList()` allocates — use for-loops instead
- Object lifecycle: `Return()` resets element state before returning to pool
- Dragon Crashers patterns: `Instantiate` cost analysis, event subscription lifecycle

**Expected Outcome:**
- `UIElementPool<T>` generic class with `Stack<T>` backing, `Get()` removing from stack and showing element, `Return()` hiding and pushing back
- Pre-allocation of 50 damage labels in `Initialize()` with `display: none`
- Damage number flow: `var label = pool.Get()` → set text → start async animation → `pool.Return(label)` on completion
- GC audit findings: replace `$"{damage}"` with `label.text = damage.ToString()` (or cached StringBuilder for complex formats)
- Replace LINQ `.Where().Select().ToList()` with manual for-loop and pre-allocated list
- Avoid lambda closures that capture local variables in hot paths (use method groups or cached delegates)
- Estimated GC reduction: from 2-3ms spikes to near-zero allocation in combat UI updates

---

### Prompt 40 — Full Profiling Workflow — Diagnosing a Janky Inventory Screen

**Prompt:**
> "Our inventory screen runs at 60fps when empty but drops to 25fps when displaying 200 items. The screen has a ScrollView with a flex-wrap grid, each item has an icon Image, rarity border, quantity Label, and an 'Equipped' indicator. Players report the screen 'hitches' when first opening and when scrolling fast. I need a complete profiling workflow: (1) Use Unity Profiler > UI Details module to identify the bottleneck, (2) Use Frame Debugger to count draw calls, (3) Check for layout thrashing in the USS, (4) Diagnose the initial hitch. Apply the Dragon Crashers profiling patterns including FPS counter integration, and recommend specific fixes with expected performance improvements."

**Skill Areas Tested:**
- Complete profiling workflow from the Performance skill
- Unity Profiler > UI Details markers: `UIR.Layout`, `UIR.RenderChainUpdate`, `UIR.DrawChain`
- Frame Debugger for draw call analysis
- Layout thrashing detection: reading `resolvedStyle` then writing style in same frame
- Initial hitch analysis: `VisualTreeAsset.Instantiate()` cost for 200 items
- Dragon Crashers FPS counter pattern for real-time monitoring
- ScrollView vs ListView decision based on profiling data
- `UsageHints` application based on profiler findings

**Expected Outcome:**
- Step-by-step profiling workflow:
  1. Open Profiler, connect to device, record while opening inventory
  2. UI Details module: identify `UIR.Layout` taking >5ms (200 items × layout calculation)
  3. Frame Debugger: count draw calls (likely 200+ without atlas)
  4. Check USS for layout-triggering properties in animations or hover states
- Initial hitch diagnosis: 200× `Instantiate()` is the bottleneck → recommend ListView virtualization or staggered instantiation
- Scroll jank diagnosis: ScrollView with 200 elements = no virtualization → every element participates in layout
- Specific fixes:
  - Replace ScrollView with ListView (reduce visible from 200 to ~20)
  - Atlas all item icons (reduce draw calls from 200 to 1)
  - Add `UsageHints.DynamicTransform` on hover-animated elements
  - Set `fixedItemHeight` on ListView for optimal scroll performance
- Expected improvement: 25fps → 60fps, initial load from 500ms to <50ms
- FPS counter integration for QA validation

---

## 9. UI Toolkit Responsive

**Skill file:** `ui-toolkit-responsive/SKILL.md`
**Covers:** Flexbox deep dive, length units, safe area API, screen adaptation, aspect ratio handling, responsive breakpoints (ScreenSizeClassifier), responsive card grid, sidebar collapse, Dragon Crashers MediaQuery/SafeAreaBorder/ThemeManager patterns

*Note: These prompts were generated from the SKILL.md content to replace unrecoverable session data.*

---

### Prompt 41 — Responsive Card Grid with Flexbox and Breakpoints

**Prompt:**
> "Build a responsive product card grid for a mobile game shop that adapts to different screen sizes. The grid should show: 2 columns on phones in portrait, 3 columns on phones in landscape, 4 columns on tablets. Each card has an image (aspect ratio 4:3), product name, price, and a Buy button. Use the `ScreenSizeClassifier` breakpoint pattern from the Responsive skill with `GeometryChangedEvent` to detect screen size changes and apply USS classes (`.screen--compact`, `.screen--medium`, `.screen--expanded`). The cards should use percentage-based widths with `calc()` for gaps. Include proper spacing using the 4px grid system and ensure the layout fills available space with `flex-grow`."

**Skill Areas Tested:**
- `ScreenSizeClassifier` pattern with `GeometryChangedEvent` callback
- `ScreenSizeClass` enum (Compact/Medium/Expanded) with configurable breakpoints
- `EnableInClassList` for applying breakpoint-specific USS classes
- Flexbox layout: `flex-wrap: wrap`, percentage widths, `flex-grow`, `flex-shrink`
- Length units: `%`, `px`, and understanding of when to use each
- USS `calc()` for width calculations accounting for gaps
- 4px grid spacing system via custom properties

**Expected Outcome:**
- `ScreenSizeClassifier` C# component with `GeometryChangedEvent`, comparing `panel.resolvedStyle.width` against breakpoints
- USS rules:
  - `.screen--compact .product-card { width: calc(50% - 8px); }` (2 columns)
  - `.screen--medium .product-card { width: calc(33.33% - 8px); }` (3 columns)
  - `.screen--expanded .product-card { width: calc(25% - 8px); }` (4 columns)
- Card layout using flexbox: container with `flex-wrap: wrap`, `gap: 8px` (or margin fallback since USS may not support `gap`)
- Image with `aspect-ratio` or fixed height + `object-fit` equivalent
- `flex-grow: 1` on content area, `flex-shrink: 0` on bottom nav
- All spacing using `var(--space-*)` tokens from 4px scale

---

### Prompt 42 — Safe Area Handling with Dragon Crashers BorderWidth Pattern

**Prompt:**
> "Implement comprehensive safe area handling for a mobile game UI that must work on iPhone 15 Pro (Dynamic Island + home indicator), iPad Pro (no notch but status bar), Samsung Galaxy S24 (punch-hole camera), and Samsung Galaxy Z Fold5 (varying safe areas in folded/unfolded). Show BOTH safe area approaches from the Responsive skill: (1) the Dragon Crashers `SafeAreaBorder` using `borderWidth` with configurable multiplier, and (2) the padding-based `SafeAreaApplier` approach. Explain why borderWidth is preferred over padding (from Dragon Crashers). The safe area must update dynamically when the device orientation changes. Include `[ExecuteInEditMode]` for editor preview and `OnValidate()` for real-time tuning."

**Skill Areas Tested:**
- `SafeAreaBorder` pattern using `borderWidth` (Dragon Crashers approach)
- `SafeAreaApplier` alternative using `paddingTop`/`paddingBottom`
- `Screen.safeArea` API and conversion to panel coordinates
- `GeometryChangedEvent` for dynamic updates on orientation change
- `[ExecuteInEditMode]` for editor preview
- `OnValidate()` for real-time multiplier tuning
- Explanation of borderWidth vs padding trade-offs
- Safe area on all 4 edges (including sides for landscape notched devices)

**Expected Outcome:**
- `SafeAreaBorder` MonoBehaviour with `[SerializeField] float m_Multiplier = 1f`, `[SerializeField] Color m_BorderColor`
- `ApplySafeArea()` method reading `Screen.safeArea`, converting to panel percentages, setting `borderTopWidth`, `borderBottomWidth`, `borderLeftWidth`, `borderRightWidth`
- `GeometryChangedEvent` registration for dynamic updates
- `[ExecuteInEditMode]` attribute on class, `OnValidate()` calling `ApplySafeArea()`
- `SafeAreaApplier` alternative using `paddingTop`/`paddingBottom` for comparison
- Clear explanation: borderWidth adds visible border (can be colored for debugging), padding pushes content inward but is invisible — Dragon Crashers uses borderWidth for easier debugging and visual confirmation
- Handling for all 4 device types with different safe area configurations

---

### Prompt 43 — Orientation-Adaptive Layout with Sidebar Collapse

**Prompt:**
> "Build an orientation-adaptive main menu with a sidebar navigation pattern. In landscape: a persistent 240px sidebar on the left with navigation items (Home, Heroes, Shop, Settings icons + labels), and the main content area takes remaining space. In portrait: the sidebar collapses to a bottom tab bar (icons only, no labels), and content area fills full width. Use the Dragon Crashers `MediaQuery` component with `GeometryChangedEvent` and `MediaAspectRatio` enum — NOT polling `Screen.orientation`. The transition between layouts should use USS class toggling on the root element (`.orientation--landscape`, `.orientation--portrait`). The sidebar items must be reusable between both orientations (same data, different visual representation). Include the `OrientationHandler` pattern that manages the class toggling."

**Skill Areas Tested:**
- Dragon Crashers `MediaQuery` component with `GeometryChangedEvent`, `k_LandscapeMin` threshold
- `MediaAspectRatio` enum (Landscape/Portrait/Undefined)
- `MediaQueryEvents.AspectRatioUpdated` event
- `OrientationHandler` managing USS class toggling via `EnableInClassList`
- Sidebar collapse pattern: sidebar visible in landscape, bottom tab bar in portrait
- USS rules swapping `flex-direction`, showing/hiding elements based on orientation class
- Reusable navigation items across both orientations

**Expected Outcome:**
- `MediaQuery` MonoBehaviour with `GeometryChangedEvent` callback, computing aspect ratio from `panel.resolvedStyle.width/height`
- `MediaAspectRatio` enum with `Landscape`, `Portrait`, `Undefined`
- `OrientationHandler` component that subscribes to `MediaQueryEvents.AspectRatioUpdated` and toggles `.orientation--landscape`/`.orientation--portrait` on root element
- USS:
  - `.orientation--landscape .sidebar { width: 240px; display: flex; flex-direction: column; }`
  - `.orientation--landscape .bottom-nav { display: none; }`
  - `.orientation--portrait .sidebar { display: none; }`
  - `.orientation--portrait .bottom-nav { display: flex; height: 56px; flex-direction: row; }`
- Navigation items with both icon + label elements, label hidden in portrait via `.orientation--portrait .nav-label { display: none; }`
- UXML with both sidebar and bottom-nav in markup, visibility controlled by USS classes

---

### Prompt 44 — PanelSettings Scale Modes and Multi-Resolution Support

**Prompt:**
> "I'm targeting 3 device categories with different PanelSettings configurations: (1) Phones (720×1280 to 1440×3200) — need `ScaleWithScreenSize` with 1080×1920 reference resolution, (2) Tablets (1536×2048 to 2732×2048) — need `ScaleWithScreenSize` with 1920×1080 reference in landscape, (3) Desktop/Editor testing — need `ConstantPixelSize` for precise debugging. Create all 3 PanelSettings assets with correct configuration. Implement a `PanelSettingsSelector` that detects the device category at startup and assigns the correct PanelSettings to the UIDocument. Explain `screenMatchMode` and when to use `MatchWidthOrHeight` vs `Expand` vs `Shrink`. Show how the same UXML/USS works across all 3 configurations without modification by using relative units (`%`, `vh`, `vw`) and `flex-grow` instead of fixed pixel values."

**Skill Areas Tested:**
- PanelSettings configuration: `scaleMode`, `referenceResolution`, `screenMatchMode`
- `ScaleWithScreenSize` mode with different reference resolutions
- `ConstantPixelSize` for editor testing
- `screenMatchMode` options: `MatchWidthOrHeight` (match slider 0-1), `Expand`, `Shrink`
- Viewport units: `vh`, `vw` (if supported), percentage units
- `flex-grow` for flexible layouts that adapt to any resolution
- Device category detection at runtime

**Expected Outcome:**
- 3 PanelSettings assets with correct configuration per device category
- `PanelSettingsSelector` MonoBehaviour checking `SystemInfo.deviceType`, `Screen.width`/`Screen.height` to classify device
- Explanation of `screenMatchMode`:
  - `MatchWidthOrHeight` with slider at 0 = match width (good for landscape games)
  - `MatchWidthOrHeight` with slider at 1 = match height (good for portrait games)
  - `MatchWidthOrHeight` with slider at 0.5 = balanced (common default)
  - `Expand` = never crop, may letterbox
  - `Shrink` = never letterbox, may crop
- USS guidelines: use `%` for widths, `flex-grow` for dynamic sizing, `px` only for touch targets (44px minimum) and borders
- Demonstration that the same UXML renders correctly on all 3 configurations

---

### Prompt 45 — Responsive Aspect Ratio Handling with World-to-UI Alignment

**Prompt:**
> "Our mobile game has a 3D game world rendered behind the UI. The UI overlays include a HUD at the top, ability bar at the bottom, and a mini character portrait that must stay aligned with the 3D character's head position. The game supports 16:9, 18:9, 19.5:9, 20:9, and 21:9 aspect ratios. Problems: (1) On ultra-wide phones (21:9), the HUD elements are too spread out horizontally, (2) The character portrait drifts from the 3D character on different aspect ratios, (3) On 4:3 tablets, the ability bar buttons are too close together. Implement aspect ratio detection using `ScreenSizeClassifier` with custom breakpoints for aspect ratio categories. Use the Dragon Crashers `PositionToVisualElement` pattern for 3D-to-UI alignment. Create USS rules that constrain HUD width with `max-width` on ultra-wide screens and add spacing on tablets. Include `GeometryChangedEvent` to re-sync the character portrait position on any layout change."

**Skill Areas Tested:**
- Aspect ratio detection and categorization
- `ScreenSizeClassifier` adapted for aspect ratio breakpoints
- Dragon Crashers `PositionToVisualElement`: `worldBound` → `GetScreenCoordinate` → `ScreenPosToWorldPos`
- `GeometryChangedEvent` for re-syncing 3D-to-UI positions
- `max-width` constraint for ultra-wide displays
- Responsive spacing adjustments per aspect ratio category
- Flexbox `justify-content: space-evenly` vs `space-between` for ability bar

**Expected Outcome:**
- `AspectRatioClassifier` variant of `ScreenSizeClassifier` with categories: `Standard` (16:9), `Tall` (18:9-19.5:9), `UltraWide` (20:9-21:9), `Wide` (4:3-16:10 tablets)
- USS rules:
  - `.aspect--ultra-wide .hud-container { max-width: 1200px; align-self: center; }` (constrain spread)
  - `.aspect--wide .ability-bar { gap: 16px; }` or equivalent spacing increase for tablets
- `PositionToVisualElement` implementation:
  - `characterPortrait.worldBound` center → `RuntimePanelUtils.ScreenToPanel()` or custom conversion
  - World position calculation: `Camera.main.WorldToScreenPoint(characterHead.position)` → panel coordinates
  - Assigned to portrait element's `transform.position` (transform-only, no layout trigger)
- `GeometryChangedEvent` on the portrait element to recalculate alignment
- `UsageHints.DynamicTransform` on the portrait element since it repositions every frame
- Handling for all 5 aspect ratio variants without separate UXML files

---

## Appendix: Coverage Summary

| Sub-Skill | Prompts | Key Concepts Covered |
|---|---|---|
| **Master** | 1–5 | UXML/USS/C# triad, Dragon Crashers patterns, PanelSettings, SafeArea, UIView/UIManager, async, 3D-to-UI bridge |
| **Architecture** | 6–10 | [UxmlElement], MVC/MVP, UXML templates, composite views, UIView base, BEM, screen navigation |
| **Data Binding** | 11–15 | IDataSource, [CreateProperty], BindingMode (OneWay/TwoWay/OneWayToSource), type converters, computed properties, migration from event-driven |
| **Debugging** | 16–20 | UI Toolkit Debugger, Event Debugger, Memory Profiler, theme debugging, binding failures, async error diagnosis |
| **Mobile** | 21–25 | Touch targets, gestures, safe areas, orientation, virtual keyboard, performance budgets, battery management, haptics |
| **Theming** | 26–30 | Design tokens, TSS/USS cascade, dark/light themes, compound themes, BEM, accessibility, multi-panel sync |
| **Patterns** | 31–35 | Tabbed navigation, inventory grid, modal dialogs, stateful buttons, chat message lists, scroll behavior |
| **Performance** | 36–40 | Transform vs layout animation, ListView virtualization, draw call optimization, element pooling, GC-free, profiling workflow |
| **Responsive** | 41–45 | Flexbox, breakpoints, safe area (borderWidth), orientation adaptation, PanelSettings scale modes, aspect ratio handling |

---

*Document generated 2026-02-13. 30 prompts from agent sessions, 15 generated from SKILL.md content.*

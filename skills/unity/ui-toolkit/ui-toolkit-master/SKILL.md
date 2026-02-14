---
name: ui-toolkit-master
description: "Master guide for Unity UI Toolkit — the retained-mode UI framework for Unity 6+. Covers architecture, UXML/USS/C# anatomy, project structure, and links to specialized sub-skills. Use when: (1) Starting a new UI Toolkit project, (2) Choosing between UI Toolkit and legacy uGUI, (3) Understanding the UXML/USS/C# triad, (4) Setting up project structure for UI, (5) Learning UI Toolkit fundamentals. Triggers: 'UI Toolkit', 'UXML', 'USS', 'new UI project', 'UI Toolkit vs uGUI', 'runtime UI setup'."
---

# UI Toolkit Master

<!-- OWNERSHIP: Fundamentals, UXML/USS/C# triad, project structure, UIDocument, PanelSettings, learning path. Cross-ref other skills for all specialized topics. -->

Root skill for the UI Toolkit series. Start here for fundamentals, then follow the learning path to specialized sub-skills.

> **Based on**: Unity 6 (6000.0), Dragon Crashers official sample, and production mobile game patterns.

## Learning Path

Progress through the series from fundamentals to advanced topics. Each level builds on the previous.

### Level 1 — Foundations (Start Here)

| # | Skill | Learning Objectives | Est. Time |
|---|-------|-------------------|-----------|
| 1 | **ui-toolkit-master** (this) | UXML/USS/C# triad, project setup, UIDocument, PanelSettings | 1 hr |
| 2 | [ui-toolkit-architecture](../ui-toolkit-architecture/SKILL.md) | Custom controls, [UxmlElement], MVC pattern, template composition | 2 hrs |
| 3 | [ui-toolkit-responsive](../ui-toolkit-responsive/SKILL.md) | Flexbox layout, length units, safe area, orientation handling | 1.5 hrs |

### Level 2 — Intermediate

| # | Skill | Learning Objectives | Est. Time |
|---|-------|-------------------|-----------|
| 4 | [ui-toolkit-theming](../ui-toolkit-theming/SKILL.md) | Design tokens, TSS/USS cascade, runtime theme switching | 1.5 hrs |
| 5 | [ui-toolkit-databinding](../ui-toolkit-databinding/SKILL.md) | IDataSource, [CreateProperty], binding modes, type converters | 2 hrs |
| 6 | [ui-toolkit-patterns](../ui-toolkit-patterns/SKILL.md) | Tabs, inventory grid, modals, stateful buttons, scroll snap | 2 hrs |

### Level 3 — Advanced

| # | Skill | Learning Objectives | Est. Time |
|---|-------|-------------------|-----------|
| 7 | [ui-toolkit-performance](../ui-toolkit-performance/SKILL.md) | Profiling, draw calls, virtualization, GC-free patterns | 1.5 hrs |
| 8 | [ui-toolkit-mobile](../ui-toolkit-mobile/SKILL.md) | Touch/gesture, orientation, mobile budgets, haptic feedback | 2 hrs |
| 9 | [ui-toolkit-debugging](../ui-toolkit-debugging/SKILL.md) | UI Debugger, Event Debugger, profiler markers, diagnostic code | 1.5 hrs |

**Total estimated learning time: ~15 hours**

## Shared Resources

- [Dragon Crashers Insights](../references/dragon-crashers-insights.md) — patterns extracted from Unity's official sample project
- [Official Docs Links](../references/official-docs-links.md) — curated Unity 6 documentation links by topic
- [Code Templates](../references/code-templates.md) — 8 production-ready UXML/USS/C# templates
- [Performance Benchmarks](../references/performance-benchmarks.md) — metrics, budgets, and zero-alloc patterns
- [QuizU Patterns](../references/quizu-patterns.md) — EventRegistry, UIScreen base, Presenter pattern from Unity's QuizU sample

## UI Toolkit vs Legacy UI

| Feature | uGUI (Canvas) | UI Toolkit |
|---------|---------------|------------|
| Layout | RectTransform, anchors | Flexbox (Yoga engine) |
| Styling | Inspector per-element | USS (CSS-like cascading) |
| Structure | Prefabs in hierarchy | UXML documents (markup) |
| Theming | Manual per-element | TSS (Theme Style Sheets) |
| Data Binding | Manual callbacks | Built-in runtime binding (Unity 6) |
| Lists | ScrollRect + manual pooling | ListView with virtualization |
| Performance | Per-element Canvas rebuild | Retained-mode, batched rendering |
| Editor UI | Limited | Full support |

**When to use UI Toolkit:**
- New projects on Unity 6+
- Complex UI with many screens
- Need theming / consistent styling
- Performance-critical lists or grids
- Shared editor + runtime UI

**When uGUI may still be preferred:**
- World-space UI tightly integrated with 3D (UI Toolkit world-space is experimental in 6.2+)
- Existing uGUI project mid-development
- Heavy TextMeshPro dependency with custom shaders

## The UXML / USS / C# Triad

```
┌──────────────────────────────────────────────────┐
│                    UXML                           │
│  Structure & hierarchy (what elements exist)      │
│  <ui:VisualElement>, <ui:Label>, <ui:Button>      │
│  Template composition: <ui:Template src="...">    │
├──────────────────────────────────────────────────┤
│                    USS                            │
│  Styling & visual presentation (how it looks)     │
│  Selectors: .class, #name, Type, :hover, :active  │
│  Custom properties: --color-primary, --spacing-md │
│  Transitions: translate, opacity, scale           │
├──────────────────────────────────────────────────┤
│                    C#                             │
│  Behavior & logic (what it does)                  │
│  Query: root.Q<Button>("btn-start")               │
│  Events: RegisterCallback<ClickEvent>             │
│  Data binding: element.dataSource = myData        │
│  Custom controls: [UxmlElement] partial class     │
└──────────────────────────────────────────────────┘
```

**Separation rules:**
- UXML: No styling inline (use USS classes). No logic.
- USS: No layout hierarchy. No behavior. Only visual presentation.
- C#: No hardcoded styles. Query elements, bind data, handle events.

## Project Structure

Recommended folder organization for production projects:

```
Assets/
├── UI/
│   ├── Documents/           # UXML files
│   │   ├── Screens/         # Full-screen layouts
│   │   ├── Components/      # Reusable component templates
│   │   └── Modals/          # Popups, dialogs
│   ├── Styles/              # USS files
│   │   ├── Base/            # tokens.uss, reset.uss, typography.uss
│   │   ├── Components/      # Per-component USS
│   │   └── Themes/          # TSS files
│   └── Resources/           # Sprites, fonts, atlases
├── Scripts/
│   └── UI/
│       ├── Screens/         # Screen controllers
│       ├── Components/      # Custom VisualElement subclasses
│       ├── Binding/         # Data sources, converters
│       └── Core/            # UIManager, ScreenManager, SafeArea
└── Settings/
    └── PanelSettings.asset  # Runtime panel configuration
```

## Minimal Setup — Runtime UI

### 1. PanelSettings asset

Create via **Assets > Create > UI Toolkit > Panel Settings Asset**.

Key settings:
- **Scale Mode**: `ScaleWithScreenSize`
- **Reference Resolution**: Match target (e.g., 1920×1080)
- **Screen Match Mode**: Match width or height based on game orientation
- **Theme Style Sheet**: Assign your TSS

### 2. UIDocument component

Add `UIDocument` to a GameObject in the scene:

```csharp
// UIDocument setup
[RequireComponent(typeof(UIDocument))]
public class MainUIController : MonoBehaviour
{
    void OnEnable()
    {
        var root = GetComponent<UIDocument>().rootVisualElement;

        // Load USS
        var styleSheet = Resources.Load<StyleSheet>("Styles/MainScreen");
        root.styleSheets.Add(styleSheet);

        // Query and bind
        var startBtn = root.Q<Button>("btn-start");
        startBtn.RegisterCallback<ClickEvent>(OnStartClicked);
    }

    void OnStartClicked(ClickEvent evt)
    {
        Debug.Log("Game started");
    }
}
```

### 3. UXML document

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
    <ui:VisualElement name="root" class="screen">
        <ui:Label text="My Game" class="title" />
        <ui:Button name="btn-start" text="Start" class="btn-primary" />
    </ui:VisualElement>
</ui:UXML>
```

## Performance Fundamentals

Key rules (deep-dive in [ui-toolkit-performance](../ui-toolkit-performance/SKILL.md)):

1. **Animate transforms, not layout** — `translate`, `rotate`, `scale`, `opacity` are GPU-accelerated. `width`, `height`, `margin`, `padding` trigger expensive layout recalculation.
2. **Use ListView for lists** — Virtualization handles 1000+ items with constant memory.
3. **Cache Q() calls** — `root.Q<Label>("name")` allocates. Call once, store reference.
4. **Set UsageHints** — `DynamicTransform` on animated elements enables batching.
5. **Minimize nesting** — Deep visual trees increase layout cost.

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Inline styles in UXML | Unmaintainable, no theming | Use USS classes |
| Q() every frame | GC pressure (~40 bytes/call) | Cache in OnEnable |
| Animating width/height | Layout thrashing (full subtree recalc) | Use translate/scale |
| ScrollView for 100+ items | Memory, lag | Use ListView with virtualization |
| Rebuilding UI on data change | Expensive recreation | Use data binding |
| Ignoring safe area | Notch overlap on mobile | Use SafeAreaHandler |
| Not setting UsageHints | Missed GPU batching | DynamicTransform on animated elements |
| String concat in labels per frame | GC allocations | Cache strings or use StringBuilder |

## Dragon Crashers — How It's Built

Unity's [Dragon Crashers](../references/dragon-crashers-insights.md) sample demonstrates every pattern in this series. Key architectural takeaways:

### Actual Project Structure

```
# from Dragon Crashers project root
Assets/
├── UI/
│   ├── Uxml/                    # UXML documents (flat, not nested by scope)
│   │   ├── MainMenu.uxml       # Master UXML — single entry point for all menu screens
│   │   ├── HomeScreen.uxml     # Per-screen UXML templates
│   │   ├── CharScreen.uxml
│   │   ├── ShopScreen.uxml
│   │   ├── MailScreen.uxml
│   │   ├── InventoryScreen.uxml
│   │   ├── SettingsScreen.uxml
│   │   ├── GameScreen.uxml
│   │   ├── TabbedMenu.uxml     # Reusable component
│   │   ├── HealthBar.uxml
│   │   └── ...                 # 20+ UXML files total
│   ├── Uss/                    # USS organized by scope (see detailed breakdown below)
│   │   ├── Base/               # Design tokens (7 files)
│   │   ├── Screens/            # Per-screen styles (14 files)
│   │   ├── CustomElements/     # Custom control styles (5 files)
│   │   ├── ThemeStyles/        # Theme + orientation overrides
│   │   └── Toolbars/           # Navigation bar styles (2 files)
│   ├── Themes/                 # TSS files (7 total — orientation × theme matrix)
│   │   ├── RuntimeTheme-Default.tss
│   │   ├── RuntimeTheme-Portrait.tss / RuntimeTheme-Landscape.tss
│   │   ├── RuntimeTheme-Portrait--Halloween.tss / Landscape--Halloween.tss
│   │   └── RuntimeTheme-Portrait--Christmas.tss / Landscape--Christmas.tss
│   ├── PanelSettings/          # PanelSettings assets (Portrait + Landscape)
│   ├── Fonts/
│   └── Textures/
├── Scripts/UI/
│   ├── UIViews/                # UIView base class + all view subclasses
│   │   ├── UIView.cs           # Base class (IDisposable, Initialize/Show/Hide)
│   │   ├── UIManager.cs        # Master UI coordinator (single UIDocument)
│   │   ├── HomeView.cs         # Per-screen views (query elements, register callbacks)
│   │   ├── CharView.cs, ShopView.cs, MailView.cs, InventoryView.cs, etc.
│   │   └── MenuBarView.cs, OptionsBarView.cs, LevelMeterView.cs  # Toolbar views
│   ├── Controllers/            # Screen-level business logic
│   │   ├── HomeScreenController.cs    # Event-driven game logic
│   │   ├── CharScreenController.cs    # Character gear management (345 lines)
│   │   ├── InventoryScreenController.cs # Filtering, sorting, equip/unequip (266 lines)
│   │   ├── MailScreenController.cs    # Mail with tabs, CRUD (214 lines)
│   │   ├── ShopScreenController.cs    # Shop with category filtering
│   │   ├── SettingsScreenController.cs # Theme/framerate management
│   │   └── TabbedMenuController.cs    # Reusable tab selection logic
│   ├── Components/             # Custom VisualElement subclasses
│   │   ├── TabbedMenu.cs       # MonoBehaviour wrapper for TabbedMenuController
│   │   ├── SlideToggle.cs      # Custom toggle control ⚠️ uses deprecated UxmlFactory
│   │   ├── HealthBarComponent.cs # Custom health bar ⚠️ uses deprecated UxmlTraits
│   │   ├── GearItemComponent.cs, ShopItemComponent.cs, CharacterCard.cs
│   │   └── ...
│   ├── Events/                 # Static event bus — 10 event classes
│   │   ├── MainMenuUIEvents.cs # Screen navigation events
│   │   ├── HomeEvents.cs       # Home screen events
│   │   ├── CharEvents.cs, MailEvents.cs, ShopEvents.cs, InventoryEvents.cs
│   │   ├── GameplayEvents.cs, MediaQueryEvents.cs
│   │   └── ThemeEvents.cs, SettingsEvents.cs
│   ├── Themes/                 # ThemeManager.cs — TSS/PanelSettings swapping
│   ├── GameScreens/            # Gameplay UI screens
│   ├── MenuScreens/            # Menu screen base classes
│   └── FX/                     # UI visual effects
├── Scripts/Utilities/
│   ├── SafeAreaBorder.cs        # borderWidth-based safe area (see below)
│   └── PositionToVisualElement.cs # 3D-to-UI alignment (see below)
```

### USS File Organization

DC uses a 5-folder scope-based USS architecture: `Base/` (7 design token files), `Screens/` (14 per-screen files), `Toolbars/`, `CustomElements/`, and `ThemeStyles/` (with Landscape/ and Portrait/ orientation overrides). See [ui-toolkit-theming](../ui-toolkit-theming/SKILL.md#dc-uss-file-architecture) for the complete file listing and cascade rules.

**Key insight**: Orientation-specific overrides are loaded via TSS files, not media queries. The ThemeManager swaps the entire TSS at runtime based on `Screen.orientation`.

### Core Architecture: Single UIDocument + UIView Pattern

Dragon Crashers uses **one master UIDocument** with a single `MainMenu.uxml`. All screens are branches of this tree, toggled via `DisplayStyle.Flex/None`. See [ui-toolkit-architecture](../ui-toolkit-architecture/SKILL.md#dragon-crashers--architecture-in-practice) for full UIView base class, HomeView example, UIManager navigation, TabbedMenuController, and custom controls code.

**Key architectural decisions:**
- UIView base class enforces lifecycle: `Initialize()` → `SetVisualElements()` (cache Q()) → `RegisterButtonCallbacks()`
- UIManager implements modal (replace) and overlay (stack) navigation
- Static `Action` event bus decouples View ↔ Controller communication
- Custom controls use `UxmlFactory`/`UxmlTraits` (DC legacy) — use `[UxmlElement]` for new Unity 6 projects

### SafeAreaBorder — borderWidth Approach

> **Source**: `Assets/Scripts/Utilities/SafeAreaBorder.cs`

Unlike padding-based safe area solutions, Dragon Crashers uses **borderWidth** to create safe area insets. This preserves the content area's layout coordinates while visually masking unsafe regions with a configurable `m_BorderColor`. The `m_Multiplier` field (0–1) allows designers to dial inset strength.

**Why borderWidth instead of padding**: Padding pushes child content inward but children can still overflow; borderWidth creates a hard visual boundary. `GeometryChangedEvent` ensures recalculation on orientation change.

> **Full implementation & comparison**: See [ui-toolkit-responsive](../ui-toolkit-responsive/SKILL.md#safe-area-handling) for the complete SafeAreaBorder code, padding-based alternative, and comparison table.

### Async/Await Fire-and-Forget Pattern

Since UIView subclasses are plain C# (not MonoBehaviours), they cannot use coroutines. Dragon Crashers uses **async Task with fire-and-forget discard** (`_ = AsyncMethod()`) for UI animations like label counter lerp, radial progress, and typing effects. The sync event handler calls `_ = AsyncMethod()` to suppress CS4014 warnings, and the async method wraps logic in `try/catch` since unhandled exceptions in fire-and-forget Tasks are silently swallowed.

**Unity 6+ improvement**: Replace `Task.Delay(TimeSpan.FromSeconds(Time.deltaTime))` with `await Awaitable.NextFrameAsync()` for proper frame synchronization.

> **Full code & usage examples**: See [ui-toolkit-patterns](../ui-toolkit-patterns/SKILL.md#async-task-fire-and-forget) for the complete pattern with LerpRoutine, views that use it, and error handling rules.

### PositionToVisualElement — 3D-to-UI Alignment

> **Source**: `Assets/Scripts/Utilities/PositionToVisualElement.cs`

Bridges 3D world-space GameObjects with UI Toolkit overlay elements by converting panel coordinates → screen pixels → world position at a given depth. Used for aligning 3D characters behind UI cards, positioning particle effects at UI locations, and syncing 3D decorations with responsive layout. Reacts to both `GeometryChangedEvent` and `ThemeEvents.CameraUpdated` to survive orientation changes.

> **Full implementation**: See [ui-toolkit-responsive](../ui-toolkit-responsive/SKILL.md#3d-to-ui-alignment) for the complete PositionToVisualElement code and coordinate conversion pipeline.

**Production metrics from Dragon Crashers:**
- Visual tree depth: 8–12 levels per screen
- Elements per screen: 50–200
- Draw calls: 4–8 per screen (well-batched)
- UI memory footprint: 2–4 MB total
- Initialization: <100ms on mid-range mobile

## Exercise: Hello UI Toolkit

Build a minimal main menu to practice the fundamentals:

**Goal**: Create a main menu with title, start button, and settings button.

1. Create `Assets/UI/Documents/Screens/MainMenu.uxml`:
```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
    <ui:VisualElement name="root" class="screen">
        <ui:VisualElement class="spacer" />
        <ui:Label text="My Game" class="title" />
        <ui:Button name="btn-start" text="Start Game" class="btn-primary" />
        <ui:Button name="btn-settings" text="Settings" class="btn-secondary" />
        <ui:VisualElement class="spacer" />
    </ui:VisualElement>
</ui:UXML>
```

2. Create `Assets/UI/Styles/Base/MainMenu.uss`:
```css
.screen {
    flex-grow: 1;
    align-items: center;
    justify-content: center;
    background-color: #1A1A2E;
}
.spacer { flex-grow: 1; }
.title {
    font-size: 48px;
    color: white;
    -unity-font-style: bold;
    margin-bottom: 40px;
}
.btn-primary, .btn-secondary {
    width: 280px;
    height: 56px;
    margin: 8px;
    border-radius: 8px;
    font-size: 18px;
    -unity-font-style: bold;
}
.btn-primary { background-color: #4A90D9; color: white; }
.btn-secondary { background-color: #2A2A4E; color: #B0BEC5; border-width: 1px; border-color: #4A90D9; }
```

3. Create the controller `Assets/Scripts/UI/Screens/MainMenuController.cs`:
```csharp
using UnityEngine;
using UnityEngine.UIElements;

[RequireComponent(typeof(UIDocument))]
public class MainMenuController : MonoBehaviour
{
    Button _startBtn;
    Button _settingsBtn;

    void OnEnable()
    {
        var root = GetComponent<UIDocument>().rootVisualElement;
        _startBtn = root.Q<Button>("btn-start");
        _settingsBtn = root.Q<Button>("btn-settings");

        _startBtn.RegisterCallback<ClickEvent>(OnStartClicked);
        _settingsBtn.RegisterCallback<ClickEvent>(OnSettingsClicked);
    }

    void OnDisable()
    {
        _startBtn?.UnregisterCallback<ClickEvent>(OnStartClicked);
        _settingsBtn?.UnregisterCallback<ClickEvent>(OnSettingsClicked);
    }

    void OnStartClicked(ClickEvent evt) => Debug.Log("Start Game!");
    void OnSettingsClicked(ClickEvent evt) => Debug.Log("Open Settings!");
}
```

**Checklist:**
- [ ] No inline styles in UXML
- [ ] Q() calls cached in OnEnable, not Update
- [ ] Events unregistered in OnDisable
- [ ] USS uses design token pattern (extractable to variables later)

## Official Documentation

- [UI Toolkit Overview](https://docs.unity3d.com/6000.0/Documentation/Manual/UIElements.html)
- [Getting Started](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-simple-ui-toolkit-workflow.html)
- [UXML Reference](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-UXML.html)
- [USS Reference](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-USS.html)
- [UI Toolkit vs uGUI](https://docs.unity3d.com/6000.0/Documentation/Manual/UI-system-compare.html)
- See [all curated links](../references/official-docs-links.md) for topic-specific documentation

> **Dragon Crashers Source References**: See [Dragon Crashers Insights](../references/dragon-crashers-insights.md) (section: DC Source Files Reference) for the complete file listing of all UIView, Controller, Event, USS, UXML, and TSS files referenced in this skill.

## Sub-Skill Cross-Reference

Quick reference for which sub-skill covers each topic:

| Topic | Sub-Skill | Key Patterns |
|-------|-----------|--------------|
| Custom controls, [UxmlElement], MVC, templates | [ui-toolkit-architecture](../ui-toolkit-architecture/SKILL.md) | UIView pattern, template composition, multi-document |
| Flexbox, safe area, orientation, length units | [ui-toolkit-responsive](../ui-toolkit-responsive/SKILL.md) | SafeAreaBorder, orientation-aware layouts |
| Design tokens, TSS cascade, theme switching | [ui-toolkit-theming](../ui-toolkit-theming/SKILL.md) | 7-TSS matrix, Decoration-*.uss seasonal themes |
| IDataSource, [CreateProperty], binding modes | [ui-toolkit-databinding](../ui-toolkit-databinding/SKILL.md) | Runtime data binding, type converters |
| Tabs, inventory, modals, scroll snap | [ui-toolkit-patterns](../ui-toolkit-patterns/SKILL.md) | TabbedMenu, modal/overlay nav, static event bus |
| Profiling, draw calls, virtualization | [ui-toolkit-performance](../ui-toolkit-performance/SKILL.md) | ListView, UsageHints, GC-free patterns |
| Touch/gesture, mobile budgets, haptics | [ui-toolkit-mobile](../ui-toolkit-mobile/SKILL.md) | PositionToVisualElement, mobile optimization |
| UI Debugger, Event Debugger, diagnostics | [ui-toolkit-debugging](../ui-toolkit-debugging/SKILL.md) | Profiler markers, diagnostic code |

## Coverage Gaps (Stub Guidance)

The following topics are not yet covered by dedicated sub-skills. Use the guidance below as a starting point.

### Accessibility

UI Toolkit has limited built-in accessibility support compared to web. Key areas to address:

| Area | Status in Unity 6 | Recommendation |
|---|---|---|
| **Screen readers** | No native support | Use `Label` with descriptive text; set `tooltip` for icon-only buttons |
| **Focus navigation** | ✅ Built-in `focusable`, `tabIndex` | Set `tabIndex` on interactive elements; test keyboard-only navigation |
| **High contrast** | No built-in detection | Create a high-contrast TSS with `var(--color-*)` overrides; swap via `PanelSettings.themeStyleSheet` |
| **Touch target size** | Manual enforcement | Minimum 44×44px for all interactive elements (WCAG 2.5.5) |
| **Color contrast** | Manual verification | Ensure 4.5:1 contrast ratio for text (WCAG AA); tools: WebAIM Contrast Checker |
| **Reduced motion** | No `prefers-reduced-motion` | Add `--transition-duration: 0ms` override TSS; let user toggle in settings |

```csharp
// Minimum pattern: ensure focusable + tooltip on icon buttons
iconButton.focusable = true;
iconButton.tabIndex = 1;
iconButton.tooltip = "Open inventory";
```

### Testing UI Toolkit

No dedicated testing framework exists for UI Toolkit elements. Current approaches:

| Approach | Scope | Setup |
|---|---|---|
| **Edit Mode tests** | UIDocument creation, element queries, class assertions | `[Test]` + `UIDocument` in code |
| **Play Mode tests** | Full UI interaction, event simulation | `[UnityTest]` + scene with UIDocument |
| **Event simulation** | Click, pointer, keyboard events | `using var evt = ClickEvent.GetPooled(); element.SendEvent(evt);` |
| **Visual regression** | Screenshot comparison | `ScreenCapture.CaptureScreenshotAsTexture()` + image diff |

```csharp
// Edit Mode test pattern
[Test]
public void TabBar_SelectsCorrectTab()
{
    var doc = new UIDocument();
    // ... setup UXML
    var tab = root.Q<Button>("tab-inventory");
    using var evt = ClickEvent.GetPooled();
    tab.SendEvent(evt);
    Assert.IsTrue(tab.ClassListContains("tab-bar__tab--active"));
}
```

> ⚠️ `VisualElement.SendEvent()` requires the element to be attached to a panel. In Edit Mode, create a `UIDocument` or use `new RuntimePanel()`.

### Localization

No built-in localization. Use `com.unity.localization` package: bind `LocalizedString.StringChanged` to `Label.text`. USS `direction: rtl` for RTL (Unity 6+). Use `Font Asset` with fallback chain for CJK/Arabic. Use `CultureInfo` for date/number formatting in C#.

---
name: ui-toolkit-master
description: "Master guide for Unity UI Toolkit — the retained-mode UI framework for Unity 6+. Covers architecture, UXML/USS/C# anatomy, project structure, and links to specialized sub-skills. Use when: (1) Starting a new UI Toolkit project, (2) Choosing between UI Toolkit and legacy uGUI, (3) Understanding the UXML/USS/C# triad, (4) Setting up project structure for UI, (5) Learning UI Toolkit fundamentals. Triggers: 'UI Toolkit', 'UXML', 'USS', 'new UI project', 'UI Toolkit vs uGUI', 'runtime UI setup'."
---

# UI Toolkit Master

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

### USS File Organization (Detailed)

The USS directory follows a 5-folder scope-based architecture. This is the actual file layout:

```
Assets/UI/Uss/
├── Base/                        # Design tokens — imported by all screens
│   ├── Colors.uss               # Color custom properties
│   ├── Text.uss                 # Typography: font sizes, weights, line heights
│   ├── Common.uss               # Shared layout patterns, spacers, containers
│   ├── Buttons.uss              # Button variants (primary, secondary, icon)
│   ├── Sliders.uss              # Slider track, thumb, fill styles
│   ├── Cursors.uss              # Cursor overrides (hover, drag)
│   └── Dropdowns.uss            # Dropdown/popup styles
├── Screens/                     # One USS per screen (14 files)
│   ├── HomeScreen.uss           # Home screen layout + elements
│   ├── CharScreen.uss           # Character screen
│   ├── CharStats.uss            # Character stats sub-panel
│   ├── ShopScreen.uss, ShopItem.uss
│   ├── MailScreen.uss, MailItem.uss
│   ├── Inventory.uss, SettingsScreen.uss
│   ├── InfoScreen.uss
│   ├── GameScreen.uss, GameWinLoseScreen.uss, PauseScreen.uss
│   └── PopUpText.uss
├── Toolbars/                    # Navigation bar styles
│   ├── MenuBar.uss              # Bottom tab bar
│   └── OptionsBar.uss           # Top toolbar (gold/gem/settings)
├── CustomElements/              # Custom control-specific styles
│   ├── HealthBar.uss            # Player health bar
│   ├── HealthBarBoss.uss        # Boss variant
│   ├── LevelMeter.uss           # Radial progress meter
│   ├── LevelMeter.uxml          # Inline template for level meter
│   └── SlideToggle.uss          # Custom toggle switch
└── ThemeStyles/                 # Theme × orientation overrides
    ├── Decoration-Default.uss   # Default seasonal decorations
    ├── Decoration-Halloween.uss # Halloween theme overrides
    ├── Decoration-Christmas.uss # Christmas theme overrides
    ├── Landscape/               # 11 per-screen landscape overrides
    │   ├── MainMenu-Landscape.uss
    │   ├── HomeScreen-Landscape.uss
    │   ├── CharScreen-Landscape.uss, CharStats-Landscape.uss
    │   ├── ShopScreen-Landscape.uss, MailScreen-Landscape.uss
    │   ├── InventoryScreen-Landscape.uss, SettingsScreen-Landscape.uss
    │   ├── InfoScreen-Landscape.uss, GameScreen-Landscape.uss
    │   └── MenuBar-Landscape.uss
    └── Portrait/                # 11 per-screen portrait overrides (same naming)
        ├── MainMenu-Portrait.uss
        ├── HomeScreen-Portrait.uss
        └── ... (mirrors Landscape/ structure)
```

**Key insight**: Orientation-specific overrides are loaded via TSS files, not media queries. The ThemeManager swaps the entire TSS at runtime based on `Screen.orientation`, which swaps in the correct Landscape/ or Portrait/ USS files.

### Core Architecture: Single UIDocument + UIView Pattern

Dragon Crashers uses **one master UIDocument** with a single `MainMenu.uxml`. All screens are branches of this tree, toggled via `DisplayStyle.Flex/None`:

```csharp
// from Assets/Scripts/UI/UIViews/UIManager.cs
[RequireComponent(typeof(UIDocument))]
public class UIManager : MonoBehaviour
{
    UIDocument m_MainMenuDocument;
    UIView m_CurrentView;
    UIView m_PreviousView;
    List<UIView> m_AllViews = new List<UIView>();

    // String IDs match UXML element names
    public const string k_HomeViewName = "HomeScreen";
    public const string k_CharViewName = "CharScreen";
    public const string k_ShopViewName = "ShopScreen";
    // ... one constant per screen

    void OnEnable()
    {
        m_MainMenuDocument = GetComponent<UIDocument>();
        SetupViews();       // Create all UIView instances
        SubscribeToEvents(); // Wire up static event bus
        ShowModalView(m_HomeView); // Start on home screen
    }

    void SetupViews()
    {
        VisualElement root = m_MainMenuDocument.rootVisualElement;

        // Each view gets its branch of the visual tree
        m_HomeView = new HomeView(root.Q<VisualElement>(k_HomeViewName));
        m_CharView = new CharView(root.Q<VisualElement>(k_CharViewName));
        m_ShopView = new ShopView(root.Q<VisualElement>(k_ShopViewName));
        // ...

        // Track for disposal
        m_AllViews.Add(m_HomeView);
        m_AllViews.Add(m_CharView);
        // ...
    }
}
```

### UIView Base Class — Template Method Pattern

Every screen/toolbar extends `UIView`, which enforces a consistent lifecycle:

```csharp
// from Assets/Scripts/UI/UIViews/UIView.cs
public class UIView : IDisposable
{
    protected VisualElement m_TopElement;

    public UIView(VisualElement topElement)
    {
        m_TopElement = topElement ?? throw new ArgumentNullException(nameof(topElement));
        Initialize();
    }

    public virtual void Initialize()
    {
        Hide();                     // Hidden by default
        SetVisualElements();        // Step 1: Query and cache elements
        RegisterButtonCallbacks();  // Step 2: Wire up click handlers
    }

    protected virtual void SetVisualElements() { }    // Override to Q() elements
    protected virtual void RegisterButtonCallbacks() { } // Override to register clicks

    public virtual void Show() => m_TopElement.style.display = DisplayStyle.Flex;
    public virtual void Hide() => m_TopElement.style.display = DisplayStyle.None;
    public virtual void Dispose() { } // Override to unregister events
}
```

### Concrete View Example

```csharp
// from Assets/Scripts/UI/UIViews/HomeView.cs
public class HomeView : UIView
{
    VisualElement m_PlayLevelButton;
    Label m_LevelNumber;
    Label m_LevelLabel;

    public HomeView(VisualElement topElement) : base(topElement)
    {
        // Subscribe to game events in constructor
        HomeEvents.LevelInfoShown += OnShowLevelInfo;
    }

    protected override void SetVisualElements()
    {
        base.SetVisualElements();
        // Cache all Q() calls — never call Q() in Update
        m_PlayLevelButton = m_TopElement.Q("home-play__level-button");
        m_LevelLabel = m_TopElement.Q<Label>("home-play__level-name");
        m_LevelNumber = m_TopElement.Q<Label>("home-play__level-number");
    }

    protected override void RegisterButtonCallbacks()
    {
        m_PlayLevelButton.RegisterCallback<ClickEvent>(ClickPlayButton);
    }

    public override void Dispose()
    {
        base.Dispose();
        HomeEvents.LevelInfoShown -= OnShowLevelInfo;
        m_PlayLevelButton.UnregisterCallback<ClickEvent>(ClickPlayButton);
    }

    void ClickPlayButton(ClickEvent evt)
    {
        AudioManager.PlayDefaultButtonSound();
        HomeEvents.PlayButtonClicked?.Invoke();
    }
}
```

### Modal vs Overlay Navigation

UIManager implements two navigation modes:

```csharp
// from Assets/Scripts/UI/UIViews/UIManager.cs

// MODAL: Hides current view, shows new one (full replacement)
void ShowModalView(UIView newView)
{
    if (m_CurrentView != null)
        m_CurrentView.Hide();

    m_PreviousView = m_CurrentView;
    m_CurrentView = newView;

    if (m_CurrentView != null)
    {
        m_CurrentView.Show();
        MainMenuUIEvents.CurrentViewChanged?.Invoke(m_CurrentView.GetType().Name);
    }
}

// OVERLAY: Shows on top without hiding the current view
void OnSettingsScreenShown()
{
    m_PreviousView = m_CurrentView; // Remember where we came from
    m_SettingsView.Show();          // Show on top (doesn't hide current)
}

void OnSettingsScreenHidden()
{
    m_SettingsView.Hide();
    if (m_PreviousView != null)
    {
        m_PreviousView.Show();
        m_CurrentView = m_PreviousView;
    }
}
```

### Static Event Bus Pattern

Dragon Crashers decouples UI from game logic via static `Action` delegates grouped by feature:

```csharp
// from Assets/Scripts/UI/Events/MainMenuUIEvents.cs
public static class MainMenuUIEvents
{
    public static Action HomeScreenShown;      // Navigate to home
    public static Action CharScreenShown;      // Navigate to character
    public static Action ShopScreenShown;      // Navigate to shop
    public static Action SettingsScreenShown;  // Open settings overlay
    public static Action SettingsScreenHidden; // Close settings overlay
    public static Action<string> CurrentViewChanged; // Notify view change
}

// from Assets/Scripts/UI/Events/HomeEvents.cs
public static class HomeEvents
{
    public static Action<string> HomeMessageShown;
    public static Action<LevelSO> LevelInfoShown;
    public static Action PlayButtonClicked;
}
```

**Key takeaway**: Controllers subscribe in `OnEnable()` and unsubscribe in `OnDisable()`. Views subscribe in their constructor and unsubscribe in `Dispose()`. This prevents memory leaks and dangling references.

### Dual UIDocument Strategy

Dragon Crashers uses **two UIDocument tiers** to separate menu UI from gameplay UI:

1. **Menu UIDocument** — Single master UIDocument on `UIManager` holds all menu screens (`MainMenu.uxml`). All 10 views (5 modal, 2 overlay, 3 toolbar) are branches of this one document.
2. **Gameplay UIDocuments** — Separate UIDocuments for in-game HUD elements (e.g., `HealthBarComponent` on individual GameObjects). These have their own UXML/USS and operate independently of the menu system.

This separation ensures gameplay UI lifecycle is tied to gameplay GameObjects, while menu UI persists across the session. See [ui-toolkit-architecture](../ui-toolkit-architecture/SKILL.md) for detailed multi-document patterns.

### SafeAreaBorder — borderWidth Approach

> **Source**: `Assets/Scripts/Utilities/SafeAreaBorder.cs`

Unlike padding-based safe area solutions, Dragon Crashers uses **borderWidth** to create safe area insets. This preserves the content area's layout coordinates while visually masking unsafe regions:

```csharp
// from Assets/Scripts/Utilities/SafeAreaBorder.cs
[ExecuteInEditMode]
public class SafeAreaBorder : MonoBehaviour
{
    [SerializeField] UIDocument m_Document;
    [SerializeField] Color m_BorderColor = Color.black;  // Visible border color
    [SerializeField] string m_Element;                    // Target element name (empty = root)
    [Range(0, 1f)]
    [SerializeField] float m_Multiplier = 1f;             // Scale insets (useful for testing)

    void ApplySafeArea()
    {
        Rect safeArea = Screen.safeArea;

        // Calculate insets from Screen.safeArea
        m_Root.style.borderTopWidth    = (Screen.height - safeArea.yMax) * m_Multiplier;
        m_Root.style.borderBottomWidth = safeArea.y * m_Multiplier;
        m_Root.style.borderLeftWidth   = safeArea.x * m_Multiplier;
        m_Root.style.borderRightWidth  = (Screen.width - safeArea.xMax) * m_Multiplier;

        // Color the border (black hides notch area, transparent shows background)
        m_Root.style.borderBottomColor = m_BorderColor;
        m_Root.style.borderTopColor    = m_BorderColor;
        m_Root.style.borderLeftColor   = m_BorderColor;
        m_Root.style.borderRightColor  = m_BorderColor;
    }
}
```

**Why borderWidth instead of padding?**
- **Padding** pushes child content inward but children can still overflow into unsafe areas
- **borderWidth** creates a hard visual boundary — the border area is rendered with `m_BorderColor`, cleanly masking notch/rounded-corner regions
- The `m_Multiplier` field allows designers to dial the inset strength (0 = disabled, 1 = full safe area)
- `GeometryChangedEvent` callback ensures recalculation on orientation change

See [ui-toolkit-responsive](../ui-toolkit-responsive/SKILL.md) and [ui-toolkit-mobile](../ui-toolkit-mobile/SKILL.md) for comprehensive safe area strategies.

### Async/Await Fire-and-Forget Pattern

> **Source**: `Assets/Scripts/UI/UIViews/OptionsBarView.cs`, `LevelMeterView.cs`, `ChatView.cs`

Since `UIView` subclasses are plain C# classes (not MonoBehaviours), they cannot use coroutines. Dragon Crashers uses **async Task with fire-and-forget discard** for UI animations:

```csharp
// from Assets/Scripts/UI/UIViews/OptionsBarView.cs
void OnFundsUpdated(GameData gameData)
{
    // Fire and forget — discard suppresses CS4014 warning
    _ = HandleFundsUpdatedAsync(gameData);
}

async Task HandleFundsUpdatedAsync(GameData gameData)
{
    try
    {
        uint startGold = (uint)Int32.Parse(m_GoldLabel.text);
        await LerpRoutine(m_GoldLabel, startGold, gameData.gold, k_LerpTime);
    }
    catch (Exception ex)
    {
        Debug.LogError($"[OptionsBarView] HandleFundsUpdatedAsync error: {ex.Message}");
    }
}

async Task LerpRoutine(Label label, uint startValue, uint endValue, float duration)
{
    float t = 0f;
    while (Mathf.Abs((float)endValue - Mathf.Lerp(startValue, endValue, t)) > 0.05f)
    {
        t += Time.deltaTime / duration;
        label.text = Mathf.Lerp(startValue, endValue, t).ToString("0");
        await Task.Delay(TimeSpan.FromSeconds(Time.deltaTime));
    }
    label.text = endValue.ToString();
}
```

**Pattern rules:**
1. Event handler is synchronous (`void`), calls `_ = AsyncMethod()` to discard the Task
2. Async method wraps logic in `try/catch` — unhandled exceptions in fire-and-forget Tasks are silently swallowed otherwise
3. Uses `Task.Delay` for frame-like timing (not ideal — prefer `Awaitable.NextFrameAsync()` in Unity 6+)
4. Views using this pattern: `OptionsBarView` (gold/gem counter lerp), `LevelMeterView` (radial progress animation), `ChatView` (message typing effect), `MailContentView` (mail animation)

**Unity 6+ improvement**: Replace `Task.Delay(TimeSpan.FromSeconds(Time.deltaTime))` with `await Awaitable.NextFrameAsync()` for proper frame synchronization and cancellation support.

### PositionToVisualElement — 3D-to-UI Alignment

> **Source**: `Assets/Scripts/Utilities/PositionToVisualElement.cs`

Bridges 3D world-space GameObjects with UI Toolkit overlay elements. Positions a 3D object to align with a VisualElement's screen position:

```csharp
// from Assets/Scripts/Utilities/PositionToVisualElement.cs
public class PositionToVisualElement : MonoBehaviour
{
    [SerializeField] GameObject m_ObjectToMove;
    [SerializeField] Camera m_Camera;
    [SerializeField] float m_Depth = 10f;
    [SerializeField] UIDocument m_Document;
    [SerializeField] string m_ElementName;

    public void MoveToElement()
    {
        // Step 1: Get UI element center in panel coordinates
        Rect worldBound = m_TargetElement.worldBound;
        Vector2 centerPosition = new Vector2(
            worldBound.x + worldBound.width / 2,
            worldBound.y + worldBound.height / 2);

        // Step 2: Convert panel coords → screen pixels
        Vector2 screenPos = centerPosition.GetScreenCoordinate(m_Document.rootVisualElement);

        // Step 3: Screen pixels → world position at depth
        Vector3 worldPosition = screenPos.ScreenPosToWorldPos(m_Camera, m_Depth);

        m_ObjectToMove.transform.position = worldPosition;
    }
}
```

**Use cases:**
- Aligning 3D character models behind UI cards
- Positioning particle effects at UI element locations
- Syncing 3D decorations with responsive UI layout changes

The component reacts to both `GeometryChangedEvent` (UI layout changes) and `ThemeEvents.CameraUpdated` (camera swaps during theme/orientation changes), ensuring alignment survives orientation changes.

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

## Dragon Crashers Source References

Key files referenced in this skill:

| File | Role |
|------|------|
| `Assets/Scripts/UI/UIViews/UIManager.cs` | Master UI coordinator — single UIDocument, view lifecycle, modal/overlay navigation |
| `Assets/Scripts/UI/UIViews/UIView.cs` | Base view class — template method pattern (Initialize → SetVisualElements → RegisterButtonCallbacks) |
| `Assets/Scripts/UI/UIViews/HomeView.cs` | Concrete view example — element caching, event subscription, disposal |
| `Assets/Scripts/UI/UIViews/OptionsBarView.cs` | Async/await fire-and-forget pattern — animated label counter |
| `Assets/Scripts/UI/UIViews/LevelMeterView.cs` | Async radial progress animation |
| `Assets/Scripts/UI/UIViews/ChatView.cs` | Async typing effect animation |
| `Assets/Scripts/Utilities/SafeAreaBorder.cs` | borderWidth-based safe area insets with configurable multiplier |
| `Assets/Scripts/Utilities/PositionToVisualElement.cs` | 3D GameObject-to-UI element alignment bridge |
| `Assets/Scripts/UI/Events/MainMenuUIEvents.cs` | Static event bus — screen navigation delegates |
| `Assets/Scripts/UI/Events/HomeEvents.cs` | Per-feature event bus — home screen game logic events |
| `Assets/Scripts/UI/Events/` | 10 event classes total: CharEvents, GameplayEvents, HomeEvents, InventoryEvents, MailEvents, MainMenuUIEvents, MediaQueryEvents, SettingsEvents, ShopEvents, ThemeEvents |
| `Assets/UI/Uxml/MainMenu.uxml` | Master UXML document — all screens as branches |
| `Assets/UI/Uss/Base/` | Design token USS files — Colors.uss, Text.uss, Common.uss, Buttons.uss, Sliders.uss, Cursors.uss, Dropdowns.uss |
| `Assets/UI/Uss/Screens/` | Per-screen styles — 14 USS files |
| `Assets/UI/Uss/CustomElements/` | Custom control styles — HealthBar.uss, HealthBarBoss.uss, LevelMeter.uss, SlideToggle.uss |
| `Assets/UI/Uss/Toolbars/` | MenuBar.uss, OptionsBar.uss |
| `Assets/UI/Uss/ThemeStyles/` | Theme overrides + Landscape/ (11 files) + Portrait/ (11 files) |
| `Assets/UI/Themes/` | TSS files — 7-file orientation × theme matrix |

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

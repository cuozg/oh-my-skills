# UI Toolkit Master — Dragon Crashers Structure, Exercise & Coverage Gaps

> Extracted from [ui-toolkit-master/SKILL.md](../SKILL.md) for token efficiency. All content preserved.

## Dragon Crashers — How It's Built

Unity's [Dragon Crashers](../../references/dragon-crashers-insights.md) sample demonstrates every pattern in this series. Key architectural takeaways:

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

DC uses a 5-folder scope-based USS architecture: `Base/` (7 design token files), `Screens/` (14 per-screen files), `Toolbars/`, `CustomElements/`, and `ThemeStyles/` (with Landscape/ and Portrait/ orientation overrides). See [ui-toolkit-theming](../../ui-toolkit-theming/SKILL.md#dragon-crashers-compound-theming-system) for the complete file listing and cascade rules.

**Key insight**: Orientation-specific overrides are loaded via TSS files, not media queries. The ThemeManager swaps the entire TSS at runtime based on `Screen.orientation`.

### Core Architecture: Single UIDocument + UIView Pattern

Dragon Crashers uses **one master UIDocument** with a single `MainMenu.uxml`. All screens are branches of this tree, toggled via `DisplayStyle.Flex/None`. See [ui-toolkit-architecture](../../ui-toolkit-architecture/SKILL.md#dragon-crashers--architecture-in-practice) for full UIView base class, HomeView example, UIManager navigation, TabbedMenuController, and custom controls code.

**Key architectural decisions:**
- UIView base class enforces lifecycle: `Initialize()` → `SetVisualElements()` (cache Q()) → `RegisterButtonCallbacks()`
- UIManager implements modal (replace) and overlay (stack) navigation
- Static `Action` event bus decouples View ↔ Controller communication
- Custom controls use `UxmlFactory`/`UxmlTraits` (DC legacy) — use `[UxmlElement]` for new Unity 6 projects

### SafeAreaBorder — borderWidth Approach

> **Source**: `Assets/Scripts/Utilities/SafeAreaBorder.cs`

Unlike padding-based safe area solutions, Dragon Crashers uses **borderWidth** to create safe area insets. This preserves the content area's layout coordinates while visually masking unsafe regions with a configurable `m_BorderColor`. The `m_Multiplier` field (0–1) allows designers to dial inset strength.

**Why borderWidth instead of padding**: Padding pushes child content inward but children can still overflow; borderWidth creates a hard visual boundary. `GeometryChangedEvent` ensures recalculation on orientation change.

> **Full implementation & comparison**: See [ui-toolkit-responsive](../../ui-toolkit-responsive/SKILL.md#safeareaborder-borderwidth-approach) for the complete SafeAreaBorder code, padding-based alternative, and comparison table.

### Async/Await Fire-and-Forget Pattern

Since UIView subclasses are plain C# (not MonoBehaviours), they cannot use coroutines. Dragon Crashers uses **async Task with fire-and-forget discard** (`_ = AsyncMethod()`) for UI animations like label counter lerp, radial progress, and typing effects. The sync event handler calls `_ = AsyncMethod()` to suppress CS4014 warnings, and the async method wraps logic in `try/catch` since unhandled exceptions in fire-and-forget Tasks are silently swallowed.

**Unity 6+ improvement**: Replace `Task.Delay(TimeSpan.FromSeconds(Time.deltaTime))` with `await Awaitable.NextFrameAsync()` for proper frame synchronization.

> **Full code & usage examples**: See [ui-toolkit-patterns](../../ui-toolkit-patterns/SKILL.md#async-task-fire-and-forget) for the complete pattern with LerpRoutine, views that use it, and error handling rules.

### PositionToVisualElement — 3D-to-UI Alignment

> **Source**: `Assets/Scripts/Utilities/PositionToVisualElement.cs`

Bridges 3D world-space GameObjects with UI Toolkit overlay elements by converting panel coordinates → screen pixels → world position at a given depth. Used for aligning 3D characters behind UI cards, positioning particle effects at UI locations, and syncing 3D decorations with responsive layout. Reacts to both `GeometryChangedEvent` and `ThemeEvents.CameraUpdated` to survive orientation changes.

> **Full implementation**: See [ui-toolkit-responsive](../../ui-toolkit-responsive/SKILL.md#positiontovisualelement-world-to-ui-alignment) for the complete PositionToVisualElement code and coordinate conversion pipeline.

**Production metrics from Dragon Crashers:**
- Visual tree depth: 8–12 levels per screen
- Elements per screen: 50–200
- Draw calls: 4–8 per screen (well-batched)
- UI memory footprint: 2–4 MB total
- Initialization: <100ms on mid-range mobile

---

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

---

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

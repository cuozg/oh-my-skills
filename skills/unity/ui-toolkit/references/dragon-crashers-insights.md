# Dragon Crashers: Project Insights & Code Reference

Detailed Dragon Crashers (DC) project code, USS/TSS organization patterns, performance analyses, and debugging scenarios. These are DC-specific implementations extracted from ui-toolkit skills to keep skill files lean.

> **Note**: This project folder uses Unity's official QuizU demo project, not Dragon Crashers. This file documents DC patterns for comparison and reference. See [quizu-patterns.md](quizu-patterns.md) for QuizU-specific patterns.

---

## Screen Implementations

### Mail Screen — Composite View

`MailView` demonstrates the composite view pattern — parent owns 3 child views:

```csharp
// Assets/Scripts/UI/UIViews/MailView.cs
public class MailView : UIView
{
    VisualElement m_MailboxContainer, m_ContentContainer, m_TabContainer;
    MailboxView m_MailboxView; MailContentView m_MailContentView; MailTabView m_MailTabView;

    public MailView(VisualElement topElement): base(topElement) { }

    protected override void SetVisualElements()
    {
        base.SetVisualElements();
        m_MailboxContainer = m_TopElement.Q<VisualElement>("mailbox__container");
        m_ContentContainer = m_TopElement.Q<VisualElement>("content__container");
        m_TabContainer = m_TopElement.Q<VisualElement>("tabs__container");
    }

    public override void Initialize()
    {
        base.Initialize();
        m_MailTabView = new MailTabView(m_TabContainer); m_MailTabView.Show();
        m_MailboxView = new MailboxView(m_MailboxContainer); m_MailboxView.Show();
        m_MailContentView = new MailContentView(m_ContentContainer); m_MailContentView.Show();
    }

    public override void Dispose() { base.Dispose(); m_MailboxView.Dispose(); m_MailContentView.Dispose(); m_MailTabView.Dispose(); }
}
```

**Rules:** Parent queries containers in `SetVisualElements()`, creates sub-views in `Initialize()` AFTER base completes, cascades `Dispose()` to children. Max 2 levels of nesting.

### Shop Screen — Dynamic Generation

`ShopView` generates items dynamically from `VisualTreeAsset` templates (not ListView):

```csharp
// Assets/Scripts/UI/UIViews/ShopView.cs
public void OnShopUpdated(List<ShopItemSO> shopItems)
{
    parentTab.Clear();
    foreach (ShopItemSO shopItem in shopItems)
    {
        TemplateContainer elem = m_ShopItemAsset.Instantiate();
        ShopItemComponent controller = new ShopItemComponent(m_GameIconsData, shopItem);
        controller.SetVisualElements(elem);
        controller.SetGameData(elem);
        controller.RegisterCallbacks();
        parentElement.Add(elem);
    }
}
```

**Two Tab Approaches**: (A) Reusable `TabbedMenuController` via naming convention for generic screens (Mail, Settings). (B) Manual per-screen with domain events for `ShopView` where tabs fire domain-specific events.

### HomeView — Data Binding via Events

```csharp
// Assets/Scripts/UI/UIViews/HomeView.cs
public class HomeView : UIView
{
    Label m_LevelNumber, m_LevelLabel;
    VisualElement m_LevelThumbnail;

    public HomeView(VisualElement topElement) : base(topElement)
    {
        HomeEvents.LevelInfoShown += OnShowLevelInfo;
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
        HomeEvents.LevelInfoShown -= OnShowLevelInfo;
    }

    void OnShowLevelInfo(LevelSO levelData)
    {
        m_LevelNumber.text = "Level " + levelData.levelNumber;
        m_LevelLabel.text = levelData.levelLabel;
        m_LevelThumbnail.style.backgroundImage = new StyleBackground(levelData.thumbnail);
    }
}
```

### Inventory — ScrollView + Filtering

DC uses `ScrollView` with manual `VisualTreeAsset.Instantiate()` loops — no virtualization, but simpler for small fixed sets. Pattern: `ScrollView.Clear()` → `foreach` → `Instantiate()` → component wrapper → `Add()`. Filtering uses `DropdownField.ChangeEvent<string>` → event bus → controller LINQ `Where().OrderBy()` → event back → view rebuilds.

---

## Architecture Components

### HealthBarComponent (⚠️ Deprecated UxmlFactory)

```csharp
// Assets/Scripts/UI/Components/HealthBarComponent.cs
public class HealthBarComponent : VisualElement
{
    // ⚠️ DEPRECATED — replace with [UxmlElement] + [UxmlAttribute] in Unity 6
    public new class UxmlFactory : UxmlFactory<HealthBarComponent, UxmlTraits> { }
    public new class UxmlTraits : VisualElement.UxmlTraits
    {
        readonly UxmlIntAttributeDescription _currentHealth = new() { name = "currentHealth", defaultValue = 0 };
        readonly UxmlIntAttributeDescription _maximumHealth = new() { name = "MaximumHealth", defaultValue = 100 };
        readonly UxmlStringAttributeDescription _healthBarTitle = new() { name = "HealthBarTitle" };

        public override void Init(VisualElement ve, IUxmlAttributes bag, CreationContext cc)
        {
            base.Init(ve, bag, cc);
            var hb = (HealthBarComponent)ve;
            hb.CurrentHealth = _currentHealth.GetValueFromBag(bag, cc);
            hb.MaximumHealth = _maximumHealth.GetValueFromBag(bag, cc);
            hb.HealthBarTitle = _healthBarTitle.GetValueFromBag(bag, cc);
        }
    }

    private int _currentHealth, _maximumHealth;
    private readonly Label _titleLabel, _healthStat;
    private VisualElement _progress;

    public HealthBarComponent()
    {
        AddToClassList("health-bar__container");
        var titleBg = new VisualElement(); titleBg.AddToClassList("health-bar__title_background"); Add(titleBg);
        _titleLabel = new Label(); _titleLabel.AddToClassList("health-bar__title"); titleBg.Add(_titleLabel);
        var bg = new VisualElement(); bg.AddToClassList("health-bar__background"); Add(bg);
        _progress = new VisualElement(); _progress.AddToClassList("health-bar__progress"); bg.Add(_progress);
        _healthStat = new Label(); _healthStat.AddToClassList("health-bar__label"); _progress.Add(_healthStat);
    }

    private void SetHealth(int cur, int max) {
        _healthStat.text = $"{cur}/{max}";
        if (max > 0) _progress.style.width = new StyleLength(Length.Percent(Mathf.Clamp((float)cur / max * 100, 0f, 100f)));
    }
}
```

**✅ Modern equivalent:** Add `[UxmlElement]`, make class `partial`, replace `UxmlFactory`/`UxmlTraits` with `[UxmlAttribute]` on properties.

### SlideToggle (⚠️ Deprecated + BaseField)

```csharp
// Assets/Scripts/UI/Components/SlideToggle.cs (namespace: MyUILibrary)
public class SlideToggle : BaseField<bool>
{
    public new class UxmlFactory : UxmlFactory<SlideToggle, UxmlTraits> { }   // ⚠️ DEPRECATED
    public new class UxmlTraits : BaseFieldTraits<bool, UxmlBoolAttributeDescription> { }

    public static readonly new string ussClassName = "slide-toggle";
    public static readonly string inputKnobUssClassName = "slide-toggle__input-knob";
    public static readonly string inputCheckedUssClassName = "slide-toggle__input--checked";

    VisualElement m_Input, m_Knob;

    public SlideToggle(string label = null) : base(label, null)
    {
        AddToClassList(ussClassName);
        m_Input = this.Q(className: BaseField<bool>.inputUssClassName);
        m_Knob = new(); m_Knob.AddToClassList(inputKnobUssClassName); m_Input.Add(m_Knob);

        RegisterCallback<ClickEvent>(evt => { ToggleValue(); evt.StopPropagation(); });
        RegisterCallback<KeyDownEvent>(evt => OnKeydownEvent(evt));
        RegisterCallback<NavigationSubmitEvent>(evt => OnSubmit(evt));
    }

    void ToggleValue() => value = !value;

    public override void SetValueWithoutNotify(bool newValue)
    {
        base.SetValueWithoutNotify(newValue);
        m_Input.EnableInClassList(inputCheckedUssClassName, newValue);
    }
}
```

**Why `BaseField<bool>`:** Auto `ChangeEvent<bool>` dispatch, built-in label, `INotifyValueChanged<bool>` for data binding.

### ShopItemComponent — userData + StopImmediatePropagation

```csharp
// Assets/Scripts/UI/Components/ShopItemComponent.cs
public void RegisterCallbacks()
{
    m_BuyButton.userData = m_ShopItemData;  // Store SO reference — no closures needed
    m_BuyButton.RegisterCallback<ClickEvent>(BuyAction);
    m_BuyButton.RegisterCallback<PointerMoveEvent>(evt => evt.StopImmediatePropagation());
}

void BuyAction(ClickEvent evt)
{
    ShopItemSO data = (evt.currentTarget as VisualElement).userData as ShopItemSO;
    ShopEvents.ShopItemClicked?.Invoke(data, screenPos);
}
```

- **`userData`**: Avoids allocation per item, works with recycled elements
- **`StopImmediatePropagation()`**: Prevents `PointerMoveEvent` from reaching parent ScrollView

### UIManager — Single-Document Navigation

```csharp
// Assets/Scripts/UI/UIViews/UIManager.cs
[RequireComponent(typeof(UIDocument))]
public class UIManager : MonoBehaviour
{
    UIView m_CurrentView, m_PreviousView;
    List<UIView> m_AllViews = new List<UIView>();

    void SetupViews()
    {
        var root = m_MainMenuDocument.rootVisualElement;
        m_HomeView = new HomeView(root.Q<VisualElement>("HomeScreen"));
        m_ShopView = new ShopView(root.Q<VisualElement>("ShopScreen"));
        m_MailView = new MailView(root.Q<VisualElement>("MailScreen"));
    }

    void ShowModalView(UIView newView)
    {
        m_CurrentView?.Hide();
        m_PreviousView = m_CurrentView;
        m_CurrentView = newView;
        m_CurrentView?.Show();
    }

    void OnSettingsScreenShown()
    {
        m_PreviousView = m_CurrentView;
        m_SettingsView.Show();
    }

    void OnDisable() { foreach (var v in m_AllViews) v.Dispose(); }
}
```

**Patterns:** Single UIDocument with subtree views. Modal replaces current; overlay stacks. `m_AllViews` ensures centralized lifecycle disposal.

---

## USS Organization

### Base USS Files

All 7 files in `Assets/UI/Uss/Base/`:

| File | Lines | Key Content | Notable Pattern |
|------|-------|------------|-----------------|
| **Colors.uss** | 45 | BEM text/bg/border color utilities: `.color__text--white`, `.color__background--orange` | ⚠️ BUG: `.color__text--blue` uses orange `rgb(243,156,18)` |
| **Text.uss** | 41 | Global font (`AlfaSlabOne-Regular SDF`), size scale (35/45/60/80px), text shadows | Fixed pixel sizes, not token-based |
| **Common.uss** | 118 | `:root` font/cursor, border/alignment utilities, `.screen__anchor--fill`, `.theme__decoration--default` | `:root` used ONLY for font + cursor, NOT design tokens |
| **Buttons.uss** | 65 | Transparent base `Button`, hover scale 1.1, colored variants via `-unity-background-image-tint-color` | Tint-based coloring: single sprite → many color variants |
| **Sliders.uss** | 54 | Custom dragger/tracker images, orange tint knob | Replaces Unity default parts with game-themed images |
| **Dropdowns.uss** | 37 | Label/container/hover styling for `DropdownField` | ⚠️ **MUST import via TSS, not UXML** — compound parts only resolve via TSS |
| **Cursors.uss** | 140 | Two-cursor system: `Cursor_A` (arrow), `Cursor_B` (pointer) | Applied via type selectors: `Button`, `Toggle`, `Slider`, etc. |

> **BEM naming**: `{category}__{property}--{value}`. Applied as additive classes in UXML: `<Label class="color__text--white text__size--large">`.

### DC vs Recommended Approach

| Aspect | Dragon Crashers (Actual) | Recommended (Modern) |
|---|---|---|
| **Color system** | BEM classes: `.color__text--white` with hardcoded `rgb()` | `:root` variables: `--color-text-primary` with `var()` |
| **Typography** | Fixed pixel sizes: `.text__size--small { font-size: 35px; }` | Token scale: `--font-size-sm: 12px` + `var()` |
| **Spacing** | Inline values per element | `--space-*` tokens from a 4px grid |
| **Theming** | Swap entire TSS file (7-file matrix) | Override `:root` variables per theme |
| **Strengths** | Simple, no variable indirection, easy to debug | Scalable, theme-flexible, single-source tokens |
| **Weaknesses** | Color changes require editing every class | Variable resolution adds debugging complexity |
| **Best for** | Fixed-theme games with orientation support | Apps needing dark/light modes or brand customization |

---

## TSS Inheritance Chain

### 7-File Matrix

```
Assets/UI/Themes/
├── RuntimeTheme-Default.tss               ← Base: Unity defaults + Decoration-Default.uss
├── RuntimeTheme-Landscape.tss             ← @import Default.tss + all Landscape/*.uss
│   ├── RuntimeTheme-Landscape--Christmas.tss  ← @import Landscape.tss + Decoration-Christmas.uss
│   └── RuntimeTheme-Landscape--Halloween.tss  ← @import Landscape.tss + Decoration-Halloween.uss
└── RuntimeTheme-Portrait.tss              ← @import Default.tss + all Portrait/*.uss
    ├── RuntimeTheme-Portrait--Christmas.tss   ← @import Portrait.tss + Decoration-Christmas.uss
    └── RuntimeTheme-Portrait--Halloween.tss   ← @import Portrait.tss + Decoration-Halloween.uss
```

### TSS File Details

| TSS File | Inherits From | Adds | Screen USS Count |
|---|---|---|---|
| **RuntimeTheme-Default.tss** | `unity-theme://default` | ChartLibrary.uss, Decoration-Default.uss, Dropdowns.uss¹ | 3 |
| **RuntimeTheme-Landscape.tss** | Default.tss | 11 `Landscape/*.uss` (MenuBar, HomeScreen, CharScreen, ShopScreen, MailScreen, SettingsScreen, etc.) | 11 |
| **RuntimeTheme-Portrait.tss** | Default.tss | 11 `Portrait/*.uss` (same screens as Landscape) | 11 |
| **RuntimeTheme-Landscape--Christmas.tss** | Landscape.tss | Decoration-Christmas.uss | 1 |
| **RuntimeTheme-Portrait--Halloween.tss** | Portrait.tss | Decoration-Halloween.uss | 1 |

> ¹ `Dropdowns.uss` must be in TSS (not UXML) because compound element sub-parts only resolve correctly via TSS.

### Decoration USS Files

Seasonal decorations use visibility toggling:

```
Assets/UI/Uss/ThemeStyles/
├── Decoration-Default.uss      ← Shows .theme__decoration--default, hides others
├── Decoration-Christmas.uss    ← Shows .theme__decoration--christmas, hides others
└── Decoration-Halloween.uss    ← Shows .theme__decoration--halloween, hides others
```

```css
/* Decoration-Christmas.uss */
.theme__decoration--christmas { opacity: 1; display: flex; }
.theme__decoration--halloween { opacity: 0; display: none; }
.theme__decoration--default { display: none; opacity: 0; }
```

### Orientation USS Pattern

Orientation USS files override the **same CSS classes** with different layout values — no C# class toggling needed:

| CSS Class | Landscape (Sidebar) | Portrait (Top Bar) | Key Change |
|---|---|---|---|
| `.menu-bar__container` | `width: 13%; height: 100%; flex-direction: column` | `width: 100%; height: 13%; flex-direction: row` | column → row |
| `.menu-bar__logo` | `width: 90%; height: 12%` | `width: 10%; height: 80%` | Large → small |
| `.menu-bar__button-group` | `flex-direction: column; width: 80%` | `flex-direction: row; width: 80%` | column → row |
| `.home-screen__hero` | `width: 70%; height: 80%` | `width: 100%; height: 50%` | Wide → stacked |
| `.home-screen__sidebar` | `width: 25%; flex-direction: column` | `width: 100%; flex-direction: row` | Side → bottom |

> USS files at `Assets/UI/Uss/ThemeStyles/{Landscape,Portrait}/{Screen}-{Orientation}.uss`.

---

## Theme Event System

Two event files drive theming (`Assets/Scripts/UI/Events/`):

- **`ThemeEvents.ThemeChanged`** (`Action<string>`) — compound theme name (e.g. `"Landscape--Christmas"`)
- **`ThemeEvents.CameraUpdated`** (`Action<Camera>`) — main camera reference changes
- **`MediaQueryEvents.ResolutionUpdated`** (`Action<Vector2>`)
- **`MediaQueryEvents.AspectRatioUpdated`** (`Action<MediaAspectRatio>`)
- **`MediaQueryEvents.SafeAreaUpdated`** (`Action<Rect>`)
- **`MediaQueryEvents.DpiUpdated`** (`Action<float>`)

### Theme Data Flow

```
Season change (user action):
  SettingsView → SettingsEvents.UIGameDataUpdated → SettingsScreenController.UpdateTheme()
    → constructs "Portrait--Halloween" → ThemeEvents.ThemeChanged → ThemeManager.ApplyTheme()

Orientation change (device rotation):
  MediaQuery → MediaQueryEvents.AspectRatioUpdated → ThemeManager.OnAspectRatioUpdated()
    → keeps "--Halloween" suffix, swaps prefix → ApplyTheme("Landscape--Halloween")
```

### SettingsScreenController — Compound Theme Construction

```csharp
// Assets/Scripts/UI/Controllers/SettingsScreenController.cs
public class SettingsScreenController : MonoBehaviour
{
    GameData m_SettingsData;
    MediaAspectRatio m_MediaAspectRatio = MediaAspectRatio.Undefined;

    void OnEnable()
    {
        MediaQueryEvents.ResolutionUpdated += OnResolutionUpdated;
        SettingsEvents.UIGameDataUpdated += OnUISettingsUpdated;
    }

    void UpdateTheme()
    {
        string newTheme = m_MediaAspectRatio.ToString() + "--" + m_SettingsData.theme;
        ThemeEvents.ThemeChanged(newTheme);  // e.g. "Landscape--Christmas"
    }
}
```

### Adding a New Season

1. Create `Decoration-Easter.uss` — show `.theme__decoration--easter`, hide all others
2. Create `RuntimeTheme-Landscape--Easter.tss` and `RuntimeTheme-Portrait--Easter.tss`
3. Add 2 entries to `ThemeManager.m_ThemeSettings`: `"Landscape--Easter"` and `"Portrait--Easter"`
4. Add `"Easter"` to Settings UXML dropdown and `.theme__decoration--easter { display: none; }` to existing Decoration USS files

---

## Performance Analysis

### FPS Counter with Ring Buffer

```csharp
// Assets/Scripts/Utilities/FpsCounter.cs
public class FpsCounter : MonoBehaviour
{
    public const int k_TargetFrameRate = 60;
    public const int k_BufferSize = 50;

    [SerializeField] UIDocument m_Document;
    float[] m_DeltaTimeBuffer;
    int m_CurrentIndex;
    Label m_FpsLabel;
    bool m_IsEnabled;

    void Awake() { m_DeltaTimeBuffer = new float[k_BufferSize]; Application.targetFrameRate = k_TargetFrameRate; }
    void OnEnable() { SettingsEvents.FpsCounterToggled += OnFpsCounterToggled; m_FpsLabel = m_Document.rootVisualElement.Q<Label>("fps-counter"); }
    void OnDisable() { SettingsEvents.FpsCounterToggled -= OnFpsCounterToggled; }

    void Update()
    {
        if (!m_IsEnabled) return;
        m_DeltaTimeBuffer[m_CurrentIndex] = Time.deltaTime;
        m_CurrentIndex = (m_CurrentIndex + 1) % m_DeltaTimeBuffer.Length;
        m_FpsLabel.text = $"FPS: {Mathf.RoundToInt(CalculateFps())}";  // ⚠ per-frame string alloc
    }
}
```

**Notes**: Ring buffer avoids List resizing. `m_IsEnabled` guard = zero cost when off. ⚠ Per-frame `$"FPS: {value}"` allocates ~40 bytes.

### HealthBarController — LateUpdate Cost

```csharp
// Assets/Scripts/UI/Controllers/HealthBarController.cs
void MoveToWorldPosition(VisualElement element, Vector3 worldPosition, Vector2 worldSize)
{
    Rect rect = RuntimePanelUtils.CameraTransformWorldToPanelRect(
        element.panel, worldPosition, worldSize, Camera.main);
    element.transform.position = rect.position;  // transform, not layout — good
}

private void LateUpdate()
{
    ShowNameAndStats(m_ShowNameplate, m_ShowStat);  // ⚠ calls Q<> every frame
    MoveToWorldPosition(m_HealthBar, transformToFollow.position, m_WorldSize);
}
```

**Issues**: `Camera.main` calls `FindWithTag` internally — cache it. `ShowNameAndStats` calls `Q<>` per frame — should cache in `OnEnable`.

### Async/Await GC Cost

| Pattern | Allocation per iteration | Notes |
|---------|------------------------|-------|
| `await Task.Delay(ms)` | Timer + TaskCompletionSource (~120 bytes) | Adds up in per-frame loops |
| `_ = SomeAsync()` | Task object (~72 bytes) | One-time per fire-and-forget call |
| `label.text += c` | New string per character | Use `StringBuilder` instead |
| `value.ToString("0")` | String allocation (~24 bytes) | Update only when display value changes |

### Dynamic List: Instantiate vs ListView

| Item Count | Approach | Why |
|-----------|----------|-----|
| < 20 | `Instantiate()` in loop | Simpler code, negligible cost |
| 20–50 | Consider `ListView` | Layout cost grows linearly |
| 50+ | **Must use `ListView`** | Only creates ~8-15 visible elements |

### Event Propagation — StopImmediatePropagation

| Method | Effect | Use Case |
|--------|--------|----------|
| `StopPropagation()` | Stops bubbling, remaining listeners on current target still fire | Most cases |
| `StopImmediatePropagation()` | Stops bubbling AND remaining listeners on current target | Block ScrollView drag |
| `PreventDefault()` | Prevents default behavior, event still propagates | Rarely needed |

### Event Subscription Lifecycle Rules

1. **Every `+=` must have a matching `-=`** in the symmetrical lifecycle method
2. **MonoBehaviour**: subscribe in `OnEnable`, unsubscribe in `OnDisable`
3. **Plain C# classes**: subscribe in constructor, unsubscribe in `Dispose()`
4. **UI callbacks** (`RegisterCallback`): unregister in Dispose/OnDisable if element outlives handler
5. **Static events** are most dangerous — root subscriber in memory indefinitely if not unsubscribed

---

## Debugging Scenarios

### Event Bus Debugging

**Symptom**: Button click does nothing, screen doesn't switch, handler fires twice.

**Steps**:
1. **Verify subscription pairing** — every `+=` in `OnEnable` must have `-=` in `OnDisable`:
```csharp
void SubscribeToEvents() { MainMenuUIEvents.HomeScreenShown += OnHomeScreenShown; }
void UnsubscribeFromEvents() { MainMenuUIEvents.HomeScreenShown -= OnHomeScreenShown; }
```
2. **Add temporary invocation list logging**:
```csharp
public static void DebugInvocationList(string eventName, Delegate del)
{
    if (del == null) { Debug.Log($"[EventBus] {eventName}: no subscribers"); return; }
    foreach (var d in del.GetInvocationList())
        Debug.Log($"[EventBus] {eventName} → {d.Target?.GetType().Name ?? "static"}.{d.Method.Name}");
}
```
3. **Check null invocation** — `?.Invoke()` silently does nothing if no subscriber added
4. **Watch for double-subscribe** — if `OnEnable` runs twice without `OnDisable`, handler fires twice

### Async Task Debugging

**Symptom**: Async UI animation starts but never completes. No error in console.

**Steps**:
1. **Add try/catch inside every async method** (only reliable approach for fire-and-forget):
```csharp
async Task ClaimRewardRoutineAsync()
{
    try { /* animation code */ await Task.Delay((int)(k_TransitionTime * 1000)); }
    catch (Exception ex) { Debug.LogException(ex); }
}
```
2. **Register global unobserved task handler**:
```csharp
TaskScheduler.UnobservedTaskException += (sender, e) =>
{
    Debug.LogError($"[UnobservedTask] {e.Exception.InnerException?.Message}");
    e.SetObserved();
};
```
3. **Check `Task.Delay` args** — negative ms throws `ArgumentOutOfRangeException` (swallowed)
4. **Verify UI element not null** — if view disposed mid-animation, `NullReferenceException` is swallowed

### World-to-Panel Debugging

**Symptom**: Health bar doesn't appear or appears at wrong position.

**Steps**:
1. **Check `element.panel` is not null** — element has no panel until attached to UIDocument
2. **Check `Camera.main` is not null** — returns null if no camera tagged "MainCamera"
3. **Check `transformToFollow` is assigned** — null if character destroyed
4. **Verify return values** — position behind camera gives negative/huge coordinates
5. **LateUpdate timing** — camera must move before health bar updates (execution order)

### Theme Debugging

**Symptom**: Theme doesn't change, wrong theme after rotation, styles revert to default.

**Steps**:
1. **Enable `m_Debug` on ThemeManager** — logs `[ThemeManager]` prefixed messages
2. **Verify compound name construction** — `mediaAspectRatio.ToString() + suffix` must match `ThemeSettings` list
3. **Check ThemeSettings list completeness** — all 6 combos must exist (2 orientations × 3 seasons)
4. **Verify TSS and PanelSettings assets** — null field = silent failure
5. **`[ExecuteInEditMode]` caveat** — Play mode changes persist to asset

### SafeArea Debugging

**Symptom**: Safe area borders don't appear in Editor, or values are 0.

**Steps**:
1. **Expected in Editor** — `Screen.safeArea` equals full screen (zero insets). Use Device Simulator.
2. **Enable `m_Debug` flag** — logs applied border values
3. **Check `m_Element` name** — if name doesn't match UXML element, `m_Root` is null
4. **Verify `m_Multiplier`** — `[Range(0, 1)]`, if 0 all borders = 0
5. **GeometryChangedEvent timing** — if UIDocument not initialized, safe area deferred
6. **Border color transparency** — alpha = 0 makes borders invisible

### Modal/Overlay Debugging

**Symptom**: Views stack incorrectly, previous view doesn't restore.

**Steps**:
1. **Trace view state** — log `m_CurrentView`/`m_PreviousView` in `ShowModalView`
2. **Check overlay Show/Hide pairing** — if hide event never fires, `m_PreviousView` gets stuck
3. **Check `Dispose()` on all views** — missing `base.Dispose()` causes leaked subscriptions
4. **Verify `UIView.IsHidden`** — checks inline style, not resolved style
5. **Use Visual Tree Dump** — `UIDebugUtils.DumpTree(root)` shows display state

---

## Experimental Features

### Position Animation (MenuBarView)

```csharp
void AnimateMarkerToTarget(VisualElement target, int ms = 200) {
    Vector2 world = target.parent.LocalToWorld(target.layout.position);
    Vector3 local = m_MenuMarker.parent.WorldToLocal(world);
    m_MenuMarker.experimental.animation.Position(
        local - new Vector3(m_MenuMarker.resolvedStyle.width / 2f, 0, 0), ms);
}
```

### Scale Pop-In

```csharp
element.transform.scale = new Vector3(0.1f, 0.1f, 1f);
element.experimental.animation.Scale(1f, 200);
```

### Click Cooldown Guard

```csharp
float m_NextClick = 0f;
void OnClicked(ClickEvent evt) {
    if (Time.time < m_NextClick) return;
    m_NextClick = Time.time + 0.2f;
    /* animate */
}
```

---

## DC Source Files Reference

### Event Classes (10 total)

| Event Class | Domain | Key Delegates |
|-------------|--------|---------------|
| `CharEvents` | Character screen | `CharacterShown`, `LevelPotionUsed`, `GearSlotUpdated` |
| `ShopEvents` | Shop/purchasing | `ShopItemPurchasing`, `TransactionProcessed`, `FundsUpdated` |
| `HomeEvents` | Home screen | `LevelInfoShown`, `PlayButtonClicked`, `ChatWindowShown` |
| `MailEvents` | Mail system | `RewardClaimed` |
| `InventoryEvents` | Inventory | Gear selection/equipment |
| `SettingsEvents` | Settings | `SettingsUpdated`, `PlayerFundsReset`, `FpsCounterToggled` |
| `GameplayEvents` | Gameplay | `SettingsUpdated` |
| `MainMenuUIEvents` | Main menu | `HomeScreenShown` |
| `MediaQueryEvents` | Responsive | Resolution, aspect ratio, safe area, DPI |
| `ThemeEvents` | Theming | `ThemeChanged`, `CameraUpdated` |

### Architecture Files

| File | Path | Role |
|------|------|------|
| UIView.cs | Assets/Scripts/UI/UIViews/ | Base class — template method |
| UIManager.cs | Assets/Scripts/UI/UIViews/ | Single-document modal navigation |
| MailView.cs | Assets/Scripts/UI/UIViews/ | Composite view — 3 sub-views |
| ShopView.cs | Assets/Scripts/UI/UIViews/ | Dynamic UI — Instantiate() |
| HomeView.cs | Assets/Scripts/UI/UIViews/ | Element caching + event wiring |
| HomeScreenController.cs | Assets/Scripts/UI/Controllers/ | Thin controller coordinator |
| TabbedMenuController.cs | Assets/Scripts/UI/Controllers/ | CSS class toggling tabs |
| HealthBarComponent.cs | Assets/Scripts/UI/Components/ | Custom control (deprecated UxmlFactory) |
| SlideToggle.cs | Assets/Scripts/UI/Components/ | Custom BaseField control |
| ShopItemComponent.cs | Assets/Scripts/UI/Components/ | Button.userData + StopImmediatePropagation |

### USS/TSS Files

| File | Content |
|------|---------|
| `Assets/UI/Uss/Base/Colors.uss` | BEM color utility classes |
| `Assets/UI/Uss/Base/Text.uss` | Font definition, text styles |
| `Assets/UI/Uss/Base/Common.uss` | `:root` font/cursor, utilities |
| `Assets/UI/Uss/Base/Buttons.uss` | Button states, tint variants |
| `Assets/UI/Uss/Base/Sliders.uss` | Custom slider styling |
| `Assets/UI/Uss/Base/Dropdowns.uss` | Dropdown styling (TSS-only) |
| `Assets/UI/Uss/Base/Cursors.uss` | Two-cursor system |
| `Assets/UI/Uss/ThemeStyles/Decoration-*.uss` | Season visibility toggles |
| `Assets/UI/Themes/RuntimeTheme-*.tss` | 7-file TSS matrix |
| `Assets/UI/Uss/ThemeStyles/{L,P}/*.uss` | 22 orientation USS files |

### Data & Persistence

| File | Role |
|------|------|
| `GameData.cs` | Serializable player state |
| `SaveManager.cs` | JsonUtility persistence |
| `GameDataManager.cs` | Central state, purchase logic |
| `ShopItemSO`, `EquipmentSO`, `CharacterBaseSO` | ScriptableObject data |
| `LevelSO`, `ChatSO`, `MailMessageSO` | Content data |
| `GameIconsSO` | Shared icon references |

### Shop Purchase Flow

```
User clicks "Buy" on shop item
  → ShopItemComponent fires ShopEvents.ShopItemClicked(shopItemSO, screenPos)
  → ShopScreenController.OnTryBuyItem()
    → ShopEvents.ShopItemPurchasing(shopItemSO, screenPos)
  → GameDataManager.OnPurchaseItem()
    → HasSufficientFunds?
    ├─ YES: PayTransaction() → ReceivePurchasedGoods()
    │       → ShopEvents.TransactionProcessed
    │       → ShopEvents.FundsUpdated(gameData)
    └─ NO:  ShopEvents.TransactionFailed(shopItem)
  → OptionsBarView receives FundsUpdated → updates gold/gem labels
  → PopUpText receives TransactionProcessed → shows animation
```

---
name: ui-toolkit-mobile
description: "Mobile optimization and touch input for Unity UI Toolkit. Covers touch handling, gesture detection, safe areas, orientation changes, mobile performance budgets, virtual keyboard management, and battery-conscious UI patterns. Use when: (1) Building touch-friendly UI with proper hit targets, (2) Handling safe areas and notches, (3) Detecting orientation changes, (4) Optimizing UI performance for mobile, (5) Managing virtual keyboard interactions, (6) Implementing swipe/long-press gestures. Triggers: 'mobile UI', 'touch input', 'safe area', 'orientation', 'mobile performance', 'virtual keyboard', 'swipe gesture', 'thumb zone'."
---

# UI Toolkit Mobile

> **Based on**: Unity 6 (6000.0), [Dragon Crashers](../references/dragon-crashers-insights.md) official sample

Mobile-first UI design for Unity UI Toolkit — touch input, safe areas, orientation, performance, and platform-specific behavior. Dragon Crashers uses `SafeAreaHandler` on root, bottom tab navigation, and transform-only animations for mobile-grade performance.

## Touch Input Handling

UI Toolkit pointer events map directly to touch on mobile. Use `PointerDownEvent`, `PointerMoveEvent`, `PointerUpEvent` — not `ClickEvent` for gesture-aware interactions.

### Minimum Touch Target Size

Every interactive element must meet the **44×44dp minimum** (Apple HIG / Material Design):

```css
.touch-target {
    min-width: 44px;
    min-height: 44px;
    padding: 8px;
}
```

### Gesture Detection

```csharp
using UnityEngine;
using UnityEngine.UIElements;

public class GestureDetector : Manipulator
{
    const float SwipeThreshold = 50f;
    const float LongPressDuration = 0.5f;

    Vector2 _startPos;
    float _startTime;
    bool _isActive;
    IVisualElementScheduledItem _longPressTimer;

    public event System.Action<Vector2> OnSwipe;
    public event System.Action OnLongPress;
    public event System.Action OnTap;

    protected override void RegisterCallbacksOnTarget()
    {
        target.RegisterCallback<PointerDownEvent>(OnPointerDown);
        target.RegisterCallback<PointerMoveEvent>(OnPointerMove);
        target.RegisterCallback<PointerUpEvent>(OnPointerUp);
    }

    protected override void UnregisterCallbacksFromTarget()
    {
        target.UnregisterCallback<PointerDownEvent>(OnPointerDown);
        target.UnregisterCallback<PointerMoveEvent>(OnPointerMove);
        target.UnregisterCallback<PointerUpEvent>(OnPointerUp);
    }

    void OnPointerDown(PointerDownEvent evt)
    {
        _startPos = evt.position;
        _startTime = Time.unscaledTime;
        _isActive = true;
        target.CapturePointer(evt.pointerId);
        _longPressTimer = target.schedule.Execute(() =>
        {
            if (_isActive) { OnLongPress?.Invoke(); _isActive = false; }
        }).StartingIn((long)(LongPressDuration * 1000));
    }

    void OnPointerMove(PointerMoveEvent evt)
    {
        if (!_isActive) return;
        if (((Vector2)evt.position - _startPos).magnitude > SwipeThreshold * 0.5f)
            _longPressTimer?.Pause();
    }

    void OnPointerUp(PointerUpEvent evt)
    {
        if (!_isActive) return;
        _isActive = false;
        _longPressTimer?.Pause();
        target.ReleasePointer(evt.pointerId);

        Vector2 delta = (Vector2)evt.position - _startPos;
        float elapsed = Time.unscaledTime - _startTime;

        if (delta.magnitude >= SwipeThreshold) OnSwipe?.Invoke(delta.normalized);
        else if (elapsed < LongPressDuration) OnTap?.Invoke();
    }
}
```

Usage:

```csharp
var gesture = new GestureDetector();
gesture.OnSwipe += dir => Debug.Log($"Swipe: {dir}");
gesture.OnLongPress += () => Debug.Log("Long press");
gesture.OnTap += () => Debug.Log("Tap");
element.AddManipulator(gesture);
```

## Mobile Layouts

### Thumb Zone Design

Place primary actions in the **bottom third** — the natural thumb reach zone.

```
┌──────────────────┐
│  Status / Info    │  ← Hard to reach
│  Content Area     │  ← Scrollable
│  ───────────────  │
│  Primary Actions  │  ← Thumb zone (bottom 1/3)
│  [Tab] [Tab] [Tab]│
└──────────────────┘
```

### Bottom Navigation (UXML + USS)

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
  <ui:VisualElement name="screen-root" class="screen-root">
    <ui:VisualElement name="content-area" class="content-area">
      <ui:ScrollView name="scroll" class="content-scroll" />
    </ui:VisualElement>
    <ui:VisualElement name="bottom-nav" class="bottom-nav">
      <ui:Button name="tab-home" class="nav-tab nav-tab--active" text="Home" />
      <ui:Button name="tab-search" class="nav-tab" text="Search" />
      <ui:Button name="tab-profile" class="nav-tab" text="Profile" />
    </ui:VisualElement>
  </ui:VisualElement>
</ui:UXML>
```

```css
.screen-root { flex-grow: 1; flex-direction: column; }
.content-area { flex-grow: 1; overflow: hidden; }

.bottom-nav {
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    height: 56px;
    padding-bottom: var(--safe-area-bottom, 0px);
    background-color: rgb(30, 30, 30);
    border-top-width: 1px;
    border-top-color: rgb(60, 60, 60);
}

.nav-tab {
    flex-grow: 1;
    height: 100%;
    min-width: 64px;
    background-color: rgba(0, 0, 0, 0);
    border-width: 0;
    color: rgb(160, 160, 160);
    -unity-text-align: middle-center;
    font-size: 12px;
}

.nav-tab--active { color: rgb(100, 180, 255); }
```

## SafeArea Integration

Apply safe area insets as padding on the root. Reference `ui-toolkit-responsive` for the full `SafeAreaHandler`:

```csharp
public static class SafeAreaApplier
{
    public static void Apply(VisualElement root)
    {
        var sa = Screen.safeArea;
        root.style.paddingTop = new Length((Screen.height - sa.yMax) / Screen.height * 100f, LengthUnit.Percent);
        root.style.paddingBottom = new Length(sa.y / Screen.height * 100f, LengthUnit.Percent);
        root.style.paddingLeft = new Length(sa.x / Screen.width * 100f, LengthUnit.Percent);
        root.style.paddingRight = new Length((Screen.width - sa.xMax) / Screen.width * 100f, LengthUnit.Percent);
    }
}
```

Key considerations: **Notch** — top inset for status bar + notch on iOS/Android. **Home indicator** — bottom 34px on iPhones with gesture nav. **Rounded corners** — inset content from screen edges on modern devices.

### Dragon Crashers: SafeAreaBorder (borderWidth Approach)

> **Source**: `Assets/Scripts/Utilities/SafeAreaBorder.cs`

The Dragon Crashers project uses **borderWidth** instead of padding for safe area insets. Borders push content inward while allowing a configurable border color (black to match bezels, or transparent for background show-through).

**Why borderWidth over padding?** Borders can be **colored** via `borderColor`. `[ExecuteInEditMode]` enables **editor preview**. A configurable **multiplier** (0–1) fine-tunes inset intensity. Named element targeting (`m_Element`) applies safe area to a specific container.

```csharp
[ExecuteInEditMode]
public class SafeAreaBorder : MonoBehaviour
{
    [SerializeField] UIDocument m_Document;
    [SerializeField] Color m_BorderColor = Color.black;
    [SerializeField] string m_Element;        // Named element or empty for root
    [Range(0, 1f)]
    [SerializeField] float m_Multiplier = 1f; // Scale inset intensity
    VisualElement m_Root;

    public void Initialize()
    {
        m_Root = string.IsNullOrEmpty(m_Element)
            ? m_Document.rootVisualElement
            : m_Document.rootVisualElement.Q<VisualElement>(m_Element);
        m_Root?.RegisterCallback<GeometryChangedEvent>(evt => ApplySafeArea());
        ApplySafeArea();
    }

    void ApplySafeArea()
    {
        if (m_Root == null) return;
        Rect sa = Screen.safeArea;
        // Compute pixel insets — apply as borderWidth (NOT padding)
        m_Root.style.borderLeftWidth   = sa.x * m_Multiplier;
        m_Root.style.borderRightWidth  = (Screen.width - sa.xMax) * m_Multiplier;
        m_Root.style.borderTopWidth    = (Screen.height - sa.yMax) * m_Multiplier;
        m_Root.style.borderBottomWidth = sa.y * m_Multiplier;
        // Color the border (black for bezel match, transparent for show-through)
        m_Root.style.borderLeftColor = m_Root.style.borderRightColor =
        m_Root.style.borderTopColor = m_Root.style.borderBottomColor = m_BorderColor;
    }

    void OnValidate() => ApplySafeArea(); // Editor preview
}
```

**Padding vs borderWidth comparison:**

| Approach | Method | Color Control | Editor Preview | Use When |
|----------|--------|---------------|----------------|----------|
| Padding (generic) | `style.paddingTop` | No — transparent only | Manual | Content should extend to screen edge behind inset |
| **borderWidth (DC)** | `style.borderTopWidth` | Yes — `borderColor` | `[ExecuteInEditMode]` | Want visible border matching device bezel or theme |

## World-to-UI Alignment (PositionToVisualElement)

> **Source**: `Assets/Scripts/Utilities/PositionToVisualElement.cs`

Aligns 3D GameObjects to VisualElement positions — critical for mobile games that overlay 3D characters on UI panels. The conversion pipeline: `worldBound` → `GetScreenCoordinate` → `ScreenPosToWorldPos`.

```csharp
public class PositionToVisualElement : MonoBehaviour
{
    [SerializeField] GameObject m_ObjectToMove;
    [SerializeField] Camera m_Camera;
    [SerializeField] float m_Depth = 10f;
    [SerializeField] UIDocument m_Document;
    [SerializeField] string m_ElementName;
    VisualElement m_TargetElement;

    void OnEnable()
    {
        m_TargetElement = m_Document.rootVisualElement.Q<VisualElement>(name: m_ElementName);
        ThemeEvents.CameraUpdated += OnCameraUpdated;  // Orientation camera swap
        m_TargetElement?.RegisterCallback<GeometryChangedEvent>(OnGeometryChanged);
    }

    void OnDisable()
    {
        ThemeEvents.CameraUpdated -= OnCameraUpdated;
        m_TargetElement?.UnregisterCallback<GeometryChangedEvent>(OnGeometryChanged);
    }

    public void MoveToElement()
    {
        if (m_Camera == null || m_ObjectToMove == null || m_TargetElement == null) return;
        // Step 1: UI element center in UI Toolkit coords
        Rect wb = m_TargetElement.worldBound;
        Vector2 center = new(wb.x + wb.width / 2, wb.y + wb.height / 2);
        // Step 2: Convert to pixel screen coords
        Vector2 screenPos = center.GetScreenCoordinate(m_Document.rootVisualElement);
        // Step 3: Screen → 3D world at depth
        m_ObjectToMove.transform.position = screenPos.ScreenPosToWorldPos(m_Camera, m_Depth);
    }

    void OnCameraUpdated(Camera cam) { m_Camera = cam; MoveToElement(); }
    void OnGeometryChanged(GeometryChangedEvent evt) => MoveToElement();
}
```

**Key mobile considerations:** Orientation changes swap the camera via `ThemeEvents.CameraUpdated` → triggers repositioning. `GeometryChangedEvent` fires on UI resize. The `m_Depth` parameter controls distance from camera. Extension methods `GetScreenCoordinate` and `ScreenPosToWorldPos` handle coordinate space conversion.

## Orientation: MediaQuery + Event System

> **Sources**: `Assets/Scripts/Utilities/MediaQuery.cs`, `Assets/Scripts/UI/Events/MediaQueryEvents.cs`, `Assets/Scripts/UI/Events/ThemeEvents.cs`

Dragon Crashers uses an event-driven orientation system rather than polling `Screen.orientation`:

```csharp
public enum MediaAspectRatio { Undefined, Landscape, Portrait }

[ExecuteInEditMode]
public class MediaQuery : MonoBehaviour
{
    [SerializeField] UIDocument m_Document;
    public const float k_LandscapeMin = 1.2f;  // aspect >= 1.2 = landscape
    Vector2 m_CurrentResolution;
    MediaAspectRatio m_CurrentAspectRatio;

    void OnEnable()
    {
        m_Document.rootVisualElement?.RegisterCallback<GeometryChangedEvent>(
            evt => QueryResolution());
        QueryResolution();
    }

    public void QueryResolution()
    {
        Vector2 res = new(Screen.width, Screen.height);
        if (res != m_CurrentResolution)
        { m_CurrentResolution = res; MediaQueryEvents.ResolutionUpdated?.Invoke(res); }
        var ratio = CalculateAspectRatio(res);
        if (ratio != m_CurrentAspectRatio)
        { m_CurrentAspectRatio = ratio; MediaQueryEvents.AspectRatioUpdated?.Invoke(ratio); }
    }

    public static MediaAspectRatio CalculateAspectRatio(Vector2 res)
        => res.y < float.Epsilon ? MediaAspectRatio.Undefined
        : (res.x / res.y >= k_LandscapeMin ? MediaAspectRatio.Landscape : MediaAspectRatio.Portrait);
}
```

### Event Delegates

```csharp
// MediaQueryEvents — screen dimension changes
public static Action<Vector2> ResolutionUpdated;
public static Action<MediaAspectRatio> AspectRatioUpdated;
public static Action SafeAreaApplied;

// ThemeEvents — theme/camera changes triggered by orientation
public static Action<string> ThemeChanged;
public static Action<Camera> CameraUpdated;   // Fired when orientation swaps the active camera
```

**How it connects**: `MediaQuery` detects aspect ratio change → fires `AspectRatioUpdated` → `ThemeManager` switches portrait/landscape theme → fires `ThemeEvents.CameraUpdated` → `PositionToVisualElement` repositions 3D content. See `ui-toolkit-theming` for theme switching details.

## Mobile Frame Rate Control (FpsCounter)

> **Source**: `Assets/Scripts/Utilities/FpsCounter.cs`

Dragon Crashers sets `Application.targetFrameRate` explicitly for mobile battery management and provides a toggleable FPS overlay for debugging:

```csharp
public class FpsCounter : MonoBehaviour
{
    public const int k_TargetFrameRate = 60; // 60 for mobile, -1 for uncapped (PC)
    const int k_BufferSize = 50;             // Ring buffer for smoothed FPS
    [SerializeField] UIDocument m_Document;
    float[] m_DeltaTimeBuffer;
    int m_CurrentIndex;
    Label m_FpsLabel;
    bool m_IsEnabled;

    void Awake()
    {
        m_DeltaTimeBuffer = new float[k_BufferSize];
        Application.targetFrameRate = k_TargetFrameRate; // Set explicitly for mobile
    }

    void OnEnable()
    {
        SettingsEvents.FpsCounterToggled += OnToggled;
        SettingsEvents.TargetFrameRateSet += fps => Application.targetFrameRate = fps;
        m_FpsLabel = m_Document.rootVisualElement.Q<Label>("fps-counter");
    }

    void Update()
    {
        if (!m_IsEnabled) return;
        m_DeltaTimeBuffer[m_CurrentIndex] = Time.deltaTime;
        m_CurrentIndex = (m_CurrentIndex + 1) % k_BufferSize;
        float total = 0f; foreach (float dt in m_DeltaTimeBuffer) total += dt;
        m_FpsLabel.text = $"FPS: {Mathf.RoundToInt(k_BufferSize / total)}";
    }

    void OnToggled(bool state)
    {
        m_IsEnabled = state;
        m_FpsLabel.style.visibility = state ? Visibility.Visible : Visibility.Hidden;
    }
}
```

**Mobile frame rate tips:** Set `targetFrameRate = 60` in `Awake` — don't rely on default (`-1` = uncapped, wastes battery). Use ring buffer averaging (50 frames) for stable FPS display. Toggle visibility via `Visibility.Hidden` (preserves layout). Wire to settings events for user-controlled 30/60 FPS switching.

## Orientation Handling

```csharp
using UnityEngine;
using UnityEngine.UIElements;

public class OrientationHandler : MonoBehaviour
{
    [SerializeField] UIDocument _uiDocument;
    ScreenOrientation _lastOrientation;

    void OnEnable()
    {
        _lastOrientation = Screen.orientation;
        ApplyOrientation(_lastOrientation);
    }

    void Update()
    {
        if (Screen.orientation == _lastOrientation) return;
        _lastOrientation = Screen.orientation;
        ApplyOrientation(_lastOrientation);
    }

    void ApplyOrientation(ScreenOrientation orientation)
    {
        var root = _uiDocument.rootVisualElement;
        bool portrait = orientation is ScreenOrientation.Portrait
                     or ScreenOrientation.PortraitUpsideDown;
        root.EnableInClassList("orientation--portrait", portrait);
        root.EnableInClassList("orientation--landscape", !portrait);
        SafeAreaApplier.Apply(root);
    }
}
```

```css
/* Portrait: stack vertically, show bottom nav */
.orientation--portrait .main-layout { flex-direction: column; }
.orientation--portrait .sidebar { display: none; }
.orientation--portrait .bottom-nav { display: flex; }

/* Landscape: side-by-side with sidebar */
.orientation--landscape .main-layout { flex-direction: row; }
.orientation--landscape .sidebar { display: flex; width: 240px; }
.orientation--landscape .bottom-nav { display: none; }
```

## Mobile Performance

### Budget Table

| Metric | Mobile Target | Desktop Target |
|--------|--------------|----------------|
| Draw calls (UI) | < 15 | < 40 |
| Visual elements | < 200 visible | < 500 visible |
| USS selectors | < 3 levels deep | < 5 levels deep |
| Texture memory (UI) | < 8 MB | < 32 MB |
| Layout recalcs/frame | 0 during gameplay | < 2 |
| Animation properties | Transform-only | Any non-layout |

### Optimization Rules

1. **Flatten hierarchy** — each nesting level costs. Merge decorative containers.
2. **Use `UsageHints.DynamicTransform`** on animated elements.
3. **Avoid complex selectors** — prefer direct class matches over deep nesting.
4. **Pool list items** — use `ListView` with `makeItem`/`bindItem` for virtualization.
5. **Atlas textures** — combine small icons into a sprite atlas for fewer draw calls.

```csharp
animatedElement.usageHints = UsageHints.DynamicTransform;
element.visible = false;                       // Skips render, keeps layout
element.style.display = DisplayStyle.None;     // Removes from layout entirely
```

## Touch Feedback

### Press Effect via USS Transitions

```css
.btn-mobile {
    transition-property: scale, background-color;
    transition-duration: 80ms, 120ms;
    transition-timing-function: ease-out, ease-out;
    scale: 1 1;
    background-color: rgb(60, 60, 60);
}

.btn-mobile:active {
    scale: 0.95 0.95;
    background-color: rgb(80, 80, 80);
}
```

### Haptic Feedback Hook

```csharp
using UnityEngine;
#if UNITY_IOS
using System.Runtime.InteropServices;
#endif

public static class HapticFeedback
{
#if UNITY_IOS
    [DllImport("__Internal")] static extern void _TriggerHaptic(int style);
#endif

    public enum Style { Light, Medium, Heavy }

    public static void Trigger(Style style = Style.Light)
    {
#if UNITY_IOS
        _TriggerHaptic((int)style);
#elif UNITY_ANDROID
        using var player = new AndroidJavaClass("com.unity3d.player.UnityPlayer");
        using var activity = player.GetStatic<AndroidJavaObject>("currentActivity");
        using var vibrator = activity.Call<AndroidJavaObject>("getSystemService", "vibrator");
        vibrator.Call("vibrate", style == Style.Light ? 10L : style == Style.Medium ? 20L : 30L);
#endif
    }

    public static void AttachTo(Button button, Style style = Style.Light)
    {
        button.clicked += () => Trigger(style);
    }
}
```

## Virtual Keyboard

Scroll focused input fields above the on-screen keyboard:

```csharp
using UnityEngine;
using UnityEngine.UIElements;

public class VirtualKeyboardHandler : MonoBehaviour
{
    [SerializeField] UIDocument _uiDocument;
    ScrollView _scrollView;
    VisualElement _focusedField;

    void OnEnable()
    {
        var root = _uiDocument.rootVisualElement;
        _scrollView = root.Q<ScrollView>("content-scroll");
        root.RegisterCallback<FocusInEvent>(OnFocusIn);
        root.RegisterCallback<FocusOutEvent>(OnFocusOut);
    }

    void OnDisable()
    {
        var root = _uiDocument.rootVisualElement;
        root.UnregisterCallback<FocusInEvent>(OnFocusIn);
        root.UnregisterCallback<FocusOutEvent>(OnFocusOut);
    }

    void OnFocusIn(FocusInEvent evt)
    {
        if (evt.target is not TextField tf) return;
        _focusedField = tf;
        tf.schedule.Execute(ScrollToField).StartingIn(300);
    }

    void OnFocusOut(FocusOutEvent evt) => _focusedField = null;

    void ScrollToField()
    {
        if (_focusedField == null || _scrollView == null) return;
        float kbHeight = GetKeyboardHeight();
        if (kbHeight <= 0) return;
        _scrollView.style.paddingBottom = kbHeight;
        _scrollView.ScrollTo(_focusedField);
    }

    void Update()
    {
        if (_focusedField == null && _scrollView != null)
            _scrollView.style.paddingBottom = 0;
    }

    static float GetKeyboardHeight()
    {
#if UNITY_IOS || UNITY_ANDROID
        return TouchScreenKeyboard.area.height;
#else
        return 0;
#endif
    }
}
```

## Battery Considerations

| Strategy | Implementation |
|----------|---------------|
| Throttle animations | `Application.targetFrameRate = 30` when on battery |
| Reduce update frequency | Skip UI refreshes if data unchanged |
| Dark theme for OLED | Pure black backgrounds (`rgb(0,0,0)`) save power |
| Pause off-screen UI | `visible = false` for panels not in view |

```css
.theme--dark-oled .panel-background { background-color: rgb(0, 0, 0); }
.theme--dark-oled .card { background-color: rgb(18, 18, 18); border-color: rgb(40, 40, 40); }
```

```csharp
// See also: FpsCounter.cs sets Application.targetFrameRate via SettingsEvents
Application.targetFrameRate = onBattery ? 30 : 60;
if (onBattery) QualitySettings.vSyncCount = 0;
```

## Platform Detection

```csharp
public static class MobilePlatform
{
    public static bool IsMobile =>
        Application.platform is RuntimePlatform.Android or RuntimePlatform.IPhonePlayer;
    public static bool IsIOS => Application.platform == RuntimePlatform.IPhonePlayer;
    public static bool IsAndroid => Application.platform == RuntimePlatform.Android;
    public static bool IsTablet => IsMobile && Mathf.Min(Screen.width, Screen.height) >= 600;

    public static void ApplyPlatformClasses(VisualElement root)
    {
        root.EnableInClassList("platform--mobile", IsMobile);
        root.EnableInClassList("platform--desktop", !IsMobile);
        root.EnableInClassList("platform--ios", IsIOS);
        root.EnableInClassList("platform--android", IsAndroid);
        root.EnableInClassList("platform--tablet", IsTablet);
    }
}
```

```css
.platform--mobile .tooltip { display: none; }
.platform--mobile .hover-preview { display: none; }
.platform--mobile .btn { min-height: 48px; font-size: 16px; }
.platform--tablet .content-column { max-width: 720px; }
```

## Mobile Checklist

- [ ] All touch targets ≥ 44×44px
- [ ] Safe area applied — borderWidth (DC approach) or padding (generic)
- [ ] `[ExecuteInEditMode]` on SafeAreaBorder for editor preview
- [ ] Orientation changes handled with layout shifts
- [ ] MediaQuery fires AspectRatioUpdated on orientation change
- [ ] PositionToVisualElement aligns 3D content to UI panels
- [ ] CameraUpdated event wired for orientation-aware 3D positioning
- [ ] Bottom navigation in thumb zone for primary actions
- [ ] No hover-dependent interactions
- [ ] Virtual keyboard doesn't obscure focused input fields
- [ ] USS transitions use transform properties only
- [ ] `Application.targetFrameRate` set explicitly (60 active, 30 battery-save)
- [ ] Visible element count < 200 during gameplay
- [ ] Sprite atlases used for UI icons
- [ ] Haptic feedback on key interactions
- [ ] Dark/OLED theme available
- [ ] Platform-specific USS classes applied at startup
- [ ] `UsageHints.DynamicTransform` on animated elements
- [ ] FPS counter toggleable for mobile debugging
- [ ] Tested on actual devices (not just simulator)

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Touch targets < 44px | Missed taps, frustration | `min-width`/`min-height: 44px` |
| Hover-dependent UI | No hover on touch screens | `:active` or tap-to-reveal |
| Excessive animations | Battery drain, frame drops | Essential feedback only; transforms |
| Ignoring safe area | Content behind notch/home bar | `SafeAreaApplier` on root |
| Deep USS selectors | Slow style resolution | Max 2-3 levels; direct classes |
| Layout property animation | Layout thrashing | `translate`, `scale`, `rotate`, `opacity` |
| Always-on 60fps | Battery drain | Throttle to 30fps when idle |
| Pixel-based sizing | Breaks across DPI | Use `%`, flex, USS custom properties |

## Exercise: Mobile Settings Screen

Build a touch-friendly settings screen: (1) `Settings.uxml` — vertical layout with toggle rows, slider, bottom "Save" in thumb zone. (2) `Settings.uss` — touch targets ≥ 48px, `SafeArea` padding via CSS custom properties, portrait/landscape variants. (3) `SettingsScreen.cs` — apply `SafeAreaBorder`, attach `MediaQuery`, wire `GestureDetector` for swipe-back. (4) Test orientation switching, safe area insets, 44px minimum targets.

## Cross-References

| Skill | Relevance |
|-------|-----------|
| [ui-toolkit-responsive](../ui-toolkit-responsive/SKILL.md) | Responsive layouts, breakpoint systems, SafeAreaHandler base |
| [ui-toolkit-theming](../ui-toolkit-theming/SKILL.md) | Portrait/landscape theme switching, ThemeManager integration |
| [ui-toolkit-performance](../ui-toolkit-performance/SKILL.md) | Mobile performance budgets, draw call optimization, USS selector depth |

**Project source files referenced:** `SafeAreaBorder.cs`, `PositionToVisualElement.cs`, `MediaQuery.cs`, `FpsCounter.cs`, `ThemeEvents.cs`, `MediaQueryEvents.cs` (all under `Assets/Scripts/`)

## Shared Resources

- [Performance Benchmarks](../references/performance-benchmarks.md) — mobile budgets, draw call targets
- [Dragon Crashers Insights](../references/dragon-crashers-insights.md) — mobile patterns from DC
- [Code Templates](../references/code-templates.md) — SafeArea handler, base screen templates
- [Official Docs Links](../references/official-docs-links.md) — Unity 6 documentation index

## Official Documentation

- [Unity UI Toolkit Events](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-Events.html)
- [Performance Considerations](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-performance-considerations.html)
- [Apple HIG — Touch Targets](https://developer.apple.com/design/human-interface-guidelines/accessibility)
- [Material Design — Touch Targets](https://m3.material.io/foundations/accessible-design/accessibility-basics)

---
**← Previous**: [Performance](../ui-toolkit-performance/SKILL.md) | **Next →**: [Debugging](../ui-toolkit-debugging/SKILL.md)
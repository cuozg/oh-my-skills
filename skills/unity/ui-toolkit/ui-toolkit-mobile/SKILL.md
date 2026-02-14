---
name: ui-toolkit-mobile
description: "Mobile optimization and touch input for Unity UI Toolkit. Covers touch handling, gesture detection, safe areas, orientation changes, mobile performance budgets, virtual keyboard management, and battery-conscious UI patterns. Use when: (1) Building touch-friendly UI with proper hit targets, (2) Handling safe areas and notches, (3) Detecting orientation changes, (4) Optimizing UI performance for mobile, (5) Managing virtual keyboard interactions, (6) Implementing swipe/long-press gestures. Triggers: 'mobile UI', 'touch input', 'safe area', 'orientation', 'mobile performance', 'virtual keyboard', 'swipe gesture', 'thumb zone'."
---

# UI Toolkit Mobile

<!-- OWNERSHIP: Touch handling, gesture detection (swipe/long-press/pinch), virtual keyboard, haptic feedback, mobile performance budgets, thumb zone ergonomics, platform-specific behavior (iOS/Android). -->

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

Dragon Crashers uses `borderWidth` instead of padding for safe area insets — allows colored borders matching device bezels, `[ExecuteInEditMode]` for editor preview, and a configurable multiplier.

> **Full implementation**: See [SafeAreaBorder](../ui-toolkit-responsive/SKILL.md#safeareaborder--borderwidth-approach) in responsive skill — includes complete code, padding vs borderWidth comparison table, and `[ExecuteInEditMode]` details.

## World-to-UI Alignment (PositionToVisualElement)

Aligns 3D GameObjects to VisualElement positions — critical for mobile games overlaying 3D characters on UI panels. Pipeline: `worldBound` → `GetScreenCoordinate` → `ScreenPosToWorldPos`. Responds to `ThemeEvents.CameraUpdated` for orientation camera swaps and `GeometryChangedEvent` for layout changes.

> **Full implementation**: See [PositionToVisualElement](../ui-toolkit-responsive/SKILL.md#world-to-ui-alignment-positiontovisualelement) in responsive skill — includes complete code, coordinate conversion pipeline, and `GeometryChangedEvent` wiring.

## Orientation: MediaQuery + Event System

Dragon Crashers uses an event-driven orientation system via `MediaQuery` (`[ExecuteInEditMode]`) rather than polling `Screen.orientation`. It listens to `GeometryChangedEvent`, fires `MediaQueryEvents.AspectRatioUpdated` / `ResolutionUpdated`, which triggers `ThemeManager` theme switching → `ThemeEvents.CameraUpdated` → `PositionToVisualElement` repositioning.

Key events: `MediaQueryEvents.ResolutionUpdated`, `AspectRatioUpdated`, `SafeAreaApplied` | `ThemeEvents.ThemeChanged`, `CameraUpdated`.

> **Full implementation**: See [MediaQuery](../ui-toolkit-responsive/SKILL.md#mediaquery--event-driven-orientation) in responsive skill — includes complete code, event delegates, and aspect ratio threshold (`k_LandscapeMin = 1.2f`).

## Mobile Frame Rate Control (FpsCounter)

Dragon Crashers sets `Application.targetFrameRate = 60` explicitly in `Awake()` (don't rely on default `-1` = uncapped, wastes battery). Uses a 50-frame ring buffer for smoothed FPS display, toggleable via `SettingsEvents.FpsCounterToggled`. Visibility controlled via `Visibility.Hidden` (preserves layout).

**Mobile frame rate tips:** Set `targetFrameRate` explicitly. Use ring buffer averaging for stable display. Toggle via `Visibility.Hidden`. Wire to settings events for user-controlled 30/60 FPS switching.

> **Full implementation**: See [FpsCounter](../ui-toolkit-performance/SKILL.md#fpscounter--frame-rate-control) in performance skill — includes complete code, ring buffer implementation, and settings event integration.

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

Throttle to `Application.targetFrameRate = 30` on battery. Skip UI refreshes if data unchanged. Use pure black (`rgb(0,0,0)`) for OLED savings. Set `visible = false` for off-screen panels. See also: FpsCounter.cs wired via `SettingsEvents` for user-controlled 30/60 switching.

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

- [ ] All touch targets ≥ 44×44px; no hover-dependent interactions
- [ ] Safe area applied (borderWidth or padding); `[ExecuteInEditMode]` for editor preview
- [ ] Orientation changes handled — MediaQuery fires AspectRatioUpdated, layout shifts applied
- [ ] PositionToVisualElement aligns 3D content; CameraUpdated event wired
- [ ] Bottom navigation in thumb zone for primary actions
- [ ] Virtual keyboard doesn't obscure focused input fields
- [ ] USS transitions use transform properties only; `UsageHints.DynamicTransform` on animated elements
- [ ] `Application.targetFrameRate` set explicitly (60 active, 30 battery-save)
- [ ] Visible element count < 200; sprite atlases for UI icons
- [ ] Haptic feedback on key interactions; dark/OLED theme available
- [ ] Platform-specific USS classes applied at startup
- [ ] FPS counter toggleable; tested on actual devices

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Touch targets < 44px | `min-width`/`min-height: 44px` |
| Hover-dependent UI | `:active` or tap-to-reveal instead |
| Excessive animations | Transform-only; essential feedback only |
| Ignoring safe area | `SafeAreaApplier` on root |
| Deep USS selectors (>3 levels) | Direct class matches |
| Layout property animation | `translate`, `scale`, `rotate`, `opacity` only |
| Always-on 60fps | Throttle to 30fps when idle |
| Pixel-based sizing | Use `%`, flex, USS custom properties |

## Exercise: Mobile Settings Screen

Build a touch-friendly settings screen: (1) `Settings.uxml` — vertical layout with toggle rows, slider, bottom "Save" in thumb zone. (2) `Settings.uss` — touch targets ≥ 48px, `SafeArea` padding via CSS custom properties, portrait/landscape variants. (3) `SettingsScreen.cs` — apply `SafeAreaBorder`, attach `MediaQuery`, wire `GestureDetector` for swipe-back. (4) Test orientation switching, safe area insets, 44px minimum targets.

## Cross-References

- [ui-toolkit-responsive](../ui-toolkit-responsive/SKILL.md) — SafeAreaHandler, breakpoints, responsive layouts
- [ui-toolkit-theming](../ui-toolkit-theming/SKILL.md) — portrait/landscape theme switching, ThemeManager
- [ui-toolkit-performance](../ui-toolkit-performance/SKILL.md) — mobile budgets, draw call optimization

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
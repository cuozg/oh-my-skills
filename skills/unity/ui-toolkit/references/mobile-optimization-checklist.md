# Mobile Optimization Checklist — UI Toolkit

Actionable checklist for shipping UI Toolkit on iOS/Android. Items marked with **[DC]** are patterns observed in the Dragon Crashers project.

---

## Safe Area & Notch Handling

- [ ] **[DC]** Apply safe area insets using `borderWidth` (not `padding`) on root element — preserves child layout calculations
  ```csharp
  m_Root.style.borderLeftWidth = leftInset;
  m_Root.style.borderTopWidth = topInset;
  m_Root.style.borderBottomColor = Color.clear; // Invisible
  ```
  Source: `Assets/Scripts/Utilities/SafeAreaBorder.cs`

- [ ] Subscribe to `GeometryChangedEvent` on root to reapply safe area on orientation change
- [ ] Test with notch on LEFT, RIGHT, TOP, and BOTTOM (landscape both directions + portrait)
- [ ] Verify safe area updates when returning from background (iOS)
- [ ] Use Unity Device Simulator to test before deploying to device

---

## Orientation & Responsive Layout

- [ ] **[DC]** Detect orientation with aspect ratio threshold (not `Screen.orientation`)
  ```csharp
  // MediaQuery.cs — threshold at 1.2f
  public static MediaAspectRatio GetMediaAspectRatio()
  {
      float aspect = (float)Screen.width / Screen.height;
      return aspect >= 1.2f ? MediaAspectRatio.Landscape : MediaAspectRatio.Portrait;
  }
  ```
  Source: `Assets/Scripts/Utilities/MediaQuery.cs`

- [ ] **[DC]** Fire orientation change event for all listeners: `MediaQueryEvents.AspectRatioChanged?.Invoke(ratio)`
- [ ] **[DC]** Swap both `PanelSettings` AND `ThemeStyleSheet` on orientation change (not just USS)
- [ ] Provide separate USS files per orientation for complex screens (Dragon Crashers uses 20 per-screen USS files: 10 Landscape + 10 Portrait)
- [ ] Test with actual rotation on device — simulator doesn't always match

---

## Touch & Input

- [ ] Minimum touch target size: **44x44 dp** (Apple HIG) / **48x48 dp** (Material Design)
- [ ] Add touch feedback via USS transitions (`:active` pseudo-class)
  ```css
  .button:active {
      scale: 0.95;
      transition-duration: 100ms;
  }
  ```
- [ ] **[DC]** Use `StopImmediatePropagation()` on interactive children inside `ScrollView` to prevent drag conflicts
  ```csharp
  child.RegisterCallback<PointerDownEvent>(evt => {
      evt.StopImmediatePropagation();
  }, TrickleDown.TrickleDown);
  ```
  Source: `Assets/Scripts/UI/Components/ShopItemComponent.cs`

- [ ] Add swipe gesture margins (don't place interactive elements at screen edges)
- [ ] Test with both finger and stylus input

---

## Performance (Mobile-Specific)

- [ ] **[DC]** Cache ALL `Q<>()` results — never call in `Update()` or per-frame loops
- [ ] **[DC]** Use `Task.Delay()` for animation timing instead of coroutines in non-MonoBehaviour views
- [ ] Limit font count to 2-3 (each font = +1 draw call)
- [ ] Use `SpriteAtlas` for all UI sprites (each separate texture = +1 draw call)
- [ ] Set `usageHints = UsageHints.DynamicTransform` on animated elements
- [ ] Animate only transform properties (`translate`, `rotate`, `scale`, `opacity`) — never `width`/`height`/`margin`/`padding`
- [ ] Use `ListView` with virtualization for lists > 20 items
- [ ] **[DC]** For lists < 20 items, `VisualTreeAsset.Instantiate()` is acceptable
- [ ] Set `Application.targetFrameRate` (Dragon Crashers uses 60fps target)
- [ ] Profile with Unity Profiler on actual target device — editor performance differs significantly

### Memory

- [ ] Avoid string concatenation in per-frame updates — pre-cache or use `StringBuilder`
- [ ] Watch for lambda allocations in `RegisterCallback` — prefer method references
- [ ] **[DC]** Use fire-and-forget `_ = AsyncMethod()` sparingly — each creates a Task allocation
- [ ] Dispose views properly — unsubscribe ALL event delegates in `Dispose()`/`OnDisable()`

---

## World-to-UI Alignment (Mobile Considerations)

- [ ] **[DC]** Use `RuntimePanelUtils.CameraTransformWorldToPanelRect()` for UI tracking 3D objects
  Source: `Assets/Scripts/Utilities/PositionToVisualElement.cs`

- [ ] Run position updates in `LateUpdate()` (after camera movement)
- [ ] **[DC]** Listen for `ThemeEvents.CameraUpdated` to recalculate on orientation change
- [ ] Cache `Camera.main` reference (accessor is expensive on mobile)
- [ ] Consider disabling position tracking when UI element is off-screen

---

## Theming (Mobile-Specific)

- [ ] **[DC]** Use compound theme names: `"{Orientation}--{Season}"` — allows per-orientation styling with semantic themes
- [ ] **[DC]** Provide separate `PanelSettings` per orientation (different reference resolutions)
- [ ] Test theme switching doesn't cause frame spike — swap TSS + PanelSettings in one frame
- [ ] Ensure decoration USS files properly hide/show season-specific elements:
  ```css
  /* Decoration-Halloween.uss */
  .theme__decoration--default { display: none; }
  .theme__decoration--halloween { display: flex; }
  .theme__decoration--christmas { display: none; }
  ```

---

## Event & State Management

- [ ] **[DC]** Unsubscribe from ALL static Action delegates in `Dispose()` or `OnDisable()`
  ```csharp
  // MUST match every += with a -=
  void OnEnable() { CharEvents.GoldUpdated += OnGoldUpdated; }
  void OnDisable() { CharEvents.GoldUpdated -= OnGoldUpdated; }
  ```

- [ ] **[DC]** Views subscribe in constructor, unsubscribe in `Dispose()`
- [ ] **[DC]** Controllers subscribe in `OnEnable()`, unsubscribe in `OnDisable()`
- [ ] Never subscribe to events in `Awake()` without corresponding unsubscribe
- [ ] For async animations: consider `CancellationToken` to cancel on view disposal

---

## Build & Deployment

- [ ] Test with IL2CPP (not Mono) — reflection patterns may behave differently
- [ ] Enable stripping level: "High" and test UI still works (some reflection-heavy patterns break)
- [ ] Verify `PanelSettings` reference resolution matches target device class:
  - Phone portrait: 1080x1920 or 1080x2400
  - Phone landscape: 1920x1080 or 2400x1080
  - Tablet: 2048x1536 or 2560x1600
- [ ] Test on minimum-spec target device (not just flagships)
- [ ] Profile startup time — UI initialization should be < 100ms on mid-range devices

---

## Pre-Launch Verification

- [ ] Run full app lifecycle: launch → background → foreground → rotate → background → kill → relaunch
- [ ] Verify no leaked event subscriptions after screen transitions (check profiler for growing delegate lists)
- [ ] Test with system font scaling enabled (Accessibility settings)
- [ ] Test with Dark Mode / Light Mode system settings (if app respects system theme)
- [ ] Verify all interactive elements are reachable in both orientations

---

## Related Skills

- **[ui-toolkit-mobile](../ui-toolkit-mobile/SKILL.md)** — Full mobile skill with code examples
- **[ui-toolkit-responsive](../ui-toolkit-responsive/SKILL.md)** — MediaQuery, SafeArea, orientation
- **[ui-toolkit-performance](../ui-toolkit-performance/SKILL.md)** — Profiling, caching, virtualization
- **[project-patterns.md](project-patterns.md)** — All 16 architecture patterns

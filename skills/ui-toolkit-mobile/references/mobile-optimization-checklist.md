# Mobile Optimization Checklist — UI Toolkit

Actionable checklist for shipping UI Toolkit on iOS/Android. **[DC]** = Dragon Crashers pattern.

---

## Safe Area & Notch

- [ ] **[DC]** Safe area via `borderWidth` (not `padding`) on root — preserves child layout. Source: `SafeAreaBorder.cs`
- [ ] `GeometryChangedEvent` on root to reapply on orientation change
- [ ] Test notch LEFT/RIGHT/TOP/BOTTOM; verify after background→foreground (iOS)

## Orientation & Responsive

- [ ] **[DC]** Detect orientation via aspect ratio threshold (`width/height >= 1.2f`), not `Screen.orientation`. Source: `MediaQuery.cs`
- [ ] **[DC]** Fire `MediaQueryEvents.AspectRatioChanged` for listeners
- [ ] **[DC]** Swap both `PanelSettings` AND `ThemeStyleSheet` on orientation change
- [ ] Separate USS per orientation for complex screens (DC: 10 Landscape + 10 Portrait)

## Touch & Input

- [ ] Touch targets ≥ **44×44dp** (Apple) / **48×48dp** (Material)
- [ ] `:active` USS transitions for touch feedback (`scale: 0.95; transition-duration: 100ms`)
- [ ] **[DC]** `StopImmediatePropagation()` on interactive children inside ScrollView. Source: `ShopItemComponent.cs`
- [ ] Swipe gesture margins — no interactive elements at screen edges

## Performance

- [ ] **[DC]** Cache ALL `Q<>()` — never in `Update()` or per-frame loops
- [ ] Limit fonts to 2-3; `SpriteAtlas` for all UI sprites
- [ ] `UsageHints.DynamicTransform` on animated elements
- [ ] Animate only `translate/rotate/scale/opacity` — never layout properties
- [ ] `ListView` with virtualization for 20+ item lists
- [ ] `Application.targetFrameRate` set explicitly (DC: 60fps)
- [ ] Profile on actual target device

### Memory

- [ ] No string concat in per-frame updates — pre-cache or `StringBuilder`
- [ ] Method references over lambdas in `RegisterCallback`
- [ ] Dispose views properly — unsubscribe ALL delegates in `Dispose()`/`OnDisable()`

## World-to-UI Alignment

- [ ] **[DC]** `RuntimePanelUtils.CameraTransformWorldToPanelRect()`. Source: `PositionToVisualElement.cs`
- [ ] Position updates in `LateUpdate()`; cache `Camera.main`
- [ ] **[DC]** Listen for `ThemeEvents.CameraUpdated` on orientation change

## Theming (Mobile)

- [ ] **[DC]** Compound theme names: `"{Orientation}--{Season}"`
- [ ] **[DC]** Separate `PanelSettings` per orientation (different reference resolutions)
- [ ] Theme switching in one frame — no spike

## Event & State Management

- [ ] **[DC]** Every `+=` has matching `-=` (OnEnable/OnDisable for controllers, constructor/Dispose for views)
- [ ] Never subscribe in `Awake()` without unsubscribe
- [ ] `CancellationToken` for async animations on view disposal

## Build & Deployment

- [ ] Test with IL2CPP (not Mono); stripping level "High" verified
- [ ] `PanelSettings` reference resolution matches device class (phone: 1080×1920/2400, tablet: 2048×1536/2560×1600)
- [ ] Startup UI initialization < 100ms on mid-range

## Pre-Launch

- [ ] Full lifecycle: launch → background → foreground → rotate → kill → relaunch
- [ ] No leaked event subscriptions after screen transitions
- [ ] System font scaling, Dark/Light Mode, both orientations tested



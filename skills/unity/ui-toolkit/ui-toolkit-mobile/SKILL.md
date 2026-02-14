---
name: ui-toolkit-mobile
description: "Mobile optimization and touch input for Unity UI Toolkit. Covers touch handling, gesture detection, safe areas, orientation changes, mobile performance budgets, virtual keyboard management, and battery-conscious UI patterns. Use when: (1) Building touch-friendly UI with proper hit targets, (2) Handling safe areas and notches, (3) Detecting orientation changes, (4) Optimizing UI performance for mobile, (5) Managing virtual keyboard interactions, (6) Implementing swipe/long-press gestures. Triggers: 'mobile UI', 'touch input', 'safe area', 'orientation', 'mobile performance', 'virtual keyboard', 'swipe gesture', 'thumb zone'."
---

# UI Toolkit Mobile

<!-- OWNERSHIP: Touch handling, gesture detection (swipe/long-press/pinch), virtual keyboard, haptic feedback, mobile performance budgets, thumb zone ergonomics, platform-specific behavior (iOS/Android). -->

> **Based on**: Unity 6 (6000.0), [Dragon Crashers](../references/dragon-crashers-insights.md) official sample

Mobile-first UI design for Unity UI Toolkit — touch input, safe areas, orientation, performance, and platform-specific behavior. Dragon Crashers uses `SafeAreaHandler` on root, bottom tab navigation, and transform-only animations for mobile-grade performance.

## Mobile Code Patterns

> **Full mobile patterns and code**: See [Mobile Code Patterns](references/mobile-code-patterns.md) — covers Touch Input Handling (44×44dp targets), GestureDetector Manipulator (swipe/long-press/tap), Bottom Navigation (UXML+USS), SafeArea Integration, World-to-UI Alignment, Orientation MediaQuery + Event System, Mobile Frame Rate Control, OrientationHandler (C#+USS), Mobile Performance (budget table + optimization rules), Touch Feedback (USS transitions), Haptic Feedback (iOS/Android), Virtual Keyboard handler.

---

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
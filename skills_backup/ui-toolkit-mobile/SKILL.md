---
name: ui-toolkit-mobile
description: "Mobile optimization and touch input for Unity UI Toolkit. Covers touch handling, gesture detection, safe areas, orientation changes, mobile performance budgets, virtual keyboard management, and battery-conscious UI patterns. Use when: (1) Building touch-friendly UI with proper hit targets, (2) Handling safe areas and notches, (3) Detecting orientation changes, (4) Optimizing UI performance for mobile, (5) Managing virtual keyboard interactions, (6) Implementing swipe/long-press gestures. Triggers: 'mobile UI', 'touch input', 'safe area', 'orientation', 'mobile performance', 'virtual keyboard', 'swipe gesture', 'thumb zone'."
---

# UI Toolkit Mobile

Mobile-first UI: touch input, safe areas, orientation, performance, platform behavior. DC uses SafeAreaHandler on root, bottom tab nav, transform-only animations.

## Output
Production-ready C# and USS code optimized for mobile touch, safe areas, and performance budgets.

## Mobile Code Patterns

> **Full patterns**: See [Mobile Code Patterns](references/mobile-code-patterns.md) — Touch Input (44×44dp), GestureDetector, Bottom Nav, SafeArea, World-to-UI, Orientation MediaQuery, Frame Rate Control, OrientationHandler, Performance budgets, Touch Feedback, Haptic, Virtual Keyboard.

## Battery & Platform

Throttle `targetFrameRate = 30` on battery. Pure black for OLED. `visible = false` for off-screen panels.

```csharp
public static class MobilePlatform
{
    public static bool IsMobile => Application.platform is RuntimePlatform.Android or RuntimePlatform.IPhonePlayer;
    public static bool IsTablet => IsMobile && Mathf.Min(Screen.width, Screen.height) >= 600;
    public static void ApplyPlatformClasses(VisualElement root)
    {
        root.EnableInClassList("platform--mobile", IsMobile);
        root.EnableInClassList("platform--tablet", IsTablet);
    }
}
```

```css
.platform--mobile .tooltip, .platform--mobile .hover-preview { display: none; }
.platform--mobile .btn { min-height: 48px; font-size: 16px; }
```

## Mobile Checklist

- [ ] Touch targets ≥ 44×44px; no hover-dependent interactions
- [ ] Safe area applied; orientation handled via MediaQuery
- [ ] Bottom navigation in thumb zone; virtual keyboard doesn't obscure inputs
- [ ] Transform-only animations; `DynamicTransform` hints; targetFrameRate set
- [ ] Visible elements < 200; sprite atlases; platform USS classes applied

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Touch targets < 44px | `min-width/height: 44px` |
| Hover-dependent UI | `:active` or tap-to-reveal |
| Layout property animation | `translate/scale/rotate/opacity` only |
| Always-on 60fps | Throttle to 30 when idle |



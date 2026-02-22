# Project Architecture Patterns — Advanced (Patterns #9–16)

> For patterns #1–8, see [project-patterns.md](project-patterns.md).

## 9. World-to-Panel Coordinate Conversion

```csharp
void LateUpdate() // Must be LateUpdate, after camera
{
    Rect rect = RuntimePanelUtils.CameraTransformWorldToPanelRect(m_Panel, m_WorldTransform.position, m_WorldSize, m_Camera);
    m_TargetElement.style.left = rect.x; m_TargetElement.style.top = rect.y;
}
```

## 10. CSS Class Toggling for State

```csharp
m_Tab.AddToClassList("tab--active");          // Add state
m_Element.EnableInClassList("selected", true); // Toggle state
```

Keeps styling in USS, logic in C#.

## 11. experimental.animation API

```csharp
m_Element.experimental.animation.Start(new Vector2(0, 100), Vector2.zero, 300)
    .Ease(Easing.OutQuad)
    .OnValueChanged(v => m_Element.style.translate = new Translate(v.x, v.y));
```

## 12. GeometryChangedEvent (Deferred Init)

Register one-shot callback to read layout values after first layout pass. Unregister immediately in handler.

## 13. Button.userData for Data Storage

Store `ScriptableObject` on buttons via `userData`. Retrieve in click handler: `(evt.currentTarget as Button).userData as ShopItemSO`. Avoids closures.

## 14. StopImmediatePropagation

Prevent `ScrollView` from capturing child drag/click events. Register on `TrickleDown` phase.

## 15. SafeAreaBorder (borderWidth Approach)

Uses `borderWidth` (not padding) for safe area insets — doesn't affect child layout calculations. Set `borderColor = Color.clear`.

## 16. PositionToVisualElement (3D-to-UI)

Inverse of #9. Reads UI element position via `resolvedStyle`, converts to screen coords, then `Camera.ScreenToWorldPoint`. For particle effects/3D decorations aligned to UI.

## Pattern Selection Guide

| Need | Pattern # |
|------|-----------|
| Cross-module communication | 1 |
| Screen lifecycle | 2 |
| Overlapping UI layers | 3 |
| Orientation + theme | 4 |
| Reusable UXML components | 5 |
| Animation in non-MonoBehaviour | 6 |
| Complex screen with regions | 7 |
| Small dynamic lists | 8 |
| UI tracking 3D objects | 9 |
| Visual state transitions | 10 |
| Programmatic tweens | 11 |
| Layout-dependent init | 12 |
| Data on UI elements | 13 |
| ScrollView child interaction | 14 |
| Mobile safe area | 15 |
| 3D tracking UI | 16 |

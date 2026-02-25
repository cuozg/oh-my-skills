# Mobile Code Patterns

## Touch Input — Minimum 44×44dp

```css
.touch-target { min-width: 44px; min-height: 44px; padding: 8px; }
```

## Gesture Detection (Manipulator)

```csharp
public class GestureDetector : Manipulator
{
    const float SwipeThreshold = 50f;
    const float LongPressDuration = 0.5f;
    Vector2 _startPos; float _startTime; bool _isActive;
    IVisualElementScheduledItem _longPressTimer;
    public event System.Action<Vector2> OnSwipe;
    public event System.Action OnLongPress;
    public event System.Action OnTap;
    // RegisterCallbacksOnTarget: PointerDown/Move/Up
    // OnPointerMove: if drag > threshold*0.5 → pause long-press timer
    void OnPointerDown(PointerDownEvent evt) {
        _startPos = evt.position; _startTime = Time.unscaledTime; _isActive = true;
        target.CapturePointer(evt.pointerId);
        _longPressTimer = target.schedule.Execute(() => {
            if (_isActive) { OnLongPress?.Invoke(); _isActive = false; }
        }).StartingIn((long)(LongPressDuration * 1000));
    }
    void OnPointerUp(PointerUpEvent evt) {
        if (!_isActive) return;
        _isActive = false; _longPressTimer?.Pause(); target.ReleasePointer(evt.pointerId);
        Vector2 delta = (Vector2)evt.position - _startPos;
        if (delta.magnitude >= SwipeThreshold) OnSwipe?.Invoke(delta.normalized);
        else if (Time.unscaledTime - _startTime < LongPressDuration) OnTap?.Invoke();
    }
}
```

Usage: `var g = new GestureDetector(); g.OnSwipe += dir => ...; element.AddManipulator(g);`

## Bottom Navigation Layout

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
.bottom-nav { flex-direction: row; justify-content: space-around; height: 56px; padding-bottom: var(--safe-area-bottom, 0px); background-color: rgb(30,30,30); }
.nav-tab { flex-grow: 1; height: 100%; background-color: rgba(0,0,0,0); border-width: 0; color: rgb(160,160,160); font-size: 12px; }
.nav-tab--active { color: rgb(100, 180, 255); }
```

## SafeArea Integration

```csharp
public static class SafeAreaApplier {
    public static void Apply(VisualElement root) {
        var sa = Screen.safeArea;
        root.style.paddingTop = new Length((Screen.height - sa.yMax) / Screen.height * 100f, LengthUnit.Percent);
        root.style.paddingBottom = new Length(sa.y / Screen.height * 100f, LengthUnit.Percent);
        root.style.paddingLeft = new Length(sa.x / Screen.width * 100f, LengthUnit.Percent);
        root.style.paddingRight = new Length((Screen.width - sa.xMax) / Screen.width * 100f, LengthUnit.Percent);
    }
}
```

DC uses `borderWidth` instead of padding — see [SafeAreaBorder](../../ui-toolkit-responsive/SKILL.md#safeareaborder-borderwidth-approach).

See [mobile-code-patterns-advanced.md](mobile-code-patterns-advanced.md) for orientation handling, performance budgets, and touch feedback patterns.

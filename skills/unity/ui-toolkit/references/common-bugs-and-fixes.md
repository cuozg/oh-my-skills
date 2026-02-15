# Common Bugs & Fixes — UI Toolkit

**[DC]** = Dragon Crashers, **[QU]** = QuizU.

## 1. Q() Returns Null

| Cause | Fix |
|-------|-----|
| Name mismatch (case-sensitive) | Check UXML names exactly |
| Query before UXML loaded | Query in `OnEnable()` after `rootVisualElement` available |
| **[DC]** Query before `CloneTree()` | Call `CloneTree(root)` first, then `Q()` |

## 2. CSS Transitions Not Working

| Cause | Fix |
|-------|-----|
| Missing `transition-property` | Add `transition-property: translate, opacity;` |
| Transitioning layout props | Use `translate`/`scale`/`opacity` only |
| **[DC]** Class added too fast after `display: flex` | `await Task.Delay(10)` between show and class add |
| Element not in tree | Wait for `GeometryChangedEvent` |

## 3. Event Subscription Leaks

| Cause | Fix |
|-------|-----|
| **[DC]** Missing `-=` for static delegates | Match every `+=` with `-=` in `Dispose()`/`OnDisable()` |
| Lambda subscriptions | Use method references instead |
| **[DC]** View `Dispose()` never called | Controller MUST call `view.Dispose()` in `OnDisable()` |
| **[QU]** Want auto-cleanup? | Use `EventRegistry` — see [code-templates.md #9](code-templates.md#eventregistry-disposable-event-cleanup) |

## 4. ScrollView Swallows Child Events

```csharp
// [DC] StopImmediatePropagation on TrickleDown phase
m_Child.RegisterCallback<PointerDownEvent>(evt => {
    evt.StopImmediatePropagation();
}, TrickleDown.TrickleDown);
```

## 5. Safe Area Not Updating on Rotation

Use `GeometryChangedEvent` for reapplication. **[DC]** Use `borderWidth` not `padding`. Check `Screen.safeArea` changes via `MediaQueryEvents`.

## 6. Theme Switch Flash/Flicker

**[DC]** Swap BOTH `panelSettings` AND `themeStyleSheet` in same frame — see [project-patterns.md #4](project-patterns.md#4-compound-theming-orientationseason).

## 7. Layout Values Read as Zero

`resolvedStyle.width/height` = 0 until first layout pass. Use one-shot `GeometryChangedEvent`, unregister in handler.

## 8. World-to-Panel Jitters

**[DC]** Use `LateUpdate()` not `Update()`. Cache camera reference. Listen for `ThemeEvents.CameraUpdated` on orientation change.

## 9. Async Exception Silently Swallowed

`_ = AsyncMethod()` discards exceptions. Add `try/catch` inside async method, or use `.ContinueWith(t => { if (t.IsFaulted) Debug.LogException(t.Exception); })`.

## 10. Instantiate() Children Not Styled

Add `<Style src="...">` in template UXML. Apply USS classes directly to instantiated root. Ensure parent TSS includes component USS.

## 11. Button.userData Lost After Rebuild

`container.Clear()` destroys old elements. Re-assign `userData` after every `Instantiate()`.

## 12. UxmlFactory Not in UI Builder

Need `public new class UxmlFactory : UxmlFactory<MyControl, UxmlTraits> { }`. Class must compile and be in runtime assembly (not editor-only).

## Quick Diagnostic

**Not visible?** Check: `display`, `opacity`, `visibility`, parent display, element in tree.
**Not interactive?** Check: `pickingMode`, parent event capture, z-order, ScrollView TrickleDown.
**Event fires multiple times?** Check: duplicate subscriptions (use OnEnable/OnDisable), lambda unsub, bubbling, `Dispose()` called.

---
name: ui-toolkit-debugging
description: "Debugging and troubleshooting Unity UI Toolkit. Covers UI Toolkit Debugger, Event Debugger, Frame Debugger, Profiler UI Details module, Memory Profiler, common pitfalls, and diagnostic utilities. Use when: (1) Element not visible or styled incorrectly, (2) Events not firing or propagating wrong, (3) Investigating UI draw calls or layout cost, (4) Tracking UI memory leaks, (5) Diagnosing binding failures, (6) Troubleshooting safe area or theming issues. Triggers: 'debug UI', 'element not showing', 'event not firing', 'USS not applying', 'UI Toolkit Debugger', 'layout thrashing', 'UI memory leak', 'binding not working'."
---

# UI Toolkit Debugging

## Output
Diagnostic steps, root cause identification, and fix recommendations for UI Toolkit issues.

## UI Toolkit Debugger

**Window > UI Toolkit > Debugger** → select panel (`PanelSettings`=runtime, `UI Builder`=editor).

**Pick Mode**: Click crosshair icon → hover Game view → click element → right pane shows Matching USS Selectors, Computed Styles, Layout, Inline Styles.

**Live USS editing**: Double-click values in Styles pane → changes apply instantly (don't persist) → copy to USS file.

### Visibility Checklist

| Check | Look At |
|-------|---------|
| In tree? | Visual tree pane |
| `display:none`? | Computed Styles > Display |
| `visibility:hidden`? | Computed Styles > Visibility |
| `opacity:0`? | Computed Styles > Opacity |
| Size = 0? | Layout section |
| Selectors match? | Matching USS Selectors |

## Event Debugger

**Window > UI Toolkit > Event Debugger** → select panel → check event types to monitor.

Propagation: TrickleDown (Root→Target, opt-in) → Target → BubbleUp (Target→Root, default).

Each log entry shows: event type, target, propagation path, handler, StopPropagation source.

**Key issue**: Parent with `StopPropagation()` blocks child button clicks — Event Debugger shows path stopping at parent.

## Frame Debugger

**Window > Analysis > Frame Debugger** → Enable → expand `UIR.DrawChain` entries.

Draw call targets: HUD 3-5, Menu 8-15, Complex inventory 15-25.

**Batch breaks**: Different texture → SpriteAtlas | Different font → limit fonts | `overflow:hidden` nesting → minimize clips | Container opacity <1 → apply to leaves.

## Profiler — UI Details

**Window > Analysis > Profiler** → add UI Details module.

| Marker | Budget | Fix |
|--------|--------|-----|
| `UIR.Layout` | <0.5ms | Flatten hierarchy |
| `UIR.RenderChainUpdate` | <0.3ms | Fewer style changes/frame |
| `UIR.TextRegen` | <0.2ms | Batch text updates |
| `UIR.DrawChain` | <0.2ms | SpriteAtlas, fewer fonts |

### Layout Thrashing

```csharp
// BAD — read triggers layout recalc each iteration
for (int i = 0; i < items.Count; i++) {
    items[i].style.top = offset;
    offset += items[i].resolvedStyle.height; // triggers layout!
}
// FIX — use flex layout, let Yoga handle positioning
container.style.flexDirection = FlexDirection.Column;
```

## Memory Profiler

Snapshot screen A → navigate away → `GC.Collect()` → Snapshot B → Compare → filter `VisualElement` — any in both = leaked.

**Leak sources**: Callbacks not unregistered → `UnregisterCallback` | Static element refs → avoid | Lambda captures `this` → use method refs | Binding not unbound → `Unbind()` | Elements in collections → clear on exit.

## Common Pitfalls

| Problem | Fix |
|---------|-----|
| Element invisible | Check `display`, `visibility`, `opacity`, size in Debugger |
| USS not applying | Check selector specificity, verify stylesheet added to panel |
| Events not firing | Check `pickingMode:Position`, StopPropagation upstream |
| Wrong event type | Use `ClickEvent` not `MouseDownEvent` for buttons |
| Binding empty | Add `[CreateProperty]`, verify `dataSourcePath` case-sensitive |
| Safe area missing | Apply `Screen.safeArea` padding on `GeometryChangedEvent` |
| Theme not switching | Verify `ThemeStyleSheet` on PanelSettings |
| Picking broken | Set `pickingMode: Position` on target |

## Diagnostic Utilities

See [references/diagnostic-utilities.md](references/diagnostic-utilities.md) for UIDebugUtils class, debug USS styles, and C# activation code.

## DC Debugging Scenarios

See [dragon-crashers-insights.md](references/dragon-crashers-insights.md): event bus `+=`/`-=` pairing, fire-and-forget `Task` exception swallowing, world-to-panel positioning, compound theme debugging, SafeAreaBorder Editor-vs-device differences.


---
name: ui-toolkit-patterns
description: "Common UI patterns implemented in Unity UI Toolkit with complete UXML/USS/C# examples. Covers tabbed navigation, inventory grids, modal dialogs, stateful buttons, message lists, and scroll snapping. Use when: (1) Building tabbed interfaces, (2) Creating inventory or card grid layouts, (3) Implementing modal popups with backdrop, (4) Adding button states and loading spinners, (5) Building chat or mail list views, (6) Implementing horizontal scroll with page snap. Triggers: 'tab bar', 'inventory grid', 'modal popup', 'dialog overlay', 'button states', 'message list', 'scroll snap', 'UI pattern'."
---

# UI Toolkit Common Patterns

Follows ui-toolkit-architecture: UXML=structure, USS=style, C#=behavior.

## UI Pattern Implementations

> **Full code**: See [Pattern Examples](references/pattern-examples.md) — Tabs, Inventory Grid, Modal/Popup, Stateful Buttons, Message List, Scroll Snap, Async Animation, Experimental API, GeometryChangedEvent, World-to-Panel Positioning.

## Animation Decision Matrix

| Technique | Easing | Cancel | Best For |
|---|---|---|---|
| USS `transition` | ✅ ease-* | Remove class | State changes (hover, show/hide) |
| USS class toggle | ✅ via transition | `RemoveFromClassList` | Binary states, theme-aware |
| `experimental.animation` | ❌ linear | `.Stop()` | Position/scale slides |
| `async Task` | Manual Lerp | `CancellationToken` | Non-MonoBehaviour multi-step |

Only animate **transform properties**. Set `usageHints = DynamicTransform`. See ui-toolkit-performance.

```css
.panel { translate: 0 30px; opacity: 0; transition: translate 0.25s ease-out, opacity 0.2s; }
.panel--visible { translate: 0 0; opacity: 1; }
```

## Quick Reference

| Pattern | Key API | DC Example |
|---------|---------|------------|
| Tabs | `tab-bar__tab--active` | `TabbedMenuController` |
| Inventory | ListView `makeItem`/`bindItem` | `InventoryView` |
| Modal | `--visible` class toggle | `UIManager.ShowModalView()` |
| Messages | `msg-row--unread`, ListView | `MailView` composite |
| Async Anims | `_ = MethodAsync()` | `ChatView`, `LevelMeterView` |
| Composite View | Parent injects containers | `MailView` → 3 children |



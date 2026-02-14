---
name: ui-toolkit-patterns
description: "Common UI patterns implemented in Unity UI Toolkit with complete UXML/USS/C# examples. Covers tabbed navigation, inventory grids, modal dialogs, stateful buttons, message lists, and scroll snapping. Use when: (1) Building tabbed interfaces, (2) Creating inventory or card grid layouts, (3) Implementing modal popups with backdrop, (4) Adding button states and loading spinners, (5) Building chat or mail list views, (6) Implementing horizontal scroll with page snap. Triggers: 'tab bar', 'inventory grid', 'modal popup', 'dialog overlay', 'button states', 'message list', 'scroll snap', 'UI pattern'."
---

# UI Toolkit Common Patterns

<!-- OWNERSHIP: Screen implementations (tabs, inventory, modals, mail, scroll snap), async Task animation, composite view pattern, ListView usage, CSS class toggling for state, Button.userData. -->

> **Based on**: Unity 6 (6000.0), [Dragon Crashers](../references/dragon-crashers-insights.md) official sample. Production-ready patterns with complete UXML, USS, and C#. Follows [architecture](../ui-toolkit-architecture/SKILL.md) principles: UXML=structure, USS=style, C#=behavior.

---

## UI Pattern Implementations

> **Full code patterns and examples**: See [Pattern Examples](references/pattern-examples.md) — covers Tabbed Navigation, Inventory Grid, Modal/Popup Dialog, Stateful Buttons, Message List (Mail/Chat), Scroll View with Snap, Async Task Animation, Experimental Animation API, GeometryChangedEvent & Composite View, World-to-Panel Positioning. Complete UXML, USS, and C# for each pattern with Dragon Crashers comparisons.

---

## Animation Decision Matrix

| Technique | Easing | Cancel | Best For |
|---|---|---|---|
| **USS `transition`** | ✅ `ease-*` | Remove class | State changes (hover, show/hide) |
| **USS class toggle** | ✅ via transition | `RemoveFromClassList` | Binary states, theme-aware |
| **`experimental.animation`** | ❌ linear | `.Stop()` | Position/scale slides |
| **`async Task`** | Manual Lerp | `CancellationToken` | Non-MonoBehaviour multi-step |
| **`IVisualElementScheduledItem`** | Manual | `.Pause()` | Repeating timers, delayed callbacks |

> Only animate **transform properties** (`translate`, `scale`, `opacity`, `rotate`). Set `usageHints = DynamicTransform` on animated elements. See [performance skill](../ui-toolkit-performance/SKILL.md).

```css
/* USS transition example */
.panel { translate: 0 30px; opacity: 0; transition: translate 0.25s ease-out, opacity 0.2s; }
.panel--visible { translate: 0 0; opacity: 1; }
```

## Quick Reference

| Pattern | Key API | DC Example |
|---------|---------|------------|
| Tabs | `tab-bar__tab--active`, indicator translate | `TabbedMenuController` |
| Inventory | ListView `makeItem`/`bindItem` | `InventoryView` ScrollView |
| Modal | `--visible` class toggle, backdrop | `UIManager.ShowModalView()` |
| Buttons | `:hover/:active/:disabled`, `.btn--loading` | CSS class toggle |
| Messages | `msg-row--unread/--swiped`, ListView | `MailView` composite |
| Carousel | `dot--active`, scrollOffset snap | — (generic) |
| Async Anims | `_ = MethodAsync()`, `Task.Delay` | `ChatView`, `LevelMeterView` |
| Experimental | `.Position()`, `.Scale()` | `MenuBarView` marker |
| Composite View | Parent injects containers to children | `MailView` → 3 children |

## Related Skills & Resources

- [Architecture](../ui-toolkit-architecture/SKILL.md) — UIView base class, event bus, view lifecycle
- [Performance](../ui-toolkit-performance/SKILL.md) — animation cost, virtualization
- [Mobile](../ui-toolkit-mobile/SKILL.md) — touch patterns, safe area
- [Code Templates](../references/code-templates.md) | [Dragon Crashers](../references/dragon-crashers-insights.md) | [QuizU Patterns](../references/quizu-patterns.md)
**← Previous**: [Data Binding](../ui-toolkit-databinding/SKILL.md) | **Next →**: [Performance](../ui-toolkit-performance/SKILL.md)

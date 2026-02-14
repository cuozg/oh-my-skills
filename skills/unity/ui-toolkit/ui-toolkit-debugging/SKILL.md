---
name: ui-toolkit-debugging
description: "Debugging and troubleshooting Unity UI Toolkit. Covers UI Toolkit Debugger, Event Debugger, Frame Debugger, Profiler UI Details module, Memory Profiler, common pitfalls, and diagnostic utilities. Use when: (1) Element not visible or styled incorrectly, (2) Events not firing or propagating wrong, (3) Investigating UI draw calls or layout cost, (4) Tracking UI memory leaks, (5) Diagnosing binding failures, (6) Troubleshooting safe area or theming issues. Triggers: 'debug UI', 'element not showing', 'event not firing', 'USS not applying', 'UI Toolkit Debugger', 'layout thrashing', 'UI memory leak', 'binding not working'."
---

# UI Toolkit Debugging

<!-- OWNERSHIP: UI Toolkit Debugger, Event Debugger, Frame Debugger, Profiler UI Details module, Memory Profiler for UI, diagnostic flowcharts, common pitfalls catalog, event debugging utilities. -->

> **Based on**: Unity 6 (6000.0), [Dragon Crashers](../references/dragon-crashers-insights.md) official sample

Systematic workflows for finding and fixing UI Toolkit issues using Unity's built-in debugging tools.

## UI Toolkit Debugger

The primary tool for inspecting live UI hierarchy, computed styles, and layout.

### Opening the Debugger

1. **Window > UI Toolkit > Debugger**
2. In the top-left dropdown, select the target panel:
   - `PanelSettings` — runtime UI
   - `UI Builder` — editor UI being designed
   - `Inspector` / `Scene` — editor panels
3. The left pane shows the live visual tree; the right pane shows style details

### Pick Mode Workflow

1. Click the **Pick** button (crosshair icon) in the Debugger toolbar
2. Hover over elements in the Game view — they highlight with a blue overlay
3. Click an element to select it in the Debugger tree
4. The right pane shows:
   - **Matching USS Selectors** — which rules apply, in priority order
   - **Computed Styles** — final resolved values after cascade
   - **Layout** — Yoga-computed position, size, padding, margin, border
   - **Inline Styles** — styles set via C# `element.style.*`

### Live USS Editing

Styles edited in the Debugger **apply immediately** but **do not persist** — use this for rapid iteration:

1. Select an element in the Debugger
2. In Styles, modify any property (double-click a value)
3. Observe the change in Game view instantly
4. Copy the working values into your USS file

### Debugger Checklist

| Check | Where to Look | Indicates |
|-------|--------------|-----------|
| Element in tree? | Visual tree pane | Element exists in hierarchy |
| `display: none`? | Computed Styles > Display | Element hidden programmatically |
| `visibility: hidden`? | Computed Styles > Visibility | Element invisible but occupies space |
| `opacity: 0`? | Computed Styles > Opacity | Element fully transparent |
| Width/Height = 0? | Layout section | Element has no size (flex misconfiguration) |
| Matching selectors? | Matching USS Selectors | USS rules actually targeting this element |

## Event Debugger

Tracks event creation, propagation, and handling across the visual tree.

### Opening the Event Debugger

1. **Window > UI Toolkit > Event Debugger**
2. Select the target panel in the dropdown
3. Check event types to monitor (e.g., `ClickEvent`, `PointerDownEvent`, `ChangeEvent`)
4. Interact with your UI — events appear in the log

### Event Propagation Phases

```
                    Root
                     │
          ┌──────────┼──────────┐
          │     TrickleDown     │   Phase 1: Top → Target
          │    (Capture phase)  │   Rarely used, opt-in via
          │          │          │   TrickleDown.TrickleDown
          │          ▼          │
          │      ┌───────┐     │
          │      │ Target │     │   Phase 2: Target element
          │      └───────┘     │   receives the event
          │          │          │
          │       BubbleUp      │   Phase 3: Target → Root
          │    (Default phase)  │   Most handlers use this
          │          │          │
          └──────────┼──────────┘
                     ▼
                    Root
```

### Diagnosing Event Issues

In the Event Debugger log, each entry shows:
- **Event type** and timestamp
- **Target element** — where the event was aimed
- **Propagation path** — every element the event visited
- **Handled by** — which callback consumed the event
- **StopPropagation** — if propagation was halted and by whom

**Common pattern**: If a parent container has `RegisterCallback<ClickEvent>` with `StopPropagation()`, child button clicks never reach their handlers. The Event Debugger shows the propagation path stopping at the parent.

## Frame Debugger

Use Frame Debugger to count draw calls and identify batch-breaking elements.

### Step-by-Step Workflow

1. **Window > Analysis > Frame Debugger**
2. Click **Enable** to freeze the current frame
3. Expand the draw call list — look for `UIR.DrawChain` entries
4. Click each draw call to highlight the rendered region in Game view
5. Count total UI draw calls for the current screen

### Draw Call Targets

| Screen Type | Target Draw Calls | Typical Range |
|-------------|-------------------|---------------|
| Simple HUD | 3-5 | 2-8 |
| Menu screen | 8-15 | 5-20 |
| Complex inventory | 15-25 | 10-35 |

### Identifying Batch Breaks

Each new draw call entry means a batch break. Common causes:

| Batch Break Cause | What to Look For | Fix |
|-------------------|-----------------|-----|
| Different texture | Draw calls alternate textures | Pack into SpriteAtlas |
| Different font | Font switch between elements | Limit to 2-3 fonts |
| Overflow:hidden | Nested clipping containers | Minimize clip nesting |
| Opacity on container | Container with opacity < 1 | Apply opacity to leaf elements |
| Render texture | Custom render in chain | Isolate from main batch |

## Profiler — UI Details Module

### Setup

1. **Window > Analysis > Profiler**
2. Add the **UI Details** module from the module dropdown
3. Enter Play mode and interact with UI
4. Select frames in the timeline to inspect

### Key Profiler Markers

| Marker | What It Measures | Budget | Fix if Exceeded |
|--------|-----------------|--------|-----------------|
| `UIR.Layout` | Yoga flexbox recalculation | < 0.5ms | Flatten hierarchy, reduce layout triggers |
| `UIR.RenderChainUpdate` | Dirty element processing | < 0.3ms | Fewer style changes per frame |
| `UIR.TextRegen` | Text mesh regeneration | < 0.2ms | Batch text updates, cache strings |
| `UIR.DrawChain` | Draw call submission | < 0.2ms | Use SpriteAtlas, fewer fonts |
| `UIR.TransformUpdate` | Transform-only changes | < 0.1ms | Expected to be cheap |

### Detecting Layout Thrashing

Layout thrashing occurs when reading layout properties forces an immediate recalculation:

```csharp
// LAYOUT THRASHING — forces layout recalc each iteration
for (int i = 0; i < items.Count; i++)
{
    items[i].style.top = offset;
    offset += items[i].resolvedStyle.height; // Read triggers layout!
}

// FIX — use flex layout or pre-calculate sizes
container.style.flexDirection = FlexDirection.Column;
// Let Yoga handle positioning — no manual read/write loop
```

**Profiler signature**: `UIR.Layout` spikes repeating in the same frame, often with high call count.

## Memory Profiler

### Finding Leaked VisualElements

1. **Window > Analysis > Memory Profiler** (install package if needed)
2. Take a snapshot on screen A, navigate away, take snapshot on screen B
3. Compare snapshots — filter by `VisualElement` type
4. Look for elements from screen A still in memory during screen B

### Common Leak Sources

| Leak Source | Why It Leaks | Fix |
|-------------|-------------|-----|
| Event callbacks not unregistered | Delegate holds reference | `UnregisterCallback` in cleanup |
| Static references to elements | Never GC'd | Avoid static VisualElement refs |
| Closure captures | Lambda captures `this` | Use method references |
| Binding not unbound | DataBinding holds ref | Call `Unbind()` on cleanup |
| VisualElement in collection | List/Dict holds ref | Clear collections on screen exit |

### Snapshot Comparison Workflow

1. Open Memory Profiler
2. Navigate to the screen to test → **Take Snapshot A**
3. Navigate away (close/hide the screen) → force GC with `GC.Collect()`
4. **Take Snapshot B**
5. Use **Compare Snapshots** view
6. Filter by `VisualElement` — any that exist in both snapshots are leaked

## Common Pitfalls & Solutions

| Problem | Symptom | Diagnosis | Solution |
|---------|---------|-----------|----------|
| Element not visible | Nothing renders | Debugger: check display, visibility, opacity | Set `display: flex`, `visibility: visible`, `opacity: 1` |
| Element has zero size | Invisible, no layout space | Debugger: Layout shows 0x0 | Set explicit size or check parent flex properties |
| USS not applying | Element unstyled | Debugger: no matching selectors | Check selector specificity, verify stylesheet added to panel |
| USS selector mismatch | Wrong styles | Debugger: unexpected selectors match | Use Debugger's matching selectors list to trace cascade |
| Events not firing | Click does nothing | Event Debugger: event not reaching target | Check `pickingMode`, StopPropagation upstream, pointer-events |
| Wrong event type | Handler never called | Event Debugger: different event type dispatched | Use `ClickEvent` not `MouseDownEvent` for buttons |
| Layout not updating | Stale positions | Profiler: no UIR.Layout calls | Verify style changes trigger layout; check `display: none` parents |
| Flex misconfiguration | Elements overlap or collapse | Debugger: unexpected layout values | Verify `flex-grow`, `flex-shrink`, `flex-basis` on parent and children |
| Binding not working | Label stays empty | Console: binding path warnings | Add `[CreateProperty]` to source property, verify `dataSource` path |
| Binding wrong path | Wrong data displayed | Console: property not found | Match path exactly: `dataSource.propertyName`, case-sensitive |
| Safe area not applied | UI under notch | Debugger: padding = 0 on container | Apply `Screen.safeArea` padding in C# on geometry change |
| Theme not switching | Colors unchanged | Debugger: old theme selectors active | Verify `ThemeStyleSheet` assigned to PanelSettings, USS uses theme classes |
| Text overflow | Text clipped or invisible | Debugger: element too small | Set `overflow: hidden`, `text-overflow: ellipsis`, or increase size |
| Picking not working | Element doesn't receive events | Event Debugger: event hits wrong target | Set `pickingMode: Position` on the target element |

## Diagnostic Utilities

### Visual Tree Dump

```csharp
using System.Text;
using UnityEngine;
using UnityEngine.UIElements;

public static class UIDebugUtils
{
    /// <summary>Logs the full visual tree with class lists and layout info.</summary>
    public static void DumpTree(VisualElement root, int maxDepth = 10)
    {
        var sb = new StringBuilder(2048);
        sb.AppendLine("=== Visual Tree Dump ===");
        DumpElement(sb, root, 0, maxDepth);
        Debug.Log(sb.ToString());
    }

    static void DumpElement(StringBuilder sb, VisualElement el, int depth, int maxDepth)
    {
        if (depth > maxDepth) return;

        var indent = new string(' ', depth * 2);
        var name = string.IsNullOrEmpty(el.name) ? "(unnamed)" : el.name;
        var type = el.GetType().Name;
        var classes = el.GetClasses();
        var classList = string.Join(", ", classes);
        var layout = el.layout;
        var display = el.resolvedStyle.display;
        var visible = el.resolvedStyle.visibility;

        sb.AppendLine($"{indent}[{type}] #{name} .{classList}");
        sb.AppendLine($"{indent}  layout: {layout.width:F0}x{layout.height:F0} @ ({layout.x:F0},{layout.y:F0})");
        sb.AppendLine($"{indent}  display:{display} visibility:{visible} opacity:{el.resolvedStyle.opacity:F2}");

        foreach (var child in el.Children())
            DumpElement(sb, child, depth + 1, maxDepth);
    }

    /// <summary>Validates all data bindings on the tree and logs failures.</summary>
    public static void ValidateBindings(VisualElement root)
    {
        var sb = new StringBuilder(512);
        sb.AppendLine("=== Binding Validation ===");
        int issues = 0;

        root.Query().ForEach(el =>
        {
            if (el.dataSource != null)
            {
                var srcType = el.dataSource.GetType();
                var path = el.dataSourcePath;
                if (!string.IsNullOrEmpty(path.ToString()))
                {
                    var prop = srcType.GetProperty(path.ToString());
                    if (prop == null)
                    {
                        sb.AppendLine($"  MISSING: {el.name} bound to '{path}' on {srcType.Name} — property not found");
                        issues++;
                    }
                }
            }
        });

        sb.AppendLine(issues == 0 ? "  All bindings valid." : $"  {issues} binding issue(s) found.");
        Debug.Log(sb.ToString());
    }

    /// <summary>Finds elements with zero size that might be invisible.</summary>
    public static void FindZeroSizeElements(VisualElement root)
    {
        var sb = new StringBuilder(512);
        sb.AppendLine("=== Zero-Size Elements ===");
        int count = 0;

        root.Query().ForEach(el =>
        {
            if (el.resolvedStyle.display == DisplayStyle.Flex &&
                (el.layout.width <= 0 || el.layout.height <= 0))
            {
                var name = string.IsNullOrEmpty(el.name) ? el.GetType().Name : el.name;
                sb.AppendLine($"  {name}: {el.layout.width:F0}x{el.layout.height:F0}");
                count++;
            }
        });

        sb.AppendLine(count == 0 ? "  None found." : $"  {count} zero-size element(s).");
        Debug.Log(sb.ToString());
    }

    /// <summary>Highlights an element with a colored border for visual identification.</summary>
    public static void HighlightElement(VisualElement el, Color color, float width = 2f)
    {
        el.style.borderTopColor = color;
        el.style.borderBottomColor = color;
        el.style.borderLeftColor = color;
        el.style.borderRightColor = color;
        el.style.borderTopWidth = width;
        el.style.borderBottomWidth = width;
        el.style.borderLeftWidth = width;
        el.style.borderRightWidth = width;
    }
}
```

### Usage in Development

```csharp
void OnEnable()
{
    var root = GetComponent<UIDocument>().rootVisualElement;

    #if UNITY_EDITOR || DEVELOPMENT_BUILD
    UIDebugUtils.DumpTree(root);
    UIDebugUtils.ValidateBindings(root);
    UIDebugUtils.FindZeroSizeElements(root);
    #endif
}
```

## USS Debugging Helpers

Temporary USS classes for visualizing layout during development. Add to a `debug.uss` stylesheet and remove before release.

```css
/* Outline every element to see layout boxes */
.debug-outline * {
    border-width: 1px;
    border-color: rgba(255, 0, 0, 0.3);
}

/* Highlight specific element with solid red border */
.debug-highlight {
    border-width: 2px;
    border-color: red;
}

/* Visualize flex containers */
.debug-flex-row {
    background-color: rgba(0, 100, 255, 0.1);
    border-width: 1px;
    border-color: rgba(0, 100, 255, 0.5);
}

.debug-flex-col {
    background-color: rgba(0, 200, 0, 0.1);
    border-width: 1px;
    border-color: rgba(0, 200, 0, 0.5);
}

/* Show padding/margin with color fills */
.debug-padding {
    background-color: rgba(255, 165, 0, 0.15);
}

.debug-margin {
    margin: 4px;
    background-color: rgba(255, 0, 255, 0.1);
}

/* Force minimum size to make zero-size elements visible */
.debug-min-size {
    min-width: 20px;
    min-height: 20px;
    background-color: rgba(255, 0, 0, 0.3);
}

/* Overflow visualization */
.debug-overflow {
    overflow: visible;
    border-width: 1px;
    border-color: orange;
}
```

### Applying Debug Styles in C#

```csharp
#if UNITY_EDITOR || DEVELOPMENT_BUILD
// Toggle debug outlines on the entire tree
root.ToggleInClassList("debug-outline");

// Highlight a specific element
problematicElement.AddToClassList("debug-highlight");

// Make zero-size elements visible
root.Query().Where(e => e.layout.width <= 0).ForEach(e =>
    e.AddToClassList("debug-min-size"));
#endif
```

## Common Pitfalls

| Pitfall | Why It Hurts | Do This Instead |
|---------|-------------|-----------------|
| Debug by trial-and-error | Wastes time, introduces side effects | Use Debugger to inspect computed state first |
| Ignoring Profiler markers | Guessing at performance problems | Profile first, optimize what the data shows |
| `Debug.Log` spam in callbacks | Floods console, hides real errors | Use Event Debugger for propagation tracing |
| Adding inline styles to fix layout | Masks the root cause in USS | Fix the USS selector or specificity issue |
| Rebuilding UI to test changes | Slow iteration cycle | Use live USS editing in Debugger |
| Not checking `pickingMode` | Events silently miss elements | Verify picking mode in Debugger |
| Ignoring console binding warnings | Binding fails silently | Check console for path/type mismatch warnings |
| Skipping Memory Profiler | Leaks accumulate silently | Snapshot before/after screen transitions |
| Hardcoding style values in C# | Can't debug via USS tools | Use USS classes, toggle with `AddToClassList` |
| Testing only in Editor | Runtime differences missed | Test on device with Development Build enabled |

## Exercise: Debug a Broken Screen

Practice systematic debugging on a deliberately broken UI:

1. **Setup**: Create a screen with a hidden panel (`display: none` set inline), a button with wrong `pickingMode`, a label with a broken data binding path, and a ListView with no `fixedItemHeight`
2. **Visual debugging**: Open **UI Toolkit Debugger** → find the hidden panel → identify the inline `display: none` → fix it
3. **Event debugging**: Open **Event Debugger** → click the button → observe no event reaches handler → find `pickingMode: Ignore` → fix to `Position`
4. **Binding debugging**: Check **Console** for binding warnings → identify wrong property path → fix `[CreateProperty]` and path
5. **Performance debugging**: Open **Profiler > UI Details** → scroll the ListView → observe `UIR.Layout` spikes → add `fixedItemHeight: 56`

**Checklist**: ✅ Used UI Toolkit Debugger (not trial-and-error) · ✅ Used Event Debugger to trace propagation · ✅ Found binding error via Console warnings · ✅ Measured perf improvement with Profiler · ✅ All 4 issues fixed using proper tools

## Shared Resources

- [Performance Benchmarks](../references/performance-benchmarks.md) — profiler marker budgets, draw call targets
- [Dragon Crashers Insights](../references/dragon-crashers-insights.md) — production debugging patterns
- [Code Templates](../references/code-templates.md) — base screen patterns with cleanup
- [Official Docs Links](../references/official-docs-links.md) — Unity 6 documentation index

## Official Documentation

- [UI Toolkit Debugger](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-debugger.html)
- [Performance Considerations](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-performance-considerations.html)
- [Event System](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-Events.html)
- [Memory Profiler](https://docs.unity3d.com/Packages/com.unity.memoryprofiler@1.1/manual/index.html)

## Project-Specific Debugging Scenarios

For detailed Dragon Crashers debugging walkthroughs covering event bus issues, async task silent failures, world-to-panel positioning, compound theme debugging, safe area edge cases, and modal/overlay state tracking, see **[Dragon Crashers Insights — Debugging Scenarios](../references/dragon-crashers-insights.md)** (section: Debugging Scenarios).

**Key patterns covered**: Event subscription pairing (`+=`/`-=`), fire-and-forget `Task` exception swallowing, `RuntimePanelUtils.CameraTransformWorldToPanelRect` null dependencies, `ThemeManager` compound name construction, `SafeAreaBorder` Editor-vs-device differences, `UIManager` modal/overlay state machine.

## Cross-References to Related Skills

Debugging UI Toolkit issues often spans multiple domains. These sibling skills provide deeper context:

| Skill | When to Cross-Reference |
|-------|------------------------|
| [Architecture](../ui-toolkit-architecture/SKILL.md) | Understanding UIView base class, IDisposable lifecycle, event bus design |
| [Patterns](../ui-toolkit-patterns/SKILL.md) | View lifecycle management, event subscription patterns, modal/overlay navigation |
| [Theming](../ui-toolkit-theming/SKILL.md) | TSS file structure, compound theme names, PanelSettings configuration |
| [Performance](../ui-toolkit-performance/SKILL.md) | Profiler markers, draw call analysis, layout thrashing diagnosis |
| [Data Binding](../ui-toolkit-databinding/SKILL.md) | Binding path resolution, `[CreateProperty]` requirements, binding validation |
| [Responsive](../ui-toolkit-responsive/SKILL.md) | Safe area handling, media queries, aspect ratio events |
| [Mobile](../ui-toolkit-mobile/SKILL.md) | Device-specific safe area values, touch event debugging, Device Simulator |
| [Master](../ui-toolkit-master/SKILL.md) | Skill index, learning path, overall architecture overview |

---

**← Previous**: [Mobile](../ui-toolkit-mobile/SKILL.md) | **Series Start →**: [Master](../ui-toolkit-master/SKILL.md)

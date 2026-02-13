---
name: ui-toolkit-debugging
description: "Debugging and troubleshooting Unity UI Toolkit. Covers UI Toolkit Debugger, Event Debugger, Frame Debugger, Profiler UI Details module, Memory Profiler, common pitfalls, and diagnostic utilities. Use when: (1) Element not visible or styled incorrectly, (2) Events not firing or propagating wrong, (3) Investigating UI draw calls or layout cost, (4) Tracking UI memory leaks, (5) Diagnosing binding failures, (6) Troubleshooting safe area or theming issues. Triggers: 'debug UI', 'element not showing', 'event not firing', 'USS not applying', 'UI Toolkit Debugger', 'layout thrashing', 'UI memory leak', 'binding not working'."
---

# UI Toolkit Debugging

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

Debugging patterns extracted from the Dragon Crashers UIToolkit demo project. Each scenario documents the root cause, diagnostic steps, and fix.

### Event Bus Debugging

**Pattern**: The project uses static `Action` delegates as a lightweight event bus (`MainMenuUIEvents`, `MailEvents`, `ThemeEvents`). These are **not** C# `event` fields — they are plain `static Action` delegates with no built-in invocation list safety.

**Files**:
- `Assets/Scripts/UI/Events/MainMenuUIEvents.cs` — main menu navigation events
- `Assets/Scripts/UI/Events/MailEvents.cs` — mail screen events
- `Assets/Scripts/UI/Events/ThemeEvents.cs` — theme change events
- `Assets/Scripts/UI/UIViews/UIManager.cs` — subscribe in `OnEnable`, unsubscribe in `OnDisable`

**Symptom**: Button click does nothing, screen doesn't switch, or handler fires twice.

**Diagnostic Steps**:

1. **Verify subscription pairing** — every `+=` in `OnEnable`/`Initialize` must have a matching `-=` in `OnDisable`/`Dispose`:
```csharp
// UIManager.cs — correct pairing
void SubscribeToEvents()
{
    MainMenuUIEvents.HomeScreenShown += OnHomeScreenShown;
    // ...
}
void UnsubscribeFromEvents()
{
    MainMenuUIEvents.HomeScreenShown -= OnHomeScreenShown;
    // ...
}
```

2. **Add temporary invocation list logging** to trace who is subscribed:
```csharp
public static void DebugInvocationList(string eventName, Delegate del)
{
    if (del == null) { Debug.Log($"[EventBus] {eventName}: no subscribers"); return; }
    foreach (var d in del.GetInvocationList())
        Debug.Log($"[EventBus] {eventName} → {d.Target?.GetType().Name ?? "static"}.{d.Method.Name}");
}
```

3. **Check for null invocation** — `MainMenuUIEvents.HomeScreenShown?.Invoke()` is safe, but if a subscriber was never added, the `?.` silently does nothing. Add a log before invocation if the event seems dead.

4. **Watch for double-subscribe** — if `OnEnable` runs twice without `OnDisable` (e.g., re-parenting a GameObject), the handler fires twice. The invocation list debug method above reveals this.

### Async Task Debugging

**Pattern**: `MailContentView` uses fire-and-forget async: `_ = ClaimRewardRoutineAsync()`. The discarded `Task` means any exception inside the async method is **silently swallowed** — no console error, no crash, just silent failure.

**Files**:
- `Assets/Scripts/UI/UIViews/MailContentView.cs` — `ClaimRewardRoutineAsync()`, `DeleteMailMessageRoutine()`

**Symptom**: Async UI animation starts but never completes, or subsequent UI state is never reached. No error in console.

**Diagnostic Steps**:

1. **Add try/catch inside every async method** (the only reliable approach for fire-and-forget):
```csharp
async Task ClaimRewardRoutineAsync()
{
    try
    {
        m_GiftAmount.AddToClassList(k_GiftDeletedClass);
        m_GiftIcon.AddToClassList(k_GiftDeletedClass);
        await Task.Delay((int)(k_TransitionTime * 1000));
        ShowFooter(false);
        m_ClaimButton.SetEnabled(false);
    }
    catch (Exception ex)
    {
        Debug.LogException(ex);
    }
}
```

2. **Register a global unobserved task handler** in a bootstrap MonoBehaviour:
```csharp
TaskScheduler.UnobservedTaskException += (sender, e) =>
{
    Debug.LogError($"[UnobservedTask] {e.Exception.InnerException?.Message}");
    e.SetObserved();
};
```

3. **Check if `Task.Delay` throws** — `Task.Delay` with a negative millisecond value throws `ArgumentOutOfRangeException`. With fire-and-forget, this is invisible. Verify `k_TransitionTime` is positive.

4. **Verify UI element not null** — if `m_GiftAmount` or `m_GiftIcon` is null when the async method runs (e.g., view was disposed mid-animation), a `NullReferenceException` is swallowed.

### World-to-Panel Debugging

**Pattern**: `HealthBarController` uses `RuntimePanelUtils.CameraTransformWorldToPanelRect()` to position a UI element over a world-space character. This requires three non-null dependencies: `element.panel`, `Camera.main`, and the element itself.

**File**: `Assets/Scripts/UI/Controllers/HealthBarController.cs`

**Symptom**: Health bar doesn't appear, appears at wrong position, or throws `NullReferenceException` in `LateUpdate`.

**Diagnostic Steps**:

1. **Check `element.panel` is not null** — a VisualElement has no panel until it's attached to a UIDocument and the first layout pass completes:
```csharp
void MoveToWorldPosition(VisualElement element, Vector3 worldPosition, Vector2 worldSize)
{
    if (element?.panel == null)
    {
        Debug.LogWarning("[HealthBar] element.panel is null — not yet attached to panel");
        return;
    }
    Rect rect = RuntimePanelUtils.CameraTransformWorldToPanelRect(
        element.panel, worldPosition, worldSize, Camera.main);
    element.transform.position = rect.position;
}
```

2. **Check `Camera.main` is not null** — `Camera.main` returns null if no camera is tagged "MainCamera" or if the camera GameObject is inactive. `RuntimePanelUtils` will throw if camera is null.

3. **Check `transformToFollow` is assigned** — `MoveToWorldPosition` reads `transformToFollow.position` without null check. If the character is destroyed, this throws.

4. **Verify RuntimePanelUtils return values** — if the world position is behind the camera, `CameraTransformWorldToPanelRect` returns a rect with negative or extremely large coordinates. Add bounds checking:
```csharp
Rect rect = RuntimePanelUtils.CameraTransformWorldToPanelRect(...);
if (rect.x < -1000 || rect.x > Screen.width + 1000)
{
    Debug.LogWarning("[HealthBar] World position is off-screen or behind camera");
    return;
}
```

5. **LateUpdate timing** — `MoveToWorldPosition` runs every `LateUpdate()` and on `MediaQueryEvents.CameraResized`. If the health bar jitters, check that camera movement also happens in `LateUpdate` and that execution order is correct (camera moves before health bar updates).

### Theme Debugging

**Pattern**: `ThemeManager` constructs compound theme names by combining aspect ratio with a suffix delimiter `--`. For example: `"Landscape--Christmas"`. A mismatch between the constructed name and the `ThemeSettings.theme` string causes a silent fallback (no theme applied, warnings only with `m_Debug` enabled).

**Files**:
- `Assets/Scripts/UI/Themes/ThemeManager.cs` — theme application logic
- `Assets/Scripts/UI/Events/ThemeEvents.cs` — `ThemeChanged` event

**Symptom**: Theme doesn't change, wrong theme applied after rotation, or styles revert to default.

**Diagnostic Steps**:

1. **Enable `m_Debug` on ThemeManager** — the component logs warnings only when `[SerializeField] bool m_Debug` is true. Enable it in the Inspector to see `[ThemeManager]` prefixed log messages.

2. **Verify compound name construction** — the name is built as `mediaAspectRatio.ToString() + suffix`:
```csharp
// OnAspectRatioUpdated builds: "Landscape" + "--Christmas" = "Landscape--Christmas"
string suffix = GetSuffix(m_CurrentTheme, "--"); // e.g. "--Christmas"
string newThemeName = mediaAspectRatio.ToString() + suffix;
```
   Check that `ThemeSettings` list in the Inspector contains an entry with `theme` matching this exact string.

3. **Check ThemeSettings list completeness** — every combination of aspect ratio × season must exist:
   - `Landscape`, `Landscape--Christmas`, `Landscape--Halloween`
   - `Portrait`, `Portrait--Christmas`, `Portrait--Halloween`
   
   Missing entries cause `GetThemeIndex` to return `-1` and `GetThemeStyleSheet` to return null.

4. **Verify TSS and PanelSettings assets** — even if the theme name matches, a null `tss` or `panelSettings` field in `ThemeSettings` causes silent failure. Check the Inspector for missing asset references.

5. **Check PanelSettings assignment** — `ThemeManager.SetPanelSettings()` replaces `m_Document.panelSettings` entirely. If PanelSettings assets have different configurations (sort order, scale mode, target texture), switching themes can cause unexpected layout changes beyond just styling.

6. **[ExecuteInEditMode] caveat** — `ThemeManager` runs in edit mode. Theme changes in Play mode persist to the asset because `PanelSettings.themeStyleSheet` is a serialized reference. Stop play mode and verify the PanelSettings asset hasn't been permanently modified.

### SafeArea Debugging

**Pattern**: `SafeAreaBorder` reads `Screen.safeArea` and applies the insets as `borderWidth` on a container VisualElement. In the Unity Editor, `Screen.safeArea` returns the full screen rect (zero insets), so borders are always 0.

**File**: `Assets/Scripts/Utilities/SafeAreaBorder.cs`

**Symptom**: Safe area borders don't appear in Editor, or border values are 0.

**Diagnostic Steps**:

1. **Expected behavior in Editor** — `Screen.safeArea` equals `new Rect(0, 0, Screen.width, Screen.height)` in the Editor. All border values compute to 0. This is not a bug — test on device or use the Device Simulator:
   - **Window > General > Device Simulator** — simulates notch insets for specific devices

2. **Enable `m_Debug` flag** — the component logs applied border values: `[SafeAreaBorder] Applied Safe Area | Left: 0, Right: 0, Top: 44, Bottom: 34`. If all values are 0, you're running in Editor without simulator.

3. **Check `m_Element` name** — if the serialized element name doesn't match any element in the UXML, `m_Root` stays null and `ApplySafeArea()` silently returns. Add a breakpoint or log at the null check:
```csharp
if (m_Root == null)
{
    Debug.LogWarning("[SafeAreaBorder] m_Root is null — check m_Element name or UIDocument");
    return;
}
```

4. **Verify `m_Multiplier`** — the multiplier defaults to 1.0 but is `[Range(0, 1)]`. If set to 0 in the Inspector, all borders compute to 0 regardless of safe area values.

5. **GeometryChangedEvent timing** — `ApplySafeArea` also runs on `GeometryChangedEvent`. If the UIDocument isn't initialized when `Awake()` runs, `Initialize()` logs a warning and returns. The safe area won't be applied until the next geometry change. Call `Initialize()` again from a later lifecycle point if needed.

6. **Border color transparency** — if `m_BorderColor` is set to a fully transparent color (`alpha = 0`), borders are applied but invisible. Check the color alpha in the Inspector.

### Modal/Overlay Debugging

**Pattern**: `UIManager` tracks view state with `m_CurrentView` and `m_PreviousView` fields. Modal views (Home, Char, Shop, etc.) use `ShowModalView()` which hides current and shows new. Overlay views (Settings, Inventory) save `m_PreviousView` and show on top without hiding current.

**File**: `Assets/Scripts/UI/UIViews/UIManager.cs`

**Symptom**: Views stack incorrectly, previous view doesn't restore after closing overlay, or multiple views visible simultaneously.

**Diagnostic Steps**:

1. **Trace the view state** — add temporary logging to `ShowModalView`:
```csharp
void ShowModalView(UIView newView)
{
    Debug.Log($"[UIManager] ShowModal: {newView?.GetType().Name} | " +
              $"Current: {m_CurrentView?.GetType().Name} | " +
              $"Previous: {m_PreviousView?.GetType().Name}");
    // ... existing logic
}
```

2. **Check overlay Show/Hide pairing** — overlays set `m_PreviousView` on show but rely on the hide handler to restore it. If `SettingsScreenShown` fires without a corresponding `SettingsScreenHidden`, `m_PreviousView` gets stuck:
   - `OnSettingsScreenShown` → saves `m_CurrentView` as `m_PreviousView`, shows settings
   - `OnSettingsScreenHidden` → hides settings, restores `m_PreviousView` as current
   
   If the hide event never fires, the current view reference is lost.

3. **Check Dispose() on all views** — `UIManager.OnDisable()` iterates `m_AllViews` and calls `Dispose()`. If a view subclass overrides `Dispose()` but forgets to call `base.Dispose()` or unsubscribe from events, leaked subscriptions cause handlers to fire on destroyed objects.

4. **Verify UIView.IsHidden** — `UIView.IsHidden` checks `m_TopElement.style.display == DisplayStyle.None`. This checks the **inline style**, not the resolved style. If display is set via USS class rather than inline, `IsHidden` returns false even when the element is hidden.

5. **Use the Visual Tree Dump** — when views overlap unexpectedly, use `UIDebugUtils.DumpTree(root)` from the Diagnostic Utilities section above to see which elements have `display: flex` vs `display: none`.

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

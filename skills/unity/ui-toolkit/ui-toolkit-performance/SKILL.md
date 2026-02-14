---
name: ui-toolkit-performance
description: "Performance optimization for Unity UI Toolkit. Covers profiling, draw call optimization, transform vs layout animations, element pooling, ListView virtualization, memory management, and GC-free patterns. Use when: (1) UI frame rate is low, (2) Profiling UI draw calls or layout cost, (3) Optimizing list/grid rendering, (4) Reducing GC allocations in UI code, (5) Choosing animation strategies. Triggers: 'UI performance', 'draw calls', 'layout thrashing', 'UI profiling', 'element pool', 'UI memory', 'virtualization', 'UsageHints'."
---

# UI Toolkit Performance

<!-- OWNERSHIP: FpsCounter, profiling workflows, GC-free patterns, UsageHints, draw call optimization, transform vs layout animation cost, element pooling, virtualization benchmarks. -->

> **Based on**: Unity 6 (6000.0), [Dragon Crashers](../references/dragon-crashers-insights.md) official sample

Optimize UI Toolkit rendering, layout, and memory for 60fps on all platforms. Dragon Crashers achieves 2-4 draw calls per simple screen and < 0.5ms layout cost by following these patterns.

## Performance Mental Model

```
 User Input → Event Processing → Data Update → Binding → Style Resolution
                                                              │
                                                              ▼
                               ┌─────────────────────────────────┐
                               │      LAYOUT (Yoga/Flexbox)      │  ← EXPENSIVE
                               │  Calculates position & size     │
                               │  Triggered by: width, height,   │
                               │  margin, padding, flex changes   │
                               └──────────────┬──────────────────┘
                                              ▼
                               ┌─────────────────────────────────┐
                               │    TRANSFORM (GPU-accelerated)  │  ← CHEAP
                               │  translate, rotate, scale       │
                               │  Does NOT trigger layout        │
                               └──────────────┬──────────────────┘
                                              ▼
                               ┌─────────────────────────────────┐
                               │      RENDER (Batched draws)     │
                               │  Uber shader batches similar    │
                               │  elements into single draw call │
                               └─────────────────────────────────┘
```

**Rule #1: Never trigger layout during animation. Use transforms only.**

## Transform vs Layout Animations

| Property | Type | Layout Recalc | Use For |
|----------|------|--------------|---------|
| `translate` | Transform | No | Slide, position |
| `rotate` | Transform | No | Spin, flip |
| `scale` | Transform | No | Pulse, grow |
| `opacity` | Transform | No | Fade |
| `width` | Layout | **Yes — full subtree** | Never animate |
| `height` | Layout | **Yes — full subtree** | Never animate |
| `margin-*` | Layout | **Yes — full subtree** | Never animate |
| `padding-*` | Layout | **Yes — full subtree** | Never animate |
| `flex-grow` | Layout | **Yes — full subtree** | Never animate |

### Correct: Slide animation via translate

```css
.panel-slide {
    translate: 100% 0;
    opacity: 0;
    transition-property: translate, opacity;
    transition-duration: 300ms;
    transition-timing-function: ease-out;
}

.panel-slide--active {
    translate: 0 0;
    opacity: 1;
}
```

```csharp
// Toggle with USS class — no layout cost
panel.ToggleInClassList("panel-slide--active");
```

### Wrong: Slide animation via width

```css
/* DON'T — triggers layout recalc every frame */
.panel-bad {
    width: 0;
    overflow: hidden;
    transition-property: width;
    transition-duration: 300ms;
}
.panel-bad--open { width: 300px; }
```

## UsageHints

Tell the renderer how elements will change:

```csharp
// Animated elements — enables separate batch for transform changes
panel.usageHints = UsageHints.DynamicTransform;

// Container of animated children
container.usageHints = UsageHints.GroupTransform;

// Elements with color/opacity transitions
button.usageHints = UsageHints.DynamicColor;
```

| Hint | When to Use |
|------|-------------|
| `DynamicTransform` | Element's translate/rotate/scale changes frequently |
| `GroupTransform` | Container that moves/transforms with all children |
| `DynamicColor` | Element's background-color or opacity changes frequently |
| `MaskContainer` | Container with `overflow: hidden` that clips children |

**Do not set on static elements** — adds overhead for elements that don't change.

## ListView Virtualization

For any list with 20+ items, use `ListView` instead of manual ScrollView:

```csharp
// CRITICAL: Set fixedItemHeight for best performance
listView.fixedItemHeight = 72;
listView.virtualizationMethod = CollectionVirtualizationMethod.FixedHeight;

// makeItem: called only for visible + buffer items (typically 8-15)
listView.makeItem = () => itemTemplate.Instantiate();

// bindItem: called when recycled element gets new data
listView.bindItem = (element, index) =>
{
    element.Q<Label>("name").text = items[index].Name;
};

// unbindItem: clean up subscriptions when element goes off-screen
listView.unbindItem = (element, index) =>
{
    // Remove any per-item event subscriptions
};
```

Performance comparison — see [Performance Benchmarks — ListView Virtualization](../references/performance-benchmarks.md) for detailed numbers.

## Draw Call Optimization

### What creates new draw calls

| Cause | Fix |
|-------|-----|
| Different textures | Use SpriteAtlas to batch |
| Different fonts | Limit to 2-3 fonts |
| Nested `overflow: hidden` | Minimize clipping containers |
| Opacity < 1 on containers | Apply opacity to leaf elements |
| Custom render textures | Use sparingly |

### Checking draw calls

1. **Window > Analysis > Frame Debugger** — step through draw calls
2. Look for `UIR.DrawChain` entries
3. Consecutive elements with same texture/font batch together
4. Breaks in sequence indicate new draw call

### SpriteAtlas for batching

```csharp
// All sprites in the same atlas batch into one draw call
// Create atlas: Assets > Create > 2D > Sprite Atlas
// Drag sprites into atlas, ensure "Include in Build" is checked
```

## Element Pooling

For frequently created/destroyed elements (notifications, damage numbers, chat messages):

```csharp
public class VisualElementPool<T> where T : VisualElement, new()
{
    readonly Stack<T> _pool = new();
    readonly Action<T> _onGet;
    readonly Action<T> _onRelease;

    public VisualElementPool(Action<T> onGet = null, Action<T> onRelease = null, int prewarm = 0)
    {
        _onGet = onGet;
        _onRelease = onRelease;
        for (int i = 0; i < prewarm; i++)
            _pool.Push(new T());
    }

    public T Get()
    {
        var el = _pool.Count > 0 ? _pool.Pop() : new T();
        el.style.display = DisplayStyle.Flex;
        _onGet?.Invoke(el);
        return el;
    }

    public void Release(T el)
    {
        el.style.display = DisplayStyle.None;
        _onRelease?.Invoke(el);
        _pool.Push(el);
    }
}
```

## GC-Free Patterns

### Cache Q() calls

```csharp
// BAD: Allocates every frame
void Update() {
    root.Q<Label>("score").text = score.ToString();
}

// GOOD: Cache once
Label _scoreLabel;
void OnEnable() { _scoreLabel = root.Q<Label>("score"); }
void UpdateScore(int score) { _scoreLabel.text = score.ToString(); }
```

### Avoid boxing in style setters

```csharp
// BAD: Boxing allocation
element.style.width = 100; // int boxed to StyleLength

// GOOD: Explicit struct
element.style.width = new Length(100, LengthUnit.Pixel);
```

### Cache Length/StyleColor values

```csharp
// Pre-compute style values used repeatedly
static readonly StyleLength _width100 = new Length(100, LengthUnit.Percent);
static readonly StyleColor _colorRed = new StyleColor(Color.red);
```

### Use method references over lambdas

```csharp
// BAD: Lambda allocates closure
button.RegisterCallback<ClickEvent>(evt => OnClick(evt));

// GOOD: Method reference — no allocation
button.RegisterCallback<ClickEvent>(OnClick);
void OnClick(ClickEvent evt) { /* ... */ }
```

## Profiling Workflow

1. Open **Window > Analysis > Profiler**
2. Select **UI Details** module
3. Play and interact with UI
4. Watch markers:

| Marker | Target | Action if exceeded |
|--------|--------|--------------------|
| `UIR.Layout` | < 0.5ms | Reduce layout changes, flatten hierarchy |
| `UIR.RenderChainUpdate` | < 0.3ms | Reduce dirty elements per frame |
| `UIR.TextRegen` | < 0.2ms | Reduce text changes, batch updates |
| `UIR.DrawChain` | < 0.2ms | Reduce draw calls (atlas, fewer fonts) |

5. Use **Frame Debugger** to count draw calls per screen
6. Compare against targets in [Performance Benchmarks — Draw Call Targets](../references/performance-benchmarks.md)

## Dragon Crashers: Project-Specific Performance Patterns

For detailed performance analysis of Dragon Crashers patterns — FpsCounter ring buffer, HealthBarController world-to-panel cost, async/await vs coroutine GC tradeoffs, Instantiate-in-loop vs ListView thresholds, StopImmediatePropagation impact, and event subscription lifecycle — see **[Dragon Crashers Insights — Performance Analysis](../references/dragon-crashers-insights.md)** (section: Performance Analysis).

**Key takeaways**: Cache `Camera.main` and all `Q<T>()` results; use transform (not layout) for positioning; prefer USS transitions over `async Task.Delay` loops; add `CancellationToken` to infinite async loops; use `ListView` for 50+ items; match subscribe/unsubscribe lifecycle symmetrically.

## Optimization Checklist

- [ ] Lists 20+ items → ListView with fixedItemHeight
- [ ] All animations use translate/rotate/scale/opacity only
- [ ] Animated elements have `UsageHints.DynamicTransform`
- [ ] Q() calls cached in OnEnable, not called per-frame
- [ ] No string concat in per-frame updates
- [ ] Sprites in SpriteAtlas for batching
- [ ] Max 2-3 fonts per screen
- [ ] Minimal nested overflow:hidden
- [ ] Opacity on leaf elements, not containers
- [ ] Element pooling for transient UI (notifications, popups)

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Animating `width`/`height` | Full subtree layout recalc every frame | Use `translate`, `scale`, `rotate`, `opacity` |
| Q() in Update() | GC allocation every frame from string queries | Cache references in `OnEnable` |
| No `fixedItemHeight` on ListView | Falls back to variable height — slower virtualization | Always set `fixedItemHeight` |
| `UsageHints` on static elements | Adds per-frame overhead for elements that don't change | Only set on animated elements |
| String concatenation per frame | GC allocation from `$"Score: {val}"` every update | Use `StringBuilder` or update only on change |
| Opacity on containers | Breaks draw call batching for all children | Apply opacity to leaf elements only |
| Nested `overflow: hidden` | Each clip layer adds a draw call | Minimize clip nesting, flatten hierarchy |
| Creating elements in hot paths | GC pressure from `new VisualElement()` in loops | Use element pooling |

## Exercise: Optimize a Leaderboard Screen

Profile and optimize a 100-row leaderboard with player avatars:

1. **Baseline**: Create a `ScrollView` with 100 manually created row elements, each with an avatar image + name label + score label
2. **Profile**: Open **Profiler > UI Details**, measure `UIR.Layout` and draw call count
3. **Optimize Step 1**: Replace ScrollView with `ListView` + `fixedItemHeight: 56` — measure improvement
4. **Optimize Step 2**: Pack all avatar sprites into a `SpriteAtlas` — measure draw call reduction
5. **Optimize Step 3**: Add `UsageHints.DynamicTransform` to row highlight animation — verify `UIR.TransformUpdate` replaces `UIR.Layout`
6. **Optimize Step 4**: Cache all `Q()` calls, remove per-frame allocations — verify zero GC in Profiler

**Checklist**: ✅ Before/after profiler screenshots captured · ✅ ListView virtualization active (verify: only 8-15 `makeItem` calls, not 100) · ✅ Draw calls ≤ 5 for the screen · ✅ Zero GC allocations during scroll · ✅ `UIR.Layout` < 0.5ms

## Shared Resources

- [Performance Benchmarks](../references/performance-benchmarks.md) — metrics, targets, zero-alloc patterns
- [Dragon Crashers Insights](../references/dragon-crashers-insights.md) — production performance patterns
- [Code Templates](../references/code-templates.md) — Element Pool, Base Screen templates
- [Official Docs Links](../references/official-docs-links.md) — Unity 6 documentation index

## Official Documentation

- [Performance Considerations](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-performance-considerations.html)
- [ListView](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-ListView.html)
- [USS Transitions](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-Transitions.html)
- [Profiler](https://docs.unity3d.com/6000.0/Documentation/Manual/Profiler.html)

## Cross-References

- **[UI Toolkit Patterns](../ui-toolkit-patterns/SKILL.md)** — Animation patterns (USS transitions, async animations, typewriter effects) referenced by performance tradeoffs above
- **[UI Toolkit Mobile](../ui-toolkit-mobile/SKILL.md)** — Mobile-specific performance: `Application.targetFrameRate`, safe area, touch targets
- **[UI Toolkit Debugging](../ui-toolkit-debugging/SKILL.md)** — UI Toolkit Debugger, profiler workflow, draw call inspection
- **[Dragon Crashers Insights](../references/dragon-crashers-insights.md)** — Full architectural analysis of patterns used above

---

**← Previous**: [Patterns](../ui-toolkit-patterns/SKILL.md) | **Next →**: [Mobile](../ui-toolkit-mobile/SKILL.md)

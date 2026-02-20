---
name: ui-toolkit-performance
description: "Performance optimization for Unity UI Toolkit. Covers profiling, draw call optimization, transform vs layout animations, element pooling, ListView virtualization, memory management, and GC-free patterns. Use when: (1) UI frame rate is low, (2) Profiling UI draw calls or layout cost, (3) Optimizing list/grid rendering, (4) Reducing GC allocations in UI code, (5) Choosing animation strategies. Triggers: 'UI performance', 'draw calls', 'layout thrashing', 'UI profiling', 'element pool', 'UI memory', 'virtualization', 'UsageHints'."
---

# UI Toolkit Performance

Optimize UI Toolkit for 60fps. Target: 2-4 draw calls/screen, < 0.5ms layout cost.

## Performance Mental Model

```
Input → Events → Data → Binding → Style → LAYOUT (expensive, Yoga) → TRANSFORM (cheap, GPU) → RENDER (batched)
```

**Rule #1: Never trigger layout during animation. Use transforms only.**

## Transform vs Layout

| Property | Layout Recalc | Use For |
|----------|--------------|---------|
| `translate`, `rotate`, `scale`, `opacity` | No | All animations |
| `width`, `height`, `margin-*`, `padding-*`, `flex-grow` | **Yes — full subtree** | Never animate |

```css
.panel-slide { translate: 100% 0; opacity: 0; transition-property: translate, opacity; transition-duration: 300ms; transition-timing-function: ease-out; }
.panel-slide--active { translate: 0 0; opacity: 1; }
```

```csharp
panel.ToggleInClassList("panel-slide--active"); // no layout cost
```

## UsageHints

```csharp
panel.usageHints = UsageHints.DynamicTransform;   // animated elements
container.usageHints = UsageHints.GroupTransform;  // container of animated children
button.usageHints = UsageHints.DynamicColor;       // color/opacity transitions
```

| Hint | When |
|------|------|
| `DynamicTransform` | translate/rotate/scale changes frequently |
| `GroupTransform` | Container moves with all children |
| `DynamicColor` | background-color or opacity changes frequently |
| `MaskContainer` | `overflow: hidden` that clips children |

**Do not set on static elements** — adds overhead.

## ListView Virtualization

```csharp
listView.fixedItemHeight = 72;
listView.virtualizationMethod = CollectionVirtualizationMethod.FixedHeight;
listView.makeItem = () => itemTemplate.Instantiate();
listView.bindItem = (element, index) => element.Q<Label>("name").text = items[index].Name;
listView.unbindItem = (element, index) => { /* cleanup subscriptions */ };
```

Use `ListView` for 20+ items. See [Performance Benchmarks](references/performance-benchmarks.md).

## Draw Call Optimization

| Cause | Fix |
|-------|-----|
| Different textures | SpriteAtlas |
| Different fonts | Limit to 2-3 |
| Nested `overflow: hidden` | Minimize clipping |
| Opacity < 1 on containers | Apply to leaf elements |

Check: **Frame Debugger** → `UIR.DrawChain` entries. Consecutive same-texture elements batch.

## Element Pooling

```csharp
public class VisualElementPool<T> where T : VisualElement, new() {
    readonly Stack<T> _pool = new();
    readonly Action<T> _onGet, _onRelease;
    public VisualElementPool(Action<T> onGet = null, Action<T> onRelease = null, int prewarm = 0) {
        _onGet = onGet; _onRelease = onRelease;
        for (int i = 0; i < prewarm; i++) _pool.Push(new T());
    }
    public T Get() { var el = _pool.Count > 0 ? _pool.Pop() : new T(); el.style.display = DisplayStyle.Flex; _onGet?.Invoke(el); return el; }
    public void Release(T el) { el.style.display = DisplayStyle.None; _onRelease?.Invoke(el); _pool.Push(el); }
}
```

## GC-Free Patterns

```csharp
// Cache Q() calls
Label _scoreLabel;
void OnEnable() { _scoreLabel = root.Q<Label>("score"); }
void UpdateScore(int score) { _scoreLabel.text = score.ToString(); }

// Avoid boxing
element.style.width = new Length(100, LengthUnit.Pixel); // not: element.style.width = 100;

// Cache style values
static readonly StyleLength _width100 = new Length(100, LengthUnit.Percent);
static readonly StyleColor _colorRed = new StyleColor(Color.red);

// Method references over lambdas
button.RegisterCallback<ClickEvent>(OnClick); // not: evt => OnClick(evt)
```

## Profiling Workflow

1. **Profiler > UI Details** module
2. Watch markers:

| Marker | Target | Action |
|--------|--------|--------|
| `UIR.Layout` | < 0.5ms | Flatten hierarchy, reduce layout changes |
| `UIR.RenderChainUpdate` | < 0.3ms | Reduce dirty elements |
| `UIR.TextRegen` | < 0.2ms | Batch text updates |
| `UIR.DrawChain` | < 0.2ms | Atlas textures, fewer fonts |

3. **Frame Debugger** for draw call count. Compare against [Performance Benchmarks](references/performance-benchmarks.md).

## DC Performance Patterns

Cache `Camera.main` and Q<T>() results; transform (not layout) for positioning; USS transitions over async loops; `CancellationToken` on infinite async loops; `ListView` for 50+ items.

## Optimization Checklist

- [ ] Lists 20+ items → ListView with fixedItemHeight
- [ ] All animations use translate/rotate/scale/opacity only
- [ ] Animated elements have `UsageHints.DynamicTransform`
- [ ] Q() calls cached, not called per-frame
- [ ] Sprites in SpriteAtlas
- [ ] Max 2-3 fonts per screen
- [ ] Opacity on leaf elements, not containers
- [ ] Element pooling for transient UI

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Animating `width`/`height` | Use `translate`, `scale`, `opacity` |
| Q() in Update() | Cache in `OnEnable` |
| No `fixedItemHeight` on ListView | Always set it |
| `UsageHints` on static elements | Only on animated |
| String concat per frame | Update only on change |
| Opacity on containers | Apply to leaf elements |
| Nested `overflow: hidden` | Flatten hierarchy |


---

**← Previous**: [Patterns](../ui-toolkit-patterns/SKILL.md) | **Next →**: [Mobile](../ui-toolkit-mobile/SKILL.md)

---
name: ui-toolkit-performance
description: "Performance optimization for Unity UI Toolkit. Covers profiling, draw call optimization, transform vs layout animations, element pooling, ListView virtualization, memory management, and GC-free patterns. Use when: (1) UI frame rate is low, (2) Profiling UI draw calls or layout cost, (3) Optimizing list/grid rendering, (4) Reducing GC allocations in UI code, (5) Choosing animation strategies. Triggers: 'UI performance', 'draw calls', 'layout thrashing', 'UI profiling', 'element pool', 'UI memory', 'virtualization', 'UsageHints'."
---

# UI Toolkit Performance

Optimize UI Toolkit for 60fps. Target: 2-4 draw calls/screen, < 0.5ms layout cost.

## Key Rule

**Never trigger layout during animation. Use GPU transforms only.**

## Transform vs Layout

| Property | Layout Cost | Animation |
|----------|-------------|-----------|
| `translate`, `rotate`, `scale`, `opacity` | None | ✓ Use these |
| `width`, `height`, `margin`, `padding` | Full subtree | ✗ Never animate |

## Animation Example

```css
.slide { translate: 100% 0; opacity: 0; transition: 300ms; }
.slide--active { translate: 0 0; opacity: 1; }
```

```csharp
panel.ToggleInClassList("slide--active"); // GPU transform, no layout
```

## UsageHints

```csharp
element.usageHints = UsageHints.DynamicTransform; // animated only
```

## ListView Virtualization

```csharp
listView.fixedItemHeight = 72;
listView.makeItem = () => itemTemplate.Instantiate();
listView.bindItem = (el, idx) => el.Q<Label>("name").text = items[idx].Name;
```

Use for 20+ items. See [Performance Benchmarks](references/performance-benchmarks.md).

## Draw Call Optimization

| Issue | Fix |
|-------|-----|
| Multiple textures | SpriteAtlas |
| Multiple fonts | Limit to 2-3 |
| Nested clipping | Minimize |
| Container opacity < 1 | Apply to leaves |

## Element Pooling & GC Patterns

See [references/pooling-and-gc.md](references/pooling-and-gc.md) for code examples.

**Quick wins:**
- Cache Q<T>() in OnEnable
- Pool VisualElements
- Use explicit style types
- Use method refs, not lambdas
- Update values only on change

## Profiling

1. **Profiler > UI Details** module
2. Track: `UIR.Layout` < 0.5ms, `UIR.DrawChain` < 0.2ms
3. **Frame Debugger** for draw call count

## Optimization Checklist

- [ ] Lists 20+ → ListView
- [ ] Animations → translate/scale/opacity
- [ ] Animated elements → UsageHints.DynamicTransform
- [ ] Q() calls → cached
- [ ] Sprites → SpriteAtlas
- [ ] Fonts → 2-3 max
- [ ] Opacity → leaf elements
- [ ] Transient UI → pooled

## Common Pitfalls

See [references/common-pitfalls.md](references/common-pitfalls.md).

---

**← Patterns** | **Mobile →**

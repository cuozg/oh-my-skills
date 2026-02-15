# UI Toolkit Performance Benchmarks

Reference metrics, optimization targets, and profiling baselines for runtime UI Toolkit.

## Draw Call Targets

| Screen Complexity | Target | Acceptable | Poor |
|-------------------|--------|------------|------|
| Simple HUD | 1-2 | 3-4 | 5+ |
| Menu screen | 2-4 | 5-8 | 10+ |
| Complex (inventory grid) | 4-8 | 8-12 | 15+ |
| Full UI (multi-panel+overlay) | 6-12 | 12-20 | 25+ |

Draw call causes: different textures (+1/atlas → use SpriteAtlas), font change (+1/font → limit 2-3), clipping (+1-2/clip rect), custom render textures (+1), opacity<1 on container (+1 → apply to leaves).

## Layout vs Transform Performance

| Property | CPU Cost | Layout Recalc | Use For |
|----------|----------|---------------|---------|
| `translate/rotate/scale/opacity` | Minimal | None | All animations |
| `width/height/padding/margin/flex` | High | Full subtree | Avoid animating |
| `font-size` | Very High | Full subtree | Never animate |

```css
/* GOOD: GPU-accelerated slide */
.panel-enter { translate: 100% 0; opacity: 0; transition: translate 300ms ease-out, opacity 300ms; }
.panel-enter--active { translate: 0 0; opacity: 1; }
/* BAD: width animation triggers layout recalc every frame */
```

## ListView Virtualization

| Items | ScrollView (no virt.) | ListView (virt.) | Speedup |
|-------|----------------------|-----------------|---------|
| 50 | 50 elements, ~2ms | 8-12 elements, ~0.3ms | 6x |
| 200 | 200 elements, ~8ms | 8-12, ~0.3ms | 25x |
| 1000 | ~45ms | ~0.3ms | 150x |
| 5000 | Unusable (200ms+) | ~0.3ms | Viable |

```csharp
listView.fixedItemHeight = 72;  // MUST set for FixedHeight mode
listView.virtualizationMethod = CollectionVirtualizationMethod.FixedHeight;
```

## Memory Profiles

| Component | Allocation | Notes |
|-----------|-----------|-------|
| VisualElement | ~200-400B | Style complexity dependent |
| Label / Button | ~500-700B / ~800-1.2KB | Text mesh / clickable+hover |
| ListView 100 items (virt.) | ~15-25KB | Only visible allocated |
| ScrollView 100 items | ~80-120KB | All allocated |
| Full screen | ~50-200KB | Element count dependent |

## GC Allocation Hotspots

| Operation | GC | Fix |
|-----------|-----|-----|
| `Q("name")` per frame | ~40B | Cache result |
| `style.color = c` per frame | ~24B (boxing) | `StyleColor` struct |
| String concat in labels | Varies | `StringBuilder` / `string.Create` |
| Lambda in `RegisterCallback` | ~64-128B | Method reference |
| `Children()` in loop | ~40B | Cache `childCount`, index |

```csharp
// Zero-alloc pattern: cache Q() in OnEnable, pre-cache string values
Label _scoreLabel;
void OnEnable() => _scoreLabel = root.Q<Label>("score");
void UpdateScore(int s) => _scoreLabel.text = _cachedStrings[s]; // pre-built array
```

## UsageHints

| Hint | When to Use |
|------|-------------|
| `DynamicTransform` | Animated elements (translate/rotate/scale) |
| `GroupTransform` | Container of animated children |
| `DynamicColor` | Elements with color/opacity transitions |
| `MaskContainer` | Containers with overflow: hidden |

## Profiler Markers

| Marker | Target |
|--------|--------|
| `UIR.Layout` | < 0.5ms |
| `UIR.TransformUpdate` | < 0.1ms |
| `UIR.RenderChainUpdate` | < 0.3ms |
| `UIR.DrawChain` | < 0.2ms |
| `UIR.TextRegen` | < 0.2ms |
| `UIElements.BindingsUpdate` | < 0.1ms |

Profiler: Window > Analysis > Profiler > **UI Details** module. Watch `UIR.Layout` spikes (layout thrashing), `UIR.RenderChainUpdate` (dirty elements), `UIR.TextRegen` (frequent text changes).

## Dragon Crashers Production Metrics

| Technique | Impact |
|-----------|--------|
| ListView virtualization | 95% fewer visual tree elements |
| USS class toggling | Avoids layout recalculation |
| Transform animations | GPU-accelerated, no layout cost |
| `DynamicTransform` hint | Batching optimization |
| Element pooling | Reduces GC |

Metrics: tree depth 8-12, elements/screen 50-200, draw calls 4-8, memory ~2-4MB, startup <100ms mid-range mobile.

## Optimization Checklist

- [ ] Lists 20+ items → `ListView` with virtualization
- [ ] Animations: `translate/rotate/scale/opacity` only
- [ ] Animated elements: `UsageHints.DynamicTransform`
- [ ] `Q()`/`Q<T>()` cached, never per-frame
- [ ] No string concat in per-frame updates
- [ ] Max 2-3 fonts; sprites in atlases
- [ ] Minimize nested `overflow: hidden`
- [ ] Opacity on leaf elements, not containers

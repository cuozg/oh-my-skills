# UI Toolkit Performance Benchmarks

Reference metrics, optimization targets, and profiling baselines for runtime UI Toolkit.

## Draw Call Targets

| Screen Complexity | Target Draw Calls | Acceptable | Poor |
|-------------------|-------------------|------------|------|
| Simple HUD (health, score) | 1-2 | 3-4 | 5+ |
| Menu screen (buttons, text) | 2-4 | 5-8 | 10+ |
| Complex screen (inventory grid) | 4-8 | 8-12 | 15+ |
| Full UI (multiple panels + overlay) | 6-12 | 12-20 | 25+ |

### How Draw Calls Increase

| Cause | Draw Call Cost | Mitigation |
|-------|---------------|------------|
| Different textures (sprites) | +1 per atlas | Use texture atlases, SpriteAtlas |
| Font change | +1 per font | Limit to 2-3 fonts max |
| Clipping (overflow: hidden) | +1-2 per clip rect | Minimize nested clipping |
| Custom render textures | +1 each | Use sparingly |
| Opacity < 1 on container | +1 (separate batch) | Apply opacity to leaf elements |

## Layout vs Transform Performance

| Animation Type | CPU Cost | GPU Cost | Layout Recalc | Use For |
|----------------|----------|----------|---------------|---------|
| `translate` | Minimal | Low | None | Position animations, slides |
| `rotate` | Minimal | Low | None | Spin, flip effects |
| `scale` | Minimal | Low | None | Pulse, grow/shrink |
| `opacity` | Minimal | Low | None | Fade in/out |
| `width/height` | High | Low | Full subtree | Avoid for animation |
| `padding/margin` | High | Low | Full subtree | Avoid for animation |
| `flex-grow/shrink` | High | Low | Full subtree | Avoid for animation |
| `font-size` | Very High | Medium | Full subtree | Never animate |

### Transform Animation Example (Recommended)

```css
/* Slide in from right — GPU-accelerated, zero layout cost */
.panel-enter {
    translate: 100% 0;
    opacity: 0;
    transition-property: translate, opacity;
    transition-duration: 300ms;
    transition-timing-function: ease-out;
}

.panel-enter--active {
    translate: 0 0;
    opacity: 1;
}
```

### Layout Animation Example (Avoid)

```css
/* DON'T: Animating width triggers expensive layout recalculation */
.panel-bad {
    width: 0;
    transition-property: width;
    transition-duration: 300ms;
}

.panel-bad--open {
    width: 300px; /* Forces entire subtree layout recalc every frame */
}
```

## ListView Virtualization Benchmarks

| Item Count | ScrollView (no virtualization) | ListView (virtualized) | Improvement |
|------------|-------------------------------|----------------------|-------------|
| 50 items | 50 elements, ~2ms layout | 8-12 elements, ~0.3ms | 6x faster |
| 200 items | 200 elements, ~8ms layout | 8-12 elements, ~0.3ms | 25x faster |
| 1000 items | 1000 elements, ~45ms layout | 8-12 elements, ~0.3ms | 150x faster |
| 5000 items | Unusable (~200ms+) | 8-12 elements, ~0.3ms | Viable |

**Key settings for optimal virtualization:**

```csharp
listView.fixedItemHeight = 72;  // MUST set for FixedHeight mode
listView.virtualizationMethod = CollectionVirtualizationMethod.FixedHeight;
```

## Memory Profiles

| Component | Typical Allocation | Notes |
|-----------|-------------------|-------|
| VisualElement (base) | ~200-400 bytes | Depends on style complexity |
| Label | ~500-700 bytes | Includes text mesh data |
| Button | ~800-1200 bytes | Label + clickable + hover state |
| ListView (100 items, virtualized) | ~15-25 KB | Only visible items allocated |
| ScrollView (100 items, NOT virtualized) | ~80-120 KB | All items allocated |
| Full screen (moderate complexity) | ~50-200 KB | Depends on element count |
| Theme Style Sheet (loaded) | ~10-30 KB | Shared across panels |

## GC Allocation Hotspots

| Operation | GC Allocation | Fix |
|-----------|--------------|-----|
| `VisualElement.Q("name")` each frame | ~40 bytes per call | Cache the result |
| `element.style.color = newColor` each frame | ~24 bytes (boxing) | Use `StyleColor` struct |
| String concatenation in labels | Varies | Use `StringBuilder` or `string.Create` |
| Lambda in `RegisterCallback` | ~64-128 bytes | Use method reference |
| `element.Children()` in loop | ~40 bytes (enumerator) | Cache `childCount`, use index |
| Creating new `Length()` each frame | ~16 bytes | Cache `Length` values |

### Zero-Alloc Patterns

```csharp
// BAD: Allocates every frame
void Update()
{
    var label = root.Q<Label>("score");     // GC: Q allocation
    label.text = "Score: " + score;          // GC: string concat
}

// GOOD: Zero allocation
Label _scoreLabel;
readonly string[] _scoreCache = new string[10000]; // Pre-cache common values

void OnEnable()
{
    _scoreLabel = root.Q<Label>("score");   // Cache once
    for (int i = 0; i < _scoreCache.Length; i++)
        _scoreCache[i] = $"Score: {i}";
}

void UpdateScore(int score)
{
    if (score < _scoreCache.Length)
        _scoreLabel.text = _scoreCache[score];  // Zero alloc
    else
        _scoreLabel.text = $"Score: {score}";   // Rare path, acceptable
}
```

## UsageHints Impact

| Hint | What It Does | When to Use |
|------|-------------|-------------|
| `DynamicTransform` | Marks element for frequent transform changes | Animated elements (translate, rotate, scale) |
| `GroupTransform` | Groups children into single transform | Container of animated children |
| `DynamicColor` | Marks element for frequent color/opacity changes | Elements with color transitions |
| `MaskContainer` | Optimizes masking/clipping | Containers with overflow: hidden |

```csharp
// Apply usage hints for animated panel
var panel = root.Q("animated-panel");
panel.usageHints = UsageHints.DynamicTransform;

// Group hint for container of moving elements
var container = root.Q("particle-container");
container.usageHints = UsageHints.GroupTransform;
```

## Profiler Markers to Watch

| Marker | What It Measures | Target |
|--------|-----------------|--------|
| `UIR.Layout` | Yoga layout calculation | < 0.5ms |
| `UIR.TransformUpdate` | Transform matrix updates | < 0.1ms |
| `UIR.RenderChainUpdate` | Render data rebuild | < 0.3ms |
| `UIR.DrawChain` | GPU draw submission | < 0.2ms |
| `UIR.TextRegen` | Text mesh regeneration | < 0.2ms |
| `UIElements.BindingsUpdate` | Data binding updates | < 0.1ms |

### Reading the UI Profiler Module

1. Open **Window > Analysis > Profiler**
2. Select **UI Details** module
3. Look for spikes in `UIR.Layout` — indicates layout thrashing
4. Check `UIR.RenderChainUpdate` — high values mean too many dirty elements
5. Watch `UIR.TextRegen` — frequent text changes trigger expensive re-renders

## Dragon Crashers — Production Metrics

> Source: Unity's official Dragon Crashers sample (idle RPG, full UI Toolkit).

### Optimization Techniques Used

| Technique | Where Applied | Impact |
|-----------|--------------|--------|
| `ListView` virtualization | Inventory, Mail | 95% fewer elements in visual tree |
| USS class toggling (not layout changes) | Tab switching, states | Avoids layout recalculation |
| Transform animations | Screen transitions | GPU-accelerated, no layout cost |
| `usageHints: DynamicTransform` | Animated elements | Batching hint for renderer |
| Element pooling | Notification toasts | Reduces GC pressure |
| Minimal overdraw | Layered backgrounds | Fewer draw calls |

### Real-World Metrics (Approximate)

| Metric | Value |
|--------|-------|
| Visual tree depth | 8–12 levels typical for complex screens |
| Elements per screen | 50–200 depending on content |
| Draw calls | 4–8 per screen with proper batching |
| Memory | ~2–4 MB for full UI hierarchy |
| Startup | UI initialization < 100ms on mid-range mobile |

---

## Optimization Checklist

- [ ] All lists with 20+ items use `ListView` with virtualization
- [ ] Animations use `translate/rotate/scale/opacity` only (never `width/height/margin/padding`)
- [ ] Animated elements have `usageHints = UsageHints.DynamicTransform`
- [ ] `Q()` / `Q<T>()` calls cached, not called per-frame
- [ ] No string concatenation in per-frame label updates
- [ ] Maximum 2-3 fonts loaded
- [ ] Sprites in atlases (not individual textures)
- [ ] Minimize nested `overflow: hidden` (each adds clip rect)
- [ ] Opacity applied to leaf elements, not containers
- [ ] No layout property changes during transitions

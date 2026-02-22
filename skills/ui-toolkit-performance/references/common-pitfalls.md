# UI Performance Common Pitfalls

Quick reference for frequently encountered performance issues and fixes.

## Animation Mistakes

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Animating `width`/`height` | Full subtree layout recalc every frame (~10ms) | Use `translate`, `scale`, `opacity` (GPU transform) |
| Animating `margin` or `padding` | Triggers layout on siblings | Apply to element itself, use translate for offset |
| No `UsageHints` on animations | GPU readbacks, unnecessary overhead | Set `UsageHints.DynamicTransform` |

## ListView Mistakes

| Pitfall | Problem | Fix |
|---------|---------|-----|
| No `fixedItemHeight` | Measurement pass on every layout | Always set `listView.fixedItemHeight = 72;` |
| Using ScrollView for 20+ items | Manual pooling, memory explosion | Switch to ListView with virtualization |
| Not unbinding in `unbindItem` | Event subscriptions leak | Implement unbindItem cleanup |

## Caching & Updates

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Q() called every frame | Selector overhead repeated | Cache in OnEnable: `_btn = root.Q<Button>("id")` |
| String concat every frame | Allocation per update | Update only on data change; use ToString caching |
| Opacity on container elements | Compositing cost on all children | Apply opacity to leaf elements only |

## Draw Call Issues

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Sprites not in atlas | Different textures per element → batching broken | Use SpriteAtlas for all UI sprites |
| More than 3 fonts per screen | Font texture swaps | Limit to 2-3 maximum |
| Nested `overflow: hidden` | Compositing layers compound | Minimize clipping nesting depth |

## Memory & GC

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Lambdas in RegisterCallback | Closure allocation per registration | Use method reference: `RegisterCallback(OnClick)` |
| Boxing style values | Hidden allocation per assignment | Use explicit types: `new Length(100, LengthUnit.Pixel)` |
| No element pooling | Instantiate/Destroy every update | Create pool, reuse via Get/Release |

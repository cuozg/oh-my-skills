# Common UI Toolkit Mistakes & Fixes

Quick reference for frequently encountered issues and their resolutions.

## Styling & Markup

| Mistake | Problem | Fix |
|---------|---------|-----|
| Inline styles in UXML | Layout defined in wrong layer | Use USS classes instead; UXML is structure only |
| Q() every frame | Constant selector overhead | Cache reference in OnEnable: `cachedBtn = root.Q<Button>("id")` |
| Animating width/height | Expensive layout recalculation every frame | Use `translate`, `scale`, `opacity` (GPU transform only) |

## Layout & Performance

| Mistake | Problem | Fix |
|---------|---------|-----|
| ScrollView for 100+ items | Layout thrashing, memory explosion | Use ListView with virtualization |
| Ignoring safe area | Content hidden on notched devices | Use SafeAreaHandler or extend UI bounds |
| No UsageHints on animations | GPU thrashing, unnecessary readbacks | Add `UsageHints.DynamicTransform` to animated elements |
| Deep element nesting (20+ levels) | Layout cost compounds | Flatten hierarchy; use class-based styling |

## Data Flow

| Mistake | Problem | Fix |
|---------|---------|-----|
| Event spam without debounce | Callbacks fired every single frame | Add throttle/debounce to input handlers |
| Binding directly to mutable collections | Changes not reflected in UI | Use INotifyCollectionChanged or refresh binding manually |

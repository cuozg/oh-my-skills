# Performance Optimization

Rebuild profiling, RepaintBoundary, Impeller, memory management, and frame budget.

## Frame Budget

- **60 FPS** = 16.67ms per frame (target for most apps)
- **120 FPS** = 8.33ms per frame (high refresh rate devices)
- Build phase + layout + paint must all fit within budget

## Minimize Rebuilds

```dart
// 1. Use const constructors — skips rebuild entirely
const SizedBox(height: 16); // ✅ Never rebuilds
SizedBox(height: spacing);   // ❌ Rebuilds every frame

// 2. Extract widgets into classes (not methods)
// Widget classes only rebuild when their inputs change
class PriceTag extends StatelessWidget {
  const PriceTag({super.key, required this.price});
  final double price;
  @override
  Widget build(BuildContext context) => Text('\$$price');
}

// 3. Use select() in Riverpod to watch specific fields
final name = ref.watch(userProvider.select((u) => u.name));
// Only rebuilds when name changes, not when other user fields change
```

## RepaintBoundary

Isolate expensive paint operations so they don't repaint the entire subtree:

```dart
RepaintBoundary(
  child: CustomPaint(
    painter: ChartPainter(data), // Only repaints this subtree
  ),
)
```

Use when: animations, custom painters, complex shadows, blurs.

## ListView Performance

```dart
// GOOD: ListView.builder — lazy, builds only visible items
ListView.builder(
  itemCount: items.length,
  itemBuilder: (_, i) => ItemTile(key: ValueKey(items[i].id), item: items[i]),
);

// BAD: Column + map — builds ALL items upfront
Column(children: items.map((i) => ItemTile(item: i)).toList());

// For heterogeneous lists: ListView.separated or CustomScrollView + Slivers
```

## Image Optimization

- **Resize before loading**: `cacheWidth` / `cacheHeight` params in `Image`
- **Use `precacheImage()`** for critical above-the-fold images
- **Prefer SVG** for icons — vector scales without memory cost

```dart
Image.asset('assets/hero.png', cacheWidth: 400); // Decode at 400px, not full res
```

## DevTools Performance Tab

1. **Timeline**: Identify frames exceeding 16ms budget
2. **Widget Rebuild Tracker**: Find widgets rebuilding unnecessarily
3. **Memory Tab**: Check for retained objects and growing allocations

```dart
// Debug rebuild counts (dev only)
debugPrintRebuildDirtyWidgets = true;
```

## Common Performance Pitfalls

| Pitfall | Fix |
|---------|-----|
| `MediaQuery.of(context)` in deep widgets | Use `MediaQuery.sizeOf(context)` |
| Building all list items upfront | Use `ListView.builder` |
| Rebuilding on unrelated state changes | Use `ref.watch(provider.select(...))` |
| Full-resolution image decoding | Set `cacheWidth` / `cacheHeight` |
| Expensive `build()` methods | Extract const sub-widgets |
| Animating without RepaintBoundary | Wrap animated subtrees |

## Key Rules

- **Profile first** — never optimize without DevTools evidence
- **`const` everything** — cheapest optimization, biggest impact
- **Lazy build** — use `.builder` constructors for lists and grids
- **Select narrowly** — `ref.watch(provider.select(...))` over full provider watch

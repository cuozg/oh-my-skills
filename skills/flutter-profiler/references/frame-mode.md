# Frame Mode — Rendering & Jank Analysis

Analyze frame rate drops, jank, GPU vs CPU bottlenecks, and shader compilation issues.

## Jank Detection

Jank = any frame exceeding the budget. Two flavors:
- **UI jank** — build/layout phase too slow (CPU-bound)
- **Raster jank** — paint/compositing too slow (GPU-bound)

DevTools Performance tab shows both UI and Raster threads separately.

## GPU vs CPU Bottleneck

| Symptom | Bottleneck | Action |
|---------|-----------|--------|
| UI thread (blue) exceeds budget | CPU | Optimize `build()`, reduce rebuilds, offload to isolate |
| Raster thread (green) exceeds budget | GPU | Reduce overdraw, add `RepaintBoundary`, simplify painting |
| Both exceed budget | Combined | Profile each independently, fix worst first |

## Shader Compilation Jank

First-time shader compilation causes one-time frame spikes (especially on iOS):

```bash
# Warm up shaders for Impeller (Flutter 3.16+)
flutter run --profile --cache-sksl
# Export captured shaders
flutter build ios --bundle-sksl-path flutter_01.sksl.json
```

Impeller (default on iOS, opt-in Android) pre-compiles shaders — eliminates runtime shader jank.

## Overdraw Analysis

1. Enable **Performance Overlay**: `MaterialApp(showPerformanceOverlay: true)`
2. Check DevTools "Highlight Repaints" toggle — frequent repaints without user interaction = problem

## Common Rendering Anti-Patterns

| Pattern | Impact | Fix |
|---------|--------|-----|
| `ClipRRect` / `ClipPath` on large subtrees | GPU overdraw | Use `borderRadius` on `Container` instead |
| `Opacity` widget wrapping subtree | Full repaint per frame | Use `AnimatedOpacity` or widget-level opacity |
| `saveLayer` (implicit from clips/opacity) | GPU memory spike | Minimize clipping regions |
| Unbounded `CustomPaint` without `RepaintBoundary` | Repaints entire tree | Wrap in `RepaintBoundary` |
| Missing keys on animated list items | Unnecessary rebuilds | Add `ValueKey` to list items |

## Widget Rebuild Tracking

```dart
// In debug/profile mode: log which widgets rebuild
debugPrintRebuildDirtyWidgets = true;

// Targeted: override debugFillProperties in suspect widget
@override
void debugFillProperties(DiagnosticPropertiesBuilder properties) {
  super.debugFillProperties(properties);
  properties.add(IntProperty('rebuildCount', _rebuildCount));
}
```

## Impeller Diagnostics

Impeller (Flutter's new renderer) has different performance characteristics:
- No runtime shader compilation (eliminates shader jank)
- Different GPU memory patterns — watch for texture atlas pressure
- Profile with `flutter run --profile --enable-impeller` on Android

# CPU Mode — Frame & Function Analysis

Identify slow frames and trace them to specific functions in the codebase.

## Frame Budget Reference

| Target | Budget | Thermal (Mobile) |
|--------|--------|-------------------|
| 60 fps | 16.67ms | 11.67ms (0.7x) |
| 120 fps | 8.33ms | 5.83ms (0.7x) |

## DevTools Timeline Analysis

1. Open **Performance** tab in DevTools (`flutter run --profile`)
2. Record a session covering the slow interaction
3. Identify frames exceeding budget (red/orange bars)
4. Drill into the flame chart to find the longest functions

## Common CPU Bottlenecks

| Pattern | Impact | Fix |
|---------|--------|-----|
| `build()` doing computation | Blocks UI thread | Move to `initState`, provider, or isolate |
| Synchronous JSON parsing | Freezes frame | Use `compute()` or `Isolate.run()` |
| Expensive `itemBuilder` | Slow scroll | Cache widgets, use `const`, extract classes |
| Layout thrashing (nested intrinsics) | O(2^n) layout | Replace `IntrinsicWidth/Height` with `ConstrainedBox` |
| Unthrottled `setState` | Excessive rebuilds | Debounce, use `ValueNotifier`, or `ref.watch(select)` |

## Codebase Scan Targets

Grep for these anti-patterns in hot paths (widgets rebuilt per frame):

- `setState(() {` inside `StreamSubscription` callbacks without debounce
- `MediaQuery.of(context)` — use `MediaQuery.sizeOf(context)` instead
- Missing `const` on stateless widget constructors
- `toList()` / `map()` chains in `build()` creating new lists every frame
- `Future` or async work inside `build()` methods

## Isolate Offloading

For functions taking > 5ms, consider offloading:

```dart
// Heavy computation off main thread
final result = await Isolate.run(() => parseJsonData(rawData));
```

Use `Isolate.run()` (Dart 2.19+) for one-shot work; `compute()` for Flutter-specific tasks.

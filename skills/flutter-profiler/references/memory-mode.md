# Memory Mode — GC Pressure & Leak Detection

Analyze heap usage, garbage collection spikes, and memory leaks.

## DevTools Memory Tab

1. Open **Memory** tab in DevTools (`flutter run --profile`)
2. **Heap snapshot**: Capture before and after a suspected leak — compare retained sizes
3. **Allocation tracking**: Enable to see which classes allocate most
4. **GC timeline**: Watch for frequent GC pauses (visible as blue bars)

## Leak Detection Strategy

1. Navigate to suspect screen → snapshot heap
2. Navigate away (pop route) → force GC → snapshot again
3. Compare: objects from step 1 still retained = leak
4. Check retaining paths to find the root reference

## Common Memory Anti-Patterns

| Pattern | Impact | Fix |
|---------|--------|-----|
| Unclosed `StreamSubscription` | Retains widget tree | Cancel in `dispose()` or use `ref.onDispose()` |
| `addListener` without `removeListener` | Listener leak | Pair in `initState`/`dispose` |
| Static/global caches without eviction | Unbounded growth | Use `Cache` with max size or LRU policy |
| Closures capturing `BuildContext` | Retains element tree | Capture values, not context |
| Large image without `cacheWidth/Height` | Decodes full resolution | Set `cacheWidth` on `Image` widget |
| Unreleased `AnimationController` | Ticker leak | Call `.dispose()` in `State.dispose()` |

## GC Pressure Indicators

- **Frequent minor GCs** (> 2/sec) — too many short-lived allocations
- **Major GC pauses** (> 5ms) — large retained heap
- **Sawtooth pattern** — rapid alloc/dealloc cycle; check for per-frame object creation

## Codebase Scan Targets

Grep for:
- `StreamController` without matching `.close()` in `dispose()`
- `addListener(` without corresponding `removeListener(`
- `AnimationController(` without `.dispose()` in same class
- `TextEditingController(` without `.dispose()`
- `Timer.periodic(` without `.cancel()` in `dispose()`

## Profiling Heap Programmatically

```dart
import 'dart:developer';
// Trigger GC and log heap stats (profile/debug only)
assert(() {
  final info = ProcessInfo();
  debugPrint('RSS: ${info.currentRss ~/ 1024}KB');
  return true;
}());
```

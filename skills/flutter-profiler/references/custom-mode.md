# Custom Mode — Profiling Instrumentation

Generate profiling snippets: timeline events, timed sections, and DevTools configuration.

## Timeline Events (dart:developer)

Add custom markers visible in DevTools Performance tab:

```dart
import 'dart:developer';

Future<void> loadDashboard() async {
  Timeline.startSync('loadDashboard');
  try {
    final data = await fetchData();
    processData(data);
  } finally {
    Timeline.finishSync();
  }
}
```

## Timed Sections with Stopwatch

For measuring specific code paths without DevTools:

```dart
final sw = Stopwatch()..start();
await expensiveOperation();
sw.stop();
debugPrint('expensiveOperation: ${sw.elapsedMilliseconds}ms');
```

## Performance Tracking Service

Reusable pattern for tracking metrics across the app:

```dart
class PerfTracker {
  static final _timings = <String, List<int>>{};

  static T track<T>(String label, T Function() action) {
    final sw = Stopwatch()..start();
    final result = action();
    sw.stop();
    (_timings[label] ??= []).add(sw.elapsedMilliseconds);
    assert(() {
      if (sw.elapsedMilliseconds > 16) {
        debugPrint('SLOW [$label]: ${sw.elapsedMilliseconds}ms');
      }
      return true;
    }());
    return result;
  }

  static Map<String, double> averages() =>
      _timings.map((k, v) => MapEntry(k, v.average));
}
```

## Widget Rebuild Counter

Track rebuild frequency for specific widgets:

```dart
class _MyWidgetState extends State<MyWidget> {
  int _buildCount = 0;

  @override
  Widget build(BuildContext context) {
    assert(() { debugPrint('MyWidget build #${++_buildCount}'); return true; }());
    return /* ... */;
  }
}
```

## DevTools Configuration

```bash
# Launch with profile mode (accurate timings)
flutter run --profile

# Enable Impeller on Android for rendering comparison
flutter run --profile --enable-impeller

# Capture startup trace
flutter run --profile --trace-startup

# Export timeline to Chrome tracing format
flutter run --profile --trace-to-file=timeline.json
```

## When to Use Each Tool

| Need | Tool |
|------|------|
| Visualize function timing | `Timeline.startSync` / `finishSync` |
| Measure wall-clock time | `Stopwatch` |
| Track rebuild frequency | Debug counter in `build()` |
| Startup performance | `--trace-startup` flag |
| Export for offline analysis | `--trace-to-file` flag |

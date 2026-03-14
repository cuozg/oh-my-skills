# Debug & Logging

Structured logging, DevTools, crash reporting, and PlatformDispatcher error handling.

## package:logger (Recommended)

```dart
import 'package:logger/logger.dart';

final log = Logger(
  printer: PrettyPrinter(
    methodCount: 0,
    errorMethodCount: 5,
    lineLength: 80,
    colors: true,
  ),
);

// Usage
log.d('User logged in: ${user.id}');         // Debug
log.i('Payment processed: \$${amount}');      // Info
log.w('Retry attempt $attempt of $max');      // Warning
log.e('Login failed', error: e, stackTrace: st); // Error
```

## Global Error Capture

```dart
void main() {
  // Flutter framework errors (widget build, layout, paint)
  FlutterError.onError = (details) {
    log.e('Flutter error', error: details.exception, stackTrace: details.stack);
    // Forward to Crashlytics in production
  };

  // Async errors outside Flutter framework
  PlatformDispatcher.instance.onError = (error, stack) {
    log.e('Platform error', error: error, stackTrace: stack);
    return true; // Mark as handled
  };

  runApp(const ProviderScope(child: MyApp()));
}
```

## Flutter DevTools

| Tab | Use For |
|-----|---------|
| **Widget Inspector** | Widget tree, layout, constraints debugging |
| **Performance** | Frame timing, jank detection, rebuild tracking |
| **Memory** | Heap snapshots, allocation tracking, leak detection |
| **Network** | HTTP request/response inspection (with Dio logging) |
| **Logging** | Structured log output with filtering |

Launch: `flutter run` → press `d` or `dart devtools` in terminal.

## Debug Flags (Dev Only)

```dart
assert(() {
  debugPaintSizeEnabled = false;        // Layout bounds
  debugPrintRebuildDirtyWidgets = false; // Rebuild logging
  return true;
}());
```

## Dio Request Logging

```dart
final dio = Dio()
  ..interceptors.add(LogInterceptor(
    request: true,
    requestBody: true,
    responseBody: true,
    error: true,
    logPrint: (msg) => log.d(msg.toString()),
  ));
```

## Crash Reporting (Production)

```dart
// Firebase Crashlytics setup
FirebaseCrashlytics.instance.setCrashlyticsCollectionEnabled(!kDebugMode);

FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterFatalError;
PlatformDispatcher.instance.onError = (error, stack) {
  FirebaseCrashlytics.instance.recordError(error, stack, fatal: true);
  return true;
};
```

## Key Rules

- **Never** use `print()` — use `package:logger` for structured, filterable output
- **Always** set up `FlutterError.onError` + `PlatformDispatcher.instance.onError`
- **Strip debug flags** from release builds (use `assert()` wrapper)
- **Log at boundaries** — service entry/exit, API calls, state transitions

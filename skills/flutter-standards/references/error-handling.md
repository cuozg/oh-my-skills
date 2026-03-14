# Error Handling

Exception hierarchies, Result pattern, user-facing recovery, and crash reporting.

## Exception Hierarchy

```dart
// Base app exception
sealed class AppException implements Exception {
  final String message;
  final String? code;
  const AppException(this.message, {this.code});
}

// Domain-specific exceptions
class NetworkException extends AppException {
  final int? statusCode;
  const NetworkException(super.message, {this.statusCode, super.code});

  factory NetworkException.fromDio(DioException e) => switch (e.type) {
    DioExceptionType.connectionTimeout => const NetworkException('Connection timed out', code: 'TIMEOUT'),
    DioExceptionType.receiveTimeout => const NetworkException('Server took too long', code: 'TIMEOUT'),
    _ => NetworkException(e.message ?? 'Network error', statusCode: e.response?.statusCode),
  };
}

class AuthException extends AppException {
  const AuthException(super.message, {super.code});
}

class ValidationException extends AppException {
  final Map<String, String> fieldErrors;
  const ValidationException(super.message, {this.fieldErrors = const {}, super.code});
}
```

## Result Pattern

```dart
// Lightweight sealed Result
sealed class Result<T> {
  const Result();
}
class Success<T> extends Result<T> {
  final T value;
  const Success(this.value);
}
class Failure<T> extends Result<T> {
  final AppException error;
  const Failure(this.error);
}
```

## Global Error Handling

```dart
void main() {
  // Catch Flutter framework errors
  FlutterError.onError = (details) {
    FlutterError.presentError(details);
    _reportCrash(details.exception, details.stack);
  };

  PlatformDispatcher.instance.onError = (error, stack) {
    _reportCrash(error, stack);
    return true; // Handled
  };

  runApp(const ProviderScope(child: MyApp()));
}
```

## User-Facing Error Recovery

```dart
productsAsync.when(
  data: (products) => ProductList(products),
  loading: () => const LoadingIndicator(),
  error: (error, _) => ErrorView(
    message: _userMessage(error),
    onRetry: () => ref.invalidate(productListProvider),
  ),
);

String _userMessage(Object error) => switch (error) {
  NetworkException(code: 'TIMEOUT') => 'Connection timed out. Check your internet.',
  NetworkException() => 'Something went wrong. Please try again.',
  ValidationException(:final message) => message,
  _ => 'An unexpected error occurred.',
};
```

## Key Rules

- **Use sealed classes** for exception hierarchies — exhaustive switch
- **Never** catch `Exception` or `Object` without rethrowing — be specific
- **Always** provide retry actions for recoverable errors
- **Map exceptions to user-friendly messages** at the presentation layer
- **Report crashes** via Firebase Crashlytics or Sentry in production

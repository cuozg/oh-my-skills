# Async & Streams

Future, Stream, StreamController, and error propagation patterns for Flutter/Dart.

## Future Basics

```dart
// Prefer async/await over .then() chains
Future<User> fetchUser(String id) async {
  final response = await _api.get('/users/$id');
  return User.fromJson(response.data);
}

// Parallel execution
final results = await Future.wait([
  fetchUser('1'),
  fetchProducts(),
  fetchSettings(),
]);

// Timeout
final user = await fetchUser('1').timeout(
  const Duration(seconds: 10),
  onTimeout: () => throw TimeoutException('User fetch timed out'),
);
```

## Stream Patterns

```dart
// StreamController for custom streams
class ConnectionMonitor {
  final _controller = StreamController<ConnectionStatus>.broadcast();
  Stream<ConnectionStatus> get status => _controller.stream;

  void _onStatusChange(ConnectionStatus s) => _controller.add(s);

  void dispose() => _controller.close(); // Always close!
}
```

## Stream Transformations

```dart
// Debounce search input
searchStream
    .debounceTime(const Duration(milliseconds: 300))
    .distinct()
    .switchMap((query) => Stream.fromFuture(searchApi(query)))
    .listen((results) => setState(() => _results = results));

// Map + where
final activeUsers = userStream
    .where((user) => user.isActive)
    .map((user) => user.displayName);
```

## Error Handling in Async

```dart
// AsyncValue.guard (Riverpod) — cleanest pattern
state = await AsyncValue.guard(() async {
  return await repository.fetchData();
});

// Try-catch with specific exceptions
Future<User> login(String email, String pass) async {
  try {
    return await _api.post('/login', {'email': email, 'password': pass});
  } on DioException catch (e) {
    throw AuthException.fromDio(e);
  } on FormatException {
    throw const AuthException('Invalid server response');
  }
}
```

## Cancellation

```dart
// In Riverpod: ref.onDispose handles cancellation
@riverpod
Future<Data> myData(Ref ref) async {
  final cancelToken = CancelToken();
  ref.onDispose(cancelToken.cancel);
  return api.fetch('/data', cancelToken: cancelToken);
}
```

## Key Rules

- **Always** close StreamControllers in `dispose()`
- **Prefer** `async/await` over `.then()` chains
- **Use** `AsyncValue.guard()` in Riverpod notifiers for clean error handling
- **Never** swallow errors silently — rethrow or convert to domain exceptions
- **Use** `CancelToken` (Dio) or `CancelableOperation` for cancellable requests

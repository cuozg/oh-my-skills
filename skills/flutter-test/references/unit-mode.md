# Unit Mode — Provider, Service, Repository, Logic Tests

Pure Dart tests. No widget rendering. Fast, isolated, deterministic.

## Provider Testing

```dart
test('notifier increments', () {
  final container = ProviderContainer();
  addTearDown(container.dispose);
  container.read(counterProvider.notifier).increment();
  expect(container.read(counterProvider), 1);
});

test('with overrides', () {
  final container = ProviderContainer(overrides: [
    authRepoProvider.overrideWithValue(MockAuthRepository()),
  ]);
  addTearDown(container.dispose);
  expect(container.read(userProvider), isNotNull);
});
```

## Service / Repository Testing

```dart
class MockApiClient extends Mock implements ApiClient {}
late MockApiClient mockApi;
late AuthRepository sut;
setUp(() { mockApi = MockApiClient(); sut = AuthRepositoryImpl(mockApi); });

test('returns User on success', () async {
  when(() => mockApi.post(any(), data: any(named: 'data')))
      .thenAnswer((_) async => Response(data: userJson, statusCode: 200));
  final user = await sut.login('a@b.com', 'pass');
  expect(user.email, 'a@b.com');
  verify(() => mockApi.post('/auth/login', data: any(named: 'data'))).called(1);
});
```

## Async Patterns

- `expectLater(future, throwsA(isA<NotFoundException>()))` — async errors
- `await expectLater(stream, emitsInOrder([1, 2, 3]))` — streams
- `fakeAsync((async) { async.elapse(Duration(seconds: 5)); })` — time

## 10+ Test Cases Per Class

1. Happy path  2. Empty input  3. Null handling  4. Boundary values  5. Error paths
6. State transitions  7. Duplicate ops  8. Concurrent calls  9. Teardown  10. Edge combos

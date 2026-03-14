# Testing Patterns

Unit, widget, golden, and integration test patterns. AAA (Arrange-Act-Assert) throughout.

## Test File Structure

```
test/
├── features/
│   ├── auth/
│   │   ├── data/
│   │   │   └── auth_repository_test.dart
│   │   └── providers/
│   │       └── auth_provider_test.dart
│   └── home/
├── shared/
│   └── widgets/
│       └── error_view_test.dart
└── helpers/
    ├── mocks.dart          # Shared mock classes
    └── pump_app.dart       # Helper to pump MaterialApp with providers
```

## Unit Tests (Pure Dart)

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockApiClient extends Mock implements ApiClient {}

void main() {
  late AuthRepository sut; // system under test
  late MockApiClient mockApi;

  setUp(() {
    mockApi = MockApiClient();
    sut = AuthRepositoryImpl(mockApi);
  });

  group('login', () {
    test('returns User on success', () async {
      // Arrange
      when(() => mockApi.post(any(), any())).thenAnswer((_) async => userJson);
      // Act
      final user = await sut.login('a@b.com', 'pass');
      // Assert
      expect(user.email, 'a@b.com');
      verify(() => mockApi.post('/auth/login', any())).called(1);
    });

    test('throws AuthException on 401', () async {
      when(() => mockApi.post(any(), any())).thenThrow(
        DioException(requestOptions: RequestOptions(), response: Response(statusCode: 401)),
      );
      expect(() => sut.login('a@b.com', 'wrong'), throwsA(isA<AuthException>()));
    });
  });
}
```

## Widget Tests

```dart
void main() {
  testWidgets('LoginScreen shows error on invalid email', (tester) async {
    // Arrange
    await tester.pumpWidget(const MaterialApp(home: LoginScreen()));
    // Act
    await tester.enterText(find.byKey(const Key('emailField')), 'invalid');
    await tester.tap(find.byKey(const Key('loginButton')));
    await tester.pumpAndSettle();
    // Assert
    expect(find.text('Enter a valid email'), findsOneWidget);
  });
}
```

## Riverpod Provider Tests

```dart
void main() {
  test('cartNotifier adds item', () async {
    final container = ProviderContainer();
    addTearDown(container.dispose);
    final notifier = container.read(cartNotifierProvider.notifier);
    notifier.addItem(const CartItem(id: '1', name: 'Widget', price: 9.99));
    expect(container.read(cartNotifierProvider), hasLength(1));
  });
}
```

## Key Rules

- **Name tests descriptively**: `'returns User on success'` not `'test1'`
- **One assertion per test** when possible (multiple related asserts OK)
- **Use `setUp` / `tearDown`** — never share mutable state across tests
- **Mock at boundaries** — repositories, API clients, not internal classes
- **Run tests in CI**: `flutter test --coverage`

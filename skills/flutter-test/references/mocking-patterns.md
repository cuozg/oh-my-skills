# Mocking Patterns — mocktail (NOT mockito)

All mocking uses `mocktail`. Never `mockito`.

## Mocks, Fakes, Fallbacks

```dart
import 'package:mocktail/mocktail.dart';
class MockAuthRepo extends Mock implements AuthRepository {}
class FakeUser extends Fake implements User {}
setUpAll(() { registerFallbackValue(const LoginRequest(email: '', password: '')); });
```

## Stubbing

```dart
when(() => mockRepo.getCachedUser()).thenReturn(fakeUser);
when(() => mockRepo.login(any(), any())).thenAnswer((_) async => fakeUser);
when(() => mockRepo.login(any(), any())).thenThrow(AuthException('Invalid'));
```

## Verification

```dart
verify(() => mockRepo.login('a@b.com', 'pass')).called(1);
verifyNever(() => mockRepo.logout());
verifyInOrder([() => mockRepo.login(any(), any()), () => mockRepo.fetchProfile()]);
```

## Shared Setup

```dart
late MockAuthRepo mockAuthRepo;
late AuthService sut;
setUp(() { mockAuthRepo = MockAuthRepo(); sut = AuthService(mockAuthRepo); });
tearDown(() => reset(mockAuthRepo));
```

## Matchers

- `any()` — positional · `any(named: 'data')` — named · `captureAny()` — capture
- `any(that: isA<LoginRequest>())` — typed constraint

# Dependency Injection

Primary: **Riverpod as DI container**. Alternative: GetIt + Injectable for non-Flutter Dart.

## Riverpod as DI (Recommended)

Riverpod providers naturally serve as a DI container — no extra package needed.

```dart
// 1. Define the dependency
@riverpod
ApiClient apiClient(Ref ref) {
  return ApiClient(baseUrl: 'https://api.example.com');
}

// 2. Define repository using the dependency
@riverpod
AuthRepository authRepository(Ref ref) {
  final api = ref.watch(apiClientProvider);
  final storage = ref.watch(secureStorageProvider);
  return AuthRepositoryImpl(api, storage);
}

// 3. Consume in notifier or widget
@riverpod
class AuthNotifier extends _$AuthNotifier {
  @override
  Future<User?> build() async {
    final repo = ref.watch(authRepositoryProvider);
    return repo.getCurrentUser();
  }
}
```

## Overriding for Tests

```dart
void main() {
  test('login success', () async {
    final container = ProviderContainer(
      overrides: [
        authRepositoryProvider.overrideWithValue(MockAuthRepository()),
      ],
    );
    addTearDown(container.dispose);
    final user = await container.read(authNotifierProvider.future);
    expect(user, isNotNull);
  });
}
```

## Scoped Providers

```dart
// Screen-scoped provider (auto-disposed when screen is popped)
@riverpod
class FormNotifier extends _$FormNotifier {
  @override
  FormState build() => const FormState.initial();
  // ...auto-disposed when no longer watched
}
```

## GetIt + Injectable (Alternative)

Use when you need DI outside the Flutter widget tree (pure Dart services, CLI tools).

```dart
// injection.dart
import 'package:get_it/get_it.dart';
import 'package:injectable/injectable.dart';
import 'injection.config.dart';

final getIt = GetIt.instance;

@InjectableInit()
void configureDependencies() => getIt.init();
```


## DI Comparison

| Approach | Pros | Cons |
|----------|------|------|
| Riverpod | No extra pkg, compile-safe, testable | Flutter-only |
| GetIt + Injectable | Works in pure Dart, codegen | Manual registration, no reactive updates |
| Manual constructor injection | Zero dependencies | Tedious at scale |

## Key Rules

- **Prefer Riverpod** for Flutter apps — it's both state management AND DI
- **Never** instantiate repositories/services directly in widgets
- **Always** program against abstractions (interfaces) for testability
- **Scope** providers to the narrowest lifecycle possible

<!-- Related: state-management-guide.md, architecture-patterns.md -->

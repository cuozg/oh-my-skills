# Architecture Patterns

For state management specifics → `read_skill_file("flutter-standards", "references/state-management-guide.md")`
For DI patterns → `read_skill_file("flutter-standards", "references/dependency-injection.md")`

## Feature-First Architecture (Recommended)

Organize by feature, not by type. Each feature owns its data, state, and UI layers.

```
features/
├── auth/           # Login, registration, token management
│   ├── data/       # AuthRepository, UserModel, AuthApi
│   ├── providers/  # authProvider, userProvider
│   └── presentation/  # LoginScreen, SignUpScreen
├── profile/
│   ├── data/
│   ├── providers/
│   └── presentation/
```

**Why feature-first**: Changes to "auth" touch files in one folder. Type-first (all models/, all screens/) scatters related code across the tree.

## Layered Architecture Within Features

```
┌──────────────────────────┐
│     Presentation         │  Widgets, Screens
│     (Flutter-dependent)  │  Reads providers, dispatches actions
├──────────────────────────┤
│     State / Providers    │  Riverpod Notifiers
│     (Business logic)     │  Coordinates data ↔ UI
├──────────────────────────┤
│     Data                 │  Repositories, Models, DTOs
│     (Pure Dart)          │  API calls, local storage, mapping
└──────────────────────────┘
```

**Dependency rule**: Presentation → State → Data. Never upward.

## Repository Pattern

```dart
abstract class AuthRepository {
  Future<User> login(String email, String password);
  Future<void> logout();
  Stream<User?> watchCurrentUser();
}

class AuthRepositoryImpl implements AuthRepository {
  final ApiClient _api;
  final SecureStorage _storage;

  AuthRepositoryImpl(this._api, this._storage);

  @override
  Future<User> login(String email, String password) async {
    final dto = await _api.post('/auth/login', {'email': email, 'password': password});
    final user = User.fromJson(dto);
    await _storage.saveToken(dto['token']);
    return user;
  }
}
```

## MVVM (With Riverpod)

```
Model:      Freezed data class (immutable)
View:       Widget tree (reads provider, calls notifier methods)
ViewModel:  Riverpod AsyncNotifier (holds state, business logic)
```

## Architecture Comparison

| Pattern | Complexity | Best For |
|---------|-----------|----------|
| Feature-first + Riverpod | Low-Medium | Solo dev, most apps (recommended) |
| Clean Architecture | High | Large teams, strict domain boundaries |
| BLoC pattern | Medium | Event-driven, complex state transitions |
| MVC (vanilla) | Low | Prototypes, simple CRUD apps |

## When to Reach for Clean Architecture

- **DO** use when: Multiple data sources per feature, complex domain rules, team >3 devs
- **DON'T** use when: Solo dev, CRUD-heavy app, rapid prototyping — the ceremony outweighs the benefit

<!-- Related: code-organization.md, state-management-guide.md -->

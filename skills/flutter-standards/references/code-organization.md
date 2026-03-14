# Code Organization

Feature-first folder layout for solo Flutter developers. Scales cleanly from MVP to production.

## Project Structure (Feature-First)

```
lib/
├── main.dart                    # App entry, ProviderScope, MaterialApp
├── app/
│   ├── app.dart                 # MaterialApp.router configuration
│   ├── router.dart              # GoRouter route definitions
│   └── theme.dart               # ThemeData, ColorScheme, TextTheme
├── core/
│   ├── constants.dart           # App-wide constants
│   ├── extensions/              # Dart extension methods
│   ├── exceptions.dart          # Custom exception classes
│   ├── utils/                   # Pure utility functions
│   └── network/
│       ├── api_client.dart      # Dio/http client setup
│       └── interceptors.dart    # Auth, logging interceptors
├── features/
│   ├── auth/
│   │   ├── data/
│   │   │   ├── auth_repository.dart
│   │   │   └── models/user.dart
│   │   ├── presentation/
│   │   │   ├── login_screen.dart
│   │   │   └── widgets/
│   │   └── providers/
│   │       └── auth_provider.dart
│   └── home/
│       ├── data/
│       ├── presentation/
│       └── providers/
├── shared/
│   ├── widgets/                 # Reusable UI components
│   ├── models/                  # Shared data models
│   └── providers/               # App-wide providers
└── l10n/                        # Localization ARB files
```

## Feature Folder Anatomy

Each feature follows the same 3-layer structure:

| Layer | Folder | Contains |
|-------|--------|----------|
| Data | `data/` | Repository classes, models, DTOs, data sources |
| State | `providers/` | Riverpod providers, Notifiers, state classes |
| UI | `presentation/` | Screens, page-level widgets, feature-specific widgets |

## Barrel Files

Use sparingly — only for public API of a feature:

```dart
// features/auth/auth.dart (barrel)
export 'data/auth_repository.dart';
export 'providers/auth_provider.dart';
// Don't export internal widgets or private models
```

## pubspec.yaml Essentials

```yaml
environment:
  sdk: ^3.5.0
  flutter: ^3.24.0

dependencies:
  flutter_riverpod: ^2.6.0
  riverpod_annotation: ^2.6.0
  go_router: ^14.0.0
  dio: ^5.0.0
  freezed_annotation: ^2.4.0
  json_annotation: ^4.9.0

dev_dependencies:
  riverpod_generator: ^2.6.0
  build_runner: ^2.4.0
  freezed: ^2.5.0
  json_serializable: ^6.8.0
  flutter_lints: ^5.0.0
  mocktail: ^1.0.0
```

## Key Rules

- One widget/class per file — file name matches class name in snake_case
- Feature folders are self-contained — no cross-feature imports at data layer
- Shared code goes in `core/` (pure Dart) or `shared/` (Flutter widgets)
- Keep `main.dart` minimal — delegate to `app/app.dart`

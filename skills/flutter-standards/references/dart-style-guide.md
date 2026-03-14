# Dart Style Guide

Based on [Effective Dart](https://dart.dev/effective-dart). Primary source for all naming, formatting, and null-safety rules.

## Naming Conventions

| Element | Style | Example |
|---------|-------|---------|
| Class / Enum | UpperCamelCase | `UserProfile` |
| Extension | UpperCamelCase | `StringExtension` |
| Mixin | UpperCamelCase | `LoggingMixin` |
| Library / Package | lowercase_with_underscores | `my_app` |
| File | lowercase_with_underscores | `user_profile.dart` |
| Variable / Parameter | lowerCamelCase | `itemCount` |
| Constant | lowerCamelCase | `defaultTimeout` |
| Private member | _lowerCamelCase | `_isLoading` |
| Named parameter | lowerCamelCase | `{required String name}` |
| Typedef | UpperCamelCase | `typedef Callback = void Function()` |

## Boolean Naming

Prefix with `is`, `has`, `can`, `should`:

```dart
bool isLoading = false;
bool hasPermission = true;
bool canRetry = attempts < maxRetries;
```

## Formatting Rules (dart format)

- 80-char line width (default `dart format`)
- Always use trailing commas in argument lists → forces multi-line formatting
- Prefer single quotes for strings: `'hello'` not `"hello"`
- Use `///` for doc comments, `//` for implementation comments

```dart
// GOOD: trailing comma forces readable formatting
final widget = Padding(
  padding: const EdgeInsets.all(16),
  child: Text(
    'Hello',
    style: theme.textTheme.bodyLarge,
  ), // ← trailing comma
);
```

## Null Safety

- Prefer non-nullable types by default
- Use `late` only when initialization is guaranteed before access
- Avoid `!` (bang operator) — prefer null-aware alternatives

```dart
// GOOD: null-aware patterns
final name = user?.name ?? 'Unknown';
final items = list?.where((e) => e.isActive).toList() ?? [];

// BAD: bang operator risk
final name = user!.name; // throws if null
```

## Linting (analysis_options.yaml)

```yaml
include: package:flutter_lints/flutter.yaml

linter:
  rules:
    prefer_const_constructors: true
    prefer_const_declarations: true
    avoid_print: true
    prefer_single_quotes: true
    sort_constructors_first: true
    unawaited_futures: true
    always_declare_return_types: true
```

## Import Ordering

```dart
// 1. Dart SDK
import 'dart:async';
import 'dart:convert';

// 2. Flutter SDK
import 'package:flutter/material.dart';

// 3. Third-party packages
import 'package:riverpod_annotation/riverpod_annotation.dart';

// 4. Project imports (relative or package)
import '../models/user.dart';
import 'widgets/profile_card.dart';
```


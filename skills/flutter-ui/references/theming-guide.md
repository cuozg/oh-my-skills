# Theming Guide

Centralized theme setup, dark/light mode, and custom theme extensions.

## ThemeData Setup

Use `ColorScheme.fromSeed(seedColor:, brightness:)` for Material 3 color generation. Define in a single `app_theme.dart` file with a factory function accepting `Brightness` for light/dark variants. Set component themes (input, button, card) in the same ThemeData.

## Dark/Light Mode Toggle

Wire `MaterialApp` with `theme:` (light), `darkTheme:` (dark), and `themeMode:` from a provider or ValueNotifier. Use `ThemeMode.system` as default.

## ThemeExtension for Custom Properties

Use `ThemeExtension<T>` for custom tokens (success, warning, surface variants). Implement `copyWith()` and `lerp()`. Register via `ThemeData(extensions: [...])`. Access via `Theme.of(context).extension<T>()!`.

## Context Extensions

Define on `BuildContext` for clean access:
- `context.textTheme` → `Theme.of(this).textTheme`
- `context.colorScheme` → `Theme.of(this).colorScheme`
- `context.themeExt<T>()` → `Theme.of(this).extension<T>()!`

## Typography Scale

Use Material 3 text styles — never create ad-hoc `TextStyle`:

| Style | Usage |
|-------|-------|
| `displayLarge/Medium/Small` | Hero text, splash |
| `headlineLarge/Medium/Small` | Screen titles, sections |
| `titleLarge/Medium/Small` | Card titles, dialogs |
| `bodyLarge/Medium/Small` | Body text, descriptions |
| `labelLarge/Medium/Small` | Buttons, chips, badges |

## Rules

- Define theme in one file (`app_theme.dart`) — never scatter theme logic
- Use `ColorScheme.fromSeed()` — never hardcode hex colors in widgets
- Access via context extensions — never inline `Theme.of(context).textTheme.bodyLarge`
- Custom colors go in `ThemeExtension` — not in a global constants file
- Test both light and dark themes in golden tests

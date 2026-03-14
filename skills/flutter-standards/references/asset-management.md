# Asset Management

Images, fonts, localization, and code generation for type-safe asset access.

## Asset Organization

```
assets/
├── images/
│   ├── 1.5x/          # Optional density variants
│   ├── 2.0x/
│   ├── 3.0x/
│   └── logo.png       # Base (1x) resolution
├── icons/
│   └── app_icon.svg
├── fonts/
│   ├── Inter-Regular.ttf
│   └── Inter-Bold.ttf
└── l10n/
    ├── app_en.arb      # English strings
    └── app_vi.arb      # Vietnamese strings
```

## pubspec.yaml Asset Declaration

```yaml
flutter:
  assets:
    - assets/images/
    - assets/icons/

  fonts:
    - family: Inter
      fonts:
        - asset: assets/fonts/Inter-Regular.ttf
        - asset: assets/fonts/Inter-Bold.ttf
          weight: 700
```

## flutter_gen (Type-Safe Assets)

Generates constants for all declared assets — no more string typos.

```yaml
# pubspec.yaml
dev_dependencies:
  flutter_gen_runner: ^5.7.0

flutter_gen:
  output: lib/gen/
  integrations:
    flutter_svg: true
```

```dart
// Generated usage
Image.asset(Assets.images.logo.path);
SvgPicture.asset(Assets.icons.appIcon.path);
```

## Localization (gen_l10n)

```yaml
# l10n.yaml (project root)
arb-dir: assets/l10n
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
```

```dart
// Usage in widgets
Text(AppLocalizations.of(context)!.appTitle)
Text(AppLocalizations.of(context)!.itemCount(items.length))
```

## Image Loading Best Practices

- Use `CachedNetworkImage` for remote images (caches to disk)
- Use `Image.asset()` for bundled assets
- Use `SvgPicture.asset()` for vector icons (flutter_svg)
- **Prefer SVG** for icons and illustrations — scales without density variants

```dart
CachedNetworkImage(
  imageUrl: user.avatarUrl,
  placeholder: (_, __) => const CircularProgressIndicator(),
  errorWidget: (_, __, ___) => const Icon(Icons.person),
);
```

## Key Rules

- **Always** declare assets in pubspec.yaml — undeclared assets won't bundle
- **Use flutter_gen** — eliminates string-based asset references
- **Provide density variants** (2x, 3x) for raster images
- **Keep ARB files flat** — avoid deeply nested structures
- **Lazy-load heavy assets** — don't block app startup

<!-- Related: ui-best-practices.md, code-organization.md -->

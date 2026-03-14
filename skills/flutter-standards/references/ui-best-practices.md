# UI Best Practices

Widget composition, performance, responsive layout, and theming patterns.

## Widget Composition Rules

- **Extract widgets into classes** — not methods. Methods rebuild the entire parent.
- **Use `const` constructors** everywhere possible — skips rebuild entirely.
- **Keep `build()` lean** — extract complex logic into providers or helper methods.

```dart
// GOOD: const constructor, extracted widget
class ProfileHeader extends StatelessWidget {
  const ProfileHeader({super.key, required this.name});
  final String name;

  @override
  Widget build(BuildContext context) => Text(name, style: context.textTheme.headlineMedium);
}

// BAD: method-extracted widget (rebuilds with parent)
Widget _buildHeader(String name) => Text(name);
```

## Keys

- Use `ValueKey` on list items to preserve state during reordering
- Use `UniqueKey` to force widget recreation
- **Never** use `Key(index.toString())` — breaks on reorder

```dart
ListView.builder(
  itemBuilder: (_, i) => ProductTile(key: ValueKey(products[i].id), product: products[i]),
);
```

## Responsive Layout

```dart
// LayoutBuilder for parent-constrained sizing
LayoutBuilder(
  builder: (context, constraints) {
    if (constraints.maxWidth > 600) return const WideLayout();
    return const NarrowLayout();
  },
);

// MediaQuery for screen-level decisions
final isTablet = MediaQuery.sizeOf(context).width > 600;
```

**Prefer `MediaQuery.sizeOf(context)`** over `MediaQuery.of(context).size` — the former only rebuilds on size changes, not on all media query changes.

## Theming

```dart
// Define theme in one place
ThemeData buildAppTheme() => ThemeData(
  colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
  textTheme: GoogleFonts.interTextTheme(),
  inputDecorationTheme: const InputDecorationTheme(border: OutlineInputBorder()),
  filledButtonTheme: FilledButtonThemeData(
    style: FilledButton.styleFrom(minimumSize: const Size(double.infinity, 48)),
  ),
);

// Access in widgets via context extensions
extension ThemeX on BuildContext {
  TextTheme get textTheme => Theme.of(this).textTheme;
  ColorScheme get colorScheme => Theme.of(this).colorScheme;
}
```

## Spacing & Padding Consistency

Use a spacing scale constant — not magic numbers:

```dart
abstract final class AppSpacing {
  static const double xs = 4;
  static const double sm = 8;
  static const double md = 16;
  static const double lg = 24;
  static const double xl = 32;

  static const gap4 = SizedBox(height: xs);
  static const gap8 = SizedBox(height: sm);
  static const gap16 = SizedBox(height: md);
}
```

## Avoid Common Pitfalls

- **Don't nest `Scaffold`** — one per route
- **Don't use `setState` for global state** — use Riverpod
- **Don't put logic in `build()`** — use providers or `initState`
- **Wrap expensive subtrees with `RepaintBoundary`** if they animate independently

<!-- Related: performance-optimization.md, asset-management.md -->

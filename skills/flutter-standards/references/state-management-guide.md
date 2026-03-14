# State Management Guide

Primary: **Riverpod 2.x with codegen**. Alternatives documented for context.

## Riverpod 2.x — Core Concepts

| Concept | Purpose |
|---------|---------|
| `Provider` | Read-only value (config, repository instances) |
| `FutureProvider` | Async data fetching |
| `StreamProvider` | Reactive stream data |
| `NotifierProvider` | Mutable state with methods |
| `AsyncNotifierProvider` | Mutable state + async operations |

## Codegen Pattern (Recommended)

```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';
part 'user_provider.g.dart';

// Simple computed value (auto-disposed, read-only)
@riverpod
Future<User> currentUser(Ref ref) async {
  final repo = ref.watch(authRepositoryProvider);
  return repo.getCurrentUser();
}

// Mutable state with notifier
@riverpod
class CartNotifier extends _$CartNotifier {
  @override
  List<CartItem> build() => []; // initial state

  void addItem(CartItem item) {
    state = [...state, item];
  }

  void removeItem(String id) {
    state = state.where((e) => e.id != id).toList();
  }

  double get total => state.fold(0, (sum, e) => sum + e.price);
}
```

Run codegen: `dart run build_runner watch --delete-conflicting-outputs`

## AsyncNotifier (Async State)

```dart
@riverpod
class ProductList extends _$ProductList {
  @override
  Future<List<Product>> build() async {
    final repo = ref.watch(productRepositoryProvider);
    return repo.fetchAll();
  }

  Future<void> refresh() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() => ref.read(productRepositoryProvider).fetchAll());
  }
}
```

## Consuming in Widgets

```dart
class ProductScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final productsAsync = ref.watch(productListProvider);
    return productsAsync.when(
      data: (products) => ListView.builder(
        itemCount: products.length,
        itemBuilder: (_, i) => ProductTile(products[i]),
      ),
      loading: () => const CircularProgressIndicator(),
      error: (e, st) => ErrorWidget.withDetails(message: e.toString()),
    );
  }
}
```

## Provider Scoping

- `ref.watch()` — Rebuild widget when value changes (use in `build()`)
- `ref.read()` — One-time read, no rebuild (use in callbacks/methods)
- `ref.listen()` — Side effects on change (snackbars, navigation)
- `ref.invalidate()` — Force provider to recompute

## Alternatives Comparison

| Library | Approach | When to Use |
|---------|----------|-------------|
| **Riverpod 2.x** | Compile-safe, codegen, testable | Default choice (recommended) |
| **flutter_bloc** | Event→State, strict separation | Complex event-driven flows |
| **Provider** | InheritedWidget wrapper | Legacy projects, simple apps |
| **GetX** | Reactive + routing + DI bundle | Not recommended (tight coupling) |

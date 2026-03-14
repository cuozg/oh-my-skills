# Integration Mode — Full App Flow, Navigation, User Journey

End-to-end tests launching the full app. Multi-screen journeys.

## Setup + Flow

```dart
import 'package:integration_test/integration_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('login navigates to home', (tester) async {
    await tester.pumpWidget(const MyApp());
    await tester.pumpAndSettle();
    await tester.enterText(find.byKey(const Key('emailField')), 'user@test.com');
    await tester.enterText(find.byKey(const Key('passField')), 'password');
    await tester.tap(find.byKey(const Key('loginBtn')));
    await tester.pumpAndSettle();
    expect(find.byType(HomeScreen), findsOneWidget);
  });
}
```

## Navigation

```dart
testWidgets('bottom nav switches tabs', (tester) async {
  await tester.pumpWidget(const MyApp());
  await tester.pumpAndSettle();
  await tester.tap(find.byIcon(Icons.person));
  await tester.pumpAndSettle();
  expect(find.byType(ProfileScreen), findsOneWidget);
});
```

## State Across Screens

```dart
testWidgets('cart persists across screens', (tester) async {
  await tester.pumpWidget(createTestApp());
  await tester.tap(find.text('Add to Cart'));
  await tester.pumpAndSettle();
  await tester.tap(find.byIcon(Icons.shopping_cart));
  await tester.pumpAndSettle();
  expect(find.text('1 item'), findsOneWidget);
});
```

## Running

Place in `integration_test/` at project root.
`flutter test integration_test/` — all · `flutter drive --target=integration_test/app_test.dart` — device

# Widget Mode — Screen, Component, UI Tests

Render UI in test environment. Verify rendering, interactions, visual states.

## Pumping + Provider Overrides

```dart
Widget createApp({AuthRepository? authRepo}) => ProviderScope(
  overrides: [if (authRepo != null) authRepoProvider.overrideWithValue(authRepo)],
  child: const MaterialApp(home: LoginScreen()),
);

testWidgets('renders fields', (tester) async {
  await tester.pumpWidget(createApp());
  expect(find.byKey(const Key('emailField')), findsOneWidget);
});
```

## Finders

`find.text('Submit')` · `find.byKey(Key('btn'))` · `find.byType(ElevatedButton)` · `find.byIcon(Icons.close)` · `find.descendant(of: find.byType(Card), matching: find.text('T'))`

## Interactions

```dart
testWidgets('tap login', (tester) async {
  await tester.pumpWidget(createApp());
  await tester.enterText(find.byKey(const Key('emailField')), 'a@b.com');
  await tester.tap(find.byKey(const Key('loginBtn')));
  await tester.pumpAndSettle();
  expect(find.text('Welcome'), findsOneWidget);
});
```

## Goldens

```dart
await expectLater(find.byType(ProfileCard), matchesGoldenFile('goldens/card.png'));
// Run: flutter test --update-goldens
```

## Responsive

```dart
testWidgets('mobile layout', (tester) async {
  tester.view.physicalSize = const Size(375, 812);
  tester.view.devicePixelRatio = 1.0;
  addTearDown(tester.view.resetPhysicalSize);
  await tester.pumpWidget(createApp());
  expect(find.byType(MobileLayout), findsOneWidget);
});
```

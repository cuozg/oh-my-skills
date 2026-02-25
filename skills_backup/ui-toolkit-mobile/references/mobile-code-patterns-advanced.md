# Mobile Code Patterns — Advanced

> See [mobile-code-patterns.md](mobile-code-patterns.md) for touch input, gesture detection, and safe area basics.

## Orientation Handling

```csharp
// MonoBehaviour: poll Screen.orientation in Update(), on change toggle classes:
// root.EnableInClassList("orientation--portrait", isPortrait);
// root.EnableInClassList("orientation--landscape", !isPortrait);
// Then call SafeAreaApplier.Apply(root);
```

```css
.orientation--portrait .main-layout { flex-direction: column; }
.orientation--portrait .sidebar { display: none; }
.orientation--portrait .bottom-nav { display: flex; }
.orientation--landscape .main-layout { flex-direction: row; }
.orientation--landscape .sidebar { display: flex; width: 240px; }
.orientation--landscape .bottom-nav { display: none; }
```

## Mobile Performance Budget

| Metric | Mobile Target |
|--------|--------------|
| Draw calls (UI) | < 15 |
| Visual elements | < 200 visible |
| USS selectors | < 3 levels deep |
| Texture memory (UI) | < 8 MB |
| Layout recalcs/frame | 0 during gameplay |

Key: Flatten hierarchy. `UsageHints.DynamicTransform` on animated elements. `ListView` for virtualization. Atlas textures.

## Touch Feedback

```css
.btn-mobile { transition-property: scale, background-color; transition-duration: 80ms, 120ms; scale: 1 1; }
.btn-mobile:active { scale: 0.95 0.95; background-color: rgb(80, 80, 80); }
```

## Haptic Feedback

```csharp
// iOS: [DllImport("__Internal")] _TriggerHaptic(int style) — Light/Medium/Heavy
// Android: AndroidJavaClass("com.unity3d.player.UnityPlayer") → getSystemService("vibrator") → vibrate(10L/20L/30L)
// Attach: button.clicked += () => Trigger(style);
```

## Virtual Keyboard

```csharp
// On FocusInEvent for TextField: delay 300ms, then set scrollView.style.paddingBottom = TouchScreenKeyboard.area.height, call ScrollTo(field).
// On FocusOutEvent / Update when no focus: reset paddingBottom = 0.
// Register on root via FocusInEvent/FocusOutEvent. Use schedule.Execute().StartingIn(300) for keyboard animation delay.
```

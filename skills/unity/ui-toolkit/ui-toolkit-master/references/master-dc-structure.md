# UI Toolkit Master — Dragon Crashers Structure, Exercise & Coverage Gaps

> Extracted from [ui-toolkit-master/SKILL.md](../SKILL.md).

## Dragon Crashers Project Structure

```
Assets/
├── UI/
│   ├── Uxml/                    # 20+ UXML files (flat)
│   │   ├── MainMenu.uxml       # Master entry point for all menu screens
│   │   ├── HomeScreen.uxml, CharScreen.uxml, ShopScreen.uxml, ...
│   │   └── TabbedMenu.uxml, HealthBar.uxml  # Reusable components
│   ├── Uss/                     # 5-folder scope-based
│   │   ├── Base/ (7 files)      # Design tokens
│   │   ├── Screens/ (14 files)  # Per-screen styles
│   │   ├── CustomElements/ (5)  # Custom control styles
│   │   ├── ThemeStyles/         # Theme + orientation overrides
│   │   └── Toolbars/ (2 files)
│   ├── Themes/ (7 TSS)          # Orientation × theme matrix
│   └── PanelSettings/           # Portrait + Landscape
├── Scripts/UI/
│   ├── UIViews/       # UIView base + subclasses + UIManager
│   ├── Controllers/   # Screen-level business logic
│   ├── Components/    # Custom VisualElement subclasses
│   ├── Events/        # 10 static event classes
│   └── Themes/        # ThemeManager.cs
└── Scripts/Utilities/ # SafeAreaBorder.cs, PositionToVisualElement.cs
```

Orientation overrides via TSS swapping, not media queries. See [ui-toolkit-theming](../../ui-toolkit-theming/SKILL.md#dragon-crashers-compound-theming-system).

### Core Architecture

Single UIDocument + UIView pattern. See [ui-toolkit-architecture](../../ui-toolkit-architecture/SKILL.md#dragon-crashers--architecture-in-practice) for full code.

**Key decisions:** UIView lifecycle: `Initialize()` → `SetVisualElements()` → `RegisterButtonCallbacks()`. UIManager: modal (replace) + overlay (stack). Static `Action` event bus. `[UxmlElement]` for Unity 6 (DC uses legacy `UxmlFactory`).

### SafeAreaBorder & PositionToVisualElement

- **SafeAreaBorder**: `borderWidth` instead of padding — hard visual boundary, configurable `m_Multiplier`. See [ui-toolkit-responsive](../../ui-toolkit-responsive/SKILL.md#safeareaborder-borderwidth-approach).
- **PositionToVisualElement**: 3D-to-UI alignment via `worldBound` → screen → world. Reacts to `GeometryChangedEvent` and `ThemeEvents.CameraUpdated`. See [ui-toolkit-responsive](../../ui-toolkit-responsive/SKILL.md#positiontovisualelement-world-to-ui-alignment).

### Async/Await Fire-and-Forget

UIView (plain C#) uses `_ = AsyncMethod()` for UI animations. Wrap in `try/catch`. Unity 6+: replace `Task.Delay(TimeSpan.FromSeconds(Time.deltaTime))` with `await Awaitable.NextFrameAsync()`. See [ui-toolkit-patterns](../../ui-toolkit-patterns/SKILL.md#async-task-fire-and-forget).

**Production metrics:** 8–12 tree depth, 50–200 elements/screen, 4–8 draw calls, 2–4 MB memory, <100ms init on mobile.

## Exercise: Hello UI Toolkit

Main menu: title + start + settings. UXML with `.screen`, `.title`, `.btn-primary`, `.btn-secondary`. C# controller caches Q() in OnEnable, unregisters in OnDisable. No inline styles. USS uses token pattern.

## Coverage Gaps

### Accessibility

| Area | Recommendation |
|---|---|
| Screen readers | Use descriptive Label text; set `tooltip` on icon buttons |
| Focus navigation | Set `tabIndex` on interactive elements; test keyboard-only |
| High contrast | Create high-contrast TSS with `var(--color-*)` overrides |
| Touch targets | Min 44×44px (WCAG 2.5.5) |
| Reduced motion | `--transition-duration: 0ms` override TSS; user toggle |

```csharp
iconButton.focusable = true; iconButton.tabIndex = 1; iconButton.tooltip = "Open inventory";
```

### Testing

| Approach | Setup |
|---|---|
| Edit Mode | `[Test]` + `UIDocument`, element queries, class assertions |
| Play Mode | `[UnityTest]` + scene with UIDocument |
| Event simulation | `using var evt = ClickEvent.GetPooled(); element.SendEvent(evt);` |

> ⚠️ `SendEvent()` requires element attached to a panel.

### Localization

Use `com.unity.localization`: bind `LocalizedString.StringChanged` to `Label.text`. `direction: rtl` for RTL (Unity 6+). Font fallback chain for CJK/Arabic.

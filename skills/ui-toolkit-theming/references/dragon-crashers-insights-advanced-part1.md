# Dragon Crashers: Key Components & Advanced Patterns

> See [dragon-crashers-insights.md](dragon-crashers-insights.md) for screen implementations (MailView, ShopView, HomeView, Inventory).

---

## Key Components

### HealthBarComponent (⚠️ Deprecated UxmlFactory)

Custom `VisualElement` with `UxmlFactory`/`UxmlTraits` for `currentHealth`, `MaximumHealth`, `HealthBarTitle`. Builds hierarchy in constructor with BEM classes. **Modern:** Replace with `[UxmlElement]` + `[UxmlAttribute]`.

### SlideToggle — `BaseField<bool>` + Deprecated UxmlFactory

Extends `BaseField<bool>` for auto `ChangeEvent<bool>`, built-in label, `INotifyValueChanged<bool>`. Uses USS class toggling: `slide-toggle__input--checked`.

### ShopItemComponent — `userData` + `StopImmediatePropagation`

```csharp
m_BuyButton.userData = m_ShopItemData;  // No closures needed
m_BuyButton.RegisterCallback<PointerMoveEvent>(evt => evt.StopImmediatePropagation()); // Block ScrollView drag
```

### UIManager — Single-Document Navigation

Single UIDocument, subtree views. Modal replaces current (`m_PreviousView` for back). Overlay stacks. `m_AllViews` ensures centralized `Dispose()`.

---

## USS & TSS Organization

### Base USS (7 files in `Assets/UI/Uss/Base/`)

| File | Key Content |
|------|------------|
| Colors.uss | BEM utilities: `.color__text--white`. ⚠️ BUG: `.color__text--blue` uses orange |
| Text.uss | Global font, fixed sizes (35/45/60/80px) |
| Common.uss | `:root` font/cursor only (NOT design tokens), `.screen__anchor--fill` |
| Buttons.uss | Transparent base, hover scale 1.1, tint-based color variants |
| Dropdowns.uss | ⚠️ **MUST import via TSS** — compound parts only resolve via TSS |
| Cursors.uss | Two-cursor system via type selectors |

### DC vs Recommended Approach

| Aspect | DC (Actual) | Recommended |
|---|---|---|
| Colors | BEM classes with hardcoded `rgb()` | `:root` variables + `var()` |
| Typography | Fixed pixel sizes | Token scale + `var()` |
| Theming | Swap entire TSS file | Override `:root` variables |
| Best for | Fixed-theme games | Dark/light or brand customization |

### TSS 7-File Matrix

```
RuntimeTheme-Default.tss ← unity-theme://default + Decoration-Default.uss
├── RuntimeTheme-Landscape.tss ← + 11 Landscape/*.uss
│   ├── Landscape--Christmas.tss ← + Decoration-Christmas.uss
│   └── Landscape--Halloween.tss
└── RuntimeTheme-Portrait.tss ← + 11 Portrait/*.uss
    ├── Portrait--Christmas.tss
    └── Portrait--Halloween.tss
```

Seasonal decorations use visibility toggling: `.theme__decoration--christmas { display: flex; }` / others `{ display: none; }`.

Orientation USS overrides same classes with different layout (e.g., `.menu-bar__container`: column→row, width/height swap).

---

## Theme System

**Events**: `ThemeEvents.ThemeChanged(string)`, `MediaQueryEvents.ResolutionUpdated/AspectRatioUpdated/SafeAreaUpdated/DpiUpdated`

**Flow**: Season change → `SettingsScreenController.UpdateTheme()` → constructs `"Portrait--Halloween"` → `ThemeEvents.ThemeChanged` → `ThemeManager.ApplyTheme()`. Orientation change keeps season suffix, swaps prefix.

**Adding a season**: Create Decoration USS + 2 TSS files + 2 ThemeSettings entries + dropdown option.

---

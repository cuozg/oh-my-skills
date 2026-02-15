# Dragon Crashers: Key Patterns & Code Reference

DC-specific implementations for comparison/reference. See [quizu-patterns.md](quizu-patterns.md) for QuizU patterns.

---

## Screen Implementations

### MailView — Composite View (parent owns 3 child views)

```csharp
public class MailView : UIView
{
    MailboxView m_MailboxView; MailContentView m_MailContentView; MailTabView m_MailTabView;

    public override void Initialize()
    {
        base.Initialize();
        m_MailTabView = new MailTabView(m_TopElement.Q("tabs__container")); m_MailTabView.Show();
        m_MailboxView = new MailboxView(m_TopElement.Q("mailbox__container")); m_MailboxView.Show();
        m_MailContentView = new MailContentView(m_TopElement.Q("content__container")); m_MailContentView.Show();
    }
    public override void Dispose() { base.Dispose(); m_MailboxView.Dispose(); m_MailContentView.Dispose(); m_MailTabView.Dispose(); }
}
```

**Rules:** Parent queries containers in `SetVisualElements()`, creates sub-views in `Initialize()`, cascades `Dispose()`. Max 2 nesting levels.

### ShopView — Dynamic Generation via `VisualTreeAsset.Instantiate()` (not ListView)

```csharp
public void OnShopUpdated(List<ShopItemSO> shopItems)
{
    parentTab.Clear();
    foreach (ShopItemSO item in shopItems)
    {
        TemplateContainer elem = m_ShopItemAsset.Instantiate();
        var controller = new ShopItemComponent(m_GameIconsData, item);
        controller.SetVisualElements(elem); controller.SetGameData(elem); controller.RegisterCallbacks();
        parentElement.Add(elem);
    }
}
```

**Two tab approaches**: (A) Reusable `TabbedMenuController` via naming convention. (B) Manual per-screen with domain events for ShopView.

### HomeView — Event-Driven Data Binding

Subscribe in constructor, unsubscribe in `Dispose()`. Cache elements in `SetVisualElements()`.

### Inventory — `ScrollView.Clear()` → `foreach` Instantiate → component wrapper → `Add()`. Filtering via `DropdownField.ChangeEvent<string>` → event bus → LINQ → rebuild.

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

## Performance Notes

- **FpsCounter**: Ring buffer (50 samples), `m_IsEnabled` guard. ⚠️ Per-frame `$"FPS: {value}"` allocates ~40 bytes.
- **HealthBarController**: Uses `transform.position` (good), but ⚠️ `Camera.main` calls `FindWithTag` — cache it. `ShowNameAndStats` calls `Q<>` per frame — cache in `OnEnable`.
- **Async GC**: `Task.Delay` ~120 bytes/call, `label.text += c` allocates per char, `value.ToString()` ~24 bytes.
- **Dynamic lists**: <20 items → Instantiate loop. 50+ → **must** use `ListView`.

| Method | Effect |
|--------|--------|
| `StopPropagation()` | Stops bubbling, same-target listeners still fire |
| `StopImmediatePropagation()` | Stops bubbling AND same-target listeners |

**Event rules**: Every `+=` needs matching `-=`. MonoBehaviour: `OnEnable`/`OnDisable`. Plain C#: constructor/`Dispose()`. Static events are most dangerous.

---

## Experimental Animations

```csharp
// Position: marker slide
m_MenuMarker.experimental.animation.Position(targetLocal, 200);
// Scale: pop-in
element.transform.scale = new Vector3(0.1f, 0.1f, 1f);
element.experimental.animation.Scale(1f, 200);
// Click cooldown
if (Time.time < m_NextClick) return; m_NextClick = Time.time + 0.2f;
```

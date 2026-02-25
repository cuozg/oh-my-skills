# Dragon Crashers: Key Patterns & Code Reference (Part 1)

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

See [dragon-crashers-insights-themes.md](dragon-crashers-insights-themes.md) for USS & TSS organization, theme system, performance notes, and experimental animations.

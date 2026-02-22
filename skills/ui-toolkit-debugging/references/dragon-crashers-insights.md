# Dragon Crashers: Key Patterns & Code Reference

DC-specific implementations for comparison/reference. See [quizu-patterns.md](quizu-patterns.md) for QuizU patterns. Advanced components → [dragon-crashers-insights-advanced.md](dragon-crashers-insights-advanced.md).

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

See [dragon-crashers-insights-advanced.md](dragon-crashers-insights-advanced.md) for components, USS/TSS, theme system, performance, and animation patterns.

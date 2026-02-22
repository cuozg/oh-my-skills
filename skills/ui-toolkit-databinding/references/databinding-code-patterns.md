# Data Binding — Code Patterns & Examples

> **Parent skill**: [ui-toolkit-databinding](../SKILL.md). Advanced patterns → [databinding-code-patterns-advanced.md](databinding-code-patterns-advanced.md).

## Dragon Crashers Event-Driven Approach

### Data Flow Architecture

```
User Input ──(static Action)──▶ Controller (MonoBehaviour) ──(method call)──▶ View (UIView)
                                   ▲ OnEnable: += / OnDisable: -=                 Q<Label>().text = val
Manager (GameData) ◀──(static Action)──┘                                         
    │                                                                       
SaveManager ── JsonUtility.ToJson() / FromJsonOverwrite() ── GameData ↔ savegame.dat
    └── SaveManager.GameDataLoaded (static event) ──▶ Views
```

### Event Bus — Static Action Delegates

Each screen domain has a dedicated static event class in `Assets/Scripts/UI/Events/`:

```csharp
public static class ShopEvents {
    public static Action GoldSelected;
    public static Action<ShopItemSO, Vector2> ShopItemPurchasing;
    public static Action<GameData> FundsUpdated;
}
```

10 event classes: CharEvents, ShopEvents, HomeEvents, MailEvents, InventoryEvents, SettingsEvents, GameplayEvents, MainMenuUIEvents, MediaQueryEvents, ThemeEvents. Pattern: `public static Action<T>` delegates, null-conditional invoke (`?.Invoke()`), one class per domain.

### Controller Subscription Lifecycle

```csharp
void OnEnable()  { ShopEvents.ShopItemClicked += OnTryBuyItem; }
void OnDisable() { ShopEvents.ShopItemClicked -= OnTryBuyItem; }
void Start()     { LoadShopData(); ShopEvents.ShopUpdated?.Invoke(m_GoldShopItems); }
```

`OnEnable`/`OnDisable` for MonoBehaviours; Constructor/`Dispose()` for UIView subclasses. Every `+=` must have matching `-=`.

### View Data Update

Views extend `UIView`. Pattern: cache Q() in `SetVisualElements()`, subscribe events in constructor, unsubscribe in `Dispose()`, update via direct property assignment.

### Complete Data Flow — Shop Purchase

Click → `ShopItemClicked` → `ShopScreenController.OnTryBuyItem()` → `ShopItemPurchasing` → `GameDataManager.OnPurchaseItem()` → funds check → YES: `TransactionProcessed`/`FundsUpdated`/`PotionsUpdated` → views update; NO: `TransactionFailed`.

See [databinding-code-patterns-advanced.md](databinding-code-patterns-advanced.md) for Unity 6 declarative binding (IDataSource, C# bindings, UXML, type converters, modes, complete example).

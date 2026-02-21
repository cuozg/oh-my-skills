# Data Controller Pattern

## Overview

Data Controllers manage game state with reactive properties. They own the data, expose read-only views, and notify subscribers of changes.

## Interface Pattern

```csharp
namespace YourProject.YourGame;

// ✅ GOOD: Interface with read-only reactive properties
public interface IPlayerDataController
{
    IReadOnlyReactiveProperty<int> Score { get; }
    IReadOnlyReactiveProperty<int> Health { get; }
    IReadOnlyReactiveProperty<string> PlayerName { get; }
    IReadOnlyReactiveProperty<bool> IsAlive { get; }
}
```

## Implementation

```csharp
namespace YourProject.YourGame;

// ✅ GOOD: Sealed class, constructor injection, reactive properties
public sealed class PlayerDataController : IPlayerDataController, IDisposable
{
    private readonly ReactiveProperty<int> score = new(0);
    private readonly ReactiveProperty<int> health = new(100);
    private readonly ReactiveProperty<string> playerName = new(string.Empty);
    private readonly ReactiveProperty<bool> isAlive = new(true);
    private readonly ILogger logger; // Project-configured logger

    public IReadOnlyReactiveProperty<int> Score => this.score;
    public IReadOnlyReactiveProperty<int> Health => this.health;
    public IReadOnlyReactiveProperty<string> PlayerName => this.playerName;
    public IReadOnlyReactiveProperty<bool> IsAlive => this.isAlive;

    [Preserve]
    public PlayerDataController(ILogger logger)
    {
        this.logger = logger;
    }

    public void AddScore(int amount)
    {
        if (amount <= 0) throw new ArgumentOutOfRangeException(nameof(amount), "Score must be positive");
        this.score.Value += amount;
    }

    public void TakeDamage(int damage)
    {
        if (damage <= 0) throw new ArgumentOutOfRangeException(nameof(damage), "Damage must be positive");
        this.health.Value = Math.Max(0, this.health.Value - damage);
        if (this.health.Value <= 0)
        {
            this.isAlive.Value = false;
        }
    }

    public void SetPlayerName(string name)
    {
        ArgumentException.ThrowIfNullOrEmpty(name);
        this.playerName.Value = name;
    }

    public void Dispose()
    {
        this.score.Dispose();
        this.health.Dispose();
        this.playerName.Dispose();
        this.isAlive.Dispose();
    }
}
```

## Registration

```csharp
// In LifetimeScope
protected override void Configure(IContainerBuilder builder)
{
    builder.Register<PlayerDataController>(Lifetime.Singleton)
           .As<IPlayerDataController>();
}
```

## Consuming Data Controllers

### In Services (via constructor injection)

```csharp
public sealed class GameService
{
    private readonly IPlayerDataController playerData;

    [Preserve]
    public GameService(IPlayerDataController playerData)
    {
        this.playerData = playerData;
    }

    public bool CanPlayerAct()
    {
        return this.playerData.IsAlive.Value && this.playerData.Health.Value > 0;
    }
}
```

### In UI (reactive binding)

```csharp
public sealed class ScoreUI : MonoBehaviour
{
    [SerializeField] private TMP_Text scoreText;

    private IPlayerDataController playerData;
    private IDisposable subscription;

    [Inject]
    public void Construct(IPlayerDataController playerData)
    {
        this.playerData = playerData;
    }

    private void OnEnable()
    {
        this.subscription = this.playerData.Score.Subscribe(this.UpdateScoreText);
    }

    private void OnDisable()
    {
        this.subscription?.Dispose();
    }

    private void UpdateScoreText(int score)
    {
        this.scoreText.text = score.ToString("N0");
    }
}
```

## Data Controller Guidelines

### DO:
- ✅ Use `ReactiveProperty<T>` for mutable state
- ✅ Expose `IReadOnlyReactiveProperty<T>` on the interface
- ✅ Validate inputs (throw on invalid)
- ✅ Make the controller `IDisposable` to clean up reactive properties
- ✅ Use sealed class with constructor injection
- ✅ Keep data controllers focused (single responsibility)

### DON'T:
- ❌ Expose mutable `ReactiveProperty<T>` on the interface
- ❌ Put business logic in data controllers (they manage state, not logic)
- ❌ Subscribe to signals inside data controllers (keep them passive)
- ❌ Use `MonoBehaviour` for data controllers (they're plain C# classes)
- ❌ Store derived data — compute it from source properties

## Multiple Data Controllers

```csharp
// ✅ GOOD: Separate controllers for separate domains
public interface IInventoryDataController
{
    IReadOnlyReactiveProperty<IReadOnlyList<Item>> Items { get; }
    IReadOnlyReactiveProperty<int> Gold { get; }
}

public interface IQuestDataController
{
    IReadOnlyReactiveProperty<IReadOnlyList<Quest>> ActiveQuests { get; }
    IReadOnlyReactiveProperty<int> CompletedCount { get; }
}

// ❌ BAD: God data controller with everything
public interface IGameDataController
{
    // Player data
    IReadOnlyReactiveProperty<int> Score { get; }
    IReadOnlyReactiveProperty<int> Health { get; }
    // Inventory data
    IReadOnlyReactiveProperty<IReadOnlyList<Item>> Items { get; }
    // Quest data
    IReadOnlyReactiveProperty<IReadOnlyList<Quest>> ActiveQuests { get; }
    // Settings data
    IReadOnlyReactiveProperty<float> Volume { get; }
    // ... too much responsibility
}
```

## Persistence Integration

```csharp
// Data controller with save/load support
public sealed class PlayerDataController : IPlayerDataController, IDisposable
{
    private readonly ReactiveProperty<int> score;
    private readonly ISaveService saveService;

    [Preserve]
    public PlayerDataController(ISaveService saveService)
    {
        this.saveService = saveService;

        // Load initial state
        var savedData = saveService.Load<PlayerSaveData>();
        this.score = new ReactiveProperty<int>(savedData?.Score ?? 0);
    }

    public async UniTask SaveAsync()
    {
        var data = new PlayerSaveData { Score = this.score.Value };
        await this.saveService.SaveAsync(data);
    }
}
```

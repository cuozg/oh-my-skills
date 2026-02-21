# VContainer Dependency Injection Patterns

## Core Concepts

VContainer is the recommended DI framework. It provides constructor injection, lifetime management, and scoping.

## Registration Patterns

### LifetimeScope Configuration

```csharp
namespace YourProject.YourFeature;

public sealed class GameLifetimeScope : LifetimeScope
{
    protected override void Configure(IContainerBuilder builder)
    {
        // Services (singleton by default)
        builder.Register<PlayerService>(Lifetime.Singleton);
        builder.Register<InventoryService>(Lifetime.Singleton);

        // Interfaces → implementations
        builder.Register<IScoreCalculator, DefaultScoreCalculator>(Lifetime.Singleton);

        // Transient (new instance each resolve)
        builder.Register<EnemyFactory>(Lifetime.Transient);

        // MonoBehaviour entry points
        builder.RegisterEntryPoint<GameManager>();

        // Signal bus
        builder.RegisterSignalBus();
    }
}
```

### Constructor Injection (Preferred)

```csharp
// ✅ GOOD: Constructor injection with [Preserve]
public sealed class PlayerService
{
    private readonly ILogger logger; // Project-configured logger
    private readonly SignalBus signalBus;

    [Preserve] // Required for VContainer to find constructor
    public PlayerService(ILogger logger, SignalBus signalBus)
    {
        this.logger = logger;
        this.signalBus = signalBus;
    }
}

// ❌ BAD: Field injection
public sealed class PlayerService
{
    [Inject] private ILogger logger; // Harder to test, hidden dependencies
    [Inject] private SignalBus signalBus;
}
```

### MonoBehaviour Injection

```csharp
// MonoBehaviours can't use constructor injection — use [Inject] method
public sealed class PlayerView : MonoBehaviour
{
    private ILogger logger;
    private PlayerService playerService;

    [Inject]
    public void Construct(ILogger logger, PlayerService playerService)
    {
        this.logger = logger;
        this.playerService = playerService;
    }

    private void Start()
    {
        // Dependencies are available here
        this.logger.Info("PlayerView started");
    }
}
```

## IInitializable Pattern

```csharp
// ✅ GOOD: Use IInitializable for post-injection setup
public sealed class GameManager : IInitializable
{
    private readonly SignalBus signalBus;
    private readonly PlayerService playerService;

    [Preserve]
    public GameManager(SignalBus signalBus, PlayerService playerService)
    {
        this.signalBus = signalBus;
        this.playerService = playerService;
    }

    public void Initialize()
    {
        this.signalBus.Subscribe<GameStartedSignal>(this.OnGameStarted);
        this.playerService.LoadPlayers();
    }

    private void OnGameStarted(GameStartedSignal signal)
    {
        // Handle game start
    }
}
```

## Lifetime Scopes

```csharp
// Root scope — lives for entire application
public sealed class RootLifetimeScope : LifetimeScope
{
    protected override void Configure(IContainerBuilder builder)
    {
        // Global services
        builder.Register<ILogger, UnityLogger>(Lifetime.Singleton);
        builder.Register<SaveService>(Lifetime.Singleton);
        builder.RegisterSignalBus();
    }
}

// Scene scope — lives for scene lifetime, inherits parent
public sealed class GameSceneLifetimeScope : LifetimeScope
{
    protected override void Configure(IContainerBuilder builder)
    {
        // Scene-specific services
        builder.Register<PlayerService>(Lifetime.Singleton);
        builder.Register<EnemyManager>(Lifetime.Singleton);
        builder.RegisterEntryPoint<GameManager>();
    }
}
```

## Assembly Definition References

```json
// YourProject.YourFeature.asmdef
{
    "name": "YourProject.YourFeature",
    "references": [
        "VContainer",
        "UniTask",
        "YourProject.Core"
    ]
}
```

## Factory Pattern with VContainer

```csharp
// ✅ GOOD: Factory registered with DI
public sealed class EnemyFactory
{
    private readonly IObjectResolver resolver;

    [Preserve]
    public EnemyFactory(IObjectResolver resolver)
    {
        this.resolver = resolver;
    }

    public Enemy Create(EnemyConfig config)
    {
        var enemy = new Enemy(config);
        this.resolver.Inject(enemy); // Inject dependencies
        return enemy;
    }
}

// Registration
builder.Register<EnemyFactory>(Lifetime.Singleton);
```

## Common Anti-Patterns

```csharp
// ❌ BAD: Service locator
var service = Container.Resolve<IPlayerService>(); // Don't do this

// ❌ BAD: Static singleton
public static PlayerService Instance; // Use DI instead

// ❌ BAD: Finding dependencies manually
var service = FindObjectOfType<PlayerService>(); // Use injection

// ❌ BAD: Circular dependencies
// A depends on B, B depends on A → refactor to use signals/events
```

## Testing with VContainer

```csharp
// ✅ GOOD: Easy to test with constructor injection
[Test]
public void PlayerService_AddScore_IncreasesTotal()
{
    var mockLogger = new MockLogger();
    var mockSignalBus = new MockSignalBus();
    var service = new PlayerService(mockLogger, mockSignalBus);

    service.AddScore(100);

    Assert.AreEqual(100, service.TotalScore);
}
```

## Registration Cheat Sheet

| Registration | Lifetime | Use Case |
|:-------------|:---------|:---------|
| `Register<T>(Lifetime.Singleton)` | App/Scene | Services, managers |
| `Register<T>(Lifetime.Transient)` | Per-resolve | Factories, builders |
| `Register<I, T>(Lifetime.Singleton)` | App/Scene | Interface → implementation |
| `RegisterEntryPoint<T>()` | Scene | MonoBehaviour-like entry points |
| `RegisterComponent(instance)` | Scene | Existing MonoBehaviour |
| `RegisterFactory<T>()` | Scene | Typed factory |

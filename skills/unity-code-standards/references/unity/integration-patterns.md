# Integration Patterns

## Cross-System Communication

### Service → Service (Direct Dependency)

```csharp
// ✅ GOOD: One service depends on another via DI
public sealed class CombatService
{
    private readonly PlayerService playerService;
    private readonly SignalBus signalBus;

    [Preserve]
    public CombatService(PlayerService playerService, SignalBus signalBus)
    {
        this.playerService = playerService;
        this.signalBus = signalBus;
    }

    public void ApplyDamage(string playerId, int damage)
    {
        var player = this.playerService.GetPlayer(playerId);
        player.TakeDamage(damage);

        if (player.Health <= 0)
        {
            this.signalBus.Fire(new PlayerDiedSignal(playerId, "Combat"));
        }
    }
}
```

### Service → UI (Signal-Based)

```csharp
// Service fires signal
public sealed class ScoreService
{
    private readonly SignalBus signalBus;

    public void AddScore(int amount)
    {
        this.currentScore += amount;
        this.signalBus.Fire(new ScoreChangedSignal(this.currentScore - amount, this.currentScore));
    }
}

// UI listens for signal
public sealed class ScorePopup : MonoBehaviour
{
    private SignalBus signalBus;

    [Inject]
    public void Construct(SignalBus signalBus)
    {
        this.signalBus = signalBus;
    }

    private void OnEnable()
    {
        this.signalBus.Subscribe<ScoreChangedSignal>(this.OnScoreChanged);
    }

    private void OnDisable()
    {
        this.signalBus.Unsubscribe<ScoreChangedSignal>(this.OnScoreChanged);
    }

    private void OnScoreChanged(ScoreChangedSignal signal)
    {
        ShowPopup($"+{signal.NewScore - signal.OldScore}");
    }
}
```

### Data Controller → UI (Reactive Binding)

```csharp
// Data controller exposes reactive property
public interface IHealthDataController
{
    IReadOnlyReactiveProperty<float> HealthPercent { get; }
}

// UI binds reactively
public sealed class HealthBar : MonoBehaviour
{
    [SerializeField] private Image fillImage;

    private IHealthDataController healthData;
    private IDisposable subscription;

    [Inject]
    public void Construct(IHealthDataController healthData)
    {
        this.healthData = healthData;
    }

    private void OnEnable()
    {
        this.subscription = this.healthData.HealthPercent
            .Subscribe(percent => this.fillImage.fillAmount = percent);
    }

    private void OnDisable()
    {
        this.subscription?.Dispose();
    }
}
```

## Initialization Order

### Using IInitializable Priority

```csharp
// ✅ GOOD: Explicit initialization order
public sealed class GameBootstrap : IInitializable
{
    private readonly ConfigService configService;
    private readonly PlayerService playerService;
    private readonly UIService uiService;

    [Preserve]
    public GameBootstrap(
        ConfigService configService,
        PlayerService playerService,
        UIService uiService)
    {
        this.configService = configService;
        this.playerService = playerService;
        this.uiService = uiService;
    }

    public void Initialize()
    {
        // Explicit order — no dependency on Unity lifecycle
        this.configService.LoadConfig();
        this.playerService.Initialize();
        this.uiService.Initialize();
    }
}
```

## Scene Transition Pattern

```csharp
public sealed class SceneTransitionService
{
    private readonly ILogger logger;

    [Preserve]
    public SceneTransitionService(ILogger logger)
    {
        this.logger = logger;
    }

    public async UniTask LoadSceneAsync(string sceneName, CancellationToken ct = default)
    {
        this.logger.Info($"Loading scene: {sceneName}");

        // Show loading screen
        await ShowLoadingScreen(ct);

        // Load scene
        await SceneManager.LoadSceneAsync(sceneName)
            .ToUniTask(cancellationToken: ct);

        // Hide loading screen
        await HideLoadingScreen(ct);

        this.logger.Info($"Scene loaded: {sceneName}");
    }
}
```

## Plugin/Module Pattern

```csharp
// Each feature module has its own LifetimeScope
public sealed class InventoryModule : LifetimeScope
{
    protected override void Configure(IContainerBuilder builder)
    {
        builder.Register<InventoryService>(Lifetime.Singleton);
        builder.Register<InventoryDataController>(Lifetime.Singleton)
               .As<IInventoryDataController>();
        builder.RegisterEntryPoint<InventoryManager>();
    }
}

public sealed class QuestModule : LifetimeScope
{
    protected override void Configure(IContainerBuilder builder)
    {
        builder.Register<QuestService>(Lifetime.Singleton);
        builder.Register<QuestDataController>(Lifetime.Singleton)
               .As<IQuestDataController>();
        builder.RegisterEntryPoint<QuestManager>();
    }
}
```

## Error Handling Pattern

```csharp
// ✅ GOOD: Centralized error handling
public sealed class ErrorHandler : IInitializable, IDisposable
{
    private readonly SignalBus signalBus;
    private readonly ILogger logger;

    [Preserve]
    public ErrorHandler(SignalBus signalBus, ILogger logger)
    {
        this.signalBus = signalBus;
        this.logger = logger;
    }

    public void Initialize()
    {
        Application.logMessageReceived += this.OnLogMessage;
    }

    public void Dispose()
    {
        Application.logMessageReceived -= this.OnLogMessage;
    }

    private void OnLogMessage(string condition, string stackTrace, LogType type)
    {
        if (type is LogType.Exception or LogType.Error)
        {
            this.signalBus.Fire(new ErrorOccurredSignal(condition, stackTrace));
        }
    }
}
```

## Configuration Pattern

```csharp
// ScriptableObject for design-time configuration
[CreateAssetMenu(fileName = "GameConfig", menuName = "Config/Game")]
public sealed class GameConfig : ScriptableObject
{
    [field: SerializeField] public int MaxPlayers { get; private set; } = 4;
    [field: SerializeField] public float RoundTime { get; private set; } = 120f;
    [field: SerializeField] public float RespawnDelay { get; private set; } = 3f;
}

// Register in LifetimeScope
protected override void Configure(IContainerBuilder builder)
{
    // SerializeField reference on the LifetimeScope MonoBehaviour
    builder.RegisterInstance(this.gameConfig);
}
```

## Testing Integration Points

```csharp
// ✅ GOOD: Test signal flow
[Test]
public void ScoreService_AddScore_FiresSignal()
{
    var signalBus = new MockSignalBus();
    var service = new ScoreService(signalBus);

    service.AddScore(100);

    Assert.IsTrue(signalBus.WasFired<ScoreChangedSignal>());
    var signal = signalBus.GetLastFired<ScoreChangedSignal>();
    Assert.AreEqual(100, signal.NewScore);
}

// ✅ GOOD: Test data controller
[Test]
public void PlayerDataController_TakeDamage_ReducesHealth()
{
    var controller = new PlayerDataController(new MockLogger());

    controller.TakeDamage(30);

    Assert.AreEqual(70, controller.Health.Value);
    Assert.IsTrue(controller.IsAlive.Value);
}
```

# Core Patterns

Concrete implementation recipes. For coding rules and standards → load `unity-code-shared`.

## Service with Events

```csharp
namespace YourProject.Combat;

public readonly record struct DamageAppliedArgs(string DefenderId, int FinalDamage);

public sealed class DamageService : IDisposable
{
    private readonly ILogger logger;
    private readonly ICombatState combatState;
    public event Action<DamageAppliedArgs> DamageApplied;

    public DamageService(ILogger logger, ICombatState combatState)
    {
        this.logger = logger;
        this.combatState = combatState;
    }

    public void ApplyDamage(string defenderId, int rawDamage, int armor)
    {
        if (rawDamage <= 0) return;
        int final = Math.Max(1, rawDamage - armor);
        this.combatState.ApplyDamage(defenderId, final);
        this.DamageApplied?.Invoke(new(defenderId, final));
    }

    public void Dispose() { this.DamageApplied = null; }
}
```

Key: `sealed` | `readonly` fields | constructor injection | `IDisposable` | `readonly record struct` args

## State with Read-Only Interface

```csharp
namespace YourProject.Player;

public interface IPlayerState
{
    int Health { get; }
    bool IsAlive { get; }
    event Action<int> HealthChanged;
}

public sealed class PlayerState : IPlayerState, IDisposable
{
    private int health = 100;
    public int Health => this.health;
    public bool IsAlive => this.health > 0;
    public event Action<int> HealthChanged;

    public void ApplyDamage(int amount)
    {
        if (amount <= 0) return;
        this.health = Math.Max(0, this.health - amount);
        this.HealthChanged?.Invoke(this.health);
    }

    public void Dispose() { this.HealthChanged = null; }
}
```

Key: read-only interface for consumers | service owns mutation | events for notification

## MonoBehaviour View

```csharp
namespace YourProject.UI;

public sealed class HealthBarView : MonoBehaviour
{
    [Header("References")]
    [SerializeField] private Slider healthSlider;
    private IPlayerState playerState;

    public void Initialize(IPlayerState playerState) { this.playerState = playerState; }
    private void OnEnable()  { this.playerState.HealthChanged += this.UpdateHealth; }
    private void OnDisable() { this.playerState.HealthChanged -= this.UpdateHealth; }
    private void UpdateHealth(int health) { this.healthSlider.value = health; }
}
```

Key: `Initialize()` for DI | subscribe `OnEnable` / unsubscribe `OnDisable` | `sealed`


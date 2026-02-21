# Unity C# Patterns

## 1. Plain C# Service

```csharp
using System;

namespace YourProject.Combat;

/// <summary>
/// Calculates and applies damage between combatants.
/// </summary>
public sealed class DamageService : IDisposable
{
    private readonly ILogger logger;
    private readonly ICombatState combatState;

    /// <summary>Raised after damage is applied. Passes defender ID and final damage.</summary>
    public event Action<string, int> DamageApplied;

    public DamageService(ILogger logger, ICombatState combatState)
    {
        this.logger = logger;
        this.combatState = combatState;
    }

    /// <summary>
    /// Applies damage to a defender, accounting for armor.
    /// </summary>
    public void ApplyDamage(string defenderId, int rawDamage, int defenderArmor)
    {
        if (rawDamage <= 0) return;

        int finalDamage = this.CalculateDamage(rawDamage, defenderArmor);
        this.combatState.ApplyDamage(defenderId, finalDamage);
        this.DamageApplied?.Invoke(defenderId, finalDamage);
        this.logger.Info($"Damage applied: {finalDamage} to {defenderId}");
    }

    public void Dispose()
    {
        this.DamageApplied = null;
    }

    private int CalculateDamage(int rawDamage, int armor)
    {
        return Math.Max(1, rawDamage - armor);
    }
}
```

Rules: `sealed` class | `readonly` fields | Constructor injection | `IDisposable` for cleanup | `event Action<T>` for notifications | Named methods for event handlers (not lambdas)

## 2. C# Event Patterns

```csharp
namespace YourProject.Combat;

// Event args: readonly record struct for immutable event data
public readonly record struct AttackExecutedArgs(string AttackerId, string DefenderId, int Damage, int DefenderArmor);
public readonly record struct DamageAppliedArgs(string DefenderId, int FinalDamage);
public readonly record struct UnitDiedArgs(string UnitId);

// Centralized event hub for a domain
public sealed class CombatEvents
{
    public event Action<AttackExecutedArgs> AttackExecuted;
    public event Action<DamageAppliedArgs> DamageApplied;
    public event Action<UnitDiedArgs> UnitDied;
    public event Action GamePaused;

    public void RaiseAttackExecuted(AttackExecutedArgs args) => this.AttackExecuted?.Invoke(args);
    public void RaiseDamageApplied(DamageAppliedArgs args) => this.DamageApplied?.Invoke(args);
    public void RaiseUnitDied(UnitDiedArgs args) => this.UnitDied?.Invoke(args);
    public void RaiseGamePaused() => this.GamePaused?.Invoke();
}
```

Rules: `readonly record struct` for event data | Past-tense naming | Immutable data only | No methods or logic in event args | Named methods for subscribers (not lambdas)

## 3. UniTask Async

```csharp
using System;
using System.Threading;
using Cysharp.Threading.Tasks;

namespace YourProject.Loading;

/// <summary>
/// Loads player data from remote API.
/// </summary>
public sealed class PlayerDataLoader
{
    private readonly ILogger logger;
    private readonly INetworkService network;

    public PlayerDataLoader(ILogger logger, INetworkService network)
    {
        this.logger = logger;
        this.network = network;
    }

    /// <summary>
    /// Loads player data by ID. Returns null on failure.
    /// </summary>
    public async UniTask<PlayerData?> LoadAsync(string playerId, CancellationToken ct)
    {
        if (string.IsNullOrEmpty(playerId)) return null;

        try
        {
            string json = await this.network.GetAsync($"/api/player/{playerId}", ct);
            return JsonUtility.FromJson<PlayerData>(json);
        }
        catch (OperationCanceledException)
        {
            throw; // Always rethrow cancellation
        }
        catch (NetworkException ex)
        {
            this.logger.Error($"Failed to load player {playerId}: {ex.Message}");
            return null;
        }
    }

    /// <summary>
    /// Loads multiple players in parallel.
    /// </summary>
    public async UniTask<PlayerData?[]> LoadBatchAsync(string[] playerIds, CancellationToken ct)
    {
        var tasks = new UniTask<PlayerData?>[playerIds.Length];
        for (int i = 0; i < playerIds.Length; i++)
        {
            tasks[i] = this.LoadAsync(playerIds[i], ct);
        }
        return await UniTask.WhenAll(tasks);
    }
}
```

Rules: `async UniTask` (not `async Task`) | `CancellationToken` on every async method | Rethrow `OperationCanceledException` | Catch specific exceptions | No `async void`

## 4. State Management (Interface-Based)

```csharp
using System;

namespace YourProject.Player;

/// <summary>
/// Read-only interface for player data — exposed to consumers.
/// </summary>
public interface IPlayerState
{
    int Health { get; }
    int Score { get; }
    bool IsAlive { get; }
    event Action<int> HealthChanged;
    event Action<int> ScoreChanged;
}

/// <summary>
/// Owns and mutates player state. Registered as singleton service.
/// </summary>
public sealed class PlayerState : IPlayerState, IDisposable
{
    private int health = 100;
    private int score;

    public int Health => this.health;
    public int Score => this.score;
    public bool IsAlive => this.health > 0;

    public event Action<int> HealthChanged;
    public event Action<int> ScoreChanged;

    public void ApplyDamage(int amount)
    {
        if (amount <= 0) return;
        this.health = Math.Max(0, this.health - amount);
        this.HealthChanged?.Invoke(this.health);
    }

    public void AddScore(int points)
    {
        if (points <= 0) return;
        this.score += points;
        this.ScoreChanged?.Invoke(this.score);
    }

    public void Dispose()
    {
        this.HealthChanged = null;
        this.ScoreChanged = null;
    }
}
```

Rules: State owned by service class | Read-only interface for consumers | `event Action<T>` for change notifications | `IDisposable` to clean up | Guard clauses on mutations

## 5. MonoBehaviour with Dependencies

```csharp
using System;
using UnityEngine;
using UnityEngine.UI;

namespace YourProject.UI;

/// <summary>
/// Displays player health bar, subscribes to state events.
/// </summary>
public sealed class HealthBarView : MonoBehaviour
{
    [Header("UI References")]
    [Tooltip("Slider component for health display")]
    [SerializeField] private Slider healthSlider;

    [Header("Configuration")]
    [Tooltip("Duration of health bar animation in seconds")]
    [SerializeField] private float animationDuration = 0.3f;

    private IPlayerState playerState;

    /// <summary>
    /// Initializes the view with its dependencies. Call after instantiation.
    /// </summary>
    public void Initialize(IPlayerState playerState)
    {
        this.playerState = playerState;
    }

    private void OnEnable()
    {
        this.playerState.HealthChanged += this.UpdateHealth;
    }

    private void OnDisable()
    {
        this.playerState.HealthChanged -= this.UpdateHealth;
    }

    private void UpdateHealth(int health)
    {
        this.healthSlider.value = health;
    }
}
```

Rules: `Initialize()` method for dependency injection | Subscribe `OnEnable`, unsubscribe `OnDisable` | `sealed` by default

## 6. State Machine

```csharp
namespace YourProject.Character;

public enum CharacterState { Idle, Walking, Jumping, Attacking }

/// <summary>
/// Simple state machine with enter/exit callbacks.
/// </summary>
public sealed class CharacterStateMachine
{
    private CharacterState currentState;

    public CharacterState CurrentState => this.currentState;

    public void ChangeState(CharacterState newState)
    {
        if (this.currentState == newState) return;
        this.ExitState(this.currentState);
        this.currentState = newState;
        this.EnterState(newState);
    }

    private void ExitState(CharacterState state) { /* cleanup per state */ }
    private void EnterState(CharacterState state) { /* setup per state */ }
}
```

## 7. SO Config

```csharp
using UnityEngine;

namespace YourProject.Config;

/// <summary>
/// Character stats configuration. Clone before runtime modification.
/// </summary>
[CreateAssetMenu(menuName = "Game/Character Stats")]
public sealed class CharacterStats : ScriptableObject
{
    [Header("Combat")]
    [Tooltip("Base damage per attack")]
    [SerializeField] private int baseDamage = 10;

    [Tooltip("Seconds between attacks")]
    [SerializeField] private float attackCooldown = 0.5f;

    [Header("Movement")]
    [Tooltip("Movement speed in units per second")]
    [SerializeField] private float moveSpeed = 5f;

    public int BaseDamage => this.baseDamage;
    public float AttackCooldown => this.attackCooldown;
    public float MoveSpeed => this.moveSpeed;
}

// Usage: clone before runtime modification
// private CharacterStats runtime;
// void Awake() => runtime = Instantiate(baseStats);
// void OnDestroy() { if (runtime) Destroy(runtime); }
```

## 8. Object Pool

```csharp
using UnityEngine;
using UnityEngine.Pool;

namespace YourProject.Combat;

/// <summary>
/// Pool for projectile instances to avoid GC allocations.
/// </summary>
public sealed class ProjectilePool : MonoBehaviour
{
    [Header("Pool Configuration")]
    [Tooltip("Prefab to pool")]
    [SerializeField] private Projectile prefab;

    [Tooltip("Initial pool capacity")]
    [SerializeField] private int capacity = 20;

    [Tooltip("Maximum pool size")]
    [SerializeField] private int maxSize = 100;

    private ObjectPool<Projectile> pool;

    private void Awake()
    {
        this.pool = new ObjectPool<Projectile>(
            createFunc: () => Instantiate(this.prefab),
            actionOnGet: p => p.gameObject.SetActive(true),
            actionOnRelease: p => p.gameObject.SetActive(false),
            actionOnDestroy: p => Destroy(p.gameObject),
            defaultCapacity: this.capacity,
            maxSize: this.maxSize);
    }

    public Projectile Get() => this.pool.Get();
    public void Return(Projectile p) => this.pool.Release(p);
}
```

## 9. Performance

```csharp
// Cache components in Awake — never GetComponent in Update
private Rigidbody rb;
private Camera cam;
private Transform cachedTransform;

private void Awake()
{
    this.rb = GetComponent<Rigidbody>();
    this.cam = Camera.main;
    this.cachedTransform = this.transform;
}

// Zero-alloc hot path — pre-allocated array, manual loop
private readonly RaycastHit[] hits = new RaycastHit[32];

private void Update()
{
    int count = Physics.RaycastNonAlloc(this.cachedTransform.position, Vector3.forward, this.hits);
    int nearCount = 0;
    for (int i = 0; i < count; i++)
    {
        if (this.hits[i].distance < 10f) nearCount++;
    }
}
```

| Avoid                           | Do                                  |
| ------------------------------- | ----------------------------------- |
| `GetComponent` in Update        | Cache in Awake                      |
| `Camera.main` in loops          | Cache reference                     |
| String concat in Update         | StringBuilder or cache              |
| `new` in hot paths              | Pool / pre-allocate                 |
| LINQ in Update                  | Manual loops                        |
| `Find` / `FindObjectOfType`     | `[SerializeField]` or dependency injection  |

## 10. Error Handling

```csharp
// Catch specific exceptions — let OperationCanceledException propagate
public async UniTask<PlayerData?> LoadAsync(string id, CancellationToken ct)
{
    try
    {
        string json = await this.network.GetAsync($"/api/player/{id}", ct);
        return JsonUtility.FromJson<PlayerData>(json);
    }
    catch (OperationCanceledException)
    {
        throw; // Always rethrow
    }
    catch (NetworkException ex)
    {
        this.logger.Error($"Load failed for {id}: {ex.Message}");
        return null;
    }
}
```

Rules: Catch specific types | Rethrow `OperationCanceledException` | Use `ILogger` (not `Debug.LogError`) | No empty catch blocks

## 11. Cleanup

```csharp
/// <summary>
/// Proper resource cleanup for MonoBehaviours.
/// </summary>
public sealed class ManagedView : MonoBehaviour
{
    private CancellationTokenSource cts;
    private IPlayerState playerState;

    /// <summary>
    /// Initializes the view with its dependencies.
    /// </summary>
    public void Initialize(IPlayerState playerState)
    {
        this.playerState = playerState;
    }

    private void OnEnable()
    {
        this.cts = new CancellationTokenSource();
        // Subscribe to events
        this.playerState.HealthChanged += this.OnValueChanged;
    }

    private void OnDisable()
    {
        // Cancel async operations
        this.cts?.Cancel();
        this.cts?.Dispose();
        this.cts = null;

        // Unsubscribe from events
        this.playerState.HealthChanged -= this.OnValueChanged;
    }

    private void OnDestroy()
    {
        // Dispose native resources, cloned ScriptableObjects
    }

    private void OnValueChanged(int value) { /* handle update */ }
}
```

Rules: Cancel `CancellationTokenSource` in `OnDisable` | Unsubscribe from events in `OnDisable` | Dispose native resources in `OnDestroy`

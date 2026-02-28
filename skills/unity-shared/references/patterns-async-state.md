# Advanced Patterns

For coding rules and standards → load `unity-shared`.

## Async with UniTask

```csharp
namespace YourProject.Loading;
public sealed class PlayerDataLoader
{
    private readonly ILogger logger;
    private readonly INetworkService network;
    public PlayerDataLoader(ILogger logger, INetworkService network)
    {
        this.logger = logger;
        this.network = network;
    }
    public async UniTask<PlayerData?> LoadAsync(string playerId, CancellationToken ct)
    {
        if (string.IsNullOrEmpty(playerId)) return null;
        try
        {
            string json = await this.network.GetAsync($"/api/player/{playerId}", ct);
            return JsonUtility.FromJson<PlayerData>(json);
        }
        catch (OperationCanceledException) { throw; }
        catch (NetworkException ex)
        {
            this.logger.Error($"Load failed for {playerId}: {ex.Message}");
            return null;
        }
    }
}
```
Key: `async UniTask` | `CancellationToken` always | rethrow `OperationCanceledException` | catch specific

## State Machine

```csharp
namespace YourProject.Character;
public enum CharacterState { Idle, Walking, Jumping, Attacking }
public sealed class CharacterStateMachine
{
    private CharacterState currentState;
    public CharacterState CurrentState => this.currentState;
    public void TransitionTo(CharacterState newState)
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

## ScriptableObject Config

```csharp
namespace YourProject.Config;
[CreateAssetMenu(menuName = "Game/Character Stats")]
public sealed class CharacterStats : ScriptableObject
{
    [Header("Combat")]
    [SerializeField] private int baseDamage = 10;
    [SerializeField] private float attackCooldown = 0.5f;
    public int BaseDamage => this.baseDamage;
    public float AttackCooldown => this.attackCooldown;
}
// Clone before runtime modification: runtime = Instantiate(baseStats);
// OnDestroy: if (runtime) Destroy(runtime);
```

## Cleanup & CTS

```csharp
public sealed class ManagedView : MonoBehaviour
{
    private CancellationTokenSource cts;
    private IPlayerState playerState;
    public void Initialize(IPlayerState playerState) { this.playerState = playerState; }
    private void OnEnable()
    {
        this.cts = new CancellationTokenSource();
        this.playerState.HealthChanged += this.OnValueChanged;
    }
    private void OnDisable()
    {
        this.cts?.Cancel();
        this.cts?.Dispose();
        this.cts = null;
        this.playerState.HealthChanged -= this.OnValueChanged;
    }
    private void OnDestroy() { /* Dispose native resources, cloned SOs */ }
    private void OnValueChanged(int value) { /* handle */ }
}
```
Key: CTS created `OnEnable`, cancelled+disposed `OnDisable` | native resources in `OnDestroy`
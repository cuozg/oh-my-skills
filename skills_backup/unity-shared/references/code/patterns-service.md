# Core Patterns
Concrete implementation recipes. For rules → load `unity-shared`.

## Service with Events
```csharp
public readonly record struct DamageArgs(string Id, int FinalDamage);

public sealed class DamageService : IDisposable {
    private readonly ICombatState state;
    public event Action<DamageArgs> DamageApplied;

    public DamageService(ICombatState state) => this.state = state;

    public void ApplyDamage(string id, int raw, int armor) {
        if (raw <= 0) return;
        int final = Math.Max(1, raw - armor);
        this.state.ApplyDamage(id, final);
        this.DamageApplied?.Invoke(new(id, final));
    }
    public void Dispose() => this.DamageApplied = null;
}
```
Key: `sealed` | DI | `IDisposable` | `readonly record struct`

## State with Read-Only Interface
```csharp
public interface IPlayerState {
    int Health { get; }
    event Action<int> HealthChanged;
}

public sealed class PlayerState : IPlayerState, IDisposable {
    public int Health { get; private set; } = 100;
    public event Action<int> HealthChanged;

    public void ApplyDamage(int amount) {
        if (amount <= 0) return;
        Health = Math.Max(0, Health - amount);
        HealthChanged?.Invoke(Health);
    }
    public void Dispose() => HealthChanged = null;
}
```
Key: read-only interface | state owns mutation

## MonoBehaviour View
```csharp
public sealed class HealthBarView : MonoBehaviour {
    [SerializeField] private Slider slider;
    private IPlayerState state;

    public void Init(IPlayerState state) => this.state = state;
    private void OnEnable()  { if (state != null) state.HealthChanged += UpdateHealth; }
    private void OnDisable() { if (state != null) state.HealthChanged -= UpdateHealth; }
    private void UpdateHealth(int h) => slider.value = h;
}
```
Key: DI via `Init()` | `OnEnable`/`OnDisable` lifecycle | `sealed`

## Command
```csharp
public interface ICommand { void Execute(); void Undo(); }

public sealed class MoveCommand : ICommand {
    private readonly Transform t; private readonly Vector3 dir;
    public MoveCommand(Transform t, Vector3 dir) { this.t = t; this.dir = dir; }
    public void Execute() => t.position += dir;
    public void Undo() => t.position -= dir;
}

public sealed class CommandHistory {
    private readonly Stack<ICommand> history = new();
    public void Execute(ICommand cmd) { cmd.Execute(); history.Push(cmd); }
    public void Undo() { if (history.TryPop(out var cmd)) cmd.Undo(); }
}
```
Key: `ICommand` | `Execute`/`Undo` | `Stack` for history

## Observer via ScriptableObject Channel
```csharp
[CreateAssetMenu(menuName = "Channels/Void Event")]
public sealed class VoidEventChannelSO : ScriptableObject {
    public event Action OnEventRaised;
    public void RaiseEvent() => OnEventRaised?.Invoke();
}

public sealed class Listener : MonoBehaviour {
    [SerializeField] private VoidEventChannelSO channel;
    [SerializeField] private UnityEvent onEvent;

    private void OnEnable()  { if (channel != null) channel.OnEventRaised += Respond; }
    private void OnDisable() { if (channel != null) channel.OnEventRaised -= Respond; }
    private void Respond() => onEvent?.Invoke();
}
```
Key: `ScriptableObject` channel | `OnEnable`/`OnDisable` lifecycle

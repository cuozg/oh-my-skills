# Advanced Patterns

For coding rules and standards → load `unity-shared`.

## Async with UniTask
```csharp
public sealed class PlayerDataLoader
{
    public async UniTask<PlayerData?> LoadAsync(string id, INetworkService net, CancellationToken ct)
    {
        try {
            string json = await net.GetAsync($"/api/player/{id}", ct);
            return JsonUtility.FromJson<PlayerData>(json);
        }
        catch (OperationCanceledException) { throw; }
        catch (Exception ex) { Debug.LogError(ex); return null; }
    }
}
```
Key: `async UniTask` | `CancellationToken` always | rethrow `OperationCanceledException`.

## Cleanup & CTS
```csharp
public sealed class ManagedView : MonoBehaviour
{
    private CancellationTokenSource cts;
    private void OnEnable() => this.cts = new CancellationTokenSource();
    private void OnDisable() { 
        this.cts?.Cancel(); 
        this.cts?.Dispose(); 
        this.cts = null; 
    }
    private void OnDestroy() { /* Dispose native resources, cloned SOs */ }
}
```
Key: CTS created `OnEnable`, cancelled+disposed `OnDisable` | native resources in `OnDestroy`.

## Jobs & Burst
```csharp
[BurstCompile]
public struct HeavyCalcJob : IJobParallelFor
{
    [ReadOnly] public NativeArray<float> Inputs;
    public NativeArray<float> Results;
    public void Execute(int i) => this.Results[i] = math.exp(this.Inputs[i]);
}
// Usage: var inArray = new NativeArray<float>(1000, Allocator.TempJob);
// var outArray = new NativeArray<float>(1000, Allocator.TempJob);
// var job = new HeavyCalcJob { Inputs = inArray, Results = outArray };
// job.Schedule(inArray.Length, 64).Complete(); // Blocks main thread until done
// inArray.Dispose(); outArray.Dispose(); // Mandatory native cleanup
```
Key: `[BurstCompile]` | strict `NativeArray` lifecycle | offload heavy computation.

## State Machine
```csharp
public enum CharacterState { Idle, Walk, Jump }
public sealed class CharacterStateMachine
{
    public CharacterState CurrentState { get; private set; }
    public void TransitionTo(CharacterState newState)
    {
        if (this.CurrentState == newState) return;
        this.ExitState(this.CurrentState);
        this.CurrentState = newState;
        this.EnterState(newState);
    }
    private void ExitState(CharacterState state) { /* cleanup */ }
    private void EnterState(CharacterState state) { /* setup */ }
}
```

## Hierarchical State Machine (HSM)
```csharp
public abstract class BaseState { public abstract void Update(); }
public sealed class GroundedState : BaseState
{
    private BaseState subState; // e.g., IdleState or RunState
    public override void Update() => this.subState?.Update();
    public void SetSubState(BaseState newState) {
        /* this.subState?.Exit(); */
        this.subState = newState;
        /* this.subState?.Enter(); */
    }
}
```
Key: Enum FSM for simple logic. Sub-states routing for hierarchical logic.

## ScriptableObject Config
```csharp
[CreateAssetMenu(menuName = "Game/Character Stats")]
public sealed class CharacterStats : ScriptableObject
{
    [field: SerializeField] public int BaseDamage { get; private set; } = 10;
    [field: SerializeField] public float AttackCooldown { get; private set; } = 0.5f;
}
// Clone before modification: var runtime = Instantiate(baseConfig);
// OnDestroy: if (runtime) Destroy(runtime); // Prevent leaks
```

# Architecture Patterns — Multi-File Unity C#

For Service Locator / DI patterns → `read_skill_file("unity-standards", "references/code-standards/dependencies.md")`
For SO event channels → `read_skill_file("unity-standards", "references/code-standards/events.md")`

## State Machine (enum + handler classes)

```csharp
// IState.cs
public interface IState { void Enter(); void Tick(); void Exit(); }

// StateMachine.cs
public sealed class StateMachine
{
    private IState _current;
    public void SetState(IState next)
    {
        _current?.Exit();
        _current = next;
        _current.Enter();
    }
    public void Tick() => _current?.Tick();
}
```

Each state = separate class implementing `IState`. Machine lives on the MonoBehaviour, calls `Tick()` in `Update`.

## MVC / MVP (UI separation)

```
Model:      Pure C# data class or ScriptableObject (no MonoBehaviour)
View:       MonoBehaviour on UI — binds to UnityEvents, exposes SetX() methods
Presenter:  MonoBehaviour — subscribes to Model changes, calls View.SetX()
```

```csharp
// HealthPresenter.cs
public sealed class HealthPresenter : MonoBehaviour
{
    [SerializeField] private HealthModel model;
    [SerializeField] private HealthView view;
    private void OnEnable() => model.OnChanged += Refresh;
    private void OnDisable() => model.OnChanged -= Refresh;
    private void Refresh() => view.SetHealth(model.Current, model.Max);
}
```

## Command Pattern (undo/redo, input decoupling)

```csharp
// ICommand.cs
public interface ICommand { void Execute(); void Undo(); }

// CommandInvoker.cs
public sealed class CommandInvoker
{
    private readonly Stack<ICommand> _history = new();
    public void Execute(ICommand cmd) { cmd.Execute(); _history.Push(cmd); }
    public void Undo() { if (_history.Count > 0) _history.Pop().Undo(); }
}
```

## Object Pool Pattern (Unity 2021+)

```csharp
using UnityEngine.Pool;

public sealed class BulletSpawner : MonoBehaviour
{
    [SerializeField] private GameObject _bulletPrefab;
    private ObjectPool<GameObject> _pool;

    void Awake()
    {
        _pool = new ObjectPool<GameObject>(
            createFunc: () => Instantiate(_bulletPrefab),
            actionOnGet: obj => obj.SetActive(true),
            actionOnRelease: obj => obj.SetActive(false),
            actionOnDestroy: obj => Destroy(obj),
            defaultCapacity: 20,
            maxSize: 100
        );
    }

    public GameObject Spawn(Vector3 pos)
    {
        var bullet = _pool.Get();
        bullet.transform.position = pos;
        return bullet;
    }

    public void Despawn(GameObject bullet) => _pool.Release(bullet);
}
```

Pre-2021: Use custom pool with `Queue<T>` and manual activate/deactivate.

## Strategy Pattern via ScriptableObject

```csharp
public abstract class AttackStrategy : ScriptableObject
{
    public abstract void Execute(Transform attacker, IDamageable target);
}

[CreateAssetMenu(menuName = "Strategy/Melee Attack")]
public sealed class MeleeAttack : AttackStrategy
{
    [SerializeField] private float _damage = 10f;
    [SerializeField] private float _range = 2f;
    public override void Execute(Transform attacker, IDamageable target)
    {
        if (Vector3.Distance(attacker.position, ((Component)target).transform.position) <= _range)
            target.TakeDamage(_damage, attacker.position);
    }
}

// Consumer — swap strategy via Inspector
public sealed class Enemy : MonoBehaviour
{
    [SerializeField] private AttackStrategy _attackStrategy;
    public void Attack(IDamageable target) => _attackStrategy.Execute(transform, target);
}
```

Designers create SO assets per strategy variant — no code changes needed for new behaviors.

## Mediator Pattern (Event Bus)

```csharp
public sealed class EventBus
{
    readonly Dictionary<System.Type, List<System.Delegate>> _handlers = new();

    public void Subscribe<T>(Action<T> handler)
    {
        var type = typeof(T);
        if (!_handlers.ContainsKey(type)) _handlers[type] = new List<System.Delegate>();
        _handlers[type].Add(handler);
    }

    public void Unsubscribe<T>(Action<T> handler)
    {
        if (_handlers.TryGetValue(typeof(T), out var list)) list.Remove(handler);
    }

    public void Publish<T>(T evt)
    {
        if (_handlers.TryGetValue(typeof(T), out var list))
            foreach (var handler in list) ((Action<T>)handler)(evt);
    }
}
// ⚠️ Use sparingly — prefer SO event channels for most decoupling needs.
```

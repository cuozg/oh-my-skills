# Architecture Patterns — Advanced

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

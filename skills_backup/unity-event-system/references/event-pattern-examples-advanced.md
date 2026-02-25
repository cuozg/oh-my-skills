# Event Pattern Examples - Advanced Patterns

## Priority Event Bus

```csharp
public static class PriorityEventBus<T> where T : struct
{
    private static readonly Dictionary<int, List<Action<T>>> _subs = new();
    
    public static void Subscribe(Action<T> handler, int priority = 0) {
        if (!_subs.ContainsKey(priority)) _subs[priority] = new();
        _subs[priority].Add(handler);
    }
    
    public static void Publish(T evt) {
        // Iterate from highest priority (reverse order)
        foreach (var priority in _subs.Keys.OrderByDescending(x => x)) {
            foreach (var sub in _subs[priority]) sub?.Invoke(evt);
        }
    }
}
// Usage: PriorityEventBus<DamageEvent>.Subscribe(OnDamage, priority: 100);
```

## Filtered Event Subscription

```csharp
public class EventBusFiltered<T> where T : struct, IFilterable
{
    private Dictionary<IEventFilter<T>, List<Action<T>>> _subscriptions = new();
    
    public void Subscribe(Action<T> handler, IEventFilter<T> filter = null) {
        filter = filter ?? new AllPassFilter<T>();
        if (!_subscriptions.ContainsKey(filter)) _subscriptions[filter] = new();
        _subscriptions[filter].Add(handler);
    }
    
    public void Publish(T evt) {
        foreach (var kvp in _subscriptions) {
            if (kvp.Key.Matches(evt)) {
                foreach (var sub in kvp.Value) sub?.Invoke(evt);
            }
        }
    }
}

// Example filter
public class DamageTypeFilter : IEventFilter<DamageEvent> {
    private DamageType _type;
    public bool Matches(DamageEvent e) => e.Type == _type;
}
```

## Observable Wrapper (Reactive Pattern)

```csharp
public class Observable<T> {
    private event Action<T> _subscribers;
    public void Subscribe(Action<T> callback) => _subscribers += callback;
    public void Unsubscribe(Action<T> callback) => _subscribers -= callback;
    public void Emit(T value) => _subscribers?.Invoke(value);
    public void Clear() => _subscribers = null;
}

// Usage
var playerDamage = new Observable<int>();
playerDamage.Subscribe(amount => Debug.Log($"Took {amount} damage"));
playerDamage.Emit(50);  // Prints: Took 50 damage
```

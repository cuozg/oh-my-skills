# Event Pattern Examples

## C# Events
```csharp
public class PlayerHealth : MonoBehaviour
{
    public event Action<int, int> OnHealthChanged; // current, max
    public event Action OnDeath;
    [SerializeField] private int _maxHealth = 100;
    private int _currentHealth;
    private void Awake() => _currentHealth = _maxHealth;
    public void TakeDamage(int amt)
    {
        if (_currentHealth <= 0) return;
        _currentHealth = Mathf.Max(0, _currentHealth - amt);
        OnHealthChanged?.Invoke(_currentHealth, _maxHealth);
        if (_currentHealth <= 0) OnDeath?.Invoke();
    }
}
// Subscribe OnEnable, unsubscribe OnDisable — prevents leaks
public class HealthBarUI : MonoBehaviour
{
    [SerializeField] private PlayerHealth _health;
    [SerializeField] private Slider _slider;
    private void OnEnable() { if (_health) _health.OnHealthChanged += Handle; }
    private void OnDisable() { if (_health) _health.OnHealthChanged -= Handle; }
    private void Handle(int cur, int max) { if (_slider) _slider.value = (float)cur / max; }
}
```

## SO Event Channel (GameEvent)
```csharp
[CreateAssetMenu(menuName = "Events/Game Event")]
public class GameEvent : ScriptableObject
{
    private readonly List<GameEventListener> _listeners = new();
    public void Raise() { for (int i = _listeners.Count - 1; i >= 0; i--) _listeners[i].OnEventRaised(); }
    public void RegisterListener(GameEventListener l) { if (!_listeners.Contains(l)) _listeners.Add(l); }
    public void UnregisterListener(GameEventListener l) => _listeners.Remove(l);
}
public class GameEventListener : MonoBehaviour
{
    [SerializeField] private GameEvent _event;
    [SerializeField] private UnityEvent _response;
    private void OnEnable() { if (_event) _event.RegisterListener(this); }
    private void OnDisable() { if (_event) _event.UnregisterListener(this); }
    public void OnEventRaised() => _response?.Invoke();
}
```

## Typed Event Channel (Generic)
```csharp
public abstract class TypedGameEvent<T> : ScriptableObject
{
    private readonly List<ITypedGameEventListener<T>> _listeners = new();
    public void Raise(T val) { for (int i = _listeners.Count - 1; i >= 0; i--) _listeners[i].OnEventRaised(val); }
    public void Register(ITypedGameEventListener<T> l) { if (!_listeners.Contains(l)) _listeners.Add(l); }
    public void Unregister(ITypedGameEventListener<T> l) => _listeners.Remove(l);
}
public interface ITypedGameEventListener<T> { void OnEventRaised(T value); }
// Concrete: subclass per type (Unity can't serialize open generics)
[CreateAssetMenu(menuName = "Events/Int Event")] public class IntGameEvent : TypedGameEvent<int> { }
[CreateAssetMenu(menuName = "Events/Float Event")] public class FloatGameEvent : TypedGameEvent<float> { }
// Concrete listener base
public abstract class TypedGameEventListener<TEvent, TVal> : MonoBehaviour, ITypedGameEventListener<TVal>
    where TEvent : TypedGameEvent<TVal>
{
    [SerializeField] private TEvent _event;
    [SerializeField] private UnityEvent<TVal> _response;
    private void OnEnable() { if (_event) _event.Register(this); }
    private void OnDisable() { if (_event) _event.Unregister(this); }
    public void OnEventRaised(TVal val) => _response?.Invoke(val);
}
public class IntGameEventListener : TypedGameEventListener<IntGameEvent, int> { }
```

## Generic Event Bus
```csharp
public static class EventBus<T> where T : struct
{
    private static readonly HashSet<Action<T>> _subs = new();
    public static void Subscribe(Action<T> h) => _subs.Add(h);
    public static void Unsubscribe(Action<T> h) => _subs.Remove(h);
    public static void Publish(T e) { foreach (var s in _subs) s?.Invoke(e); }
    public static void Clear() => _subs.Clear();
}
// Event structs
public struct PlayerDamagedEvent { public int Amount; public int Remaining; public Vector3 HitPos; }
// Publisher — fully decoupled
public class DamageDealer : MonoBehaviour
{
    public void Deal(int amt, Vector3 pos) =>
        EventBus<PlayerDamagedEvent>.Publish(new() { Amount = amt, Remaining = 75, HitPos = pos });
}
// Subscriber
public class DamageVFX : MonoBehaviour
{
    [SerializeField] private GameObject _hitFx;
    private void OnEnable() => EventBus<PlayerDamagedEvent>.Subscribe(OnHit);
    private void OnDisable() => EventBus<PlayerDamagedEvent>.Unsubscribe(OnHit);
    private void OnHit(PlayerDamagedEvent e) { if (_hitFx) Instantiate(_hitFx, e.HitPos, Quaternion.identity); }
}
```

# Event Pattern Examples

## Key Patterns

### C# Events and Delegates

```csharp
/// <summary>
/// Player health system broadcasting changes via C# events.
/// Fastest dispatch — use when all listeners are in code.
/// </summary>
public class PlayerHealth : MonoBehaviour
{
    /// <summary>Fired when health changes. Args: currentHealth, maxHealth.</summary>
    public event Action<int, int> OnHealthChanged;

    /// <summary>Fired once when health reaches zero.</summary>
    public event Action OnDeath;

    [SerializeField] private int _maxHealth = 100;

    // Current health — clamped between 0 and _maxHealth
    private int _currentHealth;

    private void Awake()
    {
        _currentHealth = _maxHealth;
    }

    /// <summary>
    /// Apply damage, broadcast change, trigger death if zero.
    /// </summary>
    public void TakeDamage(int amount)
    {
        if (_currentHealth <= 0) return; // Already dead

        _currentHealth = Mathf.Max(0, _currentHealth - amount);
        OnHealthChanged?.Invoke(_currentHealth, _maxHealth);

        if (_currentHealth <= 0)
        {
            OnDeath?.Invoke();
        }
    }
}

/// <summary>
/// Health bar UI — subscribes via C# event, no direct coupling to UI framework.
/// </summary>
public class HealthBarUI : MonoBehaviour
{
    [SerializeField] private PlayerHealth _playerHealth;
    [SerializeField] private UnityEngine.UI.Slider _slider;

    // CRITICAL: Subscribe in OnEnable, unsubscribe in OnDisable
    private void OnEnable()
    {
        if (_playerHealth != null)
        {
            _playerHealth.OnHealthChanged += HandleHealthChanged;
        }
    }

    private void OnDisable()
    {
        if (_playerHealth != null)
        {
            _playerHealth.OnHealthChanged -= HandleHealthChanged;
        }
    }

    private void HandleHealthChanged(int current, int max)
    {
        if (_slider != null)
        {
            _slider.value = (float)current / max;
        }
    }
}
```

### ScriptableObject Event Channel (GameEvent Pattern)

```csharp
/// <summary>
/// Void event channel — a ScriptableObject that acts as a decoupled event.
/// Create instances via Assets > Create > Events > Game Event.
/// </summary>
[CreateAssetMenu(fileName = "NewGameEvent", menuName = "Events/Game Event")]
public class GameEvent : ScriptableObject
{
    // Listeners registered at runtime
    private readonly List<GameEventListener> _listeners = new();

    /// <summary>
    /// Raise this event — notifies all registered listeners.
    /// </summary>
    public void Raise()
    {
        // Iterate backwards so listeners can safely unregister during callback
        for (int i = _listeners.Count - 1; i >= 0; i--)
        {
            _listeners[i].OnEventRaised();
        }
    }

    /// <summary>Register a listener. Called automatically by GameEventListener.OnEnable.</summary>
    public void RegisterListener(GameEventListener listener)
    {
        if (!_listeners.Contains(listener))
        {
            _listeners.Add(listener);
        }
    }

    /// <summary>Unregister a listener. Called automatically by GameEventListener.OnDisable.</summary>
    public void UnregisterListener(GameEventListener listener)
    {
        _listeners.Remove(listener);
    }
}

/// <summary>
/// MonoBehaviour that listens to a GameEvent and fires a UnityEvent response.
/// Attach to any GameObject, drag the GameEvent asset, and wire response in Inspector.
/// </summary>
public class GameEventListener : MonoBehaviour
{
    [Tooltip("The GameEvent ScriptableObject to listen for")]
    [SerializeField] private GameEvent _event;

    [Tooltip("Response to invoke when the event is raised")]
    [SerializeField] private UnityEngine.Events.UnityEvent _response;

    private void OnEnable()
    {
        if (_event != null)
        {
            _event.RegisterListener(this);
        }
    }

    private void OnDisable()
    {
        if (_event != null)
        {
            _event.UnregisterListener(this);
        }
    }

    /// <summary>
    /// Called by GameEvent.Raise() — invokes the UnityEvent response.
    /// </summary>
    public void OnEventRaised()
    {
        _response?.Invoke();
    }
}
```

### Typed ScriptableObject Event Channel (Generic)

```csharp
/// <summary>
/// Generic typed event channel — carries a payload of type T.
/// Subclass for each concrete type needed (Unity cannot serialize open generics).
/// </summary>
public abstract class TypedGameEvent<T> : ScriptableObject
{
    private readonly List<ITypedGameEventListener<T>> _listeners = new();

    /// <summary>
    /// Raise this event with a payload.
    /// </summary>
    public void Raise(T value)
    {
        for (int i = _listeners.Count - 1; i >= 0; i--)
        {
            _listeners[i].OnEventRaised(value);
        }
    }

    public void RegisterListener(ITypedGameEventListener<T> listener)
    {
        if (!_listeners.Contains(listener))
        {
            _listeners.Add(listener);
        }
    }

    public void UnregisterListener(ITypedGameEventListener<T> listener)
    {
        _listeners.Remove(listener);
    }
}

/// <summary>
/// Listener interface for typed events.
/// </summary>
public interface ITypedGameEventListener<T>
{
    void OnEventRaised(T value);
}

// --- Concrete implementations ---

/// <summary>
/// Integer event channel — use for score changes, damage amounts, etc.
/// </summary>
[CreateAssetMenu(fileName = "NewIntEvent", menuName = "Events/Int Event")]
public class IntGameEvent : TypedGameEvent<int> { }

/// <summary>
/// Float event channel — use for health percentages, timers, etc.
/// </summary>
[CreateAssetMenu(fileName = "NewFloatEvent", menuName = "Events/Float Event")]
public class FloatGameEvent : TypedGameEvent<float> { }

/// <summary>
/// String event channel — use for dialogue lines, notification text, etc.
/// </summary>
[CreateAssetMenu(fileName = "NewStringEvent", menuName = "Events/String Event")]
public class StringGameEvent : TypedGameEvent<string> { }

/// <summary>
/// Generic typed listener with UnityEvent response.
/// </summary>
public abstract class TypedGameEventListener<TEvent, TValue> : MonoBehaviour, ITypedGameEventListener<TValue>
    where TEvent : TypedGameEvent<TValue>
{
    [SerializeField] private TEvent _event;
    [SerializeField] private UnityEngine.Events.UnityEvent<TValue> _response;

    private void OnEnable()
    {
        if (_event != null) _event.RegisterListener(this);
    }

    private void OnDisable()
    {
        if (_event != null) _event.UnregisterListener(this);
    }

    public void OnEventRaised(TValue value)
    {
        _response?.Invoke(value);
    }
}

/// <summary>Concrete listener for IntGameEvent.</summary>
public class IntGameEventListener : TypedGameEventListener<IntGameEvent, int> { }

/// <summary>Concrete listener for FloatGameEvent.</summary>
public class FloatGameEventListener : TypedGameEventListener<FloatGameEvent, float> { }
```

### Generic Event Bus

```csharp
/// <summary>
/// Centralized event bus for global game-wide messaging.
/// Fully type-safe — events are dispatched by their type.
/// No references needed between publisher and subscriber.
/// </summary>
public static class EventBus<T> where T : struct
{
    // Subscriber list for this event type
    private static readonly HashSet<Action<T>> _subscribers = new();

    /// <summary>
    /// Subscribe to events of type T. Call in OnEnable.
    /// </summary>
    public static void Subscribe(Action<T> handler)
    {
        _subscribers.Add(handler);
    }

    /// <summary>
    /// Unsubscribe from events of type T. Call in OnDisable.
    /// </summary>
    public static void Unsubscribe(Action<T> handler)
    {
        _subscribers.Remove(handler);
    }

    /// <summary>
    /// Publish an event to all subscribers of type T.
    /// </summary>
    public static void Publish(T eventData)
    {
        foreach (var subscriber in _subscribers)
        {
            subscriber?.Invoke(eventData);
        }
    }

    /// <summary>
    /// Remove all subscribers. Call during scene unload or cleanup.
    /// </summary>
    public static void Clear()
    {
        _subscribers.Clear();
    }
}

// --- Event struct definitions ---

/// <summary>Event fired when player takes damage.</summary>
public struct PlayerDamagedEvent
{
    public int DamageAmount;
    public int RemainingHealth;
    public Vector3 HitPosition;
}

/// <summary>Event fired when a level is completed.</summary>
public struct LevelCompletedEvent
{
    public int LevelIndex;
    public float CompletionTime;
    public int StarsEarned;
}

// --- Usage example ---

/// <summary>
/// Damage dealer — publishes damage events via the bus.
/// </summary>
public class DamageDealer : MonoBehaviour
{
    public void DealDamage(int amount, Vector3 hitPos)
    {
        EventBus<PlayerDamagedEvent>.Publish(new PlayerDamagedEvent
        {
            DamageAmount = amount,
            RemainingHealth = 75, // From actual health system
            HitPosition = hitPos,
        });
    }
}

/// <summary>
/// Damage VFX — subscribes to damage events, spawns hit effects.
/// Completely decoupled from the damage dealer.
/// </summary>
public class DamageVFX : MonoBehaviour
{
    [SerializeField] private GameObject _hitEffectPrefab;

    private void OnEnable()
    {
        EventBus<PlayerDamagedEvent>.Subscribe(HandleDamage);
    }

    private void OnDisable()
    {
        EventBus<PlayerDamagedEvent>.Unsubscribe(HandleDamage);
    }

    private void HandleDamage(PlayerDamagedEvent evt)
    {
        if (_hitEffectPrefab != null)
        {
            Instantiate(_hitEffectPrefab, evt.HitPosition, Quaternion.identity);
        }
    }
}
```

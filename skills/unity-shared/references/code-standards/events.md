# Events

## C# Events — Preferred

```csharp
public sealed class Health : MonoBehaviour
{
    public event Action<float> OnHealthChanged;
    public event Action OnDeath;

    float _current;

    public void TakeDamage(float amount)
    {
        _current -= amount;
        OnHealthChanged?.Invoke(_current);
        if (_current <= 0f) OnDeath?.Invoke();
    }
}
```

## Subscribe/Unsubscribe — OnEnable/OnDisable

```csharp
public sealed class HealthUI : MonoBehaviour
{
    [SerializeField] Health _health;
    [SerializeField] Slider _slider;

    void OnEnable() => _health.OnHealthChanged += UpdateSlider;
    void OnDisable() => _health.OnHealthChanged -= UpdateSlider;
    void UpdateSlider(float value) => _slider.value = value;
}
```

## UnityEvent — Inspector Wiring

```csharp
using UnityEngine.Events;

public sealed class Interactable : MonoBehaviour
{
    [SerializeField] UnityEvent _onInteract;
    [SerializeField] UnityEvent<string> _onMessage;

    public void Interact()
    {
        _onInteract?.Invoke();
        _onMessage?.Invoke("Activated!");
    }
}
```

| Feature | C# event | UnityEvent |
|---------|----------|------------|
| Performance | ✅ Fast | ❌ Slower (reflection) |
| Inspector | ❌ No | ✅ Yes |
| Serialized | ❌ No | ✅ Yes |
| Use for | Code-to-code | Designer wiring |

## ScriptableObject Event Channels

```csharp
[CreateAssetMenu(menuName = "Events/Void Event")]
public class VoidEventChannel : ScriptableObject
{
    event Action _listeners;
    public void Register(Action cb) => _listeners += cb;
    public void Unregister(Action cb) => _listeners -= cb;
    public void Raise() => _listeners?.Invoke();
}
```

Usage — decoupled, no direct references:

```csharp
public sealed class Player : MonoBehaviour
{
    [SerializeField] VoidEventChannel _onDied;
    void OnEnable() => _onDied.Register(HandleDeath);
    void OnDisable() => _onDied.Unregister(HandleDeath);
    void HandleDeath() { /* ... */ }
}
```

## Event Naming

| Pattern | Example |
|---------|---------|
| `On` + PastParticiple | `OnDamageReceived` |
| `On` + Noun + Verb | `OnHealthChanged` |
| Handler method | `HandleDeath`, `HandleInput` |
| Channel asset | `PlayerDied_Event.asset` |

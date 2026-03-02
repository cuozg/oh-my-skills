# Architecture Patterns — Multi-File Unity C#

## Service Locator (lightweight DI alternative)

```csharp
// ServiceLocator.cs
public static class ServiceLocator
{
    private static readonly Dictionary<Type, object> _services = new();
    public static void Register<T>(T service) => _services[typeof(T)] = service;
    public static T Get<T>() => (T)_services[typeof(T)];
    public static bool TryGet<T>(out T service)
    {
        if (_services.TryGetValue(typeof(T), out var obj)) { service = (T)obj; return true; }
        service = default; return false;
    }
    public static void Clear() => _services.Clear();
}
```

Register in bootstrap MonoBehaviour `Awake()`. Consumers call `ServiceLocator.Get<IAudioService>()`.

## ScriptableObject Event Bus (decoupled cross-system messaging)

```csharp
// GameEvent.cs — base channel
public abstract class GameEvent<T> : ScriptableObject
{
    private readonly List<System.Action<T>> _listeners = new();
    public void Raise(T value) { for (int i = _listeners.Count - 1; i >= 0; i--) _listeners[i](value); }
    public void Register(System.Action<T> cb) => _listeners.Add(cb);
    public void Unregister(System.Action<T> cb) => _listeners.Remove(cb);
}

// IntEvent.cs — typed channel
[CreateAssetMenu(menuName = "Events/Int Event")]
public sealed class IntEvent : GameEvent<int> { }
```

Register in `OnEnable`, unregister in `OnDisable`. Use `event Action<T>` for code-only; `UnityEvent<T>` for inspector wiring.

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

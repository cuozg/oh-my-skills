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

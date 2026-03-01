## SOLID in Unity
- **SRP**: `MonoBehaviour` = view/lifecycle only. Logic in plain C# services, data in `ScriptableObject`.
- **OCP**: Use `ScriptableObject` channels for extension without modification.
- **LSP**: Prefer composition over deep inheritance hierarchies.
- **ISP**: Small focused interfaces (`IMovable`, `IDamageable`), not god interfaces.
- **DIP**: Depend on interfaces. Inject via constructor (plain C#) or `[Inject]` method (`MonoBehaviour`).

## Dependency Injection
- **VContainer**: Primary DI container (fast, GC-friendly, actively maintained by hadashiA).
- **MonoBehaviours**: Use `[Inject]` on METHOD, not constructor (constructors don't work for MBs).
- **Pure C#**: Use constructor injection with `readonly` fields.
- **Zenject/Extenject**: Legacy, avoid for new projects.

```csharp
public class GameLifetimeScope : LifetimeScope
{
    protected override void Configure(IContainerBuilder builder)
    {
        builder.Register<IDamageService, DamageService>(Lifetime.Singleton);
        builder.RegisterComponentInHierarchy<PlayerView>();
    }
}
```

## Event Systems — ScriptableObject Channels
- Based on Unity's official PaddleGameSO sample (Ryan Hipple Unite 2017 talk).
- `VoidEventChannelSO`: `ScriptableObject` with event `Action`, `RaiseEvent()` method.
- `GenericEventChannelSO<T>`: Typed variant.
- `VoidEventChannelListener`: `MonoBehaviour` that subscribes `OnEnable`, unsubscribes `OnDisable`.
- `RuntimeSetSO<T>`: `ScriptableObject`-based collection replacing singletons for runtime object tracking.

```csharp
[CreateAssetMenu(menuName = "Events/Void Event Channel")]
public class VoidEventChannelSO : ScriptableObject
{
    public event UnityAction OnEventRaised;
    public void RaiseEvent() => OnEventRaised?.Invoke();
}
```

## Assembly Definitions
- **Naming**: `CompanyName.ProjectName.Feature` (e.g., `Acme.Puzzle.Core`).
- **Dependencies**: No circular dependencies — use interfaces in shared assembly.
- **References**: Use GUID references (not names) for stability.
- **Separation**: Editor code in separate `.Editor` asmdef, tests in separate `.Tests` asmdef.
- **Optimization**: Set `Auto Referenced: false` for library assemblies.

## Folder Structure
Standard layout:
```text
Assets/
  Scripts/
    Core/         (shared interfaces, data, events)
    Features/     (per-feature folders)
    Services/     (plain C# services)
    Views/        (MonoBehaviour UI/display)
    Editor/       (editor-only code)
  ScriptableObjects/
  Prefabs/
  Scenes/
```
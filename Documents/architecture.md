# Unity C# Architecture Reference
> Sources: [PaddleGameSO](https://github.com/UnityTechnologies/PaddleGameSO) (1cf2568) · [VContainer](https://github.com/hadashiA/VContainer) (49bdeaa)

## 1. SOLID in Unity
- **SRP** — One MonoBehaviour = one responsibility. Push logic into SOs or plain C# classes.
- **OCP** — Extend via SO event channels and interfaces, not by modifying callers.
- **DIP** — Depend on interfaces; inject via VContainer or SO references. Never `FindObjectOfType`.
- **ISP** — Small focused interfaces (`IAttackable`, `IDamageable`) over fat base classes.

## 2. ScriptableObject Patterns

**Event Channel** — cross-scene signals, zero coupling, Inspector-serializable:
```csharp
[CreateAssetMenu(menuName = "Events/Void Event Channel")]
public class VoidEventChannelSO : ScriptableObject {
    public UnityAction OnEventRaised;
    public void RaiseEvent() => OnEventRaised?.Invoke();
}
// Typed variant: abstract class GenericEventChannelSO<T>
// Concrete:      class FloatEventChannelSO : GenericEventChannelSO<float> {}
```

**Subscribe rule** — always pair with OnEnable/OnDisable:
```csharp
[SerializeField] VoidEventChannelSO _onGoalHit;
void OnEnable()  => _onGoalHit.OnEventRaised += HandleGoal;
void OnDisable() => _onGoalHit.OnEventRaised -= HandleGoal;
```

**RuntimeSet** — replaces singleton managers for object collections:
```csharp
public abstract class RuntimeSetSO<T> : ScriptableObject where T : MonoBehaviour {
    readonly List<T> _items = new();
    public IReadOnlyList<T> Items => _items;
    public void Add(T t)    { if (!_items.Contains(t)) _items.Add(t); }
    public void Remove(T t) => _items.Remove(t);
}
```

**InputReader SO** — decouples InputSystem from gameplay MonoBehaviours:
```csharp
[CreateAssetMenu] public class InputReaderSO : ScriptableObject, IGameplayActions {
    public event UnityAction<Vector2> Moved = delegate { };
    void OnEnable()  { _controls = new PlayerControls(); _controls.Gameplay.SetCallbacks(this); _controls.Enable(); }
    void OnDisable() => _controls.Disable();
    public void OnMove(InputAction.CallbackContext ctx) => Moved.Invoke(ctx.ReadValue<Vector2>());
}
```

## 3. Dependency Injection — VContainer
```csharp
public class GameLifetimeScope : LifetimeScope {      // MonoBehaviour, ExecutionOrder -5000
    protected override void Configure(IContainerBuilder builder) {
        builder.Register<ScoreService>(Lifetime.Singleton);          // pure C# → constructor inject
        builder.RegisterComponentInHierarchy<PlayerController>();     // MonoBehaviour → [Inject] method
        builder.UseEntryPoints(ep => ep.Add<GameManager>());          // IStartable / ITickable
    }
}
// MonoBehaviour: method injection ONLY
public class PlayerController : MonoBehaviour {
    InputReaderSO _input;
    [Inject] public void Construct(InputReaderSO input) => _input = input;
}
```
> **Rule**: MonoBehaviours → `[Inject]` on a method. Pure C# → constructor. Never `new MonoBehaviour()`.

## 4. Event System — When to Use What
| Pattern | Use When | Coupling |
|---------|----------|----------|
| SO Event Channel | Cross-scene, designer-visible, Inspector-serialized | None |
| C# event / delegate | Same-assembly, performance-critical | Compile-time |
| Static event bus | Global last-resort (analytics, crash logs only) | Global — avoid |

## 5. Assembly Definitions
```
Core.asmdef                    ← no references; base types only
Features/Combat/Combat.asmdef  ← refs: Core
Features/UI/UI.asmdef          ← refs: Core
Editor/MyGame.Editor.asmdef    ← includePlatforms: ["Editor"]; refs: Core
Tests/MyGame.Tests.asmdef      ← testAssemblies: true; refs: Core
```
**Rules:** No cyclic refs. `autoReferenced: false` on all. Reference by **GUID** not name. Editor platform only on editor asmdefs. Tests never ship.

## 6. Folder Structure
```
Assets/_Project/
  Data/           ← .asset files (SOs, configs)
  Prefabs/
  Scenes/
  Scripts/
    Core/         ← interfaces, base SOs, shared utilities  → Core.asmdef
    Features/     ← one subfolder per feature slice         → one .asmdef per slice
    Editor/       ← editor-only scripts                     → MyGame.Editor.asmdef
    Tests/                                                   → MyGame.Tests.asmdef
Plugins/          ← third-party; outside _Project
```
> Match namespace to folder path. One `.asmdef` per `Scripts/` subfolder.

# Architecture, Systems Design & Platform

> Consolidated from: architecture-patterns.md, architecture-patterns-advanced.md, project-structure.md, dependencies.md, dependencies-advanced.md, events.md, refactoring-patterns.md, multi-file-workflow.md, single-file-runtime-workflow.md, editor-patterns.md, gizmos-handles.md, webgl-restrictions.md

---

## Project Folder Structure

### Layout Strategy

Use **feature-based** organization. Keep related assets together so features are self-contained and portable.

```
Assets/
├── _Project/                    # underscore prefix → sorts to top
│   ├── Core/                    # interfaces, base classes, shared data
│   │   ├── Scripts/             # Company.Project.Core.asmdef
│   │   └── Tests/               # Company.Project.Core.Tests.asmdef
│   ├── Features/
│   │   ├── Player/
│   │   │   ├── Scripts/         # Company.Project.Player.asmdef
│   │   │   ├── Prefabs/
│   │   │   ├── Animations/
│   │   │   ├── Art/
│   │   │   └── Tests/           # Company.Project.Player.Tests.asmdef
│   │   └── Combat/
│   │       ├── Scripts/         # Company.Project.Combat.asmdef → refs Core
│   │       └── Tests/
│   ├── Infrastructure/          # DI installers, bootstrapping, scene management
│   │   └── Scripts/             # Company.Project.Infrastructure.asmdef → refs Core + features
│   ├── UI/                      # shared UXML, USS, UI controllers
│   ├── Settings/                # ScriptableObject configs, InputActions, render pipeline
│   ├── Art/                     # shared materials, shaders, textures
│   ├── Audio/                   # shared SFX, music, mixer assets
│   └── Scenes/
├── Plugins/                     # 3rd-party (Odin, DoTween, etc.)
└── Resources/                   # AVOID — use Addressables instead
```

### Assembly Definitions

| Assembly | References | Purpose |
|----------|-----------|---------|
| `Company.Project.Core` | none | interfaces, enums, data, events |
| `Company.Project.{Feature}` | Core | feature runtime code |
| `Company.Project.Infrastructure` | Core + features | DI wiring, bootstrapping |
| `Company.Project.{Feature}.Editor` | feature + Core | editor tooling for feature |
| `Company.Project.{Feature}.Tests` | feature + NUnit | test assemblies |

- Name = namespace: `Company.Project.Feature` → folder `Features/Feature/Scripts/`
- Set `autoReferenced: false` on all except top-level game assembly
- No circular dependencies — route through Core interfaces
- Test assemblies: check "Test Assemblies" toggle, reference NUnit + target assembly

### Special Folders

| Folder | Behavior |
|--------|----------|
| `Editor/` | excluded from builds, `UnityEditor` API access |
| `Resources/` | included in build, loaded via `Resources.Load` — avoid, use Addressables |
| `StreamingAssets/` | copied raw to device — videos, databases, initial configs |
| `Plugins/` | native libs (.dll/.so), compiled before project scripts |
| `Gizmos/` | icons for `Gizmos.DrawIcon()` |

### Namespace Convention

```
Company.Project.Feature
```

Map 1:1 to folder path. If folder moves, namespace moves.

```csharp
// Assets/_Project/Features/Combat/Scripts/DamageCalculator.cs
namespace Company.Project.Combat
{
    public class DamageCalculator { }
}
```

### .gitignore Essentials

```gitignore
[Ll]ibrary/
[Tt]emp/
[Oo]bj/
[Bb]uild/
[Bb]uilds/
[Ll]ogs/
[Uu]tmp/
[Mm]emoryCaptures/
.vs/
.idea/
*.csproj
*.sln
.DS_Store
```

### Project Structure Rules

- Feature-based over type-based — keeps features portable
- Every script folder gets an `.asmdef` — prevents monolithic recompilation
- `_Project/` prefix keeps project code above Unity-generated folders
- `Settings/` for all ScriptableObject configs — not buried in `Resources/`
- `Editor/` folders can exist at any depth — Unity detects them automatically
- Never put runtime code in `Editor/` or reference Editor assemblies from runtime
- `Resources/` loads everything into memory at build — migrate to Addressables for large projects
- Use `Addressables` for dynamic asset loading — supports remote bundles, memory management, and async loading

---

## Dependency Management

### Constructor Injection — Pure C#

```csharp
public class DamageCalculator
{
    readonly IArmorService _armor;
    readonly IBuffService _buffs;
    public DamageCalculator(IArmorService armor, IBuffService buffs)
    {
        _armor = armor ?? throw new System.ArgumentNullException(nameof(armor));
        _buffs = buffs ?? throw new System.ArgumentNullException(nameof(buffs));
    }
    public float Calculate(float raw) => raw * _armor.Reduction * _buffs.Multiplier;
}
```

### [Inject] for MonoBehaviours — VContainer

```csharp
using VContainer;

public sealed class EnemySpawner : MonoBehaviour
{
    [Inject] readonly IEnemyFactory _factory;
    [Inject] readonly IWaveConfig _config;

    void Start() => _factory.Spawn(_config.FirstWave);
}

public class GameLifetimeScope : LifetimeScope
{
    protected override void Configure(IContainerBuilder builder)
    {
        builder.Register<IEnemyFactory, EnemyFactory>(Lifetime.Singleton);
        builder.RegisterComponentInHierarchy<EnemySpawner>();
    }
}
```

### ScriptableObject Injection

```csharp
[CreateAssetMenu(menuName = "Config/Combat")]
public class CombatConfig : ScriptableObject
{
    [SerializeField] float _baseDamage = 10f;
    [SerializeField] AnimationCurve _falloff;
    public float BaseDamage => _baseDamage;
    public float GetFalloff(float dist) => _falloff.Evaluate(dist);
}

public sealed class Weapon : MonoBehaviour
{
    [SerializeField] CombatConfig _config; // drag-drop in Inspector
}
```

### Service Locator — Fallback Only

```csharp
// Use ONLY when DI isn't available (e.g., legacy code)
public static class ServiceLocator
{
    static readonly Dictionary<System.Type, object> _services = new();
    public static void Register<T>(T service) => _services[typeof(T)] = service;
    public static T Get<T>() => (T)_services[typeof(T)];
}
// ⚠️ Prefer DI — service locator hides dependencies
```

### Assembly Definition Boundaries

```
Game.Core.asmdef           ← interfaces, data, no dependencies
Game.Combat.asmdef         ← references Core only
Game.UI.asmdef             ← references Core only
Game.Infrastructure.asmdef ← references Core, wires implementations
```

```json
{ "name": "Game.Combat", "references": ["Game.Core"], "autoReferenced": false }
```

### Avoid Singletons

```csharp
// ❌ Static singleton — untestable, hidden dependency
public class GameManager : MonoBehaviour { public static GameManager Instance; void Awake() => Instance = this; }

// ✅ Interface + DI
public interface IGameManager { void StartGame(); }
public sealed class GameManager : MonoBehaviour, IGameManager { }

// ✅ SO-based if unavoidable
[CreateAssetMenu] public class GameManagerRef : ScriptableObject { [System.NonSerialized] public IGameManager Current; }
```

### Zenject — Alternative DI Framework

```csharp
using Zenject;

public sealed class EnemySpawner : MonoBehaviour
{
    [Inject] readonly IEnemyFactory _factory;
    [Inject] readonly IWaveConfig _config;
    void Start() => _factory.Spawn(_config.FirstWave);
}

public class GameInstaller : MonoInstaller
{
    public override void InstallBindings()
    {
        Container.Bind<IEnemyFactory>().To<EnemyFactory>().AsSingle();
        Container.Bind<IWaveConfig>().To<WaveConfig>().AsSingle();
        Container.BindInterfacesAndSelfTo<EnemySpawner>().FromComponentInHierarchy().AsSingle();
    }
}
```

| Feature | VContainer | Zenject |
|---------|-----------|---------|
| Performance | ✅ Faster (codegen) | ❌ Slower (reflection) |
| API style | `builder.Register<T>()` | `Container.Bind<T>().To<T>()` |
| Unity support | 2019.4+ | 2018.4+ |
| Maintenance | Active | Community-maintained |
| Recommendation | ✅ Preferred for new projects | Legacy/existing projects |

---

## Events

### C# Events — Preferred

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

### Subscribe/Unsubscribe — OnEnable/OnDisable

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

### UnityEvent — Inspector Wiring

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

### ScriptableObject Event Channels

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

### Event Naming

| Pattern | Example |
|---------|---------|
| `On` + PastParticiple | `OnDamageReceived` |
| `On` + Noun + Verb | `OnHealthChanged` |
| Handler method | `HandleDeath`, `HandleInput` |
| Channel asset | `PlayerDied_Event.asset` |

### Event Safety Rules

- **Always** unsubscribe in `OnDisable`/`OnDestroy` — leaked subscriptions cause null refs and memory leaks
- **Never** raise events inside `OnDestroy` — listeners may already be destroyed
- **Null-check** before invoking: `OnDeath?.Invoke()` not `OnDeath.Invoke()`
- Clear all event listeners when pooling objects: `OnDeath = null;` in reset

---

## Architecture Patterns

### State Machine (enum + handler classes)

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

### MVC / MVP (UI separation)

```
Model:      Pure C# data class or ScriptableObject (no MonoBehaviour)
View:       MonoBehaviour on UI — binds to UnityEvents, exposes SetX() methods
Presenter:  MonoBehaviour — subscribes to Model changes, calls View.SetX()
```

```csharp
public sealed class HealthPresenter : MonoBehaviour
{
    [SerializeField] private HealthModel model;
    [SerializeField] private HealthView view;
    private void OnEnable() => model.OnChanged += Refresh;
    private void OnDisable() => model.OnChanged -= Refresh;
    private void Refresh() => view.SetHealth(model.Current, model.Max);
}
```

### Command Pattern (undo/redo, input decoupling)

```csharp
public interface ICommand { void Execute(); void Undo(); }

public sealed class CommandInvoker
{
    private readonly Stack<ICommand> _history = new();
    public void Execute(ICommand cmd) { cmd.Execute(); _history.Push(cmd); }
    public void Undo() { if (_history.Count > 0) _history.Pop().Undo(); }
}
```

### Strategy Pattern via ScriptableObject

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

### Mediator Pattern (Event Bus)

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

---

## Refactoring Patterns

### Extract Interface

**When:** Multiple consumers depend on concrete class, or need testability.

```csharp
// Before: consumers depend on AudioManager directly
public sealed class AudioManager : MonoBehaviour { public void PlaySFX(AudioClip clip) { } }

// After: extract IAudioService, consumers depend on interface
public interface IAudioService { void PlaySFX(AudioClip clip); }
public sealed class AudioManager : MonoBehaviour, IAudioService { public void PlaySFX(AudioClip clip) { } }
```

### Extract Class (Decompose God Class)

**When:** Class exceeds ~200 lines or has 3+ unrelated responsibilities.

```
Before: PlayerController.cs (400 lines - movement + combat + inventory + audio)
After:
  PlayerMovement.cs     ← movement logic
  PlayerCombat.cs       ← attack, damage
  PlayerInventory.cs    ← items, equipment
  PlayerController.cs   ← orchestrates via references to above
```

### Replace Inheritance With Composition

```csharp
public sealed class Enemy : MonoBehaviour
{
    [SerializeField] private MovementStrategy movement;
    [SerializeField] private AttackStrategy attack;

    private void Update()
    {
        movement.Execute(transform);
        attack.TryAttack();
    }
}
```

### Extract ScriptableObject Data

```csharp
// Before: magic numbers in MonoBehaviour
[SerializeField] private float speed = 5f, jumpForce = 10f, gravity = -20f;

// After: data in SO
[CreateAssetMenu(menuName = "Config/Movement")]
public sealed class MovementConfig : ScriptableObject
{
    [SerializeField] private float _speed = 5f;
    [SerializeField] private float _jumpForce = 10f;
    [SerializeField] private float _gravity = -20f;

    public float Speed => _speed;
    public float JumpForce => _jumpForce;
    public float Gravity => _gravity;
}

[SerializeField] private MovementConfig config;
```

### Migrate To Event-Driven

```csharp
// Before: EnemyAI directly calls UIManager.ShowDamage()
_uiManager.ShowDamage(amount);

// After: raise event, UI subscribes independently
[SerializeField] private GameEvent<float> onDamageDealt;
onDamageDealt.Raise(amount);
```

### Refactoring Safety Checklist

- [ ] Identify all callers before changing signatures
- [ ] Preserve public API unless explicitly changing it
- [ ] One refactoring type per pass — do not extract, rename, and restructure simultaneously
- [ ] If 5+ files are affected, create a file change plan before starting
- [ ] Check for serialized field references that may break in the Inspector

---

## Workflow Guides

### Single-File Runtime Workflow

**Route Before Writing:**
- One runtime `.cs` file or narrow bug fix → `unity-code` (Quick mode)
- 2+ runtime files, new abstractions, or registration steps → `unity-code` (Deep mode)
- Structural cleanup without behavior change → `unity-code` (Quick or Deep by file count) — load § Refactoring Patterns
- Editor tooling or inspectors → `unity-editor`
- UI Toolkit screens or styling → `unity-uitoolkit`
- Tests → `unity-test-unit`

**Scope Checklist:**
- [ ] Runtime code only
- [ ] One `.cs` file is enough
- [ ] No extra helper, editor, or test files needed
- [ ] No new scene, prefab, or bootstrap wiring beyond what one file can expose

**Implementation Rules:**
- One type per file; file name matches type name
- Solve the requested behavior completely inside the file
- Narrow bug fix: change the smallest correct code path; skip opportunistic refactors
- Keep the surface minimal; avoid invented namespaces, XML docs, attributes, or helper polish unless the prompt or local files call for them
- No `TODO`, stubs, placeholder returns, or "wire this later" notes

### Multi-File Workflow

**File Creation Order** — write files in dependency order:

```
1. Interfaces / base types          (IState, IDamageable)
2. Data models / ScriptableObjects  (EnemyData, GameEvent<T>)
3. Core implementations             (StateMachine, ServiceLocator)
4. Concrete implementations         (PatrolState, ChaseState)
5. MonoBehaviour consumers          (EnemyController, HealthPresenter)
6. Wiring / registration            (GameBootstrap, SceneSetup)
```

**Namespace Strategy:**

```
Company.Project.Feature           ← feature root
Company.Project.Feature.Data      ← SOs, configs, enums
Company.Project.Feature.Events    ← event channels
Company.Project.Feature.UI        ← views, presenters
```

Match existing project namespaces. If none exist, use `Game.Feature`. One namespace = one folder.

**Assembly Definition Awareness:**

Before adding cross-system references, check for `.asmdef` files:
- Never add circular asmdef references
- Shared types (interfaces, events, data) belong in the lowest-level asmdef
- If no asmdefs exist, don't create them unless asked

**Cross-File Dependency Checklist:**
- [ ] Which existing files will be modified?
- [ ] Which new files will be created?
- [ ] Are there asmdef boundaries to respect?
- [ ] Which interfaces/base types must exist before implementations?
- [ ] How does the new code register with existing systems?
- [ ] Which ScriptableObject assets need to be created?

**Scoping Heuristic:**

| Files | Complexity | Approach |
|-------|-----------|----------|
| 2–3   | Low       | Write sequentially, verify at end |
| 4–7   | Medium    | Plan file list, verify per dependency tier |
| 8+    | High      | Consider unity-plan-quick first, then implement |

**Verification Rhythm:**
- 2–3 files: diagnostics at the end
- 4+ files: verify after shared abstractions, again after concrete implementations, once more after wiring

**Integration Points:**
- **Inspector refs** — SerializeField drag-drop
- **Service locator** — Register in bootstrap
- **Event channels** — Create SO asset, wire in OnEnable/OnDisable
- **Static access** — Singleton.Instance (use sparingly)

---

## Editor Patterns

### EditorWindow

```csharp
// Editor/MyToolWindow.cs
using UnityEditor;
using UnityEngine;

public class MyToolWindow : EditorWindow
{
    [MenuItem("Tools/My Tool")]
    public static void Open() => GetWindow<MyToolWindow>("My Tool");

    private void OnGUI()
    {
        EditorGUILayout.LabelField("Settings", EditorStyles.boldLabel);
        // add controls here
    }
}
```

### CustomEditor

```csharp
// Editor/MyComponentEditor.cs
using UnityEditor;

[CustomEditor(typeof(MyComponent))]
public class MyComponentEditor : Editor
{
    SerializedProperty _speed;

    private void OnEnable() => _speed = serializedObject.FindProperty("speed");

    public override void OnInspectorGUI()
    {
        serializedObject.Update();
        base.OnInspectorGUI();
        EditorGUILayout.PropertyField(_speed);
        if (GUILayout.Button("Apply")) ((MyComponent)target).Apply();
        serializedObject.ApplyModifiedProperties();
    }
}
```

### PropertyDrawer

```csharp
// Editor/RangeDrawer.cs
using UnityEditor;
using UnityEngine;

[CustomPropertyDrawer(typeof(RangedFloat))]
public class RangedFloatDrawer : PropertyDrawer
{
    public override void OnGUI(Rect pos, SerializedProperty prop, GUIContent label)
    {
        EditorGUI.BeginProperty(pos, label, prop);
        var min = prop.FindPropertyRelative("min");
        var max = prop.FindPropertyRelative("max");
        float lo = min.floatValue, hi = max.floatValue;
        EditorGUI.MinMaxSlider(pos, label, ref lo, ref hi, 0f, 100f);
        min.floatValue = lo; max.floatValue = hi;
        EditorGUI.EndProperty();
    }
}
```

### Gizmos — OnDrawGizmos / OnDrawGizmosSelected

```csharp
// In a MonoBehaviour
private void OnDrawGizmos()
{
    Gizmos.color = Color.yellow;
    Gizmos.DrawWireSphere(transform.position, detectionRadius);
}

private void OnDrawGizmosSelected()
{
    Gizmos.color = Color.red;
    Gizmos.DrawLine(transform.position, targetPoint);
}
```

### Handles in CustomEditor (OnSceneGUI)

```csharp
// Editor/PatrolEditor.cs
[CustomEditor(typeof(PatrolPath))]
public class PatrolPathEditor : Editor
{
    private void OnSceneGUI()
    {
        var path = (PatrolPath)target;
        Handles.color = Color.cyan;

        for (int i = 0; i < path.points.Length; i++)
        {
            EditorGUI.BeginChangeCheck();
            Vector3 newPos = Handles.PositionHandle(path.points[i], Quaternion.identity);
            if (EditorGUI.EndChangeCheck())
            {
                Undo.RecordObject(path, "Move Patrol Point");
                path.points[i] = newPos;
            }
        }

        for (int i = 0; i + 1 < path.points.Length; i++)
            Handles.DrawLine(path.points[i], path.points[i + 1]);
    }
}
```

### Editor Notes

- Always place editor scripts under an `Editor/` folder (any depth)
- `SerializedProperty` path uses field name (camelCase), not display name
- Call `Undo.RecordObject(target, "label")` before direct field mutations
- Use `EditorUtility.SetDirty(target)` after direct mutations to mark scene dirty
- `OnDrawGizmos` runs always; `OnDrawGizmosSelected` only when object is selected
- Wrap `using UnityEditor` in `#if UNITY_EDITOR` inside Runtime assemblies
- `Handles.PositionHandle` returns world-space position; always check `EndChangeCheck`

---

## Web Platform Restrictions

### Treat These As Safe Defaults

Web platform behavior shifts across Unity versions, browser versions, and hosting setups. This captures conservative guidance. For exact support claims, cross-check official docs.

### Unsupported Or Constrained APIs

| Category | Restricted | Reason | Workaround |
|----------|-----------|--------|------------|
| Threading | Assume no usable gameplay background threads by default | Browser constraints | Split work across frames, coroutines, Awaitable, or UniTask |
| File system | `System.IO.File`, `Directory`, `FileStream` | Browser sandbox | Use `Application.persistentDataPath`, IndexedDB, or JSLib bridge |
| Networking | `System.Net.Sockets`, `TcpClient`, `UdpClient` | No raw socket access | Use `UnityWebRequest`, WebSocket via JSLib, or WebRTC |
| Reflection | Dynamic code generation, `Emit`, runtime assembly loading | IL2CPP AOT | Pre-register types, preserve with `linker.xml` |
| Dynamic loading | `Assembly.Load`, `AppDomain` | AOT compilation | Bundle code at build time; use Addressables for assets |
| Clipboard/Browser APIs | Unity wrappers may be limited | Browser security policies | Use a JSLib wrapper and user-initiated flow |
| Audio autoplay | Audio may not start automatically | Browser autoplay policy | Start or unlock audio from user input |

### Conditional Compilation

```csharp
#if UNITY_WEBGL && !UNITY_EDITOR
    WebGLBridge.DoSomething();
#elif UNITY_EDITOR
    Debug.Log("Web call simulated in editor");
#else
    NativePlatformAlternative();
#endif
```

Guard patterns:
- `#if UNITY_WEBGL` — true when compiling for Web platform
- `#if UNITY_WEBGL && !UNITY_EDITOR` — true only in an actual build
- `#if !UNITY_WEBGL` — exclude incompatible code paths entirely

### Performance Constraints

**Allocation Pressure** — Per-frame allocation spikes are extra painful on the Web because memory pressure and GC interact with the browser runtime:

```csharp
var sb = new StringBuilder(items.Count * 8);
for (int i = 0; i < items.Count; i++)
{
    if (i > 0) sb.Append(", ");
    sb.Append(items[i]);
}
result = sb.ToString();
```

**Heavy Work** — Do not assume background threads will save a heavy gameplay algorithm on Web. Design a frame-sliced fallback first:

```csharp
IEnumerator ProcessInChunks<T>(IList<T> items, int chunkSize, System.Action<T> process)
{
    for (int i = 0; i < items.Count; i++)
    {
        process(items[i]);
        if ((i + 1) % chunkSize == 0)
            yield return null;
    }
}
```

**Memory Budget** — Browser memory ceilings vary widely. Keep initial heap modest, prefer streaming and incremental loading, reduce texture and audio memory aggressively.

### Common Web Build Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `EntryPointNotFoundException` | Method stripped by IL2CPP | Add preserve attributes or `linker.xml` |
| `TypeLoadException` | Type stripped or generic not AOT-compiled | Preserve types explicitly |
| `NotSupportedException: System.Threading` | Threading API reached on Web code path | Guard or redesign the code path |
| `Out of memory` | Heap or decompressed assets exceed browser limits | Reduce memory footprint |
| MIME type error loading `.wasm` | Server misconfiguration | Serve the correct MIME type |
| `.br` files not decompressing | Missing `Content-Encoding: br` header | Fix server headers |

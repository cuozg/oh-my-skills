# Dependency Management

## Constructor Injection — Pure C#

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

## [Inject] for MonoBehaviours — VContainer

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

## ScriptableObject Injection

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

## Service Locator — Fallback Only

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

## Assembly Definitions — Boundaries

```
Game.Core.asmdef           ← interfaces, data, no dependencies
Game.Combat.asmdef         ← references Core only
Game.UI.asmdef             ← references Core only
Game.Infrastructure.asmdef ← references Core, wires implementations
```

```json
{ "name": "Game.Combat", "references": ["Game.Core"], "autoReferenced": false }
```

## Avoid Singletons

```csharp
// ❌ Static singleton — untestable, hidden dependency
public class GameManager : MonoBehaviour { public static GameManager Instance; void Awake() => Instance = this; }

// ✅ Interface + DI
public interface IGameManager { void StartGame(); }
public sealed class GameManager : MonoBehaviour, IGameManager { }

// ✅ SO-based if unavoidable
[CreateAssetMenu] public class GameManagerRef : ScriptableObject { [System.NonSerialized] public IGameManager Current; }
```

## Zenject — Alternative DI Framework

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

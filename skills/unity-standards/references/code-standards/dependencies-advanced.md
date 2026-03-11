# Dependency Management — Advanced

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

# Script Template

Starting point for every new script. Two templates: **Plain C# Service** (constructor injection) and **MonoBehaviour** (initialization method).

## Plain C# Service

```csharp
using System;

namespace YourProject.YourFeature;

/// <summary>
/// [PURPOSE]: What this service does.
/// [USAGE]: How other systems interact with it.
/// [DEPENDENCIES]: What it requires (injected via constructor).
/// </summary>
public sealed class NewService : IDisposable
{
    private const float DefaultValue = 1f;

    private readonly ILogger logger;
    private readonly ISomeDependency dependency;

    /// <summary>Raised when [describe event]. Passes [describe payload].</summary>
    public event Action<int> SomethingHappened;

    public NewService(ILogger logger, ISomeDependency dependency)
    {
        this.logger = logger;
        this.dependency = dependency;
    }

    public void Dispose()
    {
        this.SomethingHappened = null;
    }

    /// <summary>[What]. [When to call]. [Side effects].</summary>
    public void Execute(int value)
    {
        if (value < 0) return; // Guard clause
        this.ProcessLogic(value);
    }

    private void ProcessLogic(int value)
    {
        this.logger.Info($"Processing value: {value}");
        this.SomethingHappened?.Invoke(value);
    }
}
```

## MonoBehaviour

```csharp
using System;
using UnityEngine;
using UnityEngine.Serialization;

namespace YourProject.YourFeature;

/// <summary>
/// [PURPOSE]: What this component does.
/// [USAGE]: How other systems interact with it.
/// [DEPENDENCIES]: What it requires (via Initialize method or SerializeField).
/// </summary>
public sealed class NewView : MonoBehaviour
{
    private const float DefaultSpeed = 5f;

    [Header("Configuration")]
    [Tooltip("Movement speed in units per second")]
    [SerializeField] private float speed = DefaultSpeed;

    [Header("References")]
    [Tooltip("Drag the target transform from the scene")]
    [SerializeField] private Transform target;

    private ILogger logger;

    /// <summary>
    /// Initializes the view with its dependencies. Call after instantiation.
    /// </summary>
    public void Initialize(ILogger logger)
    {
        this.logger = logger;
    }

    private void Awake()
    {
        if (this.target == null)
        {
            this.logger.Error($"{nameof(NewView)}: Target is not assigned!");
        }
    }

    private void OnEnable()
    {
        // Subscribe to events
    }

    private void OnDisable()
    {
        // Unsubscribe from events, kill tweens, cancel async ops
    }

    /// <summary>[What]. [When to call]. [Side effects].</summary>
    public void Execute(int value)
    {
        if (value < 0) return; // Guard clause
        this.ProcessLogic(value);
    }

    private void ProcessLogic(int value)
    {
        // WHY comments, not WHAT
    }
}
```

## Event Definition

```csharp
namespace YourProject.YourFeature;

// Event args: [Subject][Verb-PastTense]Args — readonly record struct for immutable data
public readonly record struct EnemyKilledArgs(string EnemyId, int Points);
public readonly record struct LevelCompletedArgs(int Level, float Time);

// Event source: centralized event hub for a domain
public sealed class CombatEvents
{
    public event Action<EnemyKilledArgs> EnemyKilled;
    public event Action GamePaused;

    public void RaiseEnemyKilled(EnemyKilledArgs args) => this.EnemyKilled?.Invoke(args);
    public void RaiseGamePaused() => this.GamePaused?.Invoke();
}
```

## Key Rules

- **File-scoped namespace** — `namespace X.Y;` not `namespace X.Y { }`
- **`sealed`** by default — unseal only when inheritance is explicitly designed
- **`readonly`** on all fields assigned only in constructor/Initialize
- **Constructor injection** for plain C# services — all dependencies via constructor params
- **`Initialize()` method** on MonoBehaviours — for injecting dependencies after instantiation
- **`ILogger`** via DI — no `Debug.Log`, no `#if UNITY_EDITOR` guards
- **No `#region`** blocks
- **No commented-out code**

## Checklist

### Structure
- [ ] File-scoped namespace matching directory path
- [ ] `sealed` class by default
- [ ] `/// <summary>` on class with PURPOSE/USAGE/DEPENDENCIES
- [ ] `readonly` on constructor-assigned fields

### Comments
- [ ] XML docs on every public member
- [ ] `[Tooltip]` on every `[SerializeField]`, `[Header]` groups
- [ ] No commented-out code

### Architecture
- [ ] Constructor injection for services, `Initialize()` method for MonoBehaviours
- [ ] Events: subscribe in `OnEnable`, unsubscribe in `OnDisable`
- [ ] ILogger injected — no `Debug.Log`, no `?.`, no constructor logging

### Clean Code
- [ ] No magic numbers — use `const` / `static readonly` / `[SerializeField]`
- [ ] Guard clauses at method entry
- [ ] No deep nesting (4+ levels)
- [ ] Single responsibility per class

### Unity Safety
- [ ] Components cached in `Awake`, no per-frame `GetComponent`
- [ ] `[FormerlySerializedAs]` when renaming serialized fields
- [ ] Empty callbacks deleted (`Update`, `Start`, `OnGUI`)
- [ ] ScriptableObjects cloned before runtime modification
- [ ] No allocations in hot paths

# Script Template

Starting point for every new script. Two templates: **Plain C# Service** (constructor injection) and **MonoBehaviour** (initialization method).

## Plain C# Service

```csharp
using System;

namespace YourProject.YourFeature;

/// <summary>
/// [PURPOSE]. [USAGE]. [DEPENDENCIES].
/// </summary>
public sealed class NewService : IDisposable
{
    private const float DefaultValue = 1f;
    private readonly ILogger logger;
    private readonly ISomeDependency dependency;

    /// <summary>Raised when [describe event].</summary>
    public event Action<int> SomethingHappened;

    public NewService(ILogger logger, ISomeDependency dependency)
    {
        this.logger = logger;
        this.dependency = dependency;
    }

    public void Dispose() { this.SomethingHappened = null; }

    /// <summary>[What]. [When to call]. [Side effects].</summary>
    public void Execute(int value)
    {
        if (value < 0) return; // Guard clause
        this.logger.Info($"Processing value: {value}");
        this.SomethingHappened?.Invoke(value);
    }
}
```

## MonoBehaviour

```csharp
using UnityEngine;

namespace YourProject.YourFeature;

/// <summary>[PURPOSE]. [USAGE]. [DEPENDENCIES].</summary>
public sealed class NewView : MonoBehaviour
{
    private const float DefaultSpeed = 5f;

    [Header("Configuration")]
    [SerializeField] private float speed = DefaultSpeed;
    [Header("References")]
    [SerializeField] private Transform target;

    private ILogger logger;

    /// <summary>Inject dependencies after instantiation.</summary>
    public void Initialize(ILogger logger) { this.logger = logger; }

    private void Awake()
    {
        if (this.target == null)
            this.logger.Error($"{nameof(NewView)}: Target not assigned!");
    }

    private void OnEnable()  { /* Subscribe to events */ }
    private void OnDisable() { /* Unsubscribe, kill tweens, cancel async */ }

    /// <summary>[What]. [When to call]. [Side effects].</summary>
    public void Execute(int value)
    {
        if (value < 0) return;
        // WHY comments, not WHAT
    }
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

See [verification-checklist.md](verification-checklist.md) for the full pre-commit checklist.

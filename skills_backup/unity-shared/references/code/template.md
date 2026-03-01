# Script Templates

Starting point for new scripts. Plain C#, MonoBehaviour, and ScriptableObject.

## Plain C# Service
```csharp
#nullable enable
using System;

namespace YourProject.YourFeature;

/// <summary>[PURPOSE]. [USAGE]. [DEPENDENCIES].</summary>
public sealed class NewService : IDisposable
{
    private const float DefaultValue = 1f;
    private readonly ILogger logger;
    private readonly ISomeDependency dependency;

    /// <summary>Raised when [describe event].</summary>
    public event Action<int>? SomethingHappened;

    public NewService(ILogger logger, ISomeDependency dependency)
    {
        this.logger = logger;
        this.dependency = dependency;
    }

    public void Dispose() => SomethingHappened = null;

    /// <summary>[What]. [When to call]. [Side effects].</summary>
    public void Execute(int value)
    {
        if (value < 0) return; // Guard clause
        logger.Info($"Processing value: {value}");
        SomethingHappened?.Invoke(value);
    }
}
```

## MonoBehaviour
```csharp
#nullable enable
using UnityEngine;

namespace YourProject.YourFeature;

/// <summary>[PURPOSE]. [USAGE]. [DEPENDENCIES].</summary>
[DisallowMultipleComponent]
public sealed class NewView : MonoBehaviour
{
    [Header("Configuration")]
    [SerializeField] private float speed = 5f;
    [Header("References")]
    [SerializeField] private Transform target = null!;

    private ILogger? logger;
    private Transform _transform = null!;

    /// <summary>Inject dependencies after instantiation.</summary>
    public void Initialize(ILogger logger) => this.logger = logger;

    private void Awake()
    {
        _transform = transform;
        if (target == null) Debug.LogError($"{name}: Target missing!", this);
    }

    private void OnEnable()  { /* Subscribe to events */ }
    private void OnDisable() { /* Unsubscribe, kill tweens, cancel async */ }

    /// <summary>[What]. [When to call]. [Side effects].</summary>
    public void Execute() { /* WHY comments, not WHAT */ }
}
```

## ScriptableObject
```csharp
#nullable enable
using UnityEngine;

namespace YourProject.YourFeature;

/// <summary>[PURPOSE]. [USAGE].</summary>
[CreateAssetMenu(menuName = "YourProject/NewConfig", fileName = "NewConfig")]
public sealed class NewConfig : ScriptableObject
{
    [SerializeField] private float speed = 5f;

    /// <summary>Movement speed in m/s.</summary>
    public float Speed => speed;

    private void OnValidate() => speed = Mathf.Max(0f, speed);
}
```
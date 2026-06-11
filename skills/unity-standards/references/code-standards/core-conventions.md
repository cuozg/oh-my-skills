# Core Conventions

Use this file for ordinary Unity C# style: naming, layout, fields, attributes, null handling, comments, and small implementation patterns.

## First Principles

- Match the repository's current style when it is deliberate and consistent.
- Prefer readable, boring code over clever compression.
- Keep MonoBehaviours thin: scene binding, lifecycle, and Unity API calls. Put pure rules in plain C# classes or structs.
- Make serialized configuration private and expose read-only properties or explicit methods.
- Avoid public mutable state unless Unity serialization or a documented integration requires it.
- Keep files focused. A gameplay MonoBehaviour over a few hundred lines is a smell unless it is clearly orchestration code.

## Naming

| Element | Standard | Example |
| --- | --- | --- |
| Namespace | `Company.Project.Feature` | `Studio.RPG.Combat` |
| Class / struct / enum | PascalCase | `DamageCalculator` |
| Interface | `I` + PascalCase | `IDamageable` |
| Method / property | PascalCase | `ApplyDamage`, `CurrentHealth` |
| Private field | `_camelCase` | `_moveSpeed` |
| Serialized private field | `_camelCase` | `[SerializeField] float _radius;` |
| Parameter / local | camelCase | `damageAmount` |
| Constant | PascalCase | `MaxRetries` |
| Event | Past-tense or state-changed name | `DamageApplied`, `HealthChanged` |

Use names that describe intent, not implementation mechanics:

```csharp
// Good
private float _remainingLifetime;
public bool CanAttack => _cooldown <= 0f && _target != null;

// Weak
private float _timer;
public bool Flag => _cooldown <= 0f && _target != null;
```

Common Unity component abbreviations are acceptable for cached fields (`_rb`, `_anim`, `_collider`, `_audioSource`) when the type is obvious nearby. Avoid project-specific abbreviations unless the codebase already uses them.

## File And Type Shape

- One primary type per file. File name matches the type.
- Keep namespaces aligned with the feature folder.
- Order members by how readers understand the class:
  1. constants and static fields
  2. serialized fields
  3. runtime fields
  4. properties
  5. Unity callbacks in lifecycle order
  6. public API
  7. private helpers
- Seal concrete MonoBehaviours and ScriptableObjects unless inheritance is an intended extension point.
- Prefer composition over inheritance for gameplay behavior.

```csharp
public sealed class Projectile : MonoBehaviour
{
    private const float MinSpeed = 0.01f;

    [SerializeField, Min(MinSpeed)] private float _speed = 12f;
    [SerializeField] private float _lifetimeSeconds = 3f;

    private float _remainingLifetime;
    private Transform _cachedTransform;

    public bool IsActive => _remainingLifetime > 0f;

    private void Awake()
    {
        _cachedTransform = transform;
    }

    private void OnEnable()
    {
        _remainingLifetime = _lifetimeSeconds;
    }

    private void Update()
    {
        TickLifetime(Time.deltaTime);
        Move(Time.deltaTime);
    }

    public void ResetLifetime(float lifetimeSeconds)
    {
        _remainingLifetime = Mathf.Max(0f, lifetimeSeconds);
    }

    private void TickLifetime(float deltaTime)
    {
        _remainingLifetime -= deltaTime;
    }
}
```

## Formatting

- Use Allman braces and 4 spaces.
- Keep lines near 120 characters.
- Use one blank line between methods and logical field groups.
- Avoid `#region` as a substitute for smaller files or extracted classes.
- Use expression-bodied members only for simple one-line logic.
- Use `var` when the right side makes the type obvious; use explicit types for primitives, ambiguous factory returns, and public API examples.
- Do not use nested ternaries. Use clear `if` blocks when state has meaning.

## Serialized State

Prefer explicit private backing fields:

```csharp
[SerializeField, Min(0f)] private float _maxHealth = 100f;
[SerializeField] private DamageProfile _damageProfile;

public float MaxHealth => _maxHealth;
public DamageProfile DamageProfile => _damageProfile;
```

Rules:

- Do not expose fields publicly just for Inspector access.
- Add `[FormerlySerializedAs]` when renaming serialized fields in existing assets.
- Use `[Min]`, `[Range]`, `[Tooltip]`, `[Header]`, and `[ContextMenu]` when they reduce authoring mistakes.
- Use `[RequireComponent]` when a component cannot work without another component on the same GameObject.
- Use `[DisallowMultipleComponent]` when duplicates would create invalid behavior.
- Use `[SerializeReference]` only when polymorphic serialized data is required and the project supports the authoring workflow.

## Access And Mutability

- Default to `private`.
- Use `internal` for same-assembly collaboration, especially with asmdefs and tests.
- Use `protected` only for deliberate inheritance contracts.
- Expose immutable views: `IReadOnlyList<T>`, copies, or explicit query methods.
- Do not return mutable internal collections from public APIs.

```csharp
private readonly List<Enemy> _visibleEnemies = new();
public IReadOnlyList<Enemy> VisibleEnemies => _visibleEnemies;
```

Use `readonly struct` for small immutable value data. Avoid large structs copied frequently unless profiling or data layout justifies them.

## Null And Reference Safety

Unity object null checks are special because destroyed `UnityEngine.Object` instances can compare equal to null. Use simple Unity null checks for Unity objects.

```csharp
if (_target == null)
{
    return;
}
```

Standards:

- Validate required serialized references in `Awake`, `OnValidate`, or explicit initialization.
- Use `TryGetComponent` when absence is expected.
- Use `GetComponent` in `Awake` when the component is required and `[RequireComponent]` documents the contract.
- Use guard clauses to keep main logic shallow.
- Avoid the null-forgiving operator (`!`) unless the invariant is obvious and documented by initialization order.
- Add `Debug.Assert` for invariants that indicate a programming/configuration bug.

```csharp
private void Awake()
{
    if (!TryGetComponent(out Rigidbody rb))
    {
        Debug.LogError($"{nameof(Projectile)} requires a Rigidbody.", this);
        enabled = false;
        return;
    }

    _rb = rb;
}
```

## Comments

Comments explain intent, constraints, or non-obvious Unity behavior. They should not narrate the line.

```csharp
// Delay one frame so pooled objects finish OnEnable before bindings fire.
yield return null;
_view.Bind(model);
```

Use XML documentation for public APIs consumed across assemblies or by external callers. Do not add file headers with author names, dates, or change history.

Use actionable TODOs:

```csharp
// TODO(combat): Replace this lookup with cached spawn table after wave configs move to Addressables.
// FIXME(save): Legacy v2 data can miss this field; keep fallback until migration 14 is complete.
```

## Attributes Quick Guide

| Attribute | Use |
| --- | --- |
| `[SerializeField]` | Inspector-configured private fields. |
| `[FormerlySerializedAs]` | Safe rename of serialized fields. |
| `[RequireComponent]` | Required sibling component. |
| `[DisallowMultipleComponent]` | Prevent invalid duplicate components. |
| `[CreateAssetMenu]` | Authorable ScriptableObject assets. |
| `[ContextMenu]` | Manual editor-time maintenance/debug actions. |
| `[RuntimeInitializeOnLoadMethod]` | Bootstrap code when scene references are not reliable. |
| `[Preserve]` | Reflection/linker-sensitive code, especially IL2CPP. |
| `[Obsolete]` | Migration warnings with replacement guidance. |

## Small Code Patterns

Use a plain C# class for testable rules:

```csharp
public sealed class DamageCalculator
{
    public float Calculate(float baseDamage, float armor)
    {
        float reduction = Mathf.Clamp01(armor);
        return baseDamage * (1f - reduction);
    }
}
```

Use ScriptableObjects for designer-authored data, not hidden global mutable state:

```csharp
[CreateAssetMenu(menuName = "Combat/Damage Profile")]
public sealed class DamageProfile : ScriptableObject
{
    [SerializeField, Min(0f)] private float _baseDamage = 10f;
    [SerializeField] private AnimationCurve _rangeFalloff = AnimationCurve.Linear(0f, 1f, 1f, 0f);

    public float Evaluate(float normalizedDistance)
    {
        return _baseDamage * _rangeFalloff.Evaluate(Mathf.Clamp01(normalizedDistance));
    }
}
```

For async methods, use the `Async` suffix except Unity event handlers and interface methods that already define a name:

```csharp
public async Awaitable LoadAsync(CancellationToken cancellationToken) { }
private async void HandleClicked() { }
```

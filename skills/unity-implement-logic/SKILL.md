---
name: unity-implement-logic
description: "Implement Unity C# logic, gameplay systems, and architectural patterns. Use when: (1) Creating new .claude/skills/unity-implement-logic/scripts/MonoBehaviours, (2) Refactoring for performance, (3) Implementing gameplay features (controllers, combat, data), (4) Using Unity 6 features (Awaitable, New Input System)."
---

# Unity Logic Implementer

Implement robust, performant C# code following Unity best practices.

## Output Requirement (MANDATORY)

**Every new script MUST follow the template**: [SCRIPT_TEMPLATE.md](.claude/skills/unity-implement-logic/assets/templates/SCRIPT_TEMPLATE.md)

Place scripts in the appropriate `Assets/Scripts/` subdirectory.

Read the template first, then populate all sections.

## Implementation Workflow

1. **Clarify**: Identify dependencies, target assembly (`.asmdef`)
2. **Implement**: Follow [UNITY_CSHARP_PATTERNS.md](.claude/skills/unity-implement-logic/references/UNITY_CSHARP_PATTERNS.md) and `.claude/rules/`
3. **Verify**: Check edge cases (null refs, async destruction)
4. **Compile**: `refresh_unity(compile="request")` - fix errors with `unity-fix-errors`

## Key Patterns

### Awaitable (Unity 6) - Prefer over Coroutines
```csharp
private async Awaitable DoAsync()
{
    await Awaitable.WaitForSecondsAsync(1f);
    if (this == null) return; // Safety check!
    Debug.Log("Done");
}
```

### Event-Driven - Decouple systems
```csharp
public event Action<int> OnHealthChanged;
public void TakeDamage(int dmg) => OnHealthChanged?.Invoke(_health -= dmg);
```

### Singleton - Global managers
```csharp
public static GameManager Instance { get; private set; }
void Awake() {
    if (Instance != null) { Destroy(gameObject); return; }
    Instance = this;
    DontDestroyOnLoad(gameObject);
}
```

## Performance Rules

| Avoid | Do Instead |
|-------|------------|
| `GetComponent` in Update | Cache in `Awake` |
| `Camera.main` in loops | Cache reference |
| String concat in Update | Use `StringBuilder` |
| `new` in hot paths | Object pooling |
| Deep inheritance | Composition |

## Best Practices

- **Composition over Inheritance**: Small, focused components
- **ScriptableObjects**: Configuration data, not hardcoded
- **Async Safety**: Check `this == null` after every `await`
- **Namespace Hygiene**: `_Project.Scripts.Feature`
- **Inspector Friendly**: Expose meaningful properties for Designers

See [SCRIPT_TEMPLATE.md](.claude/skills/unity-implement-logic/assets/templates/SCRIPT_TEMPLATE.md) for starting point.

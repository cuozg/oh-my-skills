---
name: unity-code
description: "Expert Unity Developer implementation. Write clean, commented, performant C# code following best practices and avoiding all anti-patterns caught by unity-review-pr. Use when: (1) Creating new MonoBehaviours or ScriptableObjects, (2) Implementing gameplay features (controllers, combat, UI, data), (3) Refactoring for performance or architecture, (4) Using Unity 6 features (Awaitable, New Input System), (5) Any C# implementation work in Unity projects."
---

# unity-code — Expert Unity Developer Implementation

**Input**: Feature description or implementation task, optional target assembly, related scripts, constraints
**Output**: C# scripts in `Assets/Scripts/`, following `SCRIPT_TEMPLATE.md`, passing compile checks with zero errors

## Workflow

1. **Clarify**: dependencies, target assembly (`.asmdef`), affected systems
2. **Plan**: outline classes, interfaces, data flow before coding
3. **Implement**: follow [UNITY_CSHARP_PATTERNS.md](.opencode/skills/unity/unity-code/references/UNITY_CSHARP_PATTERNS.md) and `.opencode/rules/`
4. **Self-Review**: run Pre-Completion Checklist — fix every violation
5. **Compile**: `unityMCP_check_compile_errors` — fix errors with `unity-fix-errors`

**Every new script MUST follow**: [SCRIPT_TEMPLATE.md](.opencode/skills/unity/unity-code/references/SCRIPT_TEMPLATE.md)

## Code Quality Standards

### 1. Commented Code
- XML docs (`/// <summary>`) on every public class, method, property
- Inline comments for *why*, not *what*
- `[Header]`/`[Tooltip]` on serialized fields
- No commented-out code blocks

### 2. Clean Code

| Principle | Violation | Correct |
|:----------|:----------|:--------|
| No magic numbers | `if (health < 50)` | `const int LowHealthThreshold = 50;` |
| Clear naming | `int x`, `void DoIt()` | `int remainingLives`, `void ApplyDamageReduction()` |
| Single responsibility | 500-line MonoBehaviour | Split into focused components |
| No deep nesting | 4+ levels if/for | Early returns, guard clauses |
| Encapsulation | `public int health;` | `[SerializeField] private int _health;` + property |

### 3. Smart Logic
- Composition over inheritance
- ScriptableObjects for data/config
- Events for decoupling (`Action<T>` for logic, `UnityEvent` for inspector)
- Object pooling for frequently spawned objects
- Guard clauses for early validation

## Critical Anti-Patterns

### Performance

| Anti-Pattern | Required Pattern |
|:-------------|:-----------------|
| `GetComponent<T>()` in Update | Cache in `Awake` |
| `Camera.main` in loops | Cache in `Awake` |
| `Find()`/`FindObjectOfType()` at runtime | `[SerializeField]` injection |
| `Instantiate`/`Destroy` spam | `ObjectPool<T>` |
| String concat in hot paths | `StringBuilder` or cache |
| `new List<>()`, LINQ in Update | Pre-allocate; `NonAlloc` variants |

### Async & Lifecycle

| Anti-Pattern | Required Pattern |
|:-------------|:-----------------|
| Use `this` after `await` without null check | `if (this == null) return;` after every `await` |
| `StartCoroutine` without cleanup | Store handle, `StopCoroutine` in `OnDisable` |
| `+=` without matching `-=` | Subscribe `OnEnable`, unsubscribe `OnDisable` |
| `async void` on non-Unity-events | `async Task` or `async Awaitable` |

### General

| Anti-Pattern | Required Pattern |
|:-------------|:-----------------|
| Missing null checks on external data | `?.`, `??`, defensive checks |
| No try/catch around I/O/network | Wrap with logging and fallback |
| Field renamed without `[FormerlySerializedAs]` | Add attribute before renaming |
| Modifying ScriptableObject at runtime | Clone: `Instantiate(configSO)` |
| Empty `Update()`/`Start()`/`OnGUI()` | Delete empty callbacks |
| Magic numbers | `const`, `[SerializeField]`, `static readonly` |

## Key Patterns

### Awaitable (Unity 6)

```csharp
private async Awaitable PerformDelayedAction(float delay)
{
    await Awaitable.WaitForSecondsAsync(delay);
    if (this == null) return; // MANDATORY after every await
    Debug.Log("Action executed");
}
```

### Event-Driven

```csharp
public event Action<int> OnHealthChanged;
private void OnEnable() => _source.OnDamage += HandleDamage;
private void OnDisable() => _source.OnDamage -= HandleDamage;
```

### Singleton (use sparingly)

```csharp
public static GameManager Instance { get; private set; }
private void Awake()
{
    if (Instance != null && Instance != this) { Destroy(gameObject); return; }
    Instance = this;
    DontDestroyOnLoad(gameObject);
}
```

See [UNITY_CSHARP_PATTERNS.md](.opencode/skills/unity/unity-code/references/UNITY_CSHARP_PATTERNS.md) for more.

## Pre-Completion Checklist

### Syntax & Compilation
- [ ] Compiles without errors/warnings
- [ ] No unresolved types or missing `using`
- [ ] All string literals properly escaped

### Code Quality
- [ ] XML docs on all public API
- [ ] No magic numbers
- [ ] No deep nesting (4+) — guard clauses used
- [ ] No dead code or commented-out blocks

### Unity-Specific
- [ ] `if (this == null) return;` after every `await`
- [ ] All `+=` have matching `-=` in `OnDisable`
- [ ] `GetComponent` cached in `Awake`/`Start`
- [ ] No `Find()`/`FindObjectOfType()` in gameplay
- [ ] `[FormerlySerializedAs]` on renamed fields
- [ ] Empty callbacks deleted
- [ ] ScriptableObjects cloned before runtime modification

### Final Verification
- [ ] `lsp_diagnostics` — zero errors
- [ ] `unityMCP_check_compile_errors` — compilation succeeds

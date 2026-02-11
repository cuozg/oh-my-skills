---
name: unity-code
description: "Expert Unity Developer implementation. Write clean, commented, performant C# code following best practices and avoiding all anti-patterns caught by unity-review-pr. Use when: (1) Creating new MonoBehaviours or ScriptableObjects, (2) Implementing gameplay features (controllers, combat, UI, data), (3) Refactoring for performance or architecture, (4) Using Unity 6 features (Awaitable, New Input System), (5) Any C# implementation work in Unity projects."
---

# unity-code — Expert Unity Developer Implementation

Implement game logic for Unity games as an expert developer. Every script must be **commented, clean, and smart** — code that passes review on the first attempt.

## Output Requirement (MANDATORY)

**Every new script MUST follow**: [SCRIPT_TEMPLATE.md](.claude/skills/unity-code/references/SCRIPT_TEMPLATE.md)

Place scripts in the appropriate `Assets/Scripts/` subdirectory. Read the template first, then populate all sections.

## Implementation Workflow

1. **Clarify**: Identify dependencies, target assembly (`.asmdef`), affected systems
2. **Plan**: Outline classes, interfaces, and data flow before writing code
3. **Implement**: Follow [UNITY_CSHARP_PATTERNS.md](.claude/skills/unity-code/references/UNITY_CSHARP_PATTERNS.md) and `.claude/rules/`
4. **Self-Review**: Run the [Pre-Completion Checklist](#pre-completion-checklist) — fix every violation
5. **Compile**: `coplay-mcp_check_compile_errors` — fix errors with `unity-fix-errors`

---

## Code Quality Standards

### 1. Commented Code

Every script must have meaningful comments:

```csharp
/// <summary>
/// Manages player health, damage intake, and death state.
/// Broadcasts health changes via OnHealthChanged for UI binding.
/// </summary>
public class PlayerHealth : MonoBehaviour
{
    // Maximum health configured per-character via ScriptableObject
    [SerializeField] private int _maxHealth = 100;

    // Current health — clamped between 0 and _maxHealth
    private int _currentHealth;

    /// <summary>
    /// Apply damage, clamp health, broadcast change, trigger death if zero.
    /// </summary>
    /// <param name="amount">Raw damage before any mitigation.</param>
    public void TakeDamage(int amount)
    {
        // Ignore damage when already dead
        if (_currentHealth <= 0) return;

        _currentHealth = Mathf.Max(0, _currentHealth - amount);
        OnHealthChanged?.Invoke(_currentHealth);

        // Death check — only fires once due to early return above
        if (_currentHealth <= 0) HandleDeath();
    }
}
```

**Rules:**
- XML docs (`/// <summary>`) on every public class, method, and property
- Inline comments for non-obvious logic (the *why*, not the *what*)
- `[Header]` and `[Tooltip]` on serialized fields for designer clarity
- No commented-out code blocks — use version control

### 2. Clean Code

| Principle | Violation | Correct |
|:----------|:----------|:--------|
| **No magic numbers** | `if (health < 50)` | `if (health < LowHealthThreshold)` with `const int LowHealthThreshold = 50;` |
| **Clear naming** | `int x`, `void DoIt()` | `int remainingLives`, `void ApplyDamageReduction()` |
| **Single responsibility** | 500-line MonoBehaviour | Split into focused components |
| **No deep nesting** | 4+ levels of if/for | Early returns, guard clauses, extract methods |
| **No dead code** | Commented blocks, unused vars | Delete or document with TODO |
| **Constants over literals** | `"player_tag"` scattered | `const string PlayerTag = "player_tag";` |
| **Encapsulation** | `public int health;` | `[SerializeField] private int _health;` with read-only property |

### 3. Smart Logic

- **Composition over inheritance**: Small, focused components that combine
- **ScriptableObjects for data**: Configuration, not hardcoded values
- **Events for decoupling**: `Action<T>` for logic, `UnityEvent` for inspector
- **Object pooling**: Mandatory for frequently spawned objects
- **Guard clauses**: Validate inputs early, return fast

---

## Critical Anti-Patterns to Avoid

These are the exact issues `unity-review-pr` catches. Prevent them during implementation.

### 🔴 Performance Anti-Patterns

| Anti-Pattern | Why It's Critical | Required Pattern |
|:-------------|:------------------|:-----------------|
| `GetComponent<T>()` in Update | Reflection-based O(n) search every frame | Cache in `Awake`: `private T _cached;` |
| `Camera.main` in loops | Calls FindGameObjectWithTag every access | Cache: `private Camera _cam;` in `Awake` |
| `Find()`/`FindObjectOfType()` at runtime | O(n) scene traversal | `[SerializeField]` injection or service locator |
| `Instantiate`/`Destroy` spam | GC spikes from allocation + finalization | `ObjectPool<T>` or custom pool |
| String concat (`+`, `$""`) in hot paths | New string allocation every frame | `StringBuilder` or cache |
| `new List<>()`, `.ToList()`, LINQ in Update | Heap allocation every frame | Pre-allocate; use `NonAlloc` variants |

### 🔴 Async & Lifecycle Anti-Patterns

| Anti-Pattern | Why It's Critical | Required Pattern |
|:-------------|:------------------|:-----------------|
| Use `this`/`gameObject` after `await` without null check | MissingReferenceException if destroyed during await | `if (this == null) return;` after every `await` |
| `StartCoroutine` without handle or cleanup | Coroutine runs after disable/destroy | Store handle, `StopCoroutine` in `OnDisable` |
| `+=` without matching `-=` | Memory leak, callbacks on destroyed objects | Subscribe in `OnEnable`, unsubscribe in `OnDisable` |
| `async void` on non-Unity-event methods | Exceptions silently swallowed, unawaitable | `async Task` or `async Awaitable` |

### 🔴 General Anti-Patterns

| Anti-Pattern | Why It's Critical | Required Pattern |
|:-------------|:------------------|:-----------------|
| Missing null checks on external data | NullReferenceException in production | `?.`, `??`, defensive checks with logging |
| No `try/catch` around I/O, network, deserialization | Silent failures, data loss | Wrap with logging and fallback |
| Field renamed without `[FormerlySerializedAs]` | Existing prefabs/SOs lose data | Add attribute before renaming |
| `private` → `public` without justification | Breaks encapsulation, increases coupling | Keep private; expose via interface/property |
| Modifying ScriptableObject at runtime | Changes persist in Editor, affects all refs | Clone: `var local = Instantiate(configSO);` |

### 🔵 Quality Anti-Patterns

| Anti-Pattern | Required Pattern |
|:-------------|:-----------------|
| Magic numbers (`0.5f`, `100`, `"key"`) | `const`, `static readonly`, or `[SerializeField]` |
| `Debug.Log` without conditional | `#if UNITY_EDITOR` or logging framework |
| Empty `Update()`, `Start()`, `OnGUI()` | Delete empty Unity callbacks |
| Missing XML docs on public API | `/// <summary>` on every public member |
| Excessive nesting (4+ levels) | Early returns, extract methods, guard clauses |
| Implicit vector ops (`transform.position.x = 5f`) | Assign via temp variable |

---

## Key Patterns

### Awaitable (Unity 6) — Prefer over Coroutines

```csharp
private async Awaitable PerformDelayedAction(float delay)
{
    await Awaitable.WaitForSecondsAsync(delay);

    // MANDATORY: null check after every await
    if (this == null) return;

    await Awaitable.NextFrameAsync();
    if (this == null) return;

    Debug.Log("Action executed");
}
```

### Event-Driven — Decouple systems

```csharp
// C# Action for logic listeners
public event Action<int> OnHealthChanged;

// Subscribe/unsubscribe lifecycle
private void OnEnable() => _source.OnDamage += HandleDamage;
private void OnDisable() => _source.OnDamage -= HandleDamage;
```

### Singleton — Global managers (use sparingly)

```csharp
public static GameManager Instance { get; private set; }

private void Awake()
{
    if (Instance != null && Instance != this)
    {
        Destroy(gameObject);
        return;
    }
    Instance = this;
    DontDestroyOnLoad(gameObject);
}
```

For detailed patterns and examples, see [UNITY_CSHARP_PATTERNS.md](.claude/skills/unity-code/references/UNITY_CSHARP_PATTERNS.md).

---

## Pre-Completion Checklist

**Run this checklist before marking any implementation complete.** Every item must pass.

### Syntax & Compilation
- [ ] Code compiles without errors or warnings
- [ ] No unresolved type references or missing `using` statements
- [ ] All generic types properly closed (`List<T>`, not `List<>`)
- [ ] No mismatched braces, parentheses, or brackets
- [ ] All string literals properly escaped

### Code Quality
- [ ] XML docs on every public class, method, and property
- [ ] Inline comments on non-obvious logic (explain *why*)
- [ ] No magic numbers — use `const`, `[SerializeField]`, or `static readonly`
- [ ] No deep nesting (4+ levels) — use guard clauses
- [ ] Clear, descriptive naming following project conventions
- [ ] No dead code or commented-out blocks
- [ ] Single responsibility per class/method

### Unity-Specific
- [ ] `if (this == null) return;` after every `await`
- [ ] All `+=` subscriptions have matching `-=` in `OnDisable`
- [ ] `GetComponent` calls cached in `Awake`/`Start`, not in Update loops
- [ ] No `Find()`/`FindObjectOfType()` in gameplay code
- [ ] `[FormerlySerializedAs]` used when renaming serialized fields
- [ ] Empty Unity callbacks (`Update`, `Start`, `OnGUI`) deleted
- [ ] `Debug.Log` wrapped in `#if UNITY_EDITOR` or conditional compilation
- [ ] ScriptableObjects cloned before runtime modification
- [ ] DOTween animations killed in `OnDisable`/`OnDestroy`

### Architecture
- [ ] Composition over inheritance
- [ ] Configuration via ScriptableObject, not hardcoded
- [ ] Private by default — expose only what's needed via properties/interfaces
- [ ] Error handling around I/O, network, and deserialization
- [ ] Resources/disposables cleaned up in `OnDestroy`

### Final Verification
- [ ] Run `lsp_diagnostics` on all changed files — zero errors
- [ ] Run `coplay-mcp_check_compile_errors` — compilation succeeds
- [ ] Review own code as if running `unity-review-pr` — no flaggable issues

---

## MCP Tools Integration

Prefer `coplay-mcp_*` tools over manual file/shell operations for Unity Editor interaction.

| Operation | MCP Tool | Replaces |
|:----------|:---------|:---------|
| Check compilation | `coplay-mcp_check_compile_errors` | Manual refresh + console check |
| Read console logs | `coplay-mcp_get_unity_logs` | Manual console inspection |
| Add component | `coplay-mcp_add_component(gameobject_path, component_type)` | Manual Inspector work |
| Set component property | `coplay-mcp_set_property(gameobject_path, component_type, property_name, value)` | Manual Inspector edits |
| Create GameObject | `coplay-mcp_create_game_object(name, position)` | Manual hierarchy creation |
| Create prefab | `coplay-mcp_create_prefab(gameobject_path, prefab_name, prefab_path)` | Manual prefab creation |
| Run C# in Editor | `coplay-mcp_execute_script(filePath)` | Manual menu items / test runs |
| Play/Stop game | `coplay-mcp_play_game` / `coplay-mcp_stop_game` | Manual play button |
| Get editor state | `coplay-mcp_get_unity_editor_state` | Manual inspection |
| Inspect hierarchy | `coplay-mcp_list_game_objects_in_hierarchy` | Manual scene browsing |
| Get object info | `coplay-mcp_get_game_object_info(gameObjectPath)` | Manual component inspection |

### Post-Implementation Verification Flow

```
1. coplay-mcp_check_compile_errors          → Fix any errors
2. coplay-mcp_get_unity_logs(show_errors=true) → Check for runtime warnings
3. coplay-mcp_play_game                     → Test in Play Mode
4. coplay-mcp_get_unity_logs                → Check runtime logs
5. coplay-mcp_stop_game                     → Stop Play Mode
```

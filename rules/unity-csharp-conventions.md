---
trigger: always_on
glob: Unity C# Code Standards — MANDATORY
description: CRITICAL enforcement rule — ALL agents MUST follow unity-code-standards skill when touching C# code.
---

## MANDATORY: unity-code-standards Skill Enforcement

**This rule is NON-NEGOTIABLE. Every agent that writes, reviews, or refactors C# code in a Unity project MUST load and follow the `unity-code-standards` skill.**

### When to Load `unity-code-standards`

You MUST load `unity-code-standards` via `load_skills=["unity-code-standards"]` (or `use_skill("unity-code-standards")`) whenever:

1. **Writing C# code** — new scripts, MonoBehaviours, ScriptableObjects, any `.cs` file
2. **Reviewing C# code** — PR reviews, code reviews, logic reviews, quality audits
3. **Refactoring C# code** — renaming, restructuring, extracting, decoupling
4. **Fixing C# errors** — compiler errors, runtime exceptions, logic bugs
5. **Planning C# implementation** — design documents, implementation plans, TDDs

### 4-Priority Quality Gates (Enforced by unity-code-standards)

| Priority | Domain | Examples |
|:---------|:-------|:---------|
| **P1 — Critical** | Code quality & hygiene | Nullable annotations, access modifiers, ILogger abstraction, structured exceptions |
| **P2 — High** | Modern C# patterns | LINQ over loops, expression bodies, null-coalescing, pattern matching |
| **P3 — Medium** | Unity architecture | VContainer DI (no `new` services), SignalBus events (no direct coupling), Data Controllers |
| **P4 — Low** | Performance | Allocation-free hot paths, component caching, UniTask over coroutines |

### Delegation Rule

When delegating ANY C# task to a subagent, you MUST include `"unity-code-standards"` in `load_skills`:

```
task(
  category="...",
  load_skills=["unity-code-standards", ...other_skills...],
  prompt="..."
)
```

**Omitting `unity-code-standards` from a C#-related delegation is a BLOCKING violation.**

### Quick Reference — Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `PlayerController` |
| Methods | PascalCase | `TakeDamage(int amount)` |
| Private Fields | _camelCase | `private int _health;` |
| Public Properties | PascalCase | `public int CurrentHealth { get; }` |
| Local Variables | camelCase | `int damageAmount = 10;` |
| Constants | PascalCase | `const float MaxSpeed = 10f;` |

### Quick Reference — Architecture

1. **Component-Based**: Small, focused, single-responsibility components
2. **ScriptableObjects**: Configuration data, not hardcoded values
3. **Object Pooling**: Mandatory for frequently instantiated objects
4. **Assembly Definitions**: Use `.asmdef` to organize code

### Quick Reference — Unity 6 (6000.1)

Prefer `Awaitable` over Coroutines:
```csharp
private async Awaitable Start()
{
    await Awaitable.WaitForSecondsAsync(1f);
    if (this == null) return; // Safety check!
    Debug.Log("Done");
}
```

### Quick Reference — Performance

- **Avoid Update()**: Use events or reactive patterns
- **Cache References**: `GetComponent` and `Camera.main` in `Awake`/`Start`
- **No String Concat**: Use `StringBuilder` in hot paths
- **Watch Boxing**: Use generic collections `List<T>`

### Quick Reference — Testing

- Location: `Tests/EditMode/` and `Tests/PlayMode/`
- Naming: `[Subject]_[Scenario]_[ExpectedResult]`

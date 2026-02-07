---
name: unity-task-brainstorm
description: "Technical deep-dive for tasks. Use when: (1) Task file needs code-level details, (2) Investigating codebase for implementation, (3) Generating specific code changes with explanations."
---

# Unity Plan Brainstorm

Refine task files into execution-ready blueprints.

## Output Requirement (MANDATORY)

**Every brainstorm output MUST follow the template**: [BRAINSTORM_OUTPUT.md](assets/templates/BRAINSTORM_OUTPUT.md)

Update the task file at `Documents/Tasks/[Number][Epic][Task].md` with the brainstorm results.

Read the template first, then populate all sections.

## Workflow

1. **Read Task**: `Documents/Tasks/[Number][Epic][Task].md`
2. **Investigate**: Load `unity-investigate-code`, trace classes mentioned
3. **Brainstorm**: Identify gaps, **ask user** questions:
   - "Should cooldown be global or per-instance?"
   - "Support pooled objects here?"
4. **Detail Code Changes**: For each change, specify:
   - **Target File**: Absolute path
   - **Original Snippet**: Code being replaced
   - **New Snippet**: Implementation
   - **Rationale**: Why this change
5. **Update Task**: Refine Implementation Strategy & Code Changes sections

## Code Change Format

```markdown
### Change 1: Add Heal Method
- **File**: `Assets/Scripts/Player/HealthManager.cs`
- **Line**: 45
- **Original**: `// TODO: Add healing`
- **New**:
```csharp
public void Heal(int amount)
{
    _health = Mathf.Min(_health + amount, _maxHealth);
    OnHealthChanged?.Invoke(_health);
}
```
- **Rationale**: Symmetric to TakeDamage, fires same event for UI updates
```

## Best Practices

- **Explain "Why"**: Architectural reason for each change
- **No Ambiguity**: Exact file, line, code - not "Update the Health class"
- **Subagent Research**: Use browser for unfamiliar Unity 6000.1 APIs
- **Execution Ready**: Final task = blueprint for `unity-task-executor`

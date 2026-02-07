---
name: unity-write-docs
description: "Create Unity project documentation. Use when: (1) Creating/updating README, (2) Documenting architectures, (3) Generating API references, (4) Writing onboarding guides, (5) Documenting Prefab/Scene setups."
---

# Unity Documentation

Create clear, maintainable documentation for Unity projects.

## Output Requirement (MANDATORY)

**Every document MUST follow one of the templates**:
- [README_TEMPLATE.md](.claude/skills/unity-write-docs/assets/templates/README_TEMPLATE.md) — for project READMEs
- [API_TEMPLATE.md](.claude/skills/unity-write-docs/assets/templates/API_TEMPLATE.md) — for API references
- [ARCHITECTURE_TEMPLATE.md](.claude/skills/unity-write-docs/assets/templates/ARCHITECTURE_TEMPLATE.md) — for architecture docs
- [GUIDE_TEMPLATE.md](.claude/skills/unity-write-docs/assets/templates/GUIDE_TEMPLATE.md) — for onboarding/usage guides

Read the relevant template first, then populate all sections.

## Document Types

| Type | Purpose | Location |
|------|---------|----------|
| README.md | Project overview, setup | Root |
| ARCHITECTURE.md | System design | Docs/ |
| API.md | Public interfaces | Docs/ |
| CONTRIBUTING.md | Dev guidelines | Root |

## Workflow

1. **Analyze**: `grep` for public APIs, ScriptableObjects, serialized fields
2. **Generate**: Use templates from `.claude/skills/unity-write-docs/assets/templates/`
3. **Visualize**: Mermaid diagrams for hierarchies/flows
4. **Validate**: Cross-reference with code signatures

## Best Practices

- **Show, Don't Tell**: Include code snippets and diagrams
- **Unity Terms**: Prefabs, MonoBehaviours, URP, Addressables
- **TOC**: Tables of contents for major docs
- **Current**: Reflect latest code changes

## XML Documentation

```csharp
/// <summary>
/// Applies damage and triggers death at zero health.
/// </summary>
/// <param name="amount">Damage to apply.</param>
/// <returns>True if died from this damage.</returns>
public bool TakeDamage(int amount)
```

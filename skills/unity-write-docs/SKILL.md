---
name: unity-write-docs
description: "(opencode-project - Skill) Create Unity project documentation. Use when: (1) Creating/updating README, (2) Documenting architectures, (3) Generating API references, (4) Writing onboarding guides, (5) Documenting Prefab/Scene setups, (6) Writing code comments and XML docs. Triggers: 'write docs', 'documentation', 'README', 'API reference', 'onboarding guide', 'architecture doc', 'system overview', 'code documentation', 'prefab documentation', 'scene documentation', 'wiki', 'changelog', 'contributing guide', 'technical writing', 'document this', 'explain this system', 'write a guide', 'how-to doc', 'XML summary', 'code comments', 'project docs'."
---

# Unity Documentation

**Input**: Description of documentation task. Optional: file paths, constraints, scope.

## Output
Project documentation following the Templates below.

## Templates (MANDATORY)

- [README_TEMPLATE.md](assets/templates/README_TEMPLATE.md)
- [API_TEMPLATE.md](assets/templates/API_TEMPLATE.md)
- [ARCHITECTURE_TEMPLATE.md](assets/templates/ARCHITECTURE_TEMPLATE.md)
- [GUIDE_TEMPLATE.md](assets/templates/GUIDE_TEMPLATE.md)

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
2. **Generate**: Use templates from `assets/templates/`
3. **Visualize**: Mermaid diagrams for hierarchies/flows
4. **Validate**: Cross-reference with code signatures

## Best Practices

- **Show, Don't Tell**: Include code snippets and diagrams
- **Unity Terms**: Prefabs, MonoBehaviours, URP, Addressables
- **TOC**: Tables of contents for major docs
- **Current**: Reflect latest code changes

## XML Documentation Example

```csharp
/// <summary>
/// Applies damage and triggers death at zero health.
/// </summary>
/// <param name="amount">Damage to apply.</param>
/// <returns>True if died from this damage.</returns>
public bool TakeDamage(int amount)
```

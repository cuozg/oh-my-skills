---
name: unity-write-tdd
description: "Generate Technical Design Documents. Use when: (1) Formalizing plans into specs, (2) Documenting architecture decisions, (3) Defining client/server logic, (4) Specifying APIs and data schemas."
---

# Unity TDD Writer

Generate Technical Design Documents from implementation plans.

## Purpose

Generate Technical Design Documents — providing a structured, repeatable workflow that produces consistent results.

## Input

- **Required**: A clear description of the task or problem to address.
- **Optional**: Relevant file paths, constraints, or context that narrows the scope.

## Examples

| Trigger | What Happens |
|---------|-------------|
| "Run unity-write-tdd" | Executes the primary workflow end-to-end |
| "Apply unity-write-tdd to <target>" | Scopes execution to a specific file or module |
| "Check unity-write-tdd output" | Reviews and validates previous results |


## Output Requirement (MANDATORY)

**Every TDD MUST follow the template**: [UNITY_TDD_TEMPLATE.md](.opencode/skills/unity-write-tdd/assets/templates/UNITY_TDD_TEMPLATE.md)

Save output to: `Documents/TDDs/TDD_[FeatureName].md`

Read the template first, then populate all sections.

## Output

Save to `Documents/TDDs/TDD_[FeatureName].md` using [UNITY_TDD_TEMPLATE.md](.opencode/skills/unity-write-tdd/assets/templates/UNITY_TDD_TEMPLATE.md).

## Workflow

1. **Find Plan**: `Documents/Plans/IMPLEMENTATION_PLAN_[FeatureName].md` (run `/unity-plan` if missing)
2. **Define Architecture**: Constraints (FPS, Memory, CPU), map Epics to TDD Components
3. **Detail Logic**: UI lifecycles, asset loading (Addressables, pooling), client-server interactions
4. **Generate**: Use template, address all sections
5. **Validate**: Verify Architecture, Components, API, Analytics, Performance covered

## Required Sections

- **Architecture**: Assumptions, constraints, dependencies
- **Components**: Feature modules mapped from plan
- **API Reference**: Endpoints, request/response formats
- **Data Schema**: Blueprint/FlatBuffer changes
- **Performance**: Mobile/low-end considerations
- **Analytics**: Events to track

## Best Practices

- **Explicit Assumptions**: Never leave constraints undocumented
- **Performance First**: Address mobile/low-end risks
- **UI Lifecycle**: When data populates and refreshes
- **Error Handling**: API failures, offline behavior

---

## MCP Tools Integration

Use MCP tools to gather technical context for accurate TDD specifications.

| Operation | MCP Tool | Use Case |
| --------- | -------- | -------- |
| Project context | `unityMCP_get_unity_editor_state` | Unity version, pipeline, build target for constraints |
| Scene structure | `unityMCP_list_game_objects_in_hierarchy()` | Understand existing architecture |
| Object details | `unityMCP_get_game_object_info(gameObjectPath="...")` | Document component configurations |
| List packages | `unityMCP_list_packages` | Document dependency requirements |

### TDD Context Gathering

```
1. unityMCP_get_unity_editor_state          → platform constraints
2. unityMCP_list_game_objects_in_hierarchy() → existing systems
3. unityMCP_list_packages                   → dependency map
```

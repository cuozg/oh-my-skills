---
name: unity-mcp-basics
description: "Unity Editor automation via unityMCP. Use when: (1) Finding/creating/modifying GameObjects, (2) Managing scenes/prefabs, (3) Updating materials/shaders, (4) Batch Editor operations. Triggers: 'automate Editor', 'MCP tool', 'batch operations', 'find GameObject'."
---

# Unity MCP Basics

Automate Unity Editor tasks with `unityMCP`.

## Output Requirement (MANDATORY)

**Every operation log MUST follow the template**: [MCP_OPERATION_LOG.md](.claude/skills/unity-mcp-basics/assets/templates/MCP_OPERATION_LOG.md)

Output the log directly to the user. No file save required.

Read the template first, then populate all sections.

## Core Tools

| Tool | Purpose |
|------|---------|
| `find_gameobjects` | Locate objects by name/type |
| `manage_gameobject` | Create/modify objects |
| `manage_components` | Add/remove/update components |
| `manage_scene` | Hierarchy, screenshots |
| `manage_material` | Material properties |
| `batch_execute` | Multiple operations |
| `read_console` | Get logs/errors |
| `refresh_unity` | Compile/refresh |

## Standard Workflow

1. **Locate**: `find_gameobjects` → Get Instance ID
2. **Modify**: `manage_components` or `manage_gameobject`
3. **Verify**: `manage_scene(screenshot)` or `read_console`

## Best Practices

- **Instance IDs**: Use for reliable GameObject targeting
- **Batching**: `batch_execute` for multiple similar operations
- **Verify First**: Check hierarchy before creating to avoid duplicates
- **Monitor Logs**: `read_console` after critical operations

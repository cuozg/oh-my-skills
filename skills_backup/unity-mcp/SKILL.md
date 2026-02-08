---
name: unity-mcp
description: "Expert Unity Editor automation via CoplayDev MCP for Unity. Orchestrate GameObjects, scenes, scripts, assets, materials, prefabs, shaders, VFX, textures, tests, and editor state through MCP tools and resources. Use when: (1) Creating/modifying/finding GameObjects and components, (2) Managing scenes and prefabs headlessly, (3) Creating or editing C# scripts via structured edits, (4) Batch automating repetitive Editor operations, (5) Managing materials, shaders, textures procedurally, (6) Running Unity Test Framework tests, (7) Querying editor state, project info, or console logs, (8) Multi-instance Unity workflows, (9) Creating custom MCP tools. Triggers: 'automate Editor', 'MCP tool', 'batch operations', 'find GameObject', 'create script via MCP', 'manage prefab', 'run tests', 'editor automation', 'unity-mcp', 'manage scene'."
---

# Unity MCP — Expert Operator Guide

Automate Unity Editor through [MCP for Unity](https://github.com/CoplayDev/unity-mcp) (CoplayDev). This skill provides expert-level patterns for all 26 tools and 15 resources.

## Resource-First Workflow (MANDATORY)

Always read resources before mutating state:

```
1. Check readiness   → mcpforunity://editor/state (ready_for_tools must be true)
2. Understand scene  → mcpforunity://scene/gameobject-api
3. Find targets      → find_gameobjects or resource URIs
4. Execute           → tools (manage_*, create_script, batch_execute, etc.)
5. Verify            → read_console + manage_scene(action="screenshot")
```

## Critical Rules

1. **After script create/edit**: Always `refresh_unity(mode="force", scope="scripts", compile="request", wait_for_ready=True)` then `read_console(types=["error"])`
2. **Batch over sequential**: `batch_execute` is 10-100x faster. Max 25 commands. Use `parallel=True` for read-only ops, `fail_fast=True` for dependent ops.
3. **Screenshot to verify**: `manage_scene(action="screenshot")` returns base64 PNG — use after visual changes.
4. **Check editor state**: If `is_compiling` or `!ready_for_tools`, wait. Check `blocking_reasons`.
5. **Instance IDs > names**: Use instance IDs from `find_gameobjects` for reliable targeting.

## Tool Quick Reference

| Category | Tools | Purpose |
|----------|-------|---------|
| **Scene** | `manage_scene`, `find_gameobjects` | Hierarchy, screenshots, scene CRUD, search |
| **Objects** | `manage_gameobject`, `manage_components` | Create/modify/delete/duplicate GameObjects, components |
| **Scripts** | `create_script`, `script_apply_edits`, `apply_text_edits`, `validate_script`, `delete_script`, `get_sha` | Full script lifecycle with structured edits |
| **Assets** | `manage_asset`, `manage_prefabs` | Search/create/move/delete assets, headless prefab ops |
| **Visuals** | `manage_material`, `manage_texture`, `manage_shader`, `manage_vfx` | Materials, procedural textures, shaders, VFX |
| **Editor** | `manage_editor`, `execute_menu_item`, `read_console`, `refresh_unity` | Play/pause/stop, menu items, console, refresh |
| **ScriptableObjects** | `manage_scriptable_object` | Create/modify ScriptableObject assets |
| **Testing** | `run_tests`, `get_test_job` | Async test execution with polling |
| **Batch** | `batch_execute` | Parallel/sequential bulk operations |
| **Search** | `find_in_file` | Regex search within file contents |

## Resource Quick Reference

| URI | Purpose |
|-----|---------|
| `mcpforunity://editor/state` | Readiness, compilation status, play mode, blocking reasons |
| `mcpforunity://editor/selection` | Currently selected objects |
| `mcpforunity://editor/prefab-stage` | Current prefab editing context |
| `mcpforunity://scene/gameobject/{id}` | GameObject metadata by instance ID |
| `mcpforunity://scene/gameobject/{id}/components` | All components with serialized properties (paginated) |
| `mcpforunity://scene/gameobject/{id}/component/{name}` | Single component with full properties |
| `mcpforunity://prefab/{encoded_path}` | Prefab asset info (URL-encode path: `/` → `%2F`) |
| `mcpforunity://prefab/{encoded_path}/hierarchy` | Full prefab hierarchy |
| `mcpforunity://project/info` | Project root, Unity version, platform |
| `mcpforunity://project/tags` | All project tags |
| `mcpforunity://project/layers` | All layers (0-31) |
| `mcpforunity://menu-items` | Available menu items |
| `mcpforunity://custom-tools` | Custom tools registered in the project |
| `mcpforunity://instances` | Running Unity Editor instances |
| `mcpforunity://tests` | All tests (filter by mode: `/tests/EditMode`) |

## Core Workflows

### Script Create → Attach

```python
create_script(path="Assets/Scripts/MyScript.cs", contents="...")
refresh_unity(mode="force", scope="scripts", compile="request", wait_for_ready=True)
read_console(types=["error"], count=10)  # Must be clean before proceeding
manage_gameobject(action="modify", target="Player", components_to_add=["MyScript"])
```

### Script Edit (Structured — Preferred)

```python
script_apply_edits(name="PlayerController", path="Assets/Scripts", edits=[
    {"op": "replace_method", "methodName": "Update", "replacement": "void Update() { ... }"},
    {"op": "insert_method", "afterMethod": "Start", "code": "void OnEnable() { }"},
    {"op": "anchor_insert", "anchor": "using UnityEngine;", "position": "after", "text": "\nusing System.Linq;"},
    {"op": "regex_replace", "pattern": "Debug\\.Log\\(", "text": "Debug.LogWarning("}
])
refresh_unity(mode="force", scope="scripts", compile="request", wait_for_ready=True)
read_console(types=["error"], count=10)
```

### Script Edit (Precise Position)

```python
sha = get_sha(uri="mcpforunity://path/Assets/Scripts/MyScript.cs")
apply_text_edits(uri="mcpforunity://path/Assets/Scripts/MyScript.cs", edits=[
    {"startLine": 10, "startCol": 5, "endLine": 10, "endCol": 20, "newText": "replacement"}
], precondition_sha256=sha["sha256"])
```

### Find → Inspect → Modify

```python
result = find_gameobjects(search_term="Enemy", search_method="by_tag", page_size=50)
# Read: mcpforunity://scene/gameobject/{id}/components for full data
manage_components(action="set_property", target=result["ids"][0],
    component_type="EnemyHealth", properties={"maxHealth": 100, "armor": 5})
```

### Batch Scene Setup

```python
batch_execute(commands=[
    {"tool": "manage_gameobject", "params": {"action": "create", "name": "Ground", "primitive_type": "Plane", "scale": [10,1,10]}},
    {"tool": "manage_gameobject", "params": {"action": "create", "name": "Player", "primitive_type": "Capsule", "position": [0,1,0]}},
    {"tool": "manage_gameobject", "params": {"action": "create", "name": "Light", "primitive_type": "Cube"}}
], parallel=True)
```

### Async Test Execution

```python
result = run_tests(mode="EditMode", test_names=["MyTests.TestA"], include_failed_tests=True)
final = get_test_job(job_id=result["job_id"], wait_timeout=60, include_failed_tests=True)
```

### Multi-Instance Routing

```python
# Read mcpforunity://instances → get Name@hash
set_active_instance(instance="MyProject@abc123")
# All subsequent calls route to that instance
```

## Parameter Conventions

| Type | Format |
|------|--------|
| Vectors | `[1.0, 2.0, 3.0]` or `"[1.0, 2.0, 3.0]"` |
| Colors | `[255, 0, 0, 255]` (0-255) or `[1.0, 0.0, 0.0, 1.0]` (normalized, auto-converted) |
| Booleans | `True` or `"true"` |
| Paths | `"Assets/Scripts/MyScript.cs"` (Assets-relative) |
| URIs | `"mcpforunity://path/Assets/Scripts/MyScript.cs"` or `"file:///full/path"` |
| Prefab URIs | URL-encode path slashes: `mcpforunity://prefab/Assets%2FPrefabs%2FPlayer.prefab` |

## Error Recovery

| Symptom | Cause | Fix |
|---------|-------|-----|
| Tools return "busy" | Compilation in progress | Wait, poll `editor_state` |
| `stale_file` error | File changed since SHA | Re-fetch with `get_sha`, retry |
| Connection lost | Domain reload | Wait ~5s, retry |
| Commands fail silently | Wrong instance | Check `set_active_instance` |
| Script attach fails | Not compiled yet | `refresh_unity` with `wait_for_ready=True` first |

## Pagination

Large queries return paginated results. Always follow `next_cursor`:

```python
cursor = 0
while True:
    result = manage_scene(action="get_hierarchy", page_size=50, cursor=cursor)
    # process result["data"]["items"]
    if not result["data"].get("next_cursor"):
        break
    cursor = result["data"]["next_cursor"]
```

## Custom Tools

Extend MCP with project-specific tools. Read `mcpforunity://custom-tools` to discover available ones. See [references/custom-tools.md](references/custom-tools.md) for creation guide.

## Detailed References

For complete parameter schemas and extended examples:

- **[references/tools-reference.md](references/tools-reference.md)**: All 26 tools with full parameters
- **[references/resources-reference.md](references/resources-reference.md)**: All 15 resources with response schemas
- **[references/workflows.md](references/workflows.md)**: Extended workflow patterns (scene creation, asset management, TDD, debugging)
- **[references/custom-tools.md](references/custom-tools.md)**: Creating custom MCP tools with `[McpForUnityTool]`

## Output Requirement

After MCP operations, log results using: [assets/templates/MCP_OPERATION_LOG.md](assets/templates/MCP_OPERATION_LOG.md)

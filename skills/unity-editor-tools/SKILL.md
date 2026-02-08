---
name: unity-editor-tools
description: "Create Unity Editor tools. Use when: (1) Custom Editor Windows/Inspectors, (2) Automating asset/scene validation, (3) Building engineer utilities (search, batch processors), (4) UI Toolkit (UXML/USS) interfaces."
---

# Unity Editor Developer

Extend the Unity Editor with tools and automation.

## Output Requirement (MANDATORY)

**Every editor tool MUST follow one of the templates**:
- [EDITOR_WINDOW_TEMPLATE.md](.claude/skills/unity-editor-tools/assets/templates/EDITOR_WINDOW_TEMPLATE.md) — for EditorWindow tools
- [CUSTOM_INSPECTOR_TEMPLATE.md](.claude/skills/unity-editor-tools/assets/templates/CUSTOM_INSPECTOR_TEMPLATE.md) — for Custom Inspectors

Place scripts in `Assets/Scripts/Editor/`. Read the relevant template first, then populate all sections.

## Tool Types

| Type | Use Case |
|------|----------|
| EditorWindow | Global utility tools |
| CustomEditor | Component-specific inspectors |
| AssetPostprocessor | Import automation |
| MenuItem/Shortcut | Quick actions |

## Workflow

1. **Assess**: Identify pain point, choose Window vs Inspector
2. **Architect**: UI Toolkit (modern) vs IMGUI (legacy), data persistence
3. **Implement**: Use templates from `.claude/skills/unity-editor-tools/assets/templates/`, patterns from [EDITOR_SCRIPTING_PATTERNS.md](.claude/skills/unity-editor-tools/references/EDITOR_SCRIPTING_PATTERNS.md)
4. **Verify**: Test domain reloads, scene changes, profile if handling large data

## Best Practices

- **Undo Mandatory**: Always use `SerializedObject` or `Undo.RecordObject`
- **Match Engine**: Use USS themes for Dark/Light mode
- **Progress Bars**: `EditorUtility.DisplayProgressBar` for batch tasks
- **Batch Safety**: Wrap in `StartAssetEditing`/`StopAssetEditing`
- **No Polling**: Use `TrackPropertyValue` or events, not OnGUI checks

## Templates

- [EDITOR_WINDOW_TEMPLATE.md](.claude/skills/unity-editor-tools/assets/templates/EDITOR_WINDOW_TEMPLATE.md)
- [CUSTOM_INSPECTOR_TEMPLATE.md](.claude/skills/unity-editor-tools/assets/templates/CUSTOM_INSPECTOR_TEMPLATE.md)
- [EDITOR_UI_TOOLKIT_GUIDE.md](.claude/skills/unity-editor-tools/references/EDITOR_UI_TOOLKIT_GUIDE.md)

---

## MCP Tools Integration

Use `coplay-mcp_*` tools to test and validate editor tools after implementation.

| Operation | MCP Tool |
|-----------|----------|
| Run editor script | `coplay-mcp_execute_script(filePath="...")` |
| Check compilation | `coplay-mcp_check_compile_errors` |
| Read console | `coplay-mcp_get_unity_logs()` |
| Editor state | `coplay-mcp_get_unity_editor_state` |
| Inspect hierarchy | `coplay-mcp_list_game_objects_in_hierarchy()` |
| Add component | `coplay-mcp_add_component(gameobject_path="..", component_type="..")` |
| Set property | `coplay-mcp_set_property(gameobject_path="..", component_type="..", property_name="..", value="..")` |
| Create GameObject | `coplay-mcp_create_game_object(name="..", position="..")` |
| Capture UI | `coplay-mcp_capture_ui_canvas()` |

### Editor Tool Verification Flow

```
1. [Write editor script to Assets/Scripts/Editor/]
2. coplay-mcp_check_compile_errors             → Verify script compiles
3. coplay-mcp_execute_script(filePath="...")    → Run the editor tool
4. coplay-mcp_get_unity_logs()                 → Check for errors/output
5. coplay-mcp_capture_ui_canvas()              → Validate UI if applicable
```

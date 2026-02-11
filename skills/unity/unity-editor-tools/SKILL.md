---
name: unity-editor-tools
description: "Create Unity Editor tools. Use when: (1) Custom Editor Windows/Inspectors, (2) Automating asset/scene validation, (3) Building engineer utilities (search, batch processors), (4) UI Toolkit (UXML/USS) interfaces."
---

# Unity Editor Developer

Extend the Unity Editor with tools and automation.

## Purpose

Create custom Unity Editor extensions — windows, inspectors, asset postprocessors, and menu items — that streamline developer and artist workflows.

## Input

- **Required**: Description of the Editor tool or automation needed (pain point, target workflow)
- **Optional**: Target component types, asset types, UI framework preference (UI Toolkit vs IMGUI)

## Output

Editor scripts placed in `Assets/Scripts/Editor/`, following the appropriate template (`EDITOR_WINDOW_TEMPLATE.md` or `CUSTOM_INSPECTOR_TEMPLATE.md`). Scripts compile cleanly and support Undo, Dark/Light themes, and domain reloads.

## Examples

| User Request | Skill Action |
|:---|:---|
| "Create a batch renamer for GameObjects" | Build an EditorWindow with UI Toolkit: find/replace, prefix/suffix, undo support |
| "Custom inspector for EnemyConfig SO" | Build a CustomEditor with validated fields, preview, and help boxes |
| "Auto-set texture import settings on import" | Write an AssetPostprocessor that enforces max size, compression, and naming rules |

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

Use `unityMCP_*` tools to test and validate editor tools after implementation.

| Operation | MCP Tool |
|-----------|----------|
| Run editor script | `unityMCP_execute_script(filePath="...")` |
| Check compilation | `unityMCP_check_compile_errors` |
| Read console | `unityMCP_get_unity_logs()` |
| Editor state | `unityMCP_get_unity_editor_state` |
| Inspect hierarchy | `unityMCP_list_game_objects_in_hierarchy()` |
| Add component | `unityMCP_add_component(gameobject_path="..", component_type="..")` |
| Set property | `unityMCP_set_property(gameobject_path="..", component_type="..", property_name="..", value="..")` |
| Create GameObject | `unityMCP_create_game_object(name="..", position="..")` |
| Capture UI | `unityMCP_capture_ui_canvas()` |

### Editor Tool Verification Flow

```
1. [Write editor script to Assets/Scripts/Editor/]
2. unityMCP_check_compile_errors             → Verify script compiles
3. unityMCP_execute_script(filePath="...")    → Run the editor tool
4. unityMCP_get_unity_logs()                 → Check for errors/output
5. unityMCP_capture_ui_canvas()              → Validate UI if applicable
```

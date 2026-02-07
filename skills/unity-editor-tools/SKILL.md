---
name: unity-editor-tools
description: "Create Unity Editor tools. Use when: (1) Custom Editor Windows/Inspectors, (2) Automating asset/scene validation, (3) Building engineer utilities (search, batch processors), (4) UI Toolkit (UXML/USS) interfaces."
---

# Unity Editor Developer

Extend the Unity Editor with tools and automation.

## Output Requirement (MANDATORY)

**Every editor tool MUST follow one of the templates**:
- [EDITOR_WINDOW_TEMPLATE.md](assets/templates/EDITOR_WINDOW_TEMPLATE.md) — for EditorWindow tools
- [CUSTOM_INSPECTOR_TEMPLATE.md](assets/templates/CUSTOM_INSPECTOR_TEMPLATE.md) — for Custom Inspectors

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
3. **Implement**: Use templates from `assets/templates/`, patterns from [EDITOR_SCRIPTING_PATTERNS.md](references/EDITOR_SCRIPTING_PATTERNS.md)
4. **Verify**: Test domain reloads, scene changes, profile if handling large data

## Best Practices

- **Undo Mandatory**: Always use `SerializedObject` or `Undo.RecordObject`
- **Match Engine**: Use USS themes for Dark/Light mode
- **Progress Bars**: `EditorUtility.DisplayProgressBar` for batch tasks
- **Batch Safety**: Wrap in `StartAssetEditing`/`StopAssetEditing`
- **No Polling**: Use `TrackPropertyValue` or events, not OnGUI checks

## Templates

- [EDITOR_WINDOW_TEMPLATE.md](assets/templates/EDITOR_WINDOW_TEMPLATE.md)
- [CUSTOM_INSPECTOR_TEMPLATE.md](assets/templates/CUSTOM_INSPECTOR_TEMPLATE.md)
- [EDITOR_UI_TOOLKIT_GUIDE.md](references/EDITOR_UI_TOOLKIT_GUIDE.md)

---
name: unity-editor-tools
description: "(opencode-project - Skill) Create Unity Editor tools and extensions. Use when: (1) Custom Editor Windows/Inspectors, (2) Automating asset/scene validation, (3) Building engineer utilities (search, batch processors), (4) UI Toolkit (UXML/USS) editor interfaces, (5) Custom Gizmos and Handles, (6) Editor-only automation scripts. Triggers: 'editor window', 'custom inspector', 'PropertyDrawer', 'EditorWindow', 'ScriptableWizard', 'menu item', 'MenuItem', 'asset validation', 'scene validation', 'batch processor', 'editor utility', 'IMGUI', 'editor UI Toolkit', 'SerializedProperty', 'SerializedObject', 'OnInspectorGUI', 'CreateAssetMenu', 'editor automation', 'editor tool', 'custom tool', 'editor script', 'Gizmos', 'Handles', 'editor extension', 'toolbar button'."
---

# Unity Editor Developer

**Input**: Description of Editor tool or automation needed. Optional: target component/asset types, UI framework preference (UI Toolkit vs IMGUI).

## Output

Unity Editor tool scripts (C#) following the Templates below.

## Templates (MANDATORY)

- [EDITOR_WINDOW_TEMPLATE.md](assets/templates/EDITOR_WINDOW_TEMPLATE.md)
- [CUSTOM_INSPECTOR_TEMPLATE.md](assets/templates/CUSTOM_INSPECTOR_TEMPLATE.md)
- [EDITOR_SCRIPTING_PATTERNS.md](references/EDITOR_SCRIPTING_PATTERNS.md)
- [EDITOR_UI_TOOLKIT_GUIDE.md](references/EDITOR_UI_TOOLKIT_GUIDE.md)

Read the relevant template first, then populate all sections.

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
3. **Implement**: Use templates, patterns from references
4. **Verify**: Test domain reloads, scene changes, profile if handling large data

## Best Practices

- **Undo Mandatory**: Always use `SerializedObject` or `Undo.RecordObject`
- **Match Engine**: Use USS themes for Dark/Light mode
- **Progress Bars**: `EditorUtility.DisplayProgressBar` for batch tasks
- **Batch Safety**: Wrap in `StartAssetEditing`/`StopAssetEditing`
- **No Polling**: Use `TrackPropertyValue` or events, not OnGUI checks

---
name: unity-code-editor
description: "(opencode-project - Skill) Write Unity Editor C# code — custom EditorWindows, Inspectors, PropertyDrawers, ScriptableWizards, editor automation scripts, asset/scene validation tools, and batch processors. Covers both UI Toolkit (UXML/USS) and IMGUI approaches, Gizmos, Handles, MenuItem/Shortcut registration, SerializedObject/Property workflows, and AssetPostprocessor pipelines. Triggers: 'editor window', 'custom inspector', 'PropertyDrawer', 'EditorWindow', 'ScriptableWizard', 'menu item', 'MenuItem', 'asset validation', 'scene validation', 'batch processor', 'editor utility', 'IMGUI', 'editor UI Toolkit', 'SerializedProperty', 'SerializedObject', 'OnInspectorGUI', 'CreateAssetMenu', 'editor automation', 'editor tool', 'custom tool', 'editor script', 'Gizmos', 'Handles', 'editor extension', 'toolbar button', 'write editor code', 'create editor tool'."
---

# Unity Editor Code Writer

**Input**: Description of Editor tool or automation needed. Optional: target component/asset types, UI framework preference (UI Toolkit vs IMGUI).

## Output

Production-ready Unity Editor C# scripts following the Templates below.

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

## Workflow & Best Practices

Follow [workflow.md](references/workflow.md) — Assess → Architect → Implement → Verify + key rules.

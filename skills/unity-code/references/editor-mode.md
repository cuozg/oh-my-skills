# Editor Mode — Unity Editor Scripts

Write production-quality Editor scripts: inspectors, windows, drawers, gizmos, and menu items.

## Workflow

1. **Identify** — determine extension type: CustomEditor, EditorWindow, PropertyDrawer, Gizmo/Handle, MenuItem
2. **Locate** — find and read the target MonoBehaviour/SO/struct fully before writing
3. **Implement** — write the editor script using the correct base class and API
4. **Place** — save under an `Editor/` folder at any depth; never in Runtime
5. **Verify** — `lsp_diagnostics` on new file; fix all errors before declaring done

## Rules

- Always save under `Editor/` (compile-guard for editor-only APIs)
- Never add `using UnityEditor` to runtime scripts
- Use `[CustomEditor(typeof(X))]` on the class declaration
- Call `base.OnInspectorGUI()` before custom GUI unless fully replacing the inspector
- `serializedObject.Update()` / `ApplyModifiedProperties()` around all `SerializedProperty` edits
- Prefer `SerializedProperty` over direct field access — supports Undo and Prefab overrides
- `EditorGUILayout` for window/inspector GUI; `EditorGUI` for fixed-rect drawing
- Register EditorWindow via `GetWindow<T>()` inside a `[MenuItem]` static method
- `GUILayout.BeginHorizontal/Vertical` for layout; avoid magic pixel offsets
- Add `[InitializeOnLoad]` only when truly needed (slows editor startup)
- Null-guard `target` casts in `OnInspectorGUI`
- Handle Undo: `Undo.RecordObject(target, "action")` before mutations
- Wrap Handles/Gizmos in `#if UNITY_EDITOR` when referenced from runtime code
- Use `EditorUtility.SetDirty(target)` after direct mutations to mark scene dirty

## Extension Types

| Type | Base Class | Attribute | Entry Point |
|------|-----------|-----------|-------------|
| Custom Inspector | `Editor` | `[CustomEditor(typeof(X))]` | `OnInspectorGUI()` |
| Editor Window | `EditorWindow` | — | `[MenuItem] + GetWindow<T>()` |
| Property Drawer | `PropertyDrawer` | `[CustomPropertyDrawer(typeof(X))]` | `OnGUI(Rect, SerializedProperty, GUIContent)` |
| Scene Handles | `Editor` | `[CustomEditor(typeof(X))]` | `OnSceneGUI()` |

## Standards

Load boilerplate and examples on demand:

- `code-standards/editor-patterns.md` — EditorWindow, CustomEditor, PropertyDrawer minimal boilerplate
- `code-standards/gizmos-handles.md` — OnDrawGizmos, Handles in CustomEditor, SceneView repaint

Load via `read_skill_file("unity-standards", "references/<path>")`.

---
name: unity-code-editor
description: >
  Use this skill to write Unity Editor tooling — EditorWindows, CustomEditor inspectors, PropertyDrawers,
  Gizmos, Handles, and MenuItem commands. Use it for any editor extension task, including custom inspectors
  for components or ScriptableObjects, scene-view tools with Handles, editor windows for workflow
  automation, or menu items. Use whenever the user says "custom inspector," "editor window," "add a menu
  item," "gizmo," or wants any Editor-only tooling. Do not use for runtime scripts — use unity-code-quick
  or unity-code-deep.
metadata:
  author: kuozg
  version: "1.0"
---
# unity-code-editor

Write production-quality Unity Editor scripts — custom inspectors, editor windows, property drawers, and scene-view tools.

## When to Use

- Building a custom Inspector or window for a component or SO
- Adding Gizmos/Handles for scene-view visualization
- Creating [MenuItem] tools, context menus, or editor utilities
- Writing PropertyDrawers for serialized field rendering
- Automating editor workflows via EditorWindow

## Workflow

1. **Identify** — determine the editor extension type needed (window, inspector, drawer, gizmo)
2. **Locate** — find the target MonoBehaviour/SO/struct; read it fully before writing
3. **Implement** — write the editor script using the correct base class and API
4. **Place** — always save to an `Editor/` folder (any depth); never in Runtime
5. **Verify** — run lsp_diagnostics on new file; fix all errors before declaring done

## Rules

- Always save editor scripts under an `Editor/` folder (compile-guard)
- Never add `using UnityEditor` to runtime scripts
- Use `[CustomEditor(typeof(X))]` on the class, not in a method
- Call `base.OnInspectorGUI()` before custom GUI unless fully replacing it
- Wrap Handles/Gizmos in `#if UNITY_EDITOR` when referenced from runtime code
- Use `serializedObject.Update()` / `ApplyModifiedProperties()` around SerializedProperty edits
- Use `EditorGUILayout` for window/inspector GUI; `EditorGUI` for fixed-rect drawing
- Register EditorWindow via `GetWindow<T>()` inside a `[MenuItem]` static method
- Prefer `SerializedProperty` over direct field access to support Undo/Prefab overrides
- Use `GUILayout.BeginHorizontal/Vertical` for layout; avoid magic pixel offsets
- Add `[InitializeOnLoad]` only when truly needed (slows editor startup)
- Add null-guards on `target` casts in OnInspectorGUI
- Handle Undo with `Undo.RecordObject(target, "action name")` before mutations

## Output Format

Production Editor scripts placed under the appropriate `Editor/` folder, zero compiler errors, Undo-safe.

## Standards

Load `unity-standards` for coding conventions when writing editor scripts. Key references:

- `code-standards/naming.md` — casing, prefixes, namespace, file naming
- `code-standards/formatting.md` — braces, spacing, line length, regions
- `code-standards/serialization.md` — SerializeField, field:, JsonUtility, SO data
- `code-standards/lifecycle.md` — Awake/Start/OnEnable order, coroutine rules
- `code-standards/null-safety.md` — null checks, TryGet, nullable patterns

Load via `read_skill_file("unity-standards", "references/code-standards/<file>")`.

## Reference Files

- `references/editor-patterns.md` — EditorWindow, CustomEditor, PropertyDrawer patterns with minimal boilerplate
- `references/gizmos-handles.md` — Gizmos, Handles, SceneView patterns and OnDrawGizmos examples

Load references on demand via `read_skill_file("unity-code-editor", "references/{file}")`.

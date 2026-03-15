---
name: unity-editor
description: >
  Write Unity Editor scripts — custom inspectors, editor windows, property drawers, scene
  handles, gizmos, and menu items. Auto-triages: Quick (single editor script — one inspector,
  one window, one drawer) or Deep (multi-file editor tooling — level editors, custom pipelines,
  inspector + gizmos + window combos). MUST use for ANY Unity Editor code request — custom
  inspectors, editor windows, property drawers, gizmos, handles, menu items, scene tools.
  Triggers: "custom inspector," "editor window," "property drawer," "gizmo," "scene handles,"
  "menu item," "editor tool," "custom editor." Do not use for runtime scripts (unity-code),
  UI Toolkit (unity-uitoolkit), tests (unity-test-unit), or debugging (unity-debug).
metadata:
  author: kuozg
  version: "1.0"
---
# unity-editor

Detect scope, pick extension type, implement. Place under `Editor/`, verify compilation.

## Step 1 — Detect Scope

| Signal | Scope |
|--------|-------|
| One editor script (inspector, window, or drawer) | **Quick** |
| 2+ editor files, complex tooling (window + inspector + gizmos) | **Deep** |

State triage: "This is [scope] — [reason]."

## Step 2 — Identify Extension Type

| Type | Base Class | Attribute | Entry Point |
|------|-----------|-----------|-------------|
| Custom Inspector | `Editor` | `[CustomEditor(typeof(X))]` | `OnInspectorGUI()` |
| Editor Window | `EditorWindow` | — | `[MenuItem] + GetWindow<T>()` |
| Property Drawer | `PropertyDrawer` | `[CustomPropertyDrawer(typeof(X))]` | `OnGUI(Rect, SerializedProperty, GUIContent)` |
| Scene Handles | `Editor` | `[CustomEditor(typeof(X))]` | `OnSceneGUI()` |

## Step 3 — Execute

### Quick Scope

1. **Qualify** — confirm one editor `.cs` file suffices; escalate to Deep if scope grows
2. **Discover** — read target runtime class fully before writing editor code; check nearby Editor/ for style
3. **Implement** — write editor script under `Editor/` folder using correct base class and API
4. **Verify** — `lsp_diagnostics` on new file
5. **Handoff** — file path, what it does, diagnostics result

### Deep Scope

1. **Qualify** — confirm 2+ editor files needed; switch to Quick if single-file
2. **Discover** — read all target runtime classes + existing Editor/ scripts for style/patterns
3. **Plan** — list every file, its extension type, and dependency order
4. **Implement** — shared utilities first → individual editors → integration (menus, shortcuts)
5. **Verify** — `lsp_diagnostics` on all files
6. **Handoff** — all paths, what each does, editor follow-up (menu locations, shortcuts)

## Rules

- Always save under `Editor/` folder (compile-guard for editor-only APIs)
- Never add `using UnityEditor` to runtime scripts
- Use `[CustomEditor(typeof(X))]` on class declaration
- Call `base.OnInspectorGUI()` before custom GUI unless fully replacing inspector
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
- Local style wins — project patterns trump references
- Never leave `TODO`, stubs, or partially wired code
- One type per file, file name = type name
- `lsp_diagnostics` after every code change

## Escalation

| From | To | When |
|------|----|------|
| Quick | Deep | Work requires a second editor file |
| Deep | Quick | Plan reveals single-file scope |
| Any | unity-code | Target is runtime domain (MonoBehaviour, SO, service) |

Carry forward context; tell user why.

## Standards

Load on demand via `read_skill_file("unity-standards", "references/<path>")`:

- `code-standards/editor-patterns.md` — EditorWindow, CustomEditor, PropertyDrawer boilerplate
- `code-standards/gizmos-handles.md` — OnDrawGizmos, Handles in CustomEditor, SceneView repaint
- `code-standards/naming.md` · `serialization.md` · `null-safety.md`

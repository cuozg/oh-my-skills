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
  version: "1.1"
---
# unity-editor

Detect scope, identify extension type, implement editor script under `Editor/`, verify compilation.

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

**Quick:** Qualify → Discover (read target runtime class + nearby `Editor/`) → Implement → `lsp_diagnostics` → Handoff  
**Deep:** Qualify → Discover (all target classes + existing `Editor/` scripts) → Plan (list all files, types, dependency order) → Implement (shared utilities → individual editors → menus/shortcuts) → `lsp_diagnostics` → Handoff

## MCP Editor Tools

| Action | Tool |
|--------|------|
| Manage tags/layers | `Unity.ManageEditor` (AddTag, RemoveTag, AddLayer, GetLayers) |
| Execute/find menu items | `Unity.ManageMenuItem` (List → Execute) |
| Check editor state/selection | `Unity.ManageEditor` (GetState, GetSelection, GetPrefabStage) |
| Verify compilation | `Unity.ReadConsole` or `Unity.GetConsoleLogs` |

Full MCP routing: `read_skill_file("unity-standards", "references/other/unity-mcp-routing-matrix.md")` → Editor Control Branch.

## Rules

- Always save under `Editor/` folder
- Never add `using UnityEditor` to runtime scripts
- Call `base.OnInspectorGUI()` before custom GUI unless fully replacing
- `serializedObject.Update()` / `ApplyModifiedProperties()` around all `SerializedProperty` edits
- Prefer `SerializedProperty` over direct field access (supports Undo + Prefab overrides)
- `EditorGUILayout` for window/inspector GUI; `EditorGUI` for fixed-rect drawing
- Register EditorWindow via `GetWindow<T>()` inside `[MenuItem]` static method
- Null-guard `target` casts in `OnInspectorGUI`
- `Undo.RecordObject(target, "action")` before mutations
- Wrap Handles/Gizmos in `#if UNITY_EDITOR` when referenced from runtime code
- `EditorUtility.SetDirty(target)` after direct mutations
- Local style wins · One type per file · `lsp_diagnostics` after every change

## Escalation

| To | When |
|----|------|
| Deep | Work requires a second editor file |
| Quick | Plan reveals single-file scope |
| `unity-code` | Target is runtime domain |

## Standards

`read_skill_file("unity-standards", "references/<path>")`:
- `code-standards/architecture-systems.md` — Editor patterns, gizmos, handles
- `code-standards/core-conventions.md` — naming, serialization, null safety
- `other/unity-mcp-routing-matrix.md` — MCP editor control tools, guard clauses

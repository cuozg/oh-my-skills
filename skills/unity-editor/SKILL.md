---
name: unity-editor
description: >
  Write Unity Editor scripts — custom inspectors, editor windows, property drawers, scene
  handles, gizmos, and menu items. Auto-triages: Quick (single editor script — one inspector,
  one window, one drawer) or Deep (multi-file editor tooling — level editors, custom pipelines,
  inspector + gizmos + window combos). MUST use for ANY Unity Editor code request — custom
  inspectors, editor windows, property drawers, gizmos, handles, menu items, scene tools.
  Triggers: "custom inspector," "editor window," "property drawer," "gizmo," "scene handles,"
  "menu item," "editor tool," "custom editor." Do not use for runtime scripts (unity-standards),
  runtime UI Toolkit (unity:ui-uitk), tests (unity-test-unit), or debugging (unity-debug).
metadata:
  author: kuozg
  version: "2.0"
---
# unity-editor

Detect scope, identify extension type, implement editor script in an Editor-only assembly, verify compilation through the `unity` CLI.

Baseline: Unity 6.0+. Default to **UI Toolkit** for inspectors, drawers, and windows (Unity 6 draws default inspectors with UI Toolkit); use IMGUI only when the surrounding code already does, or for `OnSceneGUI` handles.

## Step 1 — Detect Scope

| Signal | Scope |
|--------|-------|
| One editor script (inspector, window, or drawer) | **Quick** |
| 2+ editor files, complex tooling (window + inspector + gizmos) | **Deep** |

State triage: "This is [scope] — [reason]."

## Step 2 — Identify Extension Type

| Type | Base Class | Attribute | Entry Point (UI Toolkit → IMGUI fallback) |
|------|-----------|-----------|-------------|
| Custom Inspector | `Editor` | `[CustomEditor(typeof(X))]` | `CreateInspectorGUI()` → `OnInspectorGUI()` |
| Editor Window | `EditorWindow` | `[MenuItem]` on static opener | `CreateGUI()` → `OnGUI()`; open via `GetWindow<T>()` |
| Property Drawer | `PropertyDrawer` | `[CustomPropertyDrawer(typeof(X))]` | `CreatePropertyGUI(SerializedProperty)` → `OnGUI(Rect, SerializedProperty, GUIContent)` |
| Scene Handles | `Editor` | `[CustomEditor(typeof(X))]` | `OnSceneGUI()` (IMGUI `Handles`) |
| Gizmos | runtime `MonoBehaviour` or static | `[DrawGizmo]` for editor-side | `OnDrawGizmos()` / `OnDrawGizmosSelected()` |

## Step 3 — Execute

**Quick:** Qualify → Discover (read target runtime class + nearby `Editor/` + asmdefs) → Implement → Verify compile → Handoff
**Deep:** Qualify → Discover (all target classes + existing `Editor/` scripts + asmdefs) → Plan (list all files, types, dependency order) → Implement (shared utilities → individual editors → menus/shortcuts) → Verify compile → Handoff

**Verify compile** = run the preflight and compile check in `../unity-standards/references/other/unity-cli-routing.md`:
`unity status` → `unity command recompile` (name as listed by `unity command`) → console/log scan for `error CS`. If the Editor is in Safe Mode, read `<project>/Logs/Editor.log`, fix, restart. Report "compile not verified" when no Editor is reachable.

## Editor Actions via `unity` CLI

Discover exact command names with `unity command --query <term>` first; pass `--caller plugin --skill unity-editor`.

| Action | Route |
|--------|-------|
| Check editor state / selection | `unity status --format json`, then the state/selection command the Editor lists |
| Execute a menu item or inspect tags/layers | listed menu/editor command, else `unity command eval "…"` (small, read-only unless mutation is the task) |
| Verify compilation | `recompile` + console scan (see above) |
| Visual check of a window/inspector | `unity command screenshot --output <png>` |
| Expose the new tool to agents/CI | add a `[CliCommand]` method (see `unity:unity-cli` → integration-advanced) — only when asked |

## Rules

- Editor code lives under an `Editor/` folder or an Editor-only asmdef (`"includePlatforms": ["Editor"]`)
- Runtime scripts reference `UnityEditor` only inside `#if UNITY_EDITOR` (e.g. `Handles` in `OnDrawGizmos`); `Gizmos` is runtime-safe
- IMGUI inspector: call `base.OnInspectorGUI()` / `DrawDefaultInspector()` unless fully replacing
- Bind UI Toolkit fields with `PropertyField` / `BindProperty`; IMGUI: wrap edits in `serializedObject.Update()` / `ApplyModifiedProperties()`
- Prefer `SerializedProperty` over direct field access (supports Undo, multi-edit, prefab overrides)
- Direct object mutation: `Undo.RecordObject(target, "action")` first (marks dirty); prefab instances also need `PrefabUtility.RecordPrefabInstancePropertyModifications`
- `EditorUtility.SetDirty(asset)` only for asset changes made without Undo
- `EditorGUILayout` for layout GUI; `EditorGUI` for fixed-rect drawing
- Null-guard `target` casts
- Local style wins · One type per file · Verify compile after every change

## Escalation

| To | When |
|----|------|
| Deep | Work requires a second editor file |
| Quick | Plan reveals single-file scope |
| `unity-standards` | Target is runtime domain |
| `unity:ui-imgui` / `unity:ui-uitk` | Deep IMGUI or UI Toolkit styling/layout questions |

## Standards

Read from `../unity-standards/references/`:
- `code-standards/architecture-systems.md` — Editor patterns, gizmos, handles, asmdefs
- `code-standards/core-conventions.md` — naming, serialization, null safety
- `other/unity-cli-routing.md` — Editor preflight, compile check, Safe Mode

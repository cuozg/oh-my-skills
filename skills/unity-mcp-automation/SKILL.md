---
name: unity-mcp-automation
description: "Standardize safe, repeatable use of Unity MCP tools across scripts, scenes, GameObjects, assets, packages, editor state, console checks, commands, captures, and validation. MUST use as a meta-skill for MCP-heavy Unity tasks spanning multiple tool categories. Do not replace specific skills such as unity-code, unity-debug, unity-scene-builder, unity-asset-generation, or unity-package-manager when one clearly owns the task."
metadata:
  author: kuozg
  version: "1.0"
---
# unity-mcp-automation

Coordinate Unity MCP tool usage safely when a task spans multiple editor-control categories.

## When to use

Use as a meta-skill for tasks that combine several MCP areas, such as:

- Script edits plus scene validation plus console checks.
- Asset operations plus GameObject wiring plus captures.
- Scene changes plus prefab creation plus hierarchy inspection.
- Package or project state inspection plus validation reports.

If one specialized Unity skill clearly applies, use that skill instead and load this only for MCP sequencing guidance.

## Safe sequencing

1. Inspect current state before editing.
2. Choose the narrowest MCP tool that can perform the action.
3. Make one logical change set at a time.
4. Validate immediately after each change set.
5. Read Unity console logs before claiming success.
6. Report exact files, assets, scene objects, and evidence.

## MCP tool map

- Scripts: use `ReadResource`, `FindInFile`, `GetSha`, `CreateScript`, `ScriptApplyEdits`, `ApplyTextEdits`, and `ValidateScript`.
- Scenes: use `ManageScene` for load/save/create/hierarchy/build settings.
- GameObjects: use `ManageGameObject` for create/modify/find/component inspection and prefab save operations.
- Assets: use `ManageAsset` for import/create/modify/delete/duplicate/move/rename/search/get info.
- Packages: use `PackageManager_GetData` and `PackageManager_ExecuteAction` only with explicit package-change approval.
- Editor state: use `ManageEditor` for play state, selection, tags, layers, and project root.
- Console: use `ReadConsole` or `GetConsoleLogs` after code, package, asset, or scene changes.
- Captures: use camera or scene-view capture tools only when visual validation is necessary.
- Commands: use `RunCommand` for targeted UnityEditor automation when safer MCP tools cannot do the job.

## Safety rules

- Prioritize non-destructive inspection before Unity editor changes.
- Do not perform package changes, scene saves, asset deletion, project settings changes, or command execution without clear user intent.
- For script edits, verify current content and SHA before precise text edits.
- For scene edits, inspect hierarchy before modifying and validate object placement afterward.
- For asset generation, delegate to `unity-asset-generation`.
- For package operations, delegate to `unity-package-manager`.
- Avoid broad automation scripts when a targeted MCP operation exists.

## Verification patterns

- Script changes: run script validation and check Unity console.
- Scene changes: inspect hierarchy, components, transforms, and capture when visual layout matters.
- Asset changes: confirm asset existence, type, import status, and references.
- Package changes: confirm manifest/lock state, package manager resolution, and console logs.
- Project settings changes: re-read relevant settings and check console.

## Boundaries

- `unity-code` owns runtime C# implementation.
- `unity-debug` owns errors and root-cause analysis.
- `unity-scene-builder` owns scene creation and layout.
- `unity-asset-generation` owns generated assets.
- `unity-package-manager` owns package changes.

## Handoff

Report tool sequence, state inspected before edits, exact changes, validation evidence, console status, and remaining risks.

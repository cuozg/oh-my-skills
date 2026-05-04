---
name: unity-project-settings
description: "Safely inspect and modify Unity project-level settings including tags, layers, build settings, Player Settings, quality settings, package/project configuration, and editor settings. MUST use for high-impact project configuration changes that require read-before-write discipline and console verification. Avoid bulk settings rewrites when targeted changes are possible."
metadata:
  author: kuozg
  version: "1.0"
---
# unity-project-settings

Handle Unity project configuration with conservative inspection, targeted edits, and validation.

## When to use

Use for:

- Tags and layers.
- Build settings and scenes in build.
- Player Settings and platform project configuration.
- Quality settings and graphics settings review.
- Package/project configuration under `ProjectSettings/` and `Packages/`.
- Editor settings that affect project behavior.

Treat project settings as high-impact changes requiring explicit user intent.

## Discovery

1. Read current setting files or MCP state before applying changes.
2. Identify the narrow setting category being changed.
3. Check for platform-specific implications.
4. Inspect package state when settings depend on installed packages.
5. Record current value before modification so the change can be explained.

## MCP tool usage

- Use `ManageEditor(GetTags/AddTag/RemoveTag/GetLayers/AddLayer/RemoveLayer)` for tags and layers.
- Use `ManageScene(GetBuildSettings)` for scenes in build where available.
- Use `ManageMenuItem(List/Exists/Execute)` for known safe editor menu operations after confirming exact menu path.
- Use `ManageAsset(GetInfo/Search)` for settings assets and configuration files.
- Use `RunCommand` for targeted UnityEditor settings reads or writes only when no safer MCP tool exists.
- Use `ReadConsole` or `GetConsoleLogs` after settings changes.

## Safety rules

- Require explicit user intent before changing project settings.
- Read current settings before writing.
- Avoid bulk settings rewrites when targeted changes are possible.
- Do not switch platforms, change signing, alter bundle identifiers, or rewrite build settings without explicit approval.
- Preserve unknown settings and formatting where possible.
- Prefer adding missing tags/layers over renumbering or deleting existing ones.

## Validation

Verify:

- Re-read the relevant setting after change.
- Confirm tags, layers, scenes, or settings show the intended value.
- Check Unity console for project setting, import, package, or compile errors.
- For build/player settings, verify target platform implications are documented.
- For quality settings, verify the target quality tier or asset was actually changed.

## Boundaries

- Delegate platform build readiness to `unity-build-pipeline`.
- Delegate Android/iOS-specific resolver and permission issues to `unity-mobile`.
- Delegate package operations to `unity-package-manager`.
- Delegate runtime behavior changes to `unity-code`.

## Handoff

Report previous value, new value, MCP tools used, verification evidence, console status, and any rollback considerations.

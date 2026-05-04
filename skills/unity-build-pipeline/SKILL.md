---
name: unity-build-pipeline
description: "Prepare and validate Unity builds across Android, iOS, desktop, and CI. MUST use for build readiness checks, Player Settings validation, scenes-in-build review, scripting defines, package resolution, platform requirements, CI build configuration, and non-WebGL build pipeline issues. Delegate WebGL-only work to unity-webgl and do not change platform/signing settings without explicit approval."
metadata:
  author: kuozg
  version: "1.0"
---
# unity-build-pipeline

Assess and prepare Unity projects for reliable platform builds without making high-impact settings changes implicitly.

## When to use

Use for:

- Android, iOS, desktop, and CI build preparation.
- Player Settings, Build Settings, scenes in build, and platform module readiness.
- Scripting define symbols and conditional compilation checks.
- Package resolution and dependency consistency before builds.
- Build readiness reports and preflight validation.

Use `unity-webgl` for WebGL compression, templates, browser integration, and WebGL-specific deployment.

## Discovery

1. Read `ProjectSettings/ProjectSettings.asset` and relevant package settings before changes.
2. Inspect `ProjectSettings/EditorBuildSettings.asset` for scenes in build.
3. Inspect `Packages/manifest.json` and `Packages/packages-lock.json` for package state.
4. Check platform-specific folders such as `Assets/Plugins/Android` only when relevant.
5. Identify existing build scripts, CI config, scripting defines, and asmdef constraints.

## MCP and verification tools

- Use `ManageEditor(GetState)` to inspect editor state and active platform context.
- Use `ManageScene(GetBuildSettings)` for scenes/build settings where available.
- Use `ManageAsset(GetInfo/Search)` for settings assets, plugins, scenes, and package assets.
- Use `ReadConsole` or `GetConsoleLogs` to verify compile/import state.
- Use Unity compile-check tooling for ground-truth C# compilation.
- Use `RunCommand` only for targeted UnityEditor build-settings inspection when MCP data is insufficient.

## Safety rules

- Do not switch build targets without explicit user approval.
- Do not alter signing settings, bundle identifiers, provisioning, Gradle templates, or iOS entitlements without approval.
- Prefer read-only build readiness reports before making changes.
- Keep WebGL-only recommendations delegated to `unity-webgl`.
- Avoid broad Player Settings rewrites; make targeted changes only.

## Build readiness checklist

Check:

- Scenes in build are present, enabled, and ordered intentionally.
- Player Settings match target platform requirements.
- Scripting defines and asmdefs are compatible with the target.
- Packages resolve cleanly in `manifest.json` and `packages-lock.json`.
- Platform plugins are scoped correctly.
- Unity console has no compile, import, resolver, or build-prep errors.
- CI scripts, if present, call Unity with expected project path, target, and batchmode flags.

## Boundaries

- `unity-mobile` handles Android/iOS resolver, permissions, mobile SDK, and device-specific troubleshooting.
- `unity-sdk-integration` handles SDK package API and initialization boundaries.
- `unity-debug` handles specific compile/runtime errors.
- `unity-optimize` handles build size or performance optimization beyond readiness.

## Handoff

Report target platform, inspected settings, readiness verdict, blocking issues, risky settings, and exact user approvals needed before any high-impact change.

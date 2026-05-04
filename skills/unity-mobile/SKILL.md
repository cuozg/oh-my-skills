---
name: unity-mobile
description: "Validate and troubleshoot Unity Android and iOS projects, dependency resolver issues, Gradle settings, permissions, push notifications, ads, mobile SDK integration checks, and mobile build readiness. MUST use for mobile-specific Unity problems involving `Assets/Plugins/Android`, Mobile Dependency Resolver, Push Notifications, LevelPlay, platform permissions, or device-only behavior. Do not modify manifests, Gradle files, signing, or resolver config without approval."
metadata:
  author: kuozg
  version: "1.0"
---
# unity-mobile

Handle Unity Android and iOS readiness, platform integration, dependency resolution, and mobile SDK validation safely.

## When to use

Use for:

- Android and iOS project validation.
- Mobile Dependency Resolver issues.
- Gradle templates, Android manifests, iOS capabilities, permissions, and entitlements review.
- Push notifications, ads, LevelPlay, and mobile SDK integration checks.
- Mobile-specific build readiness or device-only behavior.

## Project areas

Inspect relevant areas when present:

- `Assets/Plugins/Android`
- `Assets/MobileDependencyResolver`
- `Assets/Push Notifications`
- `Assets/LevelPlay`
- `Packages/manifest.json`
- `Packages/packages-lock.json`
- `ProjectSettings/ProjectSettings.asset`
- `ProjectSettings/AndroidResolverDependencies.xml`

## MCP tool usage

- Use `ManageAsset(Search/GetInfo)` to locate manifests, Gradle templates, resolver assets, SDK folders, and mobile config assets.
- Use `PackageManager_GetData` for package metadata; delegate package changes to `unity-package-manager`.
- Use `ReadConsole` or `GetConsoleLogs` for resolver, Gradle, SDK, compile, or import errors.
- Use `ManageEditor(GetState)` to inspect editor state before platform-sensitive work.
- Use `RunCommand` only for targeted UnityEditor inspection when MCP tools cannot expose mobile settings.

## Safety rules

- Do not modify Android manifests, Gradle files, signing settings, resolver configuration, iOS provisioning, or entitlements without explicit approval.
- Preserve platform-specific compatibility constraints.
- Do not add production keys, secrets, or store identifiers to source-controlled files.
- Prefer read-only diagnosis before making platform file changes.
- Keep mobile-specific concerns separate from general build pipeline work.

## Validation

Verify:

- Dependency resolver state and generated dependency files are consistent.
- `manifest.json` and `packages-lock.json` are compatible with mobile SDK requirements.
- Android plugin folders, Gradle templates, manifests, and resolver files are present when needed.
- Permissions and platform capabilities match the requested mobile feature.
- Unity console has no resolver, package, Gradle template, SDK, compile, or import errors.
- Mobile build settings are compatible with target Android/iOS requirements.

## Boundaries

- Use `unity-build-pipeline` for general build readiness across platforms.
- Use `unity-sdk-integration` for package API, initialization, samples, and integration tests.
- Use `unity-liveops` for ads, analytics, push, IAP, remote config, and production operations behavior.
- Use `unity-debug` for specific compile/runtime errors.

## Handoff

Report platform, relevant project areas inspected, resolver/package/build-setting findings, changes avoided or requiring approval, and validation evidence.

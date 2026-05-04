---
name: unity-liveops
description: "Plan, inspect, and validate Unity LiveOps integrations for remote config, analytics, ads, IAP, economy tuning, events, A/B testing, push notifications, consent, and release-safe operations. MUST use for live game service readiness, SDK service initialization order, test-mode checks, privacy gates, and production configuration reviews. Do not add secrets or production keys to source-controlled files."
metadata:
  author: kuozg
  version: "1.0"
---
# unity-liveops

Coordinate Unity live game operations safely across services, SDKs, environments, privacy gates, and release readiness.

## When to use

Use for:

- Remote config, analytics, events, economy tuning, A/B testing, IAP, ads, and push notifications.
- LiveOps SDK initialization order and environment setup.
- Test mode versus production mode validation.
- Consent, privacy, platform compliance, and failure fallback review.
- Release-safe checks for mobile or SDK-heavy Unity projects.

## Discovery

1. Inspect `Packages/manifest.json`, `Packages/packages-lock.json`, and package folders for LiveOps-related SDKs.
2. Search relevant project areas such as `Assets/LevelPlay`, `Assets/Push Notifications`, `Assets/Plugins/Android`, and SDK packages.
3. Read initialization code, service registration, config assets, environment selectors, and sample scenes.
4. Identify consent/privacy gates before analytics, ads, push, or tracking calls.
5. Identify whether services run in test, staging, sandbox, or production mode.

## MCP tool usage

- Use `ManageAsset(Search/GetInfo)` to locate config assets, SDK folders, scenes, prefabs, and documentation.
- Use `ManageGameObject(GetComponents)` to inspect bootstrap objects and service components.
- Use `PackageManager_GetData` for package metadata; delegate package changes to `unity-package-manager`.
- Use `ReadConsole` or `GetConsoleLogs` to detect initialization, resolver, SDK, or platform errors.
- Use `ManageScene(GetHierarchy)` when validating bootstrap scene wiring.

## Safety rules

- Never add production keys, identifiers, secrets, tokens, or private endpoints to source-controlled files.
- Preserve privacy, consent, ATT/GDPR/COPPA, store policy, and regional compliance requirements.
- Keep production and test mode changes explicit.
- Prefer read-only audits before modifying service initialization.
- Do not enable monetization, push, analytics, or IAP behavior without clear user intent.

## Validation

Verify:

- Service initialization order is deterministic and dependency-safe.
- Consent gates run before data collection, ads personalization, push registration, or tracking prompts.
- Platform compatibility is documented for Android, iOS, editor, and unsupported platforms.
- Test mode or sandbox behavior is active when validating non-production integrations.
- Failure fallbacks exist for offline, SDK unavailable, consent denied, or initialization failed states.
- Unity console has no SDK initialization, resolver, package, or platform errors.

## Boundaries

- Delegate third-party SDK package structure and API boundaries to `unity-sdk-integration`.
- Delegate Android/iOS resolver, permissions, Gradle, and platform settings to `unity-mobile`.
- Delegate runtime gameplay code to `unity-code`.
- Delegate package installation to `unity-package-manager`.

## Handoff

Report services inspected, environment mode, privacy/consent status, initialization evidence, validation results, and any production-release blockers.

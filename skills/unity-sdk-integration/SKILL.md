---
name: unity-sdk-integration
description: "Maintain Unity SDK packages, package boundaries, editor integration, runtime initialization, service management, samples, integration tests, and third-party SDK boundaries. MUST use for `com.zeno.sdk`, SDK editor menus, package API compatibility, samples, initialization validation, and package-level integration checks. Preserve public SDK APIs unless breaking changes are explicitly requested."
metadata:
  author: kuozg
  version: "1.0"
---
# unity-sdk-integration

Support Unity SDK package integration while preserving public APIs, package boundaries, and assembly dependencies.

## When to use

Use for:

- SDK package structure and public API review.
- Editor integration, menus, settings assets, and samples.
- Runtime initialization and service management.
- Integration tests and package validation.
- Third-party SDK boundaries inside Unity packages.
- `com.zeno.sdk` and related package integration work.

## Project paths

Inspect relevant paths when present:

- `Packages/com.zeno.sdk`
- `Packages/com.zeno.evolution-tactics`
- `Docs/Architecture/ServiceManagement.md`
- `Docs/Specs/SDK_Core.md`
- `Docs/zeno-sdk-architecture.html`
- `Packages/manifest.json`
- `Packages/packages-lock.json`

## Discovery

1. Read package manifests, asmdefs, runtime/editor/test folders, and public entry points.
2. Inspect editor menu files, settings providers, sample folders, and integration tests.
3. Review service initialization order and dependency boundaries.
4. Identify public APIs before making changes.
5. Confirm package dependencies and assembly references before modifying package code.

## MCP/tool usage

- Use code search and file reads for package structure, APIs, asmdefs, and docs.
- Use `ManageMenuItem(List/Exists)` to verify editor menu availability.
- Use `ManageAsset(Search/GetInfo)` for package assets, settings, samples, and test assets.
- Use `ReadConsole` or `GetConsoleLogs` for compile, package, and assembly errors.
- Use Unity compile-check tooling for package compilation validation.
- Use `PackageManager_GetData` for package metadata; delegate package changes to `unity-package-manager`.

## Safety rules

- Preserve public SDK APIs unless the user explicitly requests breaking changes.
- Respect package boundaries and assembly definition dependencies.
- Do not move code between runtime/editor/test assemblies without dependency review.
- Avoid introducing project-only dependencies into reusable SDK packages.
- Keep third-party SDK integration behind clear boundaries or adapters.

## Validation

Verify:

- Package compiles without Unity console or assembly errors.
- Editor menus and settings integration are available when relevant.
- Runtime initialization and service management follow documented order.
- Samples import or run where present.
- Integration tests are identified and run or documented when available.
- Public API changes are intentional and documented.

## Boundaries

- Delegate mobile platform resolver, permissions, and Gradle issues to `unity-mobile`.
- Delegate package add/remove/embed operations to `unity-package-manager`.
- Delegate runtime gameplay feature code to `unity-code`.
- Delegate LiveOps production services to `unity-liveops`.

## Handoff

Report packages inspected, APIs or menus affected, tests/console validation, package-boundary considerations, and any breaking-change risks.

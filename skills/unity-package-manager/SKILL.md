---
name: unity-package-manager
description: "Inspect, install, remove, embed, unembed, and import samples for Unity packages through Unity MCP Package Manager tools. MUST use for package metadata checks, manifest/lock compatibility, adding or removing registry packages, embedding local packages, unembedding packages, and sample import. Never change packages without explicit user approval."
metadata:
  author: kuozg
  version: "1.0"
---
# unity-package-manager

Manage Unity package state safely through MCP package tools and manifest/lock validation.

## When to use

Use for:

- Package metadata inspection.
- Package installation, removal, embedding, or unembedding.
- Package sample import.
- Compatibility checks against current Unity package state.
- Package resolution troubleshooting.

## Discovery

1. Read `Packages/manifest.json` for direct dependencies and local package references.
2. Read `Packages/packages-lock.json` for resolved versions and transitive dependencies.
3. Inspect local packages such as `Packages/com.zeno.sdk` and `Packages/com.zeno.evolution-tactics` before changing references.
4. Use package metadata checks before proposing adds/removals.
5. Identify samples and sample indices before sample import.

## MCP tool usage

- Use `PackageManager_GetData` to inspect available or installed package metadata.
- Use `PackageManager_ExecuteAction` with `Add` only after approval and version selection.
- Use `PackageManager_ExecuteAction` with `Remove` only after approval and dependency impact review.
- Use `PackageManager_ExecuteAction` with `Embed` or `Unembed` only after approval and package-boundary review.
- Use `PackageManager_ExecuteAction` with `Sample` only after approval and sample index confirmation.
- Use `ReadConsole` or `GetConsoleLogs` after package operations.

## Safety rules

- Do not install, remove, embed, unembed, or import samples without explicit user approval.
- Preserve existing local package references unless the user requests a change.
- Check compatibility with `Packages/manifest.json` and `Packages/packages-lock.json` before changes.
- Avoid changing multiple packages in one step unless they are a known dependency set.
- Do not delete package folders manually as a substitute for package-manager operations.

## Validation

Verify:

- `manifest.json` reflects the intended direct dependency state.
- `packages-lock.json` resolves consistently after operations.
- Unity console has no package resolution, assembly, import, or compile errors.
- Local package references remain intact when not intentionally changed.
- Imported samples exist and are documented if sample import was requested.

## Boundaries

- Delegate runtime code changes inside packages to `unity-code`.
- Delegate SDK package structure and integration validation to `unity-sdk-integration`.
- Delegate mobile resolver/platform issues to `unity-mobile`.
- Delegate Addressables package setup decisions back to domain skills after package operations are complete.

## Handoff

Report package operation, version, manifest/lock evidence, console status, samples imported, and any approval-dependent next steps.

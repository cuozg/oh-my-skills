---
name: unity-addressables-content
description: "Manage Unity Addressables content strategy, groups, labels, asset references, remote catalogs, content builds, and content update validation. MUST use for Addressables setup, group or label organization, remote content delivery, catalog/update checks, runtime load-risk review, or deciding whether assets should become Addressables. Do not use for installing packages without delegating to unity-package-manager, or for unrelated runtime loading code."
metadata:
  author: kuozg
  version: "1.0"
---
# unity-addressables-content

Guide safe Addressables content-management work from discovery through validation.

## When to use

Use for:

- Addressables package setup planning and readiness checks.
- Addressables groups, labels, profiles, schemas, and asset references.
- Remote catalogs, remote load paths, content state, and content update checks.
- Build readiness for local or remote Addressables content.
- Runtime loading risk review, including missing references, bad labels, and invalid keys.

Do not migrate assets into Addressables unless the user explicitly approves the migration scope.

## Discovery

1. Check `Packages/manifest.json` and `Packages/packages-lock.json` for `com.unity.addressables` before assuming Addressables is installed.
2. Inspect `Assets/AddressableAssetsData/` if present.
3. Identify groups, labels, profiles, schemas, build/load paths, and content update settings.
4. Find code or assets using `AssetReference`, address keys, labels, or Addressables APIs.
5. If Addressables is missing and package installation is required, delegate installation to `unity-package-manager`.

## MCP tool usage

- Use `ManageAsset(Search/GetInfo)` to locate Addressables settings assets, groups, schemas, and referenced content.
- Use `PackageManager_GetData` only for package metadata; delegate package changes to `unity-package-manager`.
- Use `ReadConsole` or `GetConsoleLogs` after content or package changes.
- Use `RunCommand` only for targeted editor API inspection or validation when asset tools cannot expose needed Addressables data.
- Use `ManageEditor(GetState)` before disruptive editor operations.

## Safe operations

- Read current package and Addressables settings before proposing changes.
- Prefer adding or adjusting one group, label, schema, or profile at a time.
- Keep local and remote path changes explicit.
- Preserve existing addresses and labels unless the user requests renaming.
- Avoid bulk asset migration, bulk relabeling, or profile rewrites without approval.

## Validation

Verify:

- Addressables package presence and version compatibility.
- Group configuration, schemas, profiles, build/load paths, and remote catalog settings.
- Missing references, duplicate addresses, broken labels, invalid keys, and unassigned content.
- Content build readiness and content update restrictions.
- Unity console has no Addressables import, build, catalog, or script errors.

## Boundaries

- Delegate package installation/removal to `unity-package-manager`.
- Delegate generated assets to `unity-asset-generation` before making them Addressables.
- Delegate runtime gameplay loading systems to `unity-code`.
- Delegate platform build issues to `unity-build-pipeline` or `unity-mobile`.

## Handoff

Report changed or inspected groups, labels, profiles, catalog settings, validation evidence, and any migration risks that still require user approval.

# Addressables And Asset Manager Standards

Use this when a Unity task touches an asset manager, Addressables loading,
runtime asset catalogs, async asset handles, scene loading, or replacing
`Resources`/direct references with Addressables.

## First Read The Project

- Check `Packages/manifest.json` for the Addressables package version before
  relying on package-specific APIs.
- Find the existing loading abstraction first. Do not introduce a second asset
  manager when one already owns caching, release, retry, logging, or platform
  differences.
- Identify the asset identity used by the project: address string, label, GUID,
  `AssetReference`, enum, generated key, ScriptableObject table, or server
  payload.
- Trace both sides of the lifecycle: where the asset is requested and where the
  returned handle, instance, or loaded object is released.

## Addressables Loading Rules

- Prefer `AssetReference` or centralized keys over hard-coded address strings in
  feature code. Use string addresses only when the project already treats server
  or config payloads as authoritative keys.
- Keep Addressables API calls behind the existing asset manager or a small
  feature boundary. UI controllers and gameplay systems should not each invent
  their own loading, caching, and release policy.
- Treat `AsyncOperationHandle` ownership as a contract. The code that stores or
  receives a handle must know whether it is responsible for `Addressables.Release`
  or whether the manager retains ownership.
- Do not release a handle while live instances, sprites, materials, or dependent
  objects still reference the loaded asset.
- Do not keep loaded assets forever by default. Cache only assets with a clear
  reuse case and an explicit invalidation or release point.
- Avoid synchronous waits on Addressables loads in gameplay or UI flow. If the
  project uses async/await, coroutines, UniTask, or callbacks, follow that local
  async style consistently.
- For instantiated prefabs, use the project's established ownership rule:
  `Addressables.InstantiateAsync`/`ReleaseInstance`, or load prefab then instantiate
  and release through the manager. Do not mix policies inside one feature.

## Labels, Catalogs, And Groups

- Use labels for intentional sets: preload groups, themed asset families,
  platform-specific variants, or content-update bundles. Do not use broad labels
  that pull unrelated assets into memory.
- Group assets by loading and update behavior, not just folder structure. Assets
  loaded together and updated together usually belong together.
- Keep frequently reused shared dependencies stable. Moving one common material,
  sprite atlas, or shader into many groups can duplicate bundle dependencies.
- For remote catalogs or content updates, preserve fallback behavior when a key
  is missing, a catalog update fails, or a platform cannot reach the CDN.

## Remote Bundle Delivery Strategy

Remote content decisions affect build size, startup, download flow, QA cost, and
player experience. Load `../production/full-cycle-ownership.md` when the asset
change is part of LiveOps or release delivery.

- Keep stable shared assets such as common fonts, shaders, and atlases in local
  or shared groups when many remote bundles depend on them.
- Build local dependencies together when remote bundles require them.
- Choose compression by delivery path and measure the tradeoff: local bundles
  usually prefer fast load/decompress, remote bundles often prioritize download
  size.
- Define predownload vs lazy-load behavior and show UI for lazy-loaded content.
- Preload critical content before the player reaches the flow that needs it.
- Plan device-tier texture variants only when the project can absorb the build,
  QA, and memory complexity.

## Asset Manager Design

- The manager should make ownership explicit:
  - key resolution
  - load or instantiate API
  - cache policy
  - release policy
  - error/logging policy
  - editor/test fallback behavior
- Return the narrowest useful result. Prefer a typed asset, prefab instance, or
  project-specific load result over leaking raw Addressables details everywhere.
- Keep retry, fallback, and placeholder behavior at the manager or presenter
  boundary, not scattered through each view.
- Preserve server-authoritative asset keys when the backend controls content.
  Validate and hydrate from the response path; do not silently recompute a
  different local key.

## Verification

- Inspect Addressables groups, labels, and references for the touched assets.
- Prove missing-key, failed-load, and successful-load paths when changing the
  manager.
- Check for leaked handles or unreleased instances by exercising open/close,
  scene unload, popup close, or repeated UI refresh flows.
- For memory work, capture before/after memory or profiler evidence.
- For remote/content-update work, state whether remote catalog, CDN, and platform
  behavior were actually tested.

## Official Docs To Check

Use `references/other/official-source-map.md` and match the local package
version before making hard claims. Addressables APIs and content-update behavior
are package-version-dependent.

# Material Work

Use this when creating, editing, reviewing, or debugging Unity material assets,
material assignments, renderer material usage, UI materials, or runtime material
property changes.

## Efficient Workflow

1. Identify where the material is used: prefab, scene renderer, UI graphic,
   particle system, VFX, addressable asset, or runtime-created instance.
2. Confirm whether the change should affect every user of the shared material or
   only one renderer.
3. Inspect shader, render pipeline, render queue, keywords, texture imports, and
   batching constraints before changing many assets.
4. Prefer one targeted material edit over cloning near-identical materials.
5. Verify visually and, for batching claims, with Frame Debugger or profiler
   evidence.

## Standards

- Share material assets intentionally. Calling `.material` creates a
  per-renderer material instance and can break batching; use `.sharedMaterial`
  only when the shared asset should change for every user.
- Use `MaterialPropertyBlock` for per-renderer values when it fits the render
  pipeline and batching constraints. Verify the actual batching result with
  Frame Debugger or profiler.
- Keep material count low for repeated renderers and UI. Prefer shared
  materials, atlases, sprite atlases, or shader properties over many
  near-identical material assets.
- Check render queue, blend mode, z-write, transparency, culling, and sorting
  settings. Transparent materials often increase overdraw and sorting cost.
- Match texture import settings to use: UI sprites usually do not need mipmaps;
  3D textures usually do.
- Keep material keywords intentional. Extra enabled keywords can create shader
  variants, increase build size, or select a slower pass.
- Respect project naming and folder conventions for material assets and texture
  dependencies.

## Runtime Rules

- Avoid mutating shared materials at runtime unless changing all users is
  explicitly intended.
- Cache material/property IDs according to the project's style before hot-path
  updates.
- Clean up runtime-created material instances when the owning object lifecycle
  requires it.
- For pooled objects, reset material properties and renderer state before reuse.

## Verification

- Inspect affected prefabs or renderers to confirm the intended material asset is
  assigned.
- Use Frame Debugger for material, texture, pass, instancing, and SRP Batcher
  claims.
- Capture screenshots for visual material changes at the relevant quality level.
- For performance-sensitive changes, capture before/after batches, SetPass
  calls, overdraw, memory, or frame time.

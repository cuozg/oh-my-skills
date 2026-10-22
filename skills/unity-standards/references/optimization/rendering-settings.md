# Rendering Optimization Settings

Baseline: Unity 6 with URP 17 (Render Graph on by default). Built-in RP
migration: `unity:migrate-birp-to-urp`; post-processing: `unity:urp-postprocessing`.

## URP 17 Pipeline Settings (Unity 6)

| Setting | Where | Guidance |
|---------|-------|----------|
| Rendering Path | URP Renderer asset | Forward+ for many real-time lights (no per-object light limit); Forward for simple mobile scenes |
| Render Graph | Project Settings > Graphics | Keep enabled; Compatibility Mode is deprecated. Custom `ScriptableRendererFeature`s must implement `RecordRenderGraph` - validate with `unity:validate-urp-render-graph-renderer-feature` |
| Light Probe System | URP Asset > Lighting | Adaptive Probe Volumes replace hand-placed Light Probe Groups for large scenes; requires a bake and adds probe data memory |
| Upscaling Filter | URP Asset > Quality | STP when Render Scale < 1 on compute-capable hardware; measure GPU cost on mobile |

## Batching Choice Matrix

| Surface | Prefer | Watch For |
| --- | --- | --- |
| uGUI Canvas | See `canvas-ui-drawcalls-batching.md` | Masks, unique materials, layout rebuilds |
| Many static/dynamic MeshRenderers (URP/HDRP) | GPU Resident Drawer + SRP Batcher | Forward+ requirement, unsupported shaders, compute support |
| URP/HDRP renderers generally | SRP Batcher, shared shader variants | Non-compatible shaders, MaterialPropertyBlocks, CBUFFER layout |
| Repeated meshes, custom draw | GPU instancing / `Graphics.RenderMeshInstanced` | Unique materials, SRP Batcher taking precedence |
| Static environment without GPU Resident Drawer | Static batching | Memory growth and immovable objects |
| Small dynamic meshes | SRP Batcher or instancing first | Dynamic batching CPU cost |

## GPU Resident Drawer (Unity 6)

Uses `BatchRendererGroup` to draw MeshRenderers with GPU instancing automatically,
cutting CPU draw cost for large scenes.

**Enable:**
1. URP Asset > Rendering > GPU Resident Drawer: Instanced Drawing
2. URP Renderer > Rendering Path: Forward+
3. Project Settings > Graphics > BatchRendererGroup Variants: Keep All
4. Optional: URP Asset > GPU Occlusion for GPU occlusion culling

**Limits:** MeshRenderers only (not SkinnedMeshRenderer or particles); shaders
must support DOTS instancing (URP Lit/Unlit and Shader Graph do); renderers using
`MaterialPropertyBlock` fall back to the normal path; needs compute shader
support, so not on OpenGL ES / WebGL. Verify in Frame Debugger and with
CPU render-thread timings before/after.

## SRP Batcher

Reduces CPU draw call overhead by batching shader state changes (not objects).

**Requirements:**
- URP or HDRP (not built-in)
- Shader must declare `CBUFFER` for all material properties
- `UnityPerMaterial` and `UnityPerDraw` CBUFFERs properly declared

**Verify:** Frame Debugger -> look for "SRP Batch" entries; the shader Inspector
shows "SRP Batcher: compatible". Non-compatible shaders break batches, and
renderers using a `MaterialPropertyBlock` drop out of the SRP Batcher.

```
// In Shader: properties must be in CBUFFER
CBUFFER_START(UnityPerMaterial)
    float4 _BaseColor;
    float _Smoothness;
CBUFFER_END
```

## GPU Instancing

Renders multiple objects with same mesh+material in one draw call.

**Setup:**
1. Material Inspector -> Enable GPU Instancing checkbox
2. Shader must support instancing (`#pragma multi_compile_instancing`; URP Lit does)
3. Objects must share exact same material instance (not `.material` copies)
4. Per-instance values go through `MaterialPropertyBlock` with properties declared
   in `UNITY_INSTANCING_BUFFER`

**Limitations:** Does not work with SkinnedMeshRenderers. For manual control use
`Graphics.RenderMeshInstanced` (replaces `Graphics.DrawMeshInstanced`).

**SRP note:** In URP/HDRP, prefer SRP Batcher for compatible shaders unless the
project has measured that instancing is the better fit for a repeated mesh set.
Custom shaders generally need to be incompatible with SRP Batcher, or SRP Batcher
disabled, before GPU instancing becomes the active path.

## Static Batching

Combines static meshes at build time into large vertex buffers.

| Pro | Con |
|-----|-----|
| Zero CPU overhead at runtime | Increases build size + memory (duplicated vertices) |
| Works with any shader | Cannot move/animate batched objects |
| Simple: mark "Batching Static" | Large meshes may exceed 64K vertex limit |

**When:** Static environment geometry (buildings, terrain props, fences).
**Skip when:** Memory-constrained mobile, procedurally placed objects, objects that need movement.

## Dynamic Batching

Combines small dynamic meshes at runtime.

| Constraint | Limit |
|------------|-------|
| Vertex count | < 300 vertices per mesh |
| Vertex attributes | < 900 total attribute count |
| Materials | Must share exact same material |
| Scale | Must have same uniform scale (or all non-uniform) |

**Reality:** Rarely beneficial with SRP Batcher enabled. CPU cost of combining can exceed draw call savings. **Prefer GPU Instancing or SRP Batcher instead.**

## Shader Variant Stripping

Unstripped projects can have 10,000+ shader variants -> slow build, large size, shader compilation stutters.

**Strategy:**
- Keyword authoring (`shader_feature` vs `multi_compile`): `references/asset-management/shader-work.md`
- Remove unused URP features in every URP Asset and Renderer in use (SSAO, HDR, Depth Texture if unused)
- Edit -> Project Settings -> Graphics -> Shader Stripping: strip unused passes

**URP-specific:**
```
// URP Asset settings that generate variants:
- HDR: disable if not needed
- SSAO: disable if not needed
- Additional Lights: reduce max count
- Shadows: disable additional light shadows if unused
- Depth/Opaque Texture: disable if unused
```

## Shader Warmup / Preloading

Prevent runtime shader compilation stutters:

1. **ShaderVariantCollection:** Create in Editor -> record variants during play -> preload at startup
2. **Preloaded Shaders:** Edit -> Project Settings -> Graphics -> Preloaded Shaders array
3. **Shader.WarmupAllShaders():** Brute-force warmup at loading screen (expensive)

On DX12, Vulkan, and Metal, classic warmup cannot build the full pipeline state
(it depends on vertex layout and render target). Warm up with representative
draws behind a loading screen, and check the local Unity docs for the
`ShaderWarmup` / graphics-state collection APIs available in the project's version.

## LOD Groups

| LOD Level | Typical Use | Triangle % | Screen Size |
|-----------|-------------|------------|-------------|
| LOD0 | Close-up | 100% | > 60% screen |
| LOD1 | Medium distance | 50% | 30-60% |
| LOD2 | Far | 25% | 10-30% |
| LOD3/Cull | Very far / invisible | 10% or culled | < 10% |

**Settings:**
- Fade Mode: Cross Fade for smooth transitions (costs extra draw call during transition)
- LOD Bias: 1.0 default, lower = more aggressive LOD (mobile: 0.5-0.7)
- Maximum LOD Level: set per Quality Level to cap detail on lower hardware

## Occlusion Culling

Skips rendering objects behind other objects.

**Setup:**
1. Mark large occluders as "Occluder Static" (walls, floors, large buildings)
2. Mark everything else as "Occludee Static"
3. Window -> Rendering -> Occlusion Culling -> Bake
4. Set cell size: smaller = more accurate but more memory

**Best for:** Indoor scenes, dense urban environments, levels with lots of walls.
**Skip when:** Open landscapes with few occluders, simple scenes with < 100 objects.
**Unity 6 alternative:** GPU occlusion culling (with GPU Resident Drawer) needs no
bake and handles dynamic occluders; measure GPU cost on the target device.

## Draw Call Reduction Checklist

- [ ] Enable SRP Batcher (URP/HDRP)
- [ ] GPU Resident Drawer for MeshRenderer-heavy scenes on compute-capable targets
- [ ] Reduce material count - atlas textures, share materials
- [ ] GPU Instancing for repeated objects (trees, grass, props)
- [ ] Static Batching for immovable geometry
- [ ] LOD Groups on complex meshes
- [ ] Occlusion Culling for indoor/dense scenes
- [ ] Camera far clip plane: reduce to actual needed distance
- [ ] Layer-based culling distances per camera

## Related UI And Asset References

- For uGUI Canvas batching, masks, atlases, and rebuild cost, load
  `references/optimization/canvas-ui-drawcalls-batching.md`.
- For material and shader asset edits that affect batching, load
  `references/asset-management/material-work.md` and
  `references/asset-management/shader-work.md` (renderer prefabs:
  `references/asset-management/prefab-work.md`).
- For runtime loading, preloading, and release ownership, load
  `references/asset-management/addressables-asset-manager.md`.

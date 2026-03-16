# Rendering Optimization Settings

## SRP Batcher

Reduces CPU draw call overhead by batching shader state changes (not objects).

**Requirements:**
- URP or HDRP (not built-in)
- Shader must declare `CBUFFER` for all material properties
- `UnityPerMaterial` and `UnityPerDraw` CBUFFERs properly declared

**Verify:** Frame Debugger → look for "SRP Batch" entries. Non-compatible shaders break batches.

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
1. Material Inspector → Enable GPU Instancing checkbox
2. Shader must support `UNITY_INSTANCING_BUFFER` (standard shaders do by default)
3. Objects must share exact same material instance (not `.material` copies)

**Limitations:** Does not work with SkinnedMeshRenderers. Broken by MaterialPropertyBlock in some cases — use `Graphics.DrawMeshInstanced` for manual control.

## Static Batching

Combines static meshes at build time into large vertex buffers.

| Pro | Con |
|-----|-----|
| Zero CPU overhead at runtime | Increases build size + memory (duplicated vertices) |
| Works with any shader | Cannot move/animate batched objects |
| Simple: check "Static" checkbox | Large meshes may exceed 64K vertex limit |

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

Unstripped projects can have 10,000+ shader variants → slow build, large size, shader compilation stutters.

**Strategy:**
- `shader_feature` for material toggles (strips unused variants)
- `multi_compile` only for runtime-toggled keywords (includes ALL variants)
- Remove unused URP features in URP Asset (SSAO, HDR, Depth Texture if unused)
- Edit → Project Settings → Graphics → Shader Stripping: strip unused passes

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

1. **ShaderVariantCollection:** Create in Editor → record variants during play → preload at startup
2. **Preloaded Shaders:** Edit → Project Settings → Graphics → Preloaded Shaders array
3. **Shader.WarmupAllShaders():** Brute-force warmup at loading screen (expensive but thorough)

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
3. Window → Rendering → Occlusion Culling → Bake
4. Set cell size: smaller = more accurate but more memory

**Best for:** Indoor scenes, dense urban environments, levels with lots of walls.
**Skip when:** Open landscapes with few occluders, simple scenes with < 100 objects.

## Draw Call Reduction Checklist

- [ ] Enable SRP Batcher (URP/HDRP)
- [ ] Reduce material count — atlas textures, share materials
- [ ] GPU Instancing for repeated objects (trees, grass, props)
- [ ] Static Batching for immovable geometry
- [ ] LOD Groups on complex meshes
- [ ] Occlusion Culling for indoor/dense scenes
- [ ] Camera far clip plane: reduce to actual needed distance
- [ ] Layer-based culling distances per camera

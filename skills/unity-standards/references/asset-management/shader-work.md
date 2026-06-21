# Shader Work

Use this when creating, editing, reviewing, or debugging ShaderLab, HLSL, Shader
Graph, custom UI shaders, render passes, shader keywords, variants, or pipeline
compatibility issues.

## Efficient Workflow

1. Identify the active render pipeline, target platforms, quality tiers, and
   material users before editing shader code.
2. Reproduce the visual or performance issue in the smallest scene, prefab, or
   material that still shows the problem.
3. Make the smallest shader change and verify compilation for the target
   pipeline. Shader fixes that work in one pipeline can silently fail in another.
4. Check variant impact when adding keywords, passes, includes, or fallback
   behavior.
5. Verify with the real material and renderer or Canvas hierarchy, not only a
   preview sphere.

## Standards

- Match the active render pipeline. Built-in, URP, HDRP, Shader Graph, and custom
  SRP code have different compatibility and batching rules.
- Preserve SRP Batcher compatibility when the project relies on URP/HDRP. Keep
  material properties in the correct constant buffer layout for the pipeline.
- Use `shader_feature` for material-controlled variants that can be stripped.
  Use `multi_compile` only for keywords that must switch at runtime.
- Avoid adding keywords, passes, grab passes, full-screen effects, or expensive
  fragment work without a measured need.
- Keep precision intentional for the target platform. Mobile shaders should not
  default to expensive precision when lower precision is visually equivalent.
- Keep property names stable when existing materials, animations, code, or
  tooling reference them.
- For transparent shaders, verify blend mode, z-write, z-test, sorting, render
  queue, and overdraw.
- For UI shaders, verify masking, clipping, stencil, alpha blending, batching,
  and `Canvas.additionalShaderChannels` needs in the actual Canvas hierarchy.

## Variant And Build Checks

- Check whether a new keyword or pass increases build size, warmup time, or
  runtime hitching.
- Confirm stripping behavior for `shader_feature` and platform variants.
- Keep includes and shared functions near existing project shader patterns.
- Avoid feature flags that multiply variants unless the product need is clear.

## Verification

- Verify shader compilation for the target platform or the repo's fastest
  available equivalent.
- Use Frame Debugger for pass count, material switches, SRP Batcher, instancing,
  stencil, and render queue evidence.
- Capture screenshots or video for visual changes in the scene, prefab, or UI
  hierarchy where the shader is used.
- Use RenderDoc, platform profiler, or Unity Profiler when fragment cost,
  bandwidth, overdraw, or GPU timing is the actual risk.

---
name: unity-tech-art
description: "(opencode-project - Skill) Bridge art and code. Use when: (1) Authoring/optimizing shaders (HLSL/Shader Graph), (2) Creating artist tools/inspectors, (3) Automating asset pipelines (Postprocessors), (4) Procedural content generation, (5) Rendering optimization, (6) Visual effects and lighting setup. Triggers: 'shader', 'HLSL', 'Shader Graph', 'URP shader', 'HDRP shader', 'material', 'rendering', 'post-processing', 'asset pipeline', 'AssetPostprocessor', 'texture import', 'model import', 'procedural generation', 'PCG', 'LOD', 'draw call', 'GPU', 'VFX Graph', 'particle system', 'lightmap', 'bake lighting', 'tech art', 'visual effect', 'render pipeline', 'custom shader', 'shader code', 'SubShader', 'ShaderLab', 'compute shader'."
---

# Unity Technical Artist

**Input**: Art/technical challenge description. Optional: target render pipeline (URP/HDRP/Built-in), reference images, performance budget.

**Output**: Shader code (HLSL or Shader Graph), asset postprocessor scripts, or procedural generation tools. Follows [ASSET_POSTPROCESSOR_TEMPLATE.md](.opencode/skills/unity/unity-tech-art/assets/templates/ASSET_POSTPROCESSOR_TEMPLATE.md) where applicable.

## Workflow

1. **Assess**: Is bottleneck artistic (workflow) or technical (performance)?
2. **Implement**: Use [ASSET_POSTPROCESSOR_TEMPLATE.md](.opencode/skills/unity/unity-tech-art/assets/templates/ASSET_POSTPROCESSOR_TEMPLATE.md), follow [SHADER_OPTIMIZATION_GUIDE.md](.opencode/skills/unity/unity-tech-art/references/SHADER_OPTIMIZATION_GUIDE.md)
3. **Validate**: Frame Debugger, Profiler for rendering impact
4. **Polish**: XML docs, help boxes, proper asset cleanup

## Key Areas

| Area | Focus |
|------|-------|
| Shaders | HLSL, Shader Graph, URP/HDRP optimization |
| Pipeline | AssetPostprocessor, batch processing |
| Tools | Artist-facing editors, property drawers |
| PCG | Procedural meshes, textures, environments |
| Rendering | Draw calls, batching, overdraw |

## Best Practices

- **Artist First**: Visual, intuitive tools with Sliders, Color Fields, Previews
- **Non-Destructive**: Prefab overrides, generate new vs overwrite
- **Batching Aware**: Keep SRP/Static/Dynamic batching in mind
- **Deterministic PCG**: Controllable seeds for reproducible results
- **Undo Groups**: Wrap all editor operations

See [PIPELINE_AUTOMATION_GUIDE.md](.opencode/skills/unity/unity-tech-art/references/PIPELINE_AUTOMATION_GUIDE.md) for automation patterns.

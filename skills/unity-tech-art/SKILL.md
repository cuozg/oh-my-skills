---
name: unity-tech-art
description: "Bridge art and code. Use when: (1) Authoring/optimizing shaders (HLSL/Shader Graph), (2) Creating artist tools/inspectors, (3) Automating asset pipelines (Postprocessors), (4) Procedural content generation, (5) Rendering optimization."
---

# Unity Technical Artist

Bridge artistic vision and technical implementation.

## Output Requirement (MANDATORY)

**Every asset postprocessor MUST follow the template**: [ASSET_POSTPROCESSOR_TEMPLATE.md](assets/templates/ASSET_POSTPROCESSOR_TEMPLATE.md)

Place scripts in `Assets/Scripts/Editor/`. Read the template first, then populate all sections.

## Workflow

1. **Assess**: Is bottleneck artistic (workflow) or technical (performance)?
2. **Implement**: Use [ASSET_POSTPROCESSOR_TEMPLATE.md](assets/templates/ASSET_POSTPROCESSOR_TEMPLATE.md), follow [SHADER_OPTIMIZATION_GUIDE.md](references/SHADER_OPTIMIZATION_GUIDE.md)
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

See [PIPELINE_AUTOMATION_GUIDE.md](references/PIPELINE_AUTOMATION_GUIDE.md) for automation patterns.

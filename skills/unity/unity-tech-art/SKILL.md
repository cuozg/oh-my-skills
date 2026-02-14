---
name: unity-tech-art
description: "(opencode-project - Skill) Bridge art and code. Use when: (1) Authoring/optimizing shaders (HLSL/Shader Graph), (2) Creating artist tools/inspectors, (3) Automating asset pipelines (Postprocessors), (4) Procedural content generation, (5) Rendering optimization, (6) Visual effects and lighting setup. Triggers: 'shader', 'HLSL', 'Shader Graph', 'URP shader', 'HDRP shader', 'material', 'rendering', 'post-processing', 'asset pipeline', 'AssetPostprocessor', 'texture import', 'model import', 'procedural generation', 'PCG', 'LOD', 'draw call', 'GPU', 'VFX Graph', 'particle system', 'lightmap', 'bake lighting', 'tech art', 'visual effect', 'render pipeline', 'custom shader', 'shader code', 'SubShader', 'ShaderLab', 'compute shader'."
---

# Unity Technical Artist

Bridge artistic vision and technical implementation.

## Purpose

Solve problems at the intersection of art and engineering — shaders, asset pipelines, procedural generation, and rendering optimization — so artists get intuitive tools and players get performant visuals.

## Input

- **Required**: Description of the art/technical challenge (shader need, pipeline bottleneck, PCG request)
- **Optional**: Target render pipeline (URP/HDRP/Built-in), reference images, performance budget

## Output

Shader code (HLSL or Shader Graph), asset postprocessor scripts, or procedural generation tools placed in the appropriate project directory. All outputs follow `ASSET_POSTPROCESSOR_TEMPLATE.md` where applicable and validate via Frame Debugger / Profiler.

## Examples

| User Request | Skill Action |
|:---|:---|
| "Optimize draw calls for the environment" | Audit materials, enable GPU instancing, merge static meshes, report before/after batch count |
| "Auto-enforce texture import rules" | Write an AssetPostprocessor setting max size, compression format, and sRGB per naming convention |
| "Create a dissolve shader for enemy death" | Author URP HLSL shader with dissolve edge glow, noise texture, `_DissolveAmount` property |

## Output Requirement (MANDATORY)

**Every asset postprocessor MUST follow the template**: [ASSET_POSTPROCESSOR_TEMPLATE.md](.opencode/skills/unity/unity-tech-art/assets/templates/ASSET_POSTPROCESSOR_TEMPLATE.md)

Place scripts in `Assets/Scripts/Editor/`. Read the template first, then populate all sections.

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

---

## MCP Tools Integration

Use `unityMCP_*` tools for material/shader/texture operations and visual validation.

| Operation | MCP Tool |
|-----------|----------|
| Create material | `unityMCP_create_material(material_name="..", color="..", material_path="..")` |
| Assign material | `unityMCP_assign_material(gameobject_path="..", material_name="..")` |
| Assign shader | `unityMCP_assign_shader_to_material(material_path="..", shader_path="..")` |
| Material to FBX | `unityMCP_assign_material_to_fbx(fbx_path="..", material_path="..")` |
| Generate texture | `unityMCP_generate_3d_model_texture(...)` |
| Scene screenshot | `unityMCP_capture_scene_object(gameObjectPath="...")` |
| High-poly audit | `unityMCP_list_objects_with_high_polygon_count(threshold=1000)` |
| Check compilation | `unityMCP_check_compile_errors` |
| Run editor script | `unityMCP_execute_script(filePath="...")` |

### Shader/Material Workflow

```
1. unityMCP_create_material(...)                → Create new material
2. unityMCP_assign_shader_to_material(...)      → Apply custom shader
3. unityMCP_assign_material(...)                → Assign to object
4. unityMCP_capture_scene_object(...)           → Visual validation
5. unityMCP_list_objects_with_high_polygon_count → Rendering audit
```

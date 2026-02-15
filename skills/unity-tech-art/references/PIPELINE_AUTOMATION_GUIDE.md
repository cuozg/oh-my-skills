# Unity Pipeline Automation

Standards for automating asset imports and artist workflows.

## 1. Asset Import Rules (AssetPostprocessor)

Automate settings based on path or naming conventions to ensure consistency.

- **Textures**: 
  - `_Albedo`, `_BaseColor` -> sRGB ON, Max Size 2048.
  - `_Normal`, `_Bump` -> Normal Map type, sRGB OFF.
  - `_Mask`, `_Metallic` -> Default, sRGB OFF.
- **Models**:
  - `Mesh Compression` -> Medium/High for non-deforming props.
  - `Read/Write` -> OFF unless needed for procedural deformation.
  - `Import Settings` -> Preserve hierarchy if needed, otherwise optimized.

## 2. Editor Tool Design

Tools should be built with **Progressive Disclosure**:
- **Basic Level**: Simple buttons for common tasks.
- **Advanced Level**: Foldout menus for fine-tuning.
- **Feedback**: Provide progress bars for batch operations and log concise success/failure messages.

## 3. Procedural Content Generation (PCG)

- **Deterministic**: Always use a seed for random generation.
- **Exporting**: Always provide an "Export to Asset" button for procedurally generated meshes or materials so they can be versioned.
- **Previewing**: Use `PreviewRenderUtility` or `SceneView` Gizmos to show results before baking.

## 4. Scripting Standards

- **AssetDatabase**: Use `AssetDatabase.StartAssetEditing()` and `StopAssetEditing()` when performing batch operations to prevent repeated re-imports.
- **Undo System**: Always wrap editor changes in `Undo.RecordObject` or `Undo.RegisterCreatedObjectUndo`.

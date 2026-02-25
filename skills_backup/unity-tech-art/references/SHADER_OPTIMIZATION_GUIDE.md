# Unity Shader & Material Optimization

Best practices for authoring performant shaders and materials in Unity (URP/HDRP).

## 1. Shader Authoring (HLSL / Shader Graph)

- **Use Half Precision**: For mobile platforms, use `half` instead of `float` for colors, normals, and low-precision math.
- **Minimize Branching**: Avoid `if/else` in shaders. Use `lerp`, `step`, or `clamp` for conditional logic.
- **Texture Packing**: Combine multiple grayscale maps (Smoothness, Metallic, AO) into a single RGBA texture (M-O-S pattern).
- **Instruction Count**: Keep math light in the Fragment (Pixel) shader. Move as much calculation as possible to the Vertex shader.
- **Math Optimization**: 
  - Use `pow(x, 2)` instead of `x * x` (compiler dependent, but check).
  - Use `rsqrt` instead of `1.0 / sqrt`.

## 2. Material Management

- **Material Batching**: Use as few unique Materials as possible to maximize **SRP Batching**.
- **GPU Instancing**: Enable on materials for repetitive environment props (trees, grass, rocks).
- **Standardize Shaders**: Use a "Master Shader" approach instead of many unique shaders to reduce variant explosion.
- **Variant Stripping**: Use `IPreprocessShaders` to strip unused shader keywords during build time.

## 3. Graphics Features

- **LOD (Level of Detail)**: Always implement LOD groups for complex meshes.
- **LOD Smoothing**: Use cross-fade for smooth transitions if the budget allows.
- **Draw Call Minimization**: Standardize on textures/atlases to allow for static and dynamic batching.
- **Overdraw**: Minimize transparent overdraw by using opaque or cutout materials where possible.

# Prefabs & Scenes (.prefab, .unity) Review Checklist

Check changed prefab/scene data for runtime breakage, missing references,
unintended overrides, and asset import regressions. Report as severity:
CRITICAL > HIGH > MEDIUM > LOW > STYLE.

### Hierarchy
- [ ] Hierarchy depth justified for UI/layout complexity; flag excessive nesting only when it affects maintainability or performance
- [ ] Root transform values are intentional for prefabs instantiated at runtime
- [ ] No negative scale on renderers, colliders, or physics objects unless explicitly required

### Prefabs
- [ ] No `Missing (Mono Script)` components
- [ ] Variant overrides intentional - review each modified property
- [ ] No direct scene references in prefabs (use SO or events)
- [ ] `Raycast Target` disabled on non-interactive UI elements
- [ ] Serialized object references are not `{fileID: 0}` unless optional
- [ ] New components have safe default values for existing prefab instances

### Textures & Mesh (if applicable)
- [ ] Read/Write disabled (halves memory) unless CPU access needed
- [ ] Compression set per platform (ASTC mobile, BC7 desktop)
- [ ] Mipmaps: enabled for 3D, disabled for UI sprites
- [ ] LOD groups on meshes >5k tris

### Audio (if applicable)
- [ ] Short SFX: Decompress On Load; Music: Streaming
- [ ] Force Mono for non-spatial SFX
- [ ] Preload Audio Data off for large files

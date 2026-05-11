# Prefabs & Scenes (.prefab, .unity) Review Checklist

Check every item against changed code. Report as severity: CRITICAL > HIGH > MEDIUM > LOW > STYLE.

### Hierarchy
- [ ] Hierarchy depth ≤ 3 levels
- [ ] Root transform at (0,0,0), rotation (0,0,0), scale (1,1,1)
- [ ] No negative scale (inverted normals, physics issues)

### Prefabs
- [ ] No `Missing (Mono Script)` components
- [ ] Variant overrides intentional — review each modified property
- [ ] No direct scene references in prefabs (use SO or events)
- [ ] `Raycast Target` disabled on non-interactive UI elements

### Textures & Mesh (if applicable)
- [ ] Read/Write disabled (halves memory) unless CPU access needed
- [ ] Compression set per platform (ASTC mobile, BC7 desktop)
- [ ] Mipmaps: enabled for 3D, disabled for UI sprites
- [ ] LOD groups on meshes >5k tris

### Audio (if applicable)
- [ ] Short SFX: Decompress On Load; Music: Streaming
- [ ] Force Mono for non-spatial SFX
- [ ] Preload Audio Data off for large files

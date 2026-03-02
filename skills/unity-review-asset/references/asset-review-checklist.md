# Asset Review Checklist

## Shaders & Materials

- [ ] No fixed-function shaders (CRITICAL in URP/HDRP projects)
- [ ] Materials have a valid shader reference — not null (CRITICAL)
- [ ] Alpha-test materials have `_ALPHATEST_ON` keyword enabled
- [ ] Unlit shaders on world-space opaque objects flagged as WARNING
- [ ] Shader properties referenced in material exist in shader source

## Textures (via .meta)

- [ ] `maxTextureSize` ≤ 2048 for UI sprites on mobile targets (WARNING if exceeded)
- [ ] Mip maps enabled for all world-space textures (`generateMipsInLinearSpace: 1`)
- [ ] Compression format matches platform — ASTC for iOS/Android, DXT for PC (WARNING if mismatch)
- [ ] `isReadable: 1` only if runtime CPU read access required (doubles memory — WARNING)
- [ ] Sprites packed into atlases where count > 5 in same canvas (NOTE)

## Animations & Controllers

- [ ] Animation clips used in locomotion states have `loop: 1`
- [ ] Blend tree child thresholds are non-zero and cover full parameter range
- [ ] `Apply Root Motion` disabled on characters using script-driven movement
- [ ] `Animation Type` set to Humanoid only for humanoid rigs

## FBX Import Settings (via .meta)

- [ ] `meshCompression` set to Medium or higher for static props (NOTE if Off)
- [ ] `isReadable: 0` unless runtime mesh access needed (WARNING if 1)
- [ ] `importAnimation: 0` for static meshes
- [ ] `normalImportMode` matches artistic intent (recalculate vs import)

## Audio (via .meta)

- [ ] No uncompressed audio in streaming assets > 100 KB (WARNING)
- [ ] Music files use `Streaming` load type; SFX use `Decompress On Load`

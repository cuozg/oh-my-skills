# Materials (.mat) Review Checklist

Check changed materials for render-pipeline compatibility, GPU cost, batching
impact, and accidental shared-material changes. Report as severity:
CRITICAL > HIGH > MEDIUM > LOW > STYLE.

### Materials
- [ ] Shader correctly assigned for the target render pipeline (e.g. URP/HDRP)
- [ ] SRP Batcher compatibility preserved (URP/HDRP); GPU Instancing only matters where SRP Batcher does not apply, since SRP Batcher takes priority
- [ ] Unused properties or textures removed/cleaned up
- [ ] Render Queue appropriately set (e.g. Transparent vs Opaque)
- [ ] No expensive features enabled unnecessarily (e.g. Environment Reflections / Specular Highlights on low-end mobile, high emission)
- [ ] Shared material edits do not unintentionally affect unrelated prefabs
- [ ] Texture references use platform-appropriate import settings when changed

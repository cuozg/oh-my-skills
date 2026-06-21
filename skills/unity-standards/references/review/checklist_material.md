# Materials (.mat) Review Checklist

Check changed materials for render-pipeline compatibility, GPU cost, batching
impact, and accidental shared-material changes. Report as severity:
CRITICAL > HIGH > MEDIUM > LOW > STYLE.

### Materials
- [ ] Shader correctly assigned for the target render pipeline (e.g. URP/HDRP)
- [ ] GPU Instancing enabled where applicable
- [ ] Unused properties or textures removed/cleaned up
- [ ] Render Queue appropriately set (e.g. Transparent vs Opaque)
- [ ] No overly expensive shader properties enabled unnecessarily (e.g. Realtime reflections, high emission)
- [ ] Shared material edits do not unintentionally affect unrelated prefabs
- [ ] Texture references use platform-appropriate import settings when changed

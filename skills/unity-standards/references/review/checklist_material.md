# Materials (.mat) Review Checklist

Check every item against changed code. Report as severity: CRITICAL > HIGH > MEDIUM > LOW > STYLE.

### Materials
- [ ] Shader correctly assigned for the target render pipeline (e.g. URP/HDRP)
- [ ] GPU Instancing enabled where applicable
- [ ] Unused properties or textures removed/cleaned up
- [ ] Render Queue appropriately set (e.g. Transparent vs Opaque)
- [ ] No overly expensive shader properties enabled unnecessarily (e.g. Realtime reflections, high emission)

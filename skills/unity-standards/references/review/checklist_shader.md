# Shaders (.shader) Review Checklist

Check changed shaders for render-pipeline compatibility, variant explosion,
batching compatibility, and platform cost. Report as severity:
CRITICAL > HIGH > MEDIUM > LOW > STYLE.

### Shaders
- [ ] Render Queue and Render Type defined correctly
- [ ] Fallbacks defined to support lower-end hardware
- [ ] Avoid complex branching (if/else) in fragment shaders
- [ ] Minimize expensive math operations (pow, sin, cos) where an approximation or lookup texture would work
- [ ] Precision types used appropriately (half for colors, float for positions)
- [ ] Unused properties removed from the Properties block
- [ ] SRP Batcher compatibility preserved where the project relies on it
- [ ] Shader keywords and multi_compile variants are justified and stripped when unused

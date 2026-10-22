# Export: preparing the source image

The splitter reads **one flat PNG**. Every later phase inherits its problems, so fix them here, in the art tool or with a quick Pillow pass. Save the result to `Assets/<Name>/Source/<name>.png`.

## Fit checklist (all must hold)
| Requirement | Why | Fix when it fails |
|---|---|---|
| **Side view** for anything that walks; any single view for objects | Gait math and facing flips assume the subject faces right or left in profile | Ask for a profile export |
| **Dark outlines** closing every fill region | Regions are found as light areas bounded by strokes (`dark_lum`, 150 by default) | Close gaps in the strokes. An edge drawn with no outline (grass bottom, fur tuft) can be closed by the white edge instead: `bg_white_lum` (config-schema.md, *Labelling*) |
| **Flat fills** (no gradients, shading or texture) | Overpaint continues the nearest clean fill colour (lightly blurred), so shading or gradients leave visible patches | Soft shading and gradients are fine at idle-sized amplitudes: patches only show where a joint opens. Dark shading that labels as outline needs `shade_hue` (config-schema.md, *Labelling*). Heavy painting: flatten it, or use the manual-layer route (below) |
| **Plain light background** that touches the image corner | The background is the region at pixel (0, 0) | Pad the image with background colour, or remove the background to white |
| **One subject**, fully in frame, with no cast shadow or ground line | A shadow becomes a part, and a cropped limb can't be rigged | Erase the shadow and pad the canvas by ~5% |
| **Facing right** | `artFacesRight = true` is the default | Mirror the image, or set `artFacesRight = false` on the controller |
| **Size** ~1000–3000 px along the long side | Too small blurs strokes into fills; too large is slow | Resample with Lanczos and keep the strokes ≥ 3 px |
| **Limbs separated** where they should move apart (legs, arms, lid edge) | Touching fills need hand-drawn `cuts`, and fused strokes can't be cut cleanly | Re-pose the art with a visible gap where possible |

## Quick checks
- Run `python3 -c "from PIL import Image; im=Image.open('x.png'); print(im.size, im.mode, im.getpixel((0,0)))"`. The size should be in range and the corner should be background.
- Save as RGB or RGBA PNG. If the image has an alpha channel, composite it onto white first, because transparent pixels read as black on `convert("RGB")`.

## Art that doesn't fit
Painted or shaded art, photos, and front-facing walkers don't fit. Tell the user plainly and offer the manual-layer route: they export one PNG per part, or a PSB, and the splitter step is replaced by editing the subject's `split_<name>.py` to read those layers. The rig, animate and test phases are reused unchanged.

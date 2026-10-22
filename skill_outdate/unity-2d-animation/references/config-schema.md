# Subject config schema (`Tools~/split_<name>.py split --config Tools~/<name>.json`)

All coordinates are **image pixels** (origin top-left, y down) of the source PNG. Measure them with `inspect` crops; don't estimate from a thumbnail.
Body-plan starting points (parts, order, bones, glue): `body-plans.md`.
The keys below describe the template splitter. If a subject's copy of `split_<name>.py` adds keys, document them in that copy's docstring.

| Key | Type | Meaning |
|---|---|---|
| `name` | string | Subject name (= folder `Assets/<Name>`). Defaults to the `--out` folder name. |
| `ppu` | number | Pixels per unit. Pick so the subject is ~2–4 units long (e.g. 1500 px wide → 500). |
| `origin` | [x, y] | Image point that becomes the subject root: on the ground line (lowest foot or base), horizontally under the body centre. The physics root sits here. |
| `dark_lum` | int (150) | Mean RGB below this = outline stroke. |
| `shade_hue` | {over, under, by} or a list (none) | Dark pixels whose `over` channel (`r`/`g`/`b`) exceeds `under` by ≥ `by` are shading, kept as fill. See *Labelling*. |
| `bg_white_lum` | int (none) | Background = near-white (mean ≥ this, unsaturated) region at (0, 0), plus off-white specks outside the subject. See *Labelling*. |
| `bg_holes` | [[x, y]…] | Seeds of enclosed white negative space (inside a curl or handle) that is background too. Needs `bg_white_lum`. |
| `stroke_reach` | int (16) | A stroke belongs to a fill within this many px. Must be ≥ stroke width. Measure the width in an inspect crop. |
| `grid` | int (20) | Mesh cell size in px. Smaller values bend more smoothly but add vertices. |
| `pad` | int (4) | Transparent padding around each trimmed PNG. |
| `min_component` | int (300) | Fill regions smaller than this are specks and join the nearest part. |
| `parts` | [string] | **Back-to-front** order. The index becomes the SpriteRenderer sorting order. |
| `cuts` | [[[x,y],[x,y]]] | Segments that split one continuous fill (e.g. neck, leg tops, ear base). Each must run stroke-to-stroke; overshoot both ends a few px into the strokes. |
| `assign` | [rule] | How fill regions map to parts, described below. |
| `dark_parts` | [{part, seed, max_pixels}] | Dark blobs that are their own part (eyes, pupils). `seed` must be on the blob. The part underneath gets the blob area overpainted when listed in its `extend.under`. |
| `exclusive` | [[front, back]] | The front part alone owns the strokes the two share. Use this when the back part continues *under* the front (body under head, head under mane, far leg top under body), so no ghost line is left behind. Leave out pairs that can separate when animated (leg vs leg, tail vs body). |
| `extend` | {back: {under:[front…], distance}} | Overpaint: the back part grows up to `distance` px under the listed front parts. This fills the joint so rotation never reveals a hole. The drawn area joins the old part seamlessly: denoised, blurred nearest-clean-fill colour (no streaks or hard borders), the part's own outline ends continued under the fronts (two facing ends bridged, e.g. the back line under the mane; other ends extended, riding the part's fill edge where it curves, e.g. an ear edge under the mane) with drawn fill outside that contour dropped (no ghost lobe in the front's shape); under a front cut from the same fill (near leg, head over neck) the contour only bounds the part and no line is drawn, since the art has none there; the back part's copy of the junction strokes and its AA fringe repainted (no ghost line or hairline seam; the fringe moves to the front part as a soft edge), short stroke tips touching a front's strokes handed to that front, and slivers thinner than ~1.5 outline widths dropped. |
| `outline_width` | number (auto) | Outline width in px used to draw the continued outline in the overpaint. Measured from the strokes when omitted; set it when the auto value (printed into `rig.json` as `outlineWidth`) is off. |
| `anchor_part` | string | The part whose fill is the glue anchor (usually `Body`). |
| `glued` | {part: blend_px} | Limbs whose first bone in `part_bones` is the body anchor. Vertices on or under the anchor fill take weight 1 on that bone and blend to the limb bones over `blend_px`. Limbs then bend at the joint instead of swinging their hidden overpaint into view. Use ~70 for legs and ~35 for tails. |
| `glue_start` | number (8) | Distance from the anchor fill (px) where the blend starts. |
| `bones` | [{name, parent, head, tail}] | Skeleton. The bone's +X axis runs head → tail. Exactly one root (`parent: null`). Children may start anywhere; they don't need to touch the parent's tail. |
| `part_bones` | {part: [bone…]} | The bones that deform each part. The first one is the sprite's root bone, and every bone's parent must also be in the list (or it becomes a sprite-local root). For glued parts, put the anchor (Pelvis/Spine) first. |
| `collider` | {direction, offset, size} (optional) | CapsuleCollider2D in units relative to `origin`. Make the bottom of the capsule touch y = 0. Omit it to auto-fit from the bounds. |

## `assign` rules (evaluated per fill region)

1. **Seed rules** `{part, seed:[x,y]}` are applied first. The region containing the seed belongs to `part`. The script exits if the seed is on a stroke.
2. Remaining regions take the **first matching filter rule**, in order:
   - `polygon: [[x,y]…]`: the region's centroid must be inside it. If omitted, the rule covers the whole image.
   - `saturated: true|false`: true when max(rgb) − min(rgb) > 40, which separates colourful hair from white or grey fills.
   - `rgb_min` / `rgb_max: [r,g,b]`: bounds on the region's median colour, e.g. a yellow horn.
3. Regions with no match print `WARN unassigned component …`. Fix that before going to Unity.

Pick seeds on the fill itself: a `components.txt` centroid can land on an inner stroke (petal vein, smile), and the seed error then names the nearest fill pixel.

Rule of thumb: use seeds for big regions (one per piece split by a cut), use polygons for small repeated regions (hoof bands, hair stripes), and put a catch-all colour rule last.

## Labelling: reading `labels.png`
Put the labelling keys in the config and re-run `inspect --config Tools~/<name>.json` until each piece is one clean region. Fix the symptom with its key:

| `labels.png` shows | Cause | Key |
|---|---|---|
| A shaded region broken into fragments or drawn as outline (black) | Dark shading is below `dark_lum`. Lowering `dark_lum` breaks lighter outline runs and leaks fills into the background | `shade_hue`: sample outline vs shading RGB in a crop and key on the channel that separates them (brown outline R > G, green shading G > R → `{"over": "g", "under": "r", "by": 20}`) |
| A coloured region drawn white (merged into the background) | An edge with no outline lets the fill touch the background | `bg_white_lum` (≈ 240) |
| White negative space enclosed by the subject labelled as a fill | It's not connected to (0, 0) | `bg_holes`: one seed inside each |
| Two pieces in one colour with no stroke between them | They share one fill | `cuts`, or keep them one part with several bones (body-plans.md, *Fused fills*) |

## Minimal skeleton (fill every value from measurements)
```json
{
  "name": "<Name>", "ppu": 500, "origin": [0, 0],
  "parts": ["<back-most>", "...", "<front-most>"],
  "cuts": [[[0, 0], [0, 0]]],
  "assign": [{"part": "<Body>", "seed": [0, 0]}, {"part": "<Hair>", "saturated": true}],
  "exclusive": [["<front>", "<back>"]],
  "extend": {"<back>": {"under": ["<front>"], "distance": 60}},
  "anchor_part": "<Body>",
  "glued": {"<Limb>": 70},
  "bones": [{"name": "<Root>", "parent": null, "head": [0, 0], "tail": [0, 0]}],
  "part_bones": {"<Body>": ["<Root>"], "<Limb>": ["<Root>", "<Upper>", "<Lower>"]}
}
```

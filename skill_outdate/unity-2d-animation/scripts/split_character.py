"""
Config-driven 2D character layer splitter + rig data generator (unity-2d-animation skill).

Turns ONE flat line-art character image (dark outline, flat fills, plain background) into:
  * trimmed RGBA part PNGs with overpainted (inpainted) hidden joints,
  * rig.json: skeleton, per-part grid mesh, auto weights (inverse distance + body glue),
    consumed by assets/Editor/SkinnedRigBuilder.cs inside Unity.

Subcommands
  inspect  python3 -I split_character.py inspect --image IMG --debug DIR [--crop x0,y0,x1,y1 ...]
           -> DIR/labels.png (fill regions, half res), DIR/components.txt, DIR/crop_*.png (20px grid,
              red line every 100px). Use it to find cut endpoints, seeds and bone landmarks.
  split    python3 -I split_character.py split --image IMG --config CFG.json --out Assets/<Name> [--debug DIR]
           -> Assets/<Name>/Art/Parts/<Part>.png, Assets/<Name>/Art/rig.json,
              DIR/composite_bones.png + DIR/part_map.png for visual verification.

Config schema: see references/config-schema.md. Requires numpy, scipy, Pillow.
"""
import argparse
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd


# ------------------------------------------------------------------------------------------------
# inspect
# ------------------------------------------------------------------------------------------------

def inspect(args):
    os.makedirs(args.debug, exist_ok=True)
    pil = Image.open(args.image).convert("RGB")
    rgb = np.array(pil).astype(np.int32)
    dark = rgb.mean(2) < args.dark_lum
    lab, n = nd.label(~dark)
    bg = lab[0, 0]
    sizes = nd.sum(np.ones_like(lab), lab, range(n + 1))
    lines = [f"image {pil.width}x{pil.height}  components={n}  background_id={bg}",
             "id size bbox(x0,x1,y0,y1) centroid(x,y) median_rgb"]
    for i, sl in enumerate(nd.find_objects(lab), start=1):
        if i == bg or sizes[i] < args.min_component:
            continue
        m = lab[sl] == i
        ys, xs = np.nonzero(m)
        col = tuple(int(v) for v in np.median(rgb[sl][m], axis=0))
        lines.append(f"{i} {int(sizes[i])} ({sl[1].start},{sl[1].stop},{sl[0].start},{sl[0].stop}) "
                     f"({xs.mean() + sl[1].start:.0f},{ys.mean() + sl[0].start:.0f}) {col}")
    with open(os.path.join(args.debug, "components.txt"), "w") as f:
        f.write("\n".join(lines))
    print("\n".join(lines))

    rng = np.random.RandomState(1)
    pal = rng.randint(60, 255, (n + 1, 3))
    pal[bg] = 255
    out = pal[lab]
    out[dark] = 0
    Image.fromarray(out.astype(np.uint8)).resize((pil.width // 2, pil.height // 2)).save(
        os.path.join(args.debug, "labels.png"))

    for k, box in enumerate(args.crop or []):
        x0, y0, x1, y1 = [int(v) for v in box.split(",")]
        c = pil.crop((x0, y0, x1, y1)).copy()
        d = ImageDraw.Draw(c)
        for x in range((x0 // 20 + 1) * 20, x1, 20):
            d.line([(x - x0, 0), (x - x0, y1 - y0)], fill=(255, 0, 0) if x % 100 == 0 else (0, 200, 255))
        for y in range((y0 // 20 + 1) * 20, y1, 20):
            d.line([(0, y - y0), (x1 - x0, y - y0)], fill=(255, 0, 0) if y % 100 == 0 else (0, 200, 255))
        c.save(os.path.join(args.debug, f"crop_{k}_{x0}_{y0}.png"))


# ------------------------------------------------------------------------------------------------
# split
# ------------------------------------------------------------------------------------------------

def point_in_poly(x, y, poly):
    """Ray-casting point-in-polygon test (image px)."""
    inside = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi:
            inside = not inside
        j = i
    return inside


def rule_matches(rule, cx, cy, col):
    """Filter rule: optional polygon (centroid inside), saturated flag, rgb_min / rgb_max bounds."""
    if "polygon" in rule and not point_in_poly(cx, cy, rule["polygon"]):
        return False
    if "saturated" in rule and (max(col) - min(col) > 40) != rule["saturated"]:
        return False
    if "rgb_min" in rule and any(c < m for c, m in zip(col, rule["rgb_min"])):
        return False
    if "rgb_max" in rule and any(c > m for c, m in zip(col, rule["rgb_max"])):
        return False
    return True


def split(args):
    cfg = json.load(open(args.config))
    name = cfg.get("name", os.path.basename(os.path.normpath(args.out)))
    ppu = float(cfg["ppu"])
    ox, oy = [float(v) for v in cfg["origin"]]
    dark_lum = cfg.get("dark_lum", 150)
    stroke_reach = cfg.get("stroke_reach", 16)
    pad = cfg.get("pad", 4)
    grid = cfg.get("grid", 20)
    min_comp = cfg.get("min_component", 300)
    parts = cfg["parts"]                                   # back-to-front = sorting order
    order = {p: i for i, p in enumerate(parts)}
    dark_parts = {d["part"]: d for d in cfg.get("dark_parts", [])}
    exclusive = {tuple(e) for e in cfg.get("exclusive", [])}
    extend = cfg.get("extend", {})
    anchor_part = cfg.get("anchor_part")
    glued = cfg.get("glued", {})
    glue_start = cfg.get("glue_start", 8.0)

    out_parts = os.path.join(args.out, "Art", "Parts")
    os.makedirs(out_parts, exist_ok=True)
    debug = args.debug or os.path.join("Tools", "RigDebug", name)
    os.makedirs(debug, exist_ok=True)

    rgb = np.array(Image.open(args.image).convert("RGB")).astype(np.int32)
    H, W = rgb.shape[:2]
    lum = rgb.mean(2)
    dark = lum < dark_lum
    outline_rgb = tuple(int(v) for v in np.median(rgb[dark], axis=0))

    # Cut lines split one continuous fill into separate parts (3px so labelling can't leak through).
    barrier_img = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(barrier_img)
    for a, b in cfg.get("cuts", []):
        d.line([tuple(a), tuple(b)], fill=255, width=3)
    barrier = np.array(barrier_img) > 0

    lab, n = nd.label(~dark & ~barrier)
    bg = lab[0, 0]
    char_mask = nd.binary_fill_holes(lab != bg)

    # --- assign fill components to parts: seeds first, then ordered filter rules ---------------------
    comp_part = {}
    rules = cfg.get("assign", [])
    for r in rules:
        if "seed" in r:
            x, y = r["seed"]
            if lab[y, x] in (0, bg):
                sys.exit(f"seed {r['seed']} for {r['part']} is on a stroke/background - move it into the fill")
            comp_part[lab[y, x]] = r["part"]
    sizes = nd.sum(np.ones_like(lab), lab, range(n + 1))
    for i, sl in enumerate(nd.find_objects(lab), start=1):
        if i == bg or i in comp_part or sizes[i] < min_comp:
            continue
        m = lab[sl] == i
        ys, xs = np.nonzero(m)
        cy, cx = ys.mean() + sl[0].start, xs.mean() + sl[1].start
        col = tuple(int(v) for v in np.median(rgb[sl][m], axis=0))
        hit = next((r["part"] for r in rules if "seed" not in r and rule_matches(r, cx, cy, col)), None)
        if hit is None:
            print(f"WARN unassigned component {i} size={int(sizes[i])} c=({cx:.0f},{cy:.0f}) col={col}")
            continue
        comp_part[i] = hit

    fill = {p: np.zeros((H, W), bool) for p in parts}
    for i, p in comp_part.items():
        fill[p] |= lab == i
    # Specks + barrier pixels join the nearest assigned fill.
    assigned = np.full((H, W), -1, np.int32)
    for p in parts:
        assigned[fill[p]] = order[p]
    leftovers = char_mask & ~dark & (assigned < 0)
    _, (iy, ix) = nd.distance_transform_edt(assigned < 0, return_indices=True)
    near = assigned[iy, ix]
    for p in parts:
        fill[p] |= leftovers & (near == order[p])

    # --- dark blobs (eyes, pupils...) that are their own part -----------------------------------------
    dark_lab, _ = nd.label(dark)
    dark_owned = np.zeros((H, W), bool)
    for p, dcfg in dark_parts.items():
        x, y = dcfg["seed"]
        blob = dark_lab == dark_lab[y, x]
        if not dark[y, x] or blob.sum() > dcfg.get("max_pixels", 6000):
            sys.exit(f"dark_parts seed for {p} is not an isolated dark blob - move the seed")
        fill[p] = nd.binary_dilation(blob, iterations=1) & char_mask
        dark_owned |= blob
    strokes = dark & ~dark_owned & char_mask

    # --- strokes: parts get strokes within reach, except where a front part owns them exclusively ----
    reach = {p: nd.distance_transform_edt(~fill[p]) <= stroke_reach for p in parts if p not in dark_parts}
    mask = {p: fill[p].copy() for p in parts}
    for p in reach:
        own = strokes & reach[p]
        for front, back in exclusive:
            if back == p and front in reach:
                own &= ~reach[front]
        mask[p] |= own

    # --- overpaint: back parts extend under front parts, drawn to join the visible art seamlessly -----
    outline_w = float(cfg.get("outline_width") or stroke_width(strokes))
    extends = [(back, e["under"], e["distance"]) for back, e in extend.items()]
    color, soft = overpaint(rgb, dark, char_mask, fill, mask, extends, order, outline_rgb, outline_w)

    ring = nd.binary_dilation(char_mask, iterations=2) & ~char_mask
    ring_alpha = np.clip((255.0 - lum) / (255.0 - 80.0), 0.0, 1.0)

    to_units = lambda x, y: [(x - ox) / ppu, (oy - y) / ppu]
    bone_px = {b["name"]: (tuple(b["head"]), tuple(b["tail"])) for b in cfg["bones"]}
    # outlineWidth lets check_split tell the redrawn continuation outline apart from stroke leftovers.
    rig = {"name": name, "ppu": ppu, "origin": [ox, oy], "outlineWidth": outline_w, "bones": [], "parts": []}
    for b in cfg["bones"]:
        rig["bones"].append({"name": b["name"], "parent": b.get("parent") or "",
                             "head": to_units(*b["head"]), "tail": to_units(*b["tail"])})
    if "collider" in cfg:
        rig["collider"] = cfg["collider"]

    anchor_dist = nd.distance_transform_edt(~fill[anchor_part]) if anchor_part else None
    composite = np.zeros((H, W, 4), np.float32)
    bmin, bmax = [1e9, 1e9], [-1e9, -1e9]
    for p in parts:
        m = mask[p]
        if not m.any():
            sys.exit(f"part {p} is empty - check assign rules/seeds")
        ring_p = ring & (nd.distance_transform_edt(~m) <= 2.5)
        alpha = np.zeros((H, W), np.float32)
        alpha[m] = 1.0
        alpha[ring_p] = np.maximum(alpha[ring_p], ring_alpha[ring_p])
        # Soft AA fringe taken over from the part behind (see overpaint): outline colour, partial alpha.
        soft_p = (soft[p] > 0) & ~m
        alpha[soft_p] = np.maximum(alpha[soft_p], soft[p][soft_p])
        img = np.zeros((H, W, 4), np.uint8)
        img[..., :3] = color[p]
        img[ring_p | soft_p, :3] = outline_rgb
        img[..., 3] = (alpha * 255).astype(np.uint8)

        ys, xs = np.nonzero(alpha > 0)
        x0, x1 = max(xs.min() - pad, 0), min(xs.max() + 1 + pad, W)
        y0, y1 = max(ys.min() - pad, 0), min(ys.max() + 1 + pad, H)
        crop = img[y0:y1, x0:x1]
        Image.fromarray(crop, "RGBA").save(os.path.join(out_parts, f"{p}.png"))

        pb = cfg["part_bones"][p]
        is_glued = p in glued
        verts, idx, edges, weights = build_mesh(crop[..., 3] > 0, x0, y0, y1, [bone_px[b] for b in pb], grid,
                                                anchor_dist if is_glued else None,
                                                glue_start, glued.get(p, 70.0))
        lo, hi = to_units(x0, y1), to_units(x1, y0)
        bmin = [min(bmin[0], lo[0]), min(bmin[1], lo[1])]
        bmax = [max(bmax[0], hi[0]), max(bmax[1], hi[1])]
        rig["parts"].append({
            "name": p, "order": order[p], "rect": [int(x0), int(y0), int(x1 - x0), int(y1 - y0)],
            "offset": lo,                                   # rect bottom-left in units (pivot = 0,0)
            "bones": pb,
            # flat arrays: Unity's JsonUtility can't parse nested arrays
            "vertices": [c for xy in verts for c in xy],
            "indices": idx,
            "edges": [i for e in edges for i in e],
            "boneIndices": [bw[0] for vw in weights for bw in vw],
            "boneWeights": [bw[1] for vw in weights for bw in vw],
        })
        src = img.astype(np.float32) / 255.0
        sa = src[..., 3:4]
        composite[..., :3] = src[..., :3] * sa + composite[..., :3] * (1 - sa)
        composite[..., 3:4] = sa + composite[..., 3:4] * (1 - sa)
        print(f"{p:16s} rect={x0},{y0} {x1 - x0}x{y1 - y0} verts={len(verts)} tris={len(idx) // 3}")

    rig["bounds"] = {"min": bmin, "max": bmax}
    with open(os.path.join(args.out, "Art", "rig.json"), "w") as f:
        json.dump(rig, f)
    save_debug(debug, composite, cfg["bones"], mask, parts)
    print(f"wrote {out_parts} + rig.json; debug images in {debug}")


def stroke_width(strokes):
    """Typical outline width (px): twice the median half-width measured on the stroke centre lines."""
    d = nd.distance_transform_edt(strokes)
    ridge = strokes & (d >= nd.maximum_filter(d, size=3)) & (d >= 2)
    return float(np.clip(2.0 * np.median(d[ridge]) - 1.0, 2.0, 40.0)) if ridge.any() else 6.0


def smooth_fill(rgb, known, sigma):
    """Normalised Gaussian blur over the `known` pixels only: every pixel gets the mean of known neighbours."""
    k = known.astype(np.float32)
    den = np.maximum(nd.gaussian_filter(k, sigma), 1e-6)
    return np.stack([nd.gaussian_filter(rgb[..., c] * k, sigma) / den for c in range(3)], -1)


def continue_outline(kept, hidden, fill_vis, outline_w, max_len, bridge_deg=40.0):
    """Carry a part's outline on into its hidden (overpainted) area.

    Returns (line, riding): the line mask inside `hidden`, and the part of it that rides the part's fill edge
    (everything on its far side is outside the part).

    An outline END is where a visible stroke of the part runs into the hidden area (the front part covers
    the rest). Its direction is the principal axis of the last ~2 outline widths of that stroke. Two ends
    that face each other are bridged with a straight segment (the belly line across a near leg's top, the
    back line under the mane). Any other end is marched along its direction until it leaves the hidden
    area (neck sides into the head, far-leg top or tail root under the body); where the part's own visible
    fill gets in the way (a curved ear tip whose edge runs on under the mane) the line is pushed back to half
    an outline width off that fill, so it rides the fill's edge the way the hidden contour would.
    """
    H, W = kept.shape
    w = max(2, int(round(outline_w)))
    zone = kept & (nd.distance_transform_edt(~hidden) <= 1.5)
    zone_lab, _ = nd.label(nd.binary_dilation(zone, iterations=max(1, w // 2)))   # one stroke end = one zone
    zone_lab *= zone
    stroke_lab, _ = nd.label(kept, structure=np.ones((3, 3)))
    df = nd.distance_transform_edt(~fill_vis)             # line centre closer than w/2 to the fill would clip
    ends = []                                              # (centre xy, unit direction into the hidden area)
    R = 2 * w
    for i, sl in enumerate(nd.find_objects(zone_lab), start=1):
        zy, zx = np.nonzero(zone_lab[sl] == i)
        if len(zy) < 3:
            continue
        c = np.array([zx.mean() + sl[1].start, zy.mean() + sl[0].start])
        sid = np.bincount(stroke_lab[zy + sl[0].start, zx + sl[1].start]).argmax()
        y0, y1 = max(int(c[1]) - R, 0), min(int(c[1]) + R + 1, H)
        x0, x1 = max(int(c[0]) - R, 0), min(int(c[0]) + R + 1, W)
        sy, sx = np.nonzero(stroke_lab[y0:y1, x0:x1] == sid)
        pts = np.stack([sx + x0, sy + y0], 1).astype(np.float64)
        pts = pts[np.hypot(*(pts - c).T) <= R]
        if len(pts) < 2 * w:
            continue
        mean = pts.mean(0)
        evals, evecs = np.linalg.eigh(np.cov((pts - mean).T))
        if evals[1] < 3.0 * max(evals[0], 1e-3):           # a blob, not a line: no direction
            continue
        v = evecs[:, 1]
        along = float(np.dot(c - mean, v))
        if abs(along) < 0.4 * w:                            # stroke touches the hidden area side-on, no end
            continue
        ends.append((c, v if along > 0 else -v))

    img = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(img)
    ride_img = Image.new("L", (W, H), 0)
    ride_d = ImageDraw.Draw(ride_img)
    cos_b = np.cos(np.radians(bridge_deg))
    pairs = []
    for i in range(len(ends)):
        for j in range(i + 1, len(ends)):
            dv = ends[j][0] - ends[i][0]
            dist = float(np.hypot(*dv))
            if 0 < dist <= max_len and np.dot(ends[i][1], dv) / dist > cos_b and np.dot(ends[j][1], -dv) / dist > cos_b:
                pairs.append((dist, i, j))
    used = set()
    for dist, i, j in sorted(pairs):
        if i in used or j in used:
            continue
        used |= {i, j}
        # start half a width back inside each stroke so the line seals against the old outline
        d.line([tuple(ends[i][0] - ends[i][1] * w / 2), tuple(ends[j][0] - ends[j][1] * w / 2)], fill=255, width=w)
    gy, gx = np.gradient(nd.gaussian_filter(df, 1.0))     # points away from the fill
    target = w / 2.0                                       # stroke centre sits half a width off the fill
    for k, (c, v) in enumerate(ends):
        if k in used:
            continue
        p, dv, path, riding, ride_from = c.copy(), v.copy(), [tuple(c - v * w / 2), tuple(c)], False, None
        for s in range(1, int(max_len)):
            q = p + dv
            x, y = int(round(q[0])), int(round(q[1]))
            if not (0 <= x < W and 0 <= y < H):
                break
            # The part's own fill is in the way: ride its edge (and keep hugging it once riding, until the
            # fill falls away by more than a width, e.g. past the end of the ear).
            if df[y, x] < target or (riding and df[y, x] < target + w):
                if not riding:
                    riding, ride_from = True, len(path) - 1
                g = np.array([gx[y, x], gy[y, x]])
                q = q + (target - df[y, x]) * g / max(np.hypot(*g), 1e-6)
                x, y = int(round(q[0])), int(round(q[1]))
                if not (0 <= x < W and 0 <= y < H):
                    break
            if s > w and not hidden[y, x]:
                break
            if np.dot(dv, v) < 0.5:                         # turned > 60 deg: it is wrapping a corner, stop
                break
            step = q - p
            dv = 0.7 * dv + 0.3 * step / max(np.hypot(*step), 1e-6)
            dv /= np.hypot(*dv)
            p = q
            path.append((float(p[0]), float(p[1])))
        if len(path) > 1:
            d.line(path, fill=255, width=w, joint="curve")
        if ride_from is not None and len(path) - ride_from > 1:
            ride_d.line(path[ride_from:], fill=255, width=w, joint="curve")
    return (np.array(img) > 0) & hidden, (np.array(ride_img) > 0) & hidden


def overpaint(rgb, dark, char_mask, fill, mask, extends, order, outline_rgb, outline_w, margin=5):
    """Draw the hidden part of each back part under its front parts so it joins the visible art seamlessly.

    extends: [(back, [front, ...], distance_px)]. Grows `mask` in place; returns (colour, soft) per part, where
    soft is an extra partial-alpha edge (outline colour) the export adds outside the part's mask.
      region   back fill grown <= distance px under the fronts (thin slivers opened away), plus the back's own
               copy of the junction strokes and its anti-aliased fringe against them -> no ghost line or
               hairline seam stays behind.
      tips     short stroke ends touching a front's strokes (a strand tip lying on the body) move to that front,
               so they travel with it instead of staying behind as specks.
      colour   nearest clean fill colour, denoised before and blurred after the copy -> no ray streaks or hard
               borders, and multi-colour parts (stripes, hoof bands) carry on colour by colour.
      outline  the outline is redrawn along the grown silhouette, so the old outline continues instead of
               stopping dead, and an exposed overpaint edge never shows as an unoutlined white wedge.
      fringe   the AA pixels taken off the back part move onto the front part as a soft outline-colour edge
               (alpha solved against the repainted fill), so the composite at rest still matches the source.
    margin: px from a stroke where fill counts as clean (anti-aliasing reaches about this far).
    """
    H, W = dark.shape
    lum = rgb.mean(2)
    color = {p: rgb.astype(np.float32) for p in mask}
    soft = {p: np.zeros((H, W), np.float32) for p in mask}
    clean = nd.distance_transform_edt(~dark) > margin     # away from anti-aliased stroke pixels
    out_rgb = np.array(outline_rgb, np.float32)
    r = max(2, int(round(outline_w * 0.75)))              # slivers thinner than ~1.5 outline widths go
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
    disk = xx * xx + yy * yy <= r * r
    by_order = {order[f]: f for f in order}
    for back, fronts, dist in extends:
        under = np.zeros((H, W), bool)
        owner = np.full((H, W), -1, np.int32)              # front part drawing each junction stroke pixel
        for f in fronts:
            under |= mask[f] | fill[f]
            owner[dark & mask[f]] = order[f]
        junction = dark & under                            # strokes/dark blobs a front part draws on top
        own_junction = mask[back] & junction
        if junction.any():
            d_j, (jy, jx) = nd.distance_transform_edt(~junction, return_indices=True)
            own = owner[jy, jx]                            # front owning the nearest junction stroke
        else:                                              # the fronts' strokes never touch this part
            d_j, own = np.full((H, W), np.inf), np.full((H, W), -1, np.int32)

        # Stroke tips: small leftover stroke pieces of the back part that touch a front's strokes.
        tips = np.zeros((H, W), bool)
        rest_lab, _ = nd.label(mask[back] & dark & ~own_junction, structure=np.ones((3, 3)))
        for i, sl in enumerate(nd.find_objects(rest_lab), start=1):
            m = rest_lab[sl] == i
            if m.sum() <= 4 * outline_w * outline_w and (d_j[sl][m] <= 2).any():
                tips[sl] |= m
        for o in np.unique(own[tips]):
            mask[by_order[o]] |= tips & (own == o)

        grow = (nd.distance_transform_edt(~fill[back]) <= dist) & under & char_mask & ~mask[back]
        grow &= nd.binary_opening(mask[back] | grow, structure=disk)
        fringe = fill[back] & (d_j <= margin)
        region = grow | own_junction | tips | fringe
        known = fill[back] & clean & ~region
        if not known.any():                                # very thin part: no pixel is 5px from a stroke
            known = fill[back] & ~region

        # Colour: denoise the source (fill grain would spread as rays), copy nearest, then soften the borders.
        src = smooth_fill(rgb, known, 2.0)
        _, (iy, ix) = nd.distance_transform_edt(~known, return_indices=True)
        c = color[back]
        c[region] = src[iy[region], ix[region]]
        c[region] = smooth_fill(c, region | known, 4.0)[region]

        # Contour continuation: the part's OWN outline ends are carried on under the fronts (bridged when two
        # ends face each other, extended along their tangent otherwise). Hidden fill on the far side of that
        # contour is dropped: it would carry the front part's shape and show as a ghost lobe once they part.
        hidden = grow | own_junction                       # only visible once the joint moves
        kept = mask[back] & dark & ~hidden & ~tips         # the part's strokes that stay visible
        line, riding = continue_outline(kept, hidden, fill[back] & ~hidden, outline_w, 4 * dist)
        # Under fronts cut from the SAME fill (near leg / body, head / neck, ear base / head) the art has no
        # line, the two read as one shape: there the continued contour only bounds the part (not drawn, not
        # part of it), since a drawn line would show as a seam once the joint bends.
        same_fill = np.zeros((H, W), bool)
        for f in fronts:
            if (nd.binary_dilation(fill[back], iterations=3) & fill[f]).any():
                same_fill |= mask[f] | fill[f]
        # Hidden pixels reached across the part's outline (its fill is an outline width farther than the
        # outline itself) lie outside the part's contour, e.g. a nub past the ear tip: drop them too. So is
        # whatever lies past a continuation line that rides the fill edge (the ear's edge under the mane).
        d_fill = nd.distance_transform_edt(~(fill[back] & ~hidden))
        beyond = hidden & (d_fill - nd.distance_transform_edt(~kept) >= 0.75 * outline_w)
        if riding.any():
            _, (ly, lx) = nd.distance_transform_edt(~(line | kept), return_indices=True)
            beyond |= hidden & ~line & riding[ly, lx] & (d_fill > outline_w)
        lab, _ = nd.label(hidden & ~line & ~beyond)
        touching = np.unique(lab[nd.binary_dilation(fill[back] & ~hidden) & (lab > 0)])
        inside = np.isin(lab, touching) & (lab > 0)
        part = (mask[back] & ~hidden) | inside | line
        pocket = nd.binary_fill_holes(part) & ~part & hidden  # trim left a pocket enclosed by the part: fill it
        inside |= pocket & ~line
        line &= ~same_fill
        line_lab, _ = nd.label(line, structure=np.ones((3, 3)))   # keep whole line pieces touching the part
        line = np.isin(line_lab, np.unique(line_lab[nd.binary_dilation(inside | (mask[back] & ~hidden))])) & line
        mask[back] = (mask[back] & ~hidden) | inside | line
        t = np.clip(nd.gaussian_filter(line.astype(np.float32), 0.8) * 1.6, 0.0, 1.0)[..., None]
        draw = inside | line                               # AA blend; never touches visible pixels
        c[draw] = (c * (1.0 - t) + out_rgb * t)[draw]

        # Fringe -> soft edge on the front part that owns the nearest junction stroke.
        cl = c.mean(2)
        a = np.clip((cl - lum) / np.maximum(cl - out_rgb.mean(), 1.0), 0.0, 1.0)
        for f in fronts:
            sel = fringe & (own == order[f])
            soft[f][sel] = np.maximum(soft[f][sel], a[sel])
    return {p: np.clip(np.rint(v), 0, 255).astype(np.uint8) for p, v in color.items()}, soft


def seg_dist(px, py, a, b):
    ax, ay = a
    bx, by = b
    vx, vy = bx - ax, by - ay
    t = np.clip(((px - ax) * vx + (py - ay) * vy) / max(vx * vx + vy * vy, 1e-6), 0, 1)
    return np.hypot(px - (ax + t * vx), py - (ay + t * vy))


def build_mesh(alpha, x0, y0, y1, bones, grid, anchor_dist=None, glue_start=8.0, glue_blend=70.0):
    """Grid mesh over opaque cells + auto weights. Vertices in sprite-rect px (origin bottom-left, y up).

    anchor_dist: distance map to the anchor (body) fill. When given, bones[0] is the anchor bone and
    owns every vertex on/under the body, handing over to the limb bones with a smoothstep over glue_blend px.
    """
    h, w = alpha.shape
    nx, ny = int(np.ceil(w / grid)), int(np.ceil(h / grid))
    vid, verts, idx = {}, [], []

    def v(ix, iy):
        if (ix, iy) not in vid:
            vid[(ix, iy)] = len(verts)
            verts.append((min(ix * grid, w), min(iy * grid, h)))
        return vid[(ix, iy)]

    cells = set()
    for cy in range(ny):
        for cx in range(nx):
            if alpha[cy * grid:(cy + 1) * grid, cx * grid:(cx + 1) * grid].any():
                cells.add((cx, cy))
                a, b, c, dd = v(cx, cy), v(cx + 1, cy), v(cx + 1, cy + 1), v(cx, cy + 1)
                idx += [a, c, b, a, dd, c]
    edges = []
    for cx, cy in cells:
        for (ax, ay), (bx, by), nb in (((cx, cy), (cx + 1, cy), (cx, cy - 1)),
                                       ((cx + 1, cy), (cx + 1, cy + 1), (cx + 1, cy)),
                                       ((cx + 1, cy + 1), (cx, cy + 1), (cx, cy + 1)),
                                       ((cx, cy + 1), (cx, cy), (cx - 1, cy))):
            if nb not in cells:
                edges.append([vid[(ax, ay)], vid[(bx, by)]])

    pts = np.array(verts, np.float64)
    gx, gy = pts[:, 0] + x0, pts[:, 1] + y0
    limb = bones[1:] if anchor_dist is not None else bones
    dists = np.stack([seg_dist(gx, gy, hd, tl) for hd, tl in limb], 1)
    wts = 1.0 / np.power(dists + 8.0, 4)
    wts = wts / wts.sum(1, keepdims=True)
    if anchor_dist is not None:
        ix = np.clip(gx.astype(int), 0, anchor_dist.shape[1] - 1)
        iy = np.clip(gy.astype(int), 0, anchor_dist.shape[0] - 1)
        t = np.clip((anchor_dist[iy, ix] - glue_start) / glue_blend, 0.0, 1.0)
        glue = 1.0 - t * t * (3.0 - 2.0 * t)
        wts = np.concatenate([glue[:, None], wts * (1.0 - glue)[:, None]], 1)
    top = np.argsort(-wts, 1)[:, :4]
    out_w = []
    for i in range(len(verts)):
        ww = wts[i, top[i]]
        ww = ww / ww.sum()
        bw = [[int(b), float(x)] for b, x in zip(top[i], ww)]
        bw += [[0, 0.0]] * (4 - len(bw))          # SpriteSkin validates all 4 indices, even weight 0
        out_w.append(bw)
    verts_up = [[float(x), float((y1 - y0) - y)] for x, y in verts]
    return verts_up, idx, edges, out_w


def save_debug(debug, composite, bones, mask, parts):
    img = Image.fromarray((composite * 255).astype(np.uint8), "RGBA")
    bgimg = Image.new("RGBA", img.size, (120, 170, 220, 255))
    bgimg.alpha_composite(img)
    d = ImageDraw.Draw(bgimg)
    for b in bones:
        h, t = tuple(b["head"]), tuple(b["tail"])
        d.line([h, t], fill=(255, 0, 0, 255), width=6)
        d.ellipse([h[0] - 9, h[1] - 9, h[0] + 9, h[1] + 9], fill=(255, 255, 0, 255))
    bgimg.resize((bgimg.width // 2, bgimg.height // 2)).save(os.path.join(debug, "composite_bones.png"))
    rng = np.random.RandomState(3)
    pm = np.full(composite.shape[:2] + (3,), 255, np.uint8)
    for p in parts:
        pm[mask[p]] = rng.randint(40, 230, 3)
    Image.fromarray(pm).resize((pm.shape[1] // 2, pm.shape[0] // 2)).save(os.path.join(debug, "part_map.png"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("inspect")
    a.add_argument("--image", required=True)
    a.add_argument("--debug", required=True)
    a.add_argument("--crop", action="append", help="x0,y0,x1,y1 (repeatable)")
    a.add_argument("--dark-lum", type=int, default=150)
    a.add_argument("--min-component", type=int, default=300)
    s = sub.add_parser("split")
    s.add_argument("--image", required=True)
    s.add_argument("--config", required=True)
    s.add_argument("--out", required=True, help="Unity character folder, e.g. Assets/Unicorn")
    s.add_argument("--debug")
    args = ap.parse_args()
    inspect(args) if args.cmd == "inspect" else split(args)


if __name__ == "__main__":
    main()

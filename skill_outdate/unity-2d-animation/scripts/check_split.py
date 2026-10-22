"""
QA check for a subject split (Tools~/split_<name>.py output; unity-2d-animation skill).

Verifies that compositing the part PNGs back-to-front, at their rig.json rects,
reproduces the source image with no gaps and no wrong-part overlap.

Usage
  python3 -I check_split.py --image SRC.png --out <SubjectDir> [--debug DIR]
          [--dark-lum 150] [--tol 40] [--min-area 12]

<SubjectDir> is the --out folder passed to the splitter (reads
Art/rig.json and Art/Parts/<name>.png beneath it).

Checks
  1. Composite match   - alpha-composite all parts back-to-front (by rig.json
     "order") over the source's background colour, compare to the source
     inside the character area. Mismatched clusters >= min-area FAIL (wrong
     part on top, missing area, overpaint showing through); any character
     pixel not covered by a part also FAILs.
  2. Overpaint quality  - per part, opaque pixels that differ from the source
     are overpaint/hidden pixels. Dark/grey ones well inside the part (not its
     own outline) are stroke leftovers -> FAIL.
  3. Holes              - transparent pixels enclosed inside a part (not
     connected to the crop border) -> FAIL, unless the source shows background
     there too (drawn negative space: inside a curl or a handle, declared with
     the splitter's bg_holes) -> INFO.
  4. Islands            - a part with more than one opaque blob -> WARN (not
     a hard failure; e.g. two eyes are legitimately separate).

Prints one line per finding plus a final PASS/FAIL, exits 1 on any FAIL.
Writes <debug>/diff.png: source dimmed, mismatches red, grey streaks yellow,
holes cyan, with bbox outlines.
"""
import argparse
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd

STRUCT8 = nd.generate_binary_structure(2, 2)


def clusters(mask, min_area):
    """Label connected components (8-conn) and return (bbox, size) for those >= min_area."""
    lab, n = nd.label(mask, structure=STRUCT8)
    out = []
    for i, sl in enumerate(nd.find_objects(lab), start=1):
        if sl is None:
            continue
        size = int((lab[sl] == i).sum())
        if size >= min_area:
            out.append(((sl[1].start, sl[0].start, sl[1].stop, sl[0].stop), size))
    return out


def border_mask(shape):
    m = np.zeros(shape, bool)
    m[0, :] = m[-1, :] = m[:, 0] = m[:, -1] = True
    return m


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--image", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--debug")
    ap.add_argument("--dark-lum", type=int, default=150)
    ap.add_argument("--tol", type=int, default=40)
    ap.add_argument("--min-area", type=int, default=12)
    args = ap.parse_args()

    debug = args.debug or os.path.join(args.out, "Tools~", "debug", "check_split")
    os.makedirs(debug, exist_ok=True)

    src = np.array(Image.open(args.image).convert("RGB")).astype(np.int32)
    H, W = src.shape[:2]
    rig = json.load(open(os.path.join(args.out, "Art", "rig.json")))
    parts_dir = os.path.join(args.out, "Art", "Parts")
    parts = sorted(rig["parts"], key=lambda p: p["order"])  # back-to-front

    bg = np.median(src[border_mask((H, W))], axis=0)       # source background colour (border median)
    bg_diff = np.abs(src - bg).max(2)
    char_mask = bg_diff > 10                                 # non-background = "character" pixels

    findings = []
    canvas = np.zeros((H, W, 4), np.float64)                 # straight-alpha accumulator
    part_imgs = {}
    for p in parts:
        x0, y0, w, h = p["rect"]
        img = np.array(Image.open(os.path.join(parts_dir, f"{p['name']}.png")).convert("RGBA")).astype(np.float64) / 255.0
        part_imgs[p["name"]] = (img, x0, y0)
        region = canvas[y0:y0 + h, x0:x0 + w]
        sa = img[..., 3:4]
        region[..., :3] = img[..., :3] * sa + region[..., :3] * (1 - sa)
        region[..., 3:4] = sa + region[..., 3:4] * (1 - sa)
        canvas[y0:y0 + h, x0:x0 + w] = region

    covered = canvas[..., 3] >= 0.5                           # pixels any part opaquely covers
    rendered = canvas[..., :3] * canvas[..., 3:4] + (bg / 255.0) * (1 - canvas[..., 3:4])
    rendered = (rendered * 255.0)

    # --- check 1: composite match -----------------------------------------------------------
    # Ignore a 2px silhouette fringe (antialiasing) on both the "should be covered" and the
    # "is covered" masks so a correct split doesn't trip on soft edges.
    cmp_region = nd.binary_erosion(covered | char_mask, iterations=2)
    diff = np.abs(rendered - src).max(2)
    mismatch = cmp_region & (diff > args.tol)
    for bbox, size in clusters(mismatch, args.min_area):
        findings.append(("FAIL", f"composite mismatch bbox={bbox} size={size} "
                                  "(wrong part on top / overpaint showing / missing area)"))
    missing = nd.binary_erosion(char_mask, iterations=2) & ~nd.binary_dilation(covered, iterations=2)
    for bbox, size in clusters(missing, args.min_area):
        findings.append(("FAIL", f"uncovered character pixels bbox={bbox} size={size} (no part covers this area)"))

    # --- check 2: overpaint quality ----------------------------------------------------------
    streak_mask_global = np.zeros((H, W), bool)
    # The splitter redraws the outline along the overpainted silhouette (outline continuation): dark
    # overpaint within one outline width of the part's edge is that outline, not a stroke leftover.
    edge_margin = max(4.0, float(rig.get("outlineWidth", 0)) + 3.0)
    for p in parts:
        img, x0, y0 = part_imgs[p["name"]]
        h, w = img.shape[:2]
        alpha_ok = img[..., 3] >= 0.5
        src_crop = src[y0:y0 + h, x0:x0 + w]
        part_rgb = img[..., :3] * 255.0
        own_diff = np.abs(part_rgb - src_crop).max(2)
        overpaint = alpha_ok & (own_diff > args.tol)
        inside = nd.distance_transform_edt(alpha_ok) >= edge_margin   # away from this part's own edge
        lum = part_rgb.mean(2)
        streak = overpaint & inside & (lum < args.dark_lum + 30)
        for bbox, size in clusters(streak, args.min_area):
            gbbox = (bbox[0] + x0, bbox[1] + y0, bbox[2] + x0, bbox[3] + y0)
            findings.append(("FAIL", f"{p['name']}: grey streak bbox={gbbox} size={size} "
                                      "(stroke leftover inside overpaint)"))
            streak_mask_global[y0:y0 + h, x0:x0 + w][bbox[1]:bbox[3], bbox[0]:bbox[2]] |= \
                streak[bbox[1]:bbox[3], bbox[0]:bbox[2]]

    # --- check 3: holes & check 4: islands -----------------------------------------------------
    hole_mask_global = np.zeros((H, W), bool)
    for p in parts:
        img, x0, y0 = part_imgs[p["name"]]
        h, w = img.shape[:2]
        alpha_ok = img[..., 3] >= 0.5
        transparent = ~alpha_ok
        lab, n = nd.label(transparent, structure=STRUCT8)
        border = border_mask((h, w))
        border_ids = set(lab[border].tolist())
        for i, sl in enumerate(nd.find_objects(lab), start=1):
            if sl is None or i in border_ids:
                continue
            m = lab[sl] == i
            size = int(m.sum())
            if size >= args.min_area:
                bbox = (sl[1].start + x0, sl[0].start + y0, sl[1].stop + x0, sl[0].stop + y0)
                # Source background under >= 95% of the hole = the art's own negative space, not a gap.
                src_bg = ~char_mask[y0:y0 + h, x0:x0 + w][sl][m]
                if src_bg.mean() >= 0.95:
                    findings.append(("INFO", f"{p['name']}: negative space bbox={bbox} size={size} (background in source)"))
                    continue
                findings.append(("FAIL", f"{p['name']}: hole bbox={bbox} size={size} (transparent gap inside part)"))
                hole_mask_global[y0:y0 + h, x0:x0 + w][sl] |= m

        comps = clusters(alpha_ok, args.min_area * 4)
        if len(comps) > 1:
            comps_src = [((b[0] + x0, b[1] + y0, b[2] + x0, b[3] + y0), s) for b, s in comps]
            findings.append(("WARN", f"{p['name']}: {len(comps)} separate opaque islands {comps_src}"))

    # --- report + debug image -------------------------------------------------------------------
    for level, msg in findings:
        print(f"{level} {msg}")
    ok = not any(level == "FAIL" for level, _ in findings)
    print("PASS" if ok else "FAIL")

    dim = (src * 0.4).astype(np.uint8)
    dbg = Image.fromarray(dim).convert("RGB")
    arr = np.array(dbg)
    arr[mismatch] = [255, 0, 0]
    arr[missing] = [255, 0, 0]
    arr[streak_mask_global] = [255, 255, 0]
    arr[hole_mask_global] = [0, 255, 255]
    dbg = Image.fromarray(arr)
    d = ImageDraw.Draw(dbg)
    all_boxes = clusters(mismatch, args.min_area) + clusters(missing, args.min_area)
    for bbox, _ in all_boxes:
        d.rectangle(bbox, outline=(255, 0, 0), width=2)
    diff_path = os.path.join(debug, "diff.png")
    dbg.save(diff_path)
    print(f"debug image: {diff_path}")

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

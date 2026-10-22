"""
QA check for Unity camera captures of an animated skinned-sprite subject,
rendered over a solid key-colour background with no other scene objects
(unity-2d-animation skill).

Usage
  python3 -I check_frames.py FRAME.png [FRAME2.png ...] [--key 255,0,255]
          [--key-tol 60] [--dark-lum 150] [--reach 4] [--min-area 6]
          [--min-len 6] [--debug DIR] [--no-outline-check] [--rest REST.png]

Checks (per frame)
  1. See-through holes - key-coloured pixels enclosed inside the silhouette
     (a connected component of key pixels that never touches the image
     border). A hole whose rim is outlined all round is natural negative
     space (e.g. between crossed legs) and is reported as INFO; a hole with
     an unoutlined rim run >= min-len (or any hole under --no-outline-check)
     is a gap in the rig and FAILs when its area >= min-area.
  2. Exposed fill edges - every silhouette pixel touching the key background
     (a "boundary" pixel) must have a dark outline pixel within --reach px
     inside the silhouette. A run of boundary pixels with none (a white
     wedge, cut seam, or overpaint swung out from under a joint) FAILs if its
     cluster has >= min-len pixels. Skip with --no-outline-check for
     outline-less art. With --rest (a Rest-pose capture from the same keyed
     session, so the framing matches), an edge that is exposed at the same
     pixels in the rest frame is the art's own unoutlined edge (grass bottom,
     a fur tuft) and is reported as INFO; anything that opens only when posed
     still FAILs.

Prints findings per frame, then a final PASS/FAIL; exits 1 on any FAIL.
Writes an annotated copy per frame (red boxes on findings, cyan fill on
holes) to --debug/<frame>_check.png, default alongside the frame.
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd

CROSS = nd.generate_binary_structure(2, 1)   # 4-connectivity (no diagonal leaks through a 1px outline)
STRUCT8 = nd.generate_binary_structure(2, 2)  # 8-connectivity (for merging/measuring found clusters)


def clusters(mask, min_size, structure=STRUCT8):
    """Label connected components and return (bbox, size) for those >= min_size."""
    lab, n = nd.label(mask, structure=structure)
    out = []
    for i, sl in enumerate(nd.find_objects(lab), start=1):
        if sl is None:
            continue
        size = int((lab[sl] == i).sum())
        if size >= min_size:
            out.append(((sl[1].start, sl[0].start, sl[1].stop, sl[0].stop), size))
    return out


def check_frame(path, args, rest_edges=None):
    """Run both checks on one frame; returns (findings, debug_image, unoutlined_mask).

    rest_edges: dilated unoutlined mask of the rest frame; exposed edges lying >= 80% inside it are art edges.
    """
    rgb = np.array(Image.open(path).convert("RGB")).astype(np.int32)
    H, W = rgb.shape[:2]
    findings = []

    # Key mask: per-channel tolerance absorbs antialiased key/fill blends near edges too,
    # since a half-blended pixel is still within key_tol of the pure key colour.
    key_mask = (np.abs(rgb - np.array(args.key)) <= args.key_tol).all(axis=2)
    silhouette = ~key_mask

    lum = rgb.mean(2)
    dist_to_dark = nd.distance_transform_edt(~(lum < args.dark_lum))

    # --- check 1: see-through holes --------------------------------------------------------
    lab, n = nd.label(key_mask, structure=CROSS)
    border_ids = set(lab[0, :].tolist()) | set(lab[-1, :].tolist()) | set(lab[:, 0].tolist()) | set(lab[:, -1].tolist())
    hole_mask = np.zeros((H, W), bool)
    for i, sl in enumerate(nd.find_objects(lab), start=1):
        if sl is None or i in border_ids:
            continue
        m = lab[sl] == i
        size = int(m.sum())
        if size >= args.min_area:
            bbox = (sl[1].start, sl[0].start, sl[1].stop, sl[0].stop)
            # Rim = silhouette pixels touching this hole. Outlined all round -> drawn negative space,
            # an unoutlined run -> the rig opened a gap (fill edge against background).
            grown = tuple(slice(max(x.start - 1, 0), x.stop + 1) for x in sl)
            hole = np.zeros((H, W), bool)
            hole[sl] = m
            rim = nd.binary_dilation(hole[grown], structure=CROSS) & silhouette[grown]
            open_rim = int((rim & (dist_to_dark[grown] > args.reach)).sum())
            if args.no_outline_check or open_rim >= args.min_len:
                findings.append(("FAIL", f"see-through hole bbox={bbox} size={size} unoutlined_rim={open_rim}"))
                hole_mask[sl] |= m
            else:
                findings.append(("INFO", f"enclosed negative space bbox={bbox} size={size} (rim fully outlined)"))

    # --- check 2: exposed fill edges (unoutlined silhouette boundary) ----------------------
    unoutlined_mask = np.zeros((H, W), bool)
    if not args.no_outline_check:
        key_touch = nd.binary_dilation(key_mask, structure=CROSS, iterations=1)
        boundary = silhouette & key_touch                      # silhouette pixels against the key bg
        unoutlined = boundary & (dist_to_dark > args.reach)     # no outline within reach -> exposed fill
        merged = nd.binary_dilation(unoutlined, iterations=1)   # small dilation to join a broken run
        lab2, n2 = nd.label(merged, structure=STRUCT8)
        for i, sl in enumerate(nd.find_objects(lab2), start=1):
            if sl is None:
                continue
            m = (lab2[sl] == i) & unoutlined[sl]                # measure the real (undilated) pixels
            size = int(m.sum())
            if size >= args.min_len:
                bbox = (sl[1].start, sl[0].start, sl[1].stop, sl[0].stop)
                unoutlined_mask[sl] |= m
                if rest_edges is not None and rest_edges[sl][m].mean() >= 0.8:
                    findings.append(("INFO", f"art edge bbox={bbox} size={size} (exposed at rest too)"))
                    continue
                findings.append(("FAIL", f"exposed fill edge bbox={bbox} size={size} (no outline within {args.reach}px)"))

    dbg = Image.fromarray(rgb.astype(np.uint8)).convert("RGB")
    arr = np.array(dbg)
    arr[hole_mask] = [0, 255, 255]
    arr[unoutlined_mask] = [255, 80, 0]
    dbg = Image.fromarray(arr)
    d = ImageDraw.Draw(dbg)
    for level, msg in findings:
        if level == "FAIL" and "bbox=(" in msg:
            bbox = eval(msg.split("bbox=")[1].split(")")[0] + ")")
            d.rectangle(bbox, outline=(255, 0, 0), width=2)
    return findings, dbg, unoutlined_mask


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("frames", nargs="+")
    ap.add_argument("--key", default="255,0,255")
    ap.add_argument("--key-tol", type=int, default=60)
    ap.add_argument("--dark-lum", type=int, default=150)
    ap.add_argument("--reach", type=int, default=4)
    ap.add_argument("--min-area", type=int, default=6)
    ap.add_argument("--min-len", type=int, default=6)
    ap.add_argument("--debug")
    ap.add_argument("--no-outline-check", action="store_true")
    ap.add_argument("--rest", help="Rest-pose capture from the same keyed session: its exposed edges are art edges")
    args = ap.parse_args()
    args.key = [int(v) for v in args.key.split(",")]
    if args.debug:
        os.makedirs(args.debug, exist_ok=True)

    rest_edges = None
    if args.rest:
        _, _, rest_unoutlined = check_frame(args.rest, args)
        rest_edges = nd.binary_dilation(rest_unoutlined, iterations=3)   # tolerate AA jitter between renders

    all_ok = True
    for frame in args.frames:
        findings, dbg, _ = check_frame(frame, args, rest_edges)
        print(f"== {frame} ==")
        for level, msg in findings:
            print(f"{level} {msg}")
            all_ok &= level != "FAIL"
        print("PASS" if not any(l == "FAIL" for l, _ in findings) else "FAIL")

        base = os.path.splitext(os.path.basename(frame))[0] + "_check.png"
        out_path = os.path.join(args.debug, base) if args.debug else os.path.join(os.path.dirname(frame) or ".", base)
        dbg.save(out_path)
        print(f"debug image: {out_path}")

    print("PASS" if all_ok else "FAIL")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()

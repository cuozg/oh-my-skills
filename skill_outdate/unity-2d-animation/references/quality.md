# Quality gates: no white gaps, no see-through holes, no wrong overlap

Two hard **gates**. Each one is an automated check that must print `PASS`, followed by a look at the images. A failing gate loops back to the phase that owns the defect. Fix the config or the motion, never the check tolerance, unless you have shown the flagged pixels are correct art.

## Gate 1: split (after `split`, before Unity)
```
python3 -I <skill>/scripts/check_split.py --image Assets/<Name>/Source/<name>.png --out Assets/<Name>
```
- **Composite match:** the parts stacked back-to-front must reproduce the source. A mismatch means a part is in the wrong order, overpaint is showing on top, or an area is missing.
- **Overpaint quality:** the hidden (overpainted) pixels must be clean fill, with no grey streaks or stroke leftovers. The redrawn continuation outline (within `outlineWidth` + 3 px of the part's edge) is expected and not flagged.
- **Holes:** no transparent pixels enclosed inside a part. A hole where the source shows background (negative space declared with `bg_holes`) is reported as `INFO`.
- **Islands** (warning): a part made of several separate pieces usually means a wrong assignment. Two eyes are fine.

Also check by eye:
- `Tools~/debug/composite_bones.png`: identical to the source, with the bones on the right landmarks.
- `part_map.png`: each part is one clean region.
- A contact sheet of the `Art/Parts/*.png` files on a coloured background: the overpaint reads as clean fill that **joins the old part seamlessly**: no hairline where old pixels meet drawn ones, no colour rays, the part's own outline continuing under the front parts (no dead end), no drawn area in the shape of a front part, and no stray stroke specks inside the part.
- The split printed no `WARN unassigned` lines.

| Finding | Fix (in `Tools~/<name>.json`, or the subject's `split_<name>.py`) |
|---|---|
| Mismatch where two parts meet | Correct the `parts` order or the `exclusive` pair |
| Ghost outline where a back part continues under a front part | Add `exclusive [front, back]` |
| Grey streak in the overpaint | The overpaint is sampling near a stroke. Grow `extend` from a cleaner fill, move the `cuts`, or raise `margin` of `overpaint()` in the splitter copy |
| Hairline seam where the drawn area meets the old part | The junction stroke isn't in the front's mask, so the fringe isn't repainted. Add the front to `extend.under`, or `exclusive [front, back]` |
| Continuation outline too thick/thin, or stroke leftovers flagged near the edge | Set `outline_width` to the stroke width measured in an inspect crop |
| Ghost lines or a lobe in a front part's shape (ear edge copied from the mane, leg-shaped bracket on the belly) appear when parts move apart | The overpaint must follow the back part's own contour. Check `continue_outline()` found that outline end (debug its ends on the part); a front cut from the same fill must get no line |
| Outline stops dead at the junction, or a dark speck stays inside a part | The stroke belongs to neither side cleanly. Move the `cuts` endpoint into the stroke, or add the missing `exclusive` pair |
| Hole in a part | Raise `extend.distance`, or add the missing `under` part |
| Island of a back part next to a seam (overpaint lobe spilling past its own contour under the front part's outline) | `extend.distance` is larger than the joint needs. Size it to the travel at the seam: pivot distance × sin(max angle), plus a few px |
| Island in the wrong part | Add a seed or polygon `assign` rule for that region |

## Gate 2: frames (after every build that changes rig or motion)
Run this in Play mode through the HUD, over a magenta key background with the environment and other subjects hidden. Capture `Rest_0` first: `KeyBackground` fixes the framing on its first call, so every sample of the session shares the rest frame's camera. Each eval returns `frameCount:isPlaying`, which catches a dropped Play session (pitfalls.md) on the sample where it happens:
```
unity command eval 'if (!UnityEditor.EditorApplication.isPlaying) return "NOTPLAYING"; var h = UnityEngine.Object.FindFirstObjectByType<<Name>.<Name>DebugHUD>(); h.KeyBackground(true); h.PoseAt("<Clip>", <t>f); return UnityEngine.Time.frameCount + ":ok";'
unity command capture_game_view --source camera --save_path Temp/Captures/<Clip>_<t>.png
python3 -I <skill>/scripts/check_frames.py Assets/Temp/Captures/*.png --rest Assets/Temp/Captures/Rest_0.png
```
- **Sample times:**
  - Loops: at least 0, .25, .5, .75 for each clip.
  - One-shots: also their extremes (the held pose, the peak of each `Bump`).
  - Rest, before any motion exists: the rest frame has to pass too.
- **See-through holes:** background visible inside the silhouette with an unoutlined rim, meaning a joint has opened. An enclosed area outlined all round (between crossed legs, inside a handle) is drawn negative space and is reported as `INFO`.
- **Exposed fill edges:** the silhouette edge must be outlined everywhere. A light edge is a white wedge, a cut seam, or overpaint that has swung into view. An edge the art itself leaves unoutlined is exposed at rest too; `--rest` reports it as an `INFO` art edge.
- **Stale captures:** frames meant to differ that come back identical (same hash, same findings) mean Play mode isn't ticking. See pitfalls.md and recapture before trusting the gate.
- **Static parts shifting between frames** (root, grass, a planted foot) mean the framing moved, not the rig: a subject HUD copy from before the frame-once fix, or another subject in view. Check the weights in `rig.json` before blaming the rig.
- **Wrong overlap** is checked by eye on the same captures. Every part must sit in front of or behind the right neighbour: near limbs in front of the body, far limbs behind it, and the head over the neck seam.

| Finding | Fix |
|---|---|
| White wedge under the body when a limb swings | Glue the limb (`glued`, with the anchor first in `part_bones`) instead of growing `extend` further |
| Hole or open wedge at a joint at extreme poses | Lower that joint's amplitude (see the ceilings in animation.md), or raise `extend.distance` for the back part |
| Dark smear or sliver at a chain root (tail, hair) | The glue blend is too long for a strongly rotating chain. Shorten it (~35 px) and reduce the clip offsets |
| Limbs look stretched | The amplitude is too high, or the glue blend is too long |
| Feet sink into or float above the ground | Reduce the root `pos` dip, or flex the legs to compensate (thigh forward, shin back) |
| Limb drawn on the wrong side of the body | Fix the `parts` order (near vs far), re-split and rebuild |
| White notch where a back part's overpaint pokes out past a front part (body above the mane, torso past a shoulder) when the two rotate apart | Reduce the relative rotation at that seam (e.g. spine vs neck), or lower that `extend.distance`, so the overpaint stays under the front part at every pose |
| Seam opens between two segments of a chain | Give both parts the shared bone in `part_bones`, so the blend spans the seam |

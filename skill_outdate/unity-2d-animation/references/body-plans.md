# Body plans: parts, order, bones and glue per subject type

These are starting points, not rules. Read the actual art first: whatever moves separately needs its own part, and every part needs a bone that moves it. Name bones consistently, because `<Name>ClipFactory` motions refer to bones by name. Motions for bones the rig lacks are skipped, and bones without a motion stay at rest.

## Rules shared by every plan
- **Back-to-front `parts`:** far-side limbs < body < near-side limbs < head < hair/mane < eyes/details. The near side is the one facing the viewer.
- **One root bone** (Pelvis, Hips, Body or Base) at the centre of mass. Every other bone descends from it.
- **`exclusive` pairs:** the front part owns the shared strokes wherever the back part continues *under* it (body under head, far-leg top under body). Leave out pairs that separate when animated, such as leg vs leg or tail vs body.
- **`extend` (overpaint):** every hidden joint gets one. Size the distance to the largest rotation the joint will see: about 45 px for small joints and 60–70 px for limb roots.
- **`glued` limbs:** every limb, tail or appendage attached to the body. Its `part_bones` starts with the anchor bone (Pelvis or Spine). Blend about 70 px for limbs and 35 px for strongly rotating chains like tails. Glue makes the joint bend instead of swinging overpaint out from under the body.
- **Chains** (tail, hair, cloth, tentacle): use 2–4 segments. The tail of one bone is the head of the next.
- **Fused fills:** pieces that meet with no stroke between them, only shading (a leaf growing out of a stem), stay **one part with several bones**. Auto weights bend that mesh continuously, so no seam exists to open. Cut a fused fill only where the pieces must overlap or separate.

## Quadruped (horse, dog, cat, pony)
- **Parts:** `Tail, BackFarLeg, FrontFarLeg, Body, BackNearLeg, FrontNearLeg, Ears, Head, [Horn], Mane, Eyes`
- **Bones:** `Pelvis → Spine → Neck → Head [→ Horn]`; `Pelvis → Tail1..3`. Each leg is `{Back,Front}{Left,Right}{Thigh,Shin,Hoof}`; back legs parent to Pelvis and front legs to Spine.
- **Cuts:** neck/head, ear base, and the four leg tops where they share the belly fill.
- **Glue:** all four legs to Body (anchor Pelvis for back legs, Spine for front legs), and the tail at 35 px.

## Biped (human, robot, bird on foot)
- **Parts:** `FarArm, FarLeg, Torso, NearLeg, Head, Hair, NearArm, Eyes`. Put the near arm in front of the torso.
- **Bones:** `Hips → Spine → Chest → Neck → Head`; `Hips → {L,R}Thigh → Shin → Foot`; `Chest → {L,R}UpperArm → Forearm → Hand`.
- **Cuts:** shoulders, hips and the neck where the fills merge.
- **Glue:** legs to Hips, arms to Chest, blend about 60 px. The shoulder overpaint goes on the torso (`extend` Torso under NearArm).

## Winged (bird, dragon, fairy)
- Use the base plan (biped or quadruped) and add `FarWing` (behind the body) and `NearWing` (in front of it).
- **Bones:** `Spine → {L,R}WingRoot → WingMid → WingTip`. Glue the wings to the Spine at about 50 px.

## Limbless (slime, worm, fish, ghost)
- **Parts:** usually `Body, Eyes, [Mouth]`, plus `Fin` or `Tail` if present.
- **Bones:** a spine chain `Root → Seg1..Seg4` along the long axis. A blob uses `Root → Top`. Squash and stretch come from scale on the root (see animation.md), so give the Root bone the whole body weight and set its head at the base, so scaling stays grounded.

## Object or prop (chest, door, lever, flag, plant)
- **Parts:** one per rigid piece (`Base, Lid` or `Pole, Cloth`). The moving piece goes in front unless it swings behind.
- **Bones:** the root sits on the static piece. Put a **hinge** bone's head exactly on the pivot (lid hinge, door edge, lever axle). Flexible pieces (cloth, leaves) get a chain of 3–5 bones.
- **Glue:** usually none for rigid pieces, because they rotate as a whole. Glue cloth to the pole only if the attached edge shows a seam.
- **Plant** (flower, sapling, vine): `Plant` (stem, leaves, tendrils, grass as one fused part) behind a rigid `Head` (bloom). Bones: `Base` (root at the ground, static) → `GrassL`/`GrassR` (static, they pin the grass) and `Stem1 → Stem2 → Stem3 → Head`, with `Leaf` and `Curl` on the stem segment they grow from. `part_bones`: Plant takes every bone but `Head`; Head takes `[Head]`. `exclusive [Head, Plant]` and `extend Plant under Head` at ~30 px (the tilt pivot sits at the stem top).
- Scaffold with `--kind object`, which gives a static subject: no Rigidbody, preview HUD only.

## Anything else
Break the subject into the pieces that move independently. Pick the closest plan above and adapt it. If the template splitter can't express the cut or the assignment the art needs (for example a curved cut or a part defined by a colour range plus a region), extend that subject's `split_<name>.py`. That copy belongs to the subject.

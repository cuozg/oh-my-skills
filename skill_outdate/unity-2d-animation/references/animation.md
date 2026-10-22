# Creating animations (`<Name>ClipFactory`)

A clip is a `Spec(name, length, loop, Motion)` returned from `Specs()`. A `Motion` maps bone names to offsets over normalized time `s` (0..1):
- `rot[bone]` holds degrees added to the rest angle.
- `pos[bone]` holds units added to the rest position, in parent space.
- `scale[bone]` holds a Vector2 multiplier.

The engine keys **every bone in every clip** and holds the bones without a motion at rest, so no pose leaks between states. Animator parameters and transitions go in `Wire()`.

This file is the recipe book: grow it whenever a new animation type is built and verified.

## Conventions
- **Angles:** + is counter-clockwise. With the subject facing right, a downward-pointing limb rotated + swings **forward**, and a negative fold bends the lower segment **back**.
- **Loops** (`loop: true`): the engine closes the loop, so the last key equals f(0). Use whole-number frequencies (`Wave(s, amp, phase, freq: 2)`), because a fractional frequency jumps at the wrap.
- **One-shots** (`loop: false`):
  - Start at the rest pose when several states can enter the clip: envelope 0 at s = 0, using `Ease` or `Bump`.
  - End at rest when the clip hands back to locomotion: envelope 0 at s = 1, using `Bump`.
  - A held pose (`Ease(s, 0.6f)`) suits phases that last as long as physics decides, such as a rise before the fall.
- **Root motion stays off.** Physics moves the subject, so clips only move bones *relative to* the root.
- **Amplitude ceilings:** the seams only hide what the overpaint covers. Start small, capture, and raise. Known limits (quadruped):
  - thigh swing ≤ 32°
  - front shin tuck ≤ 55°
  - root dip ≤ 0.04 u

## Helpers
| Helper | Shape | Use |
|---|---|---|
| `Wave(s, amp, phase, freq)` | sine | breathing, sway, bob, flaps |
| `Lift(s, phase)` | 0 in stance, a bump during swing | knee/foot fold in gaits |
| `Ease(s, end)` | 0 → 1, then held | entering a held pose |
| `Bump(s, delay, skew)` | 0 → 1 → 0 | impacts, squashes, flicks |
| `Limb(m, upper, lower, end, phase, swing, fold, endFold)` | one leg/arm cycle | walk, run |
| `Chain(m, bones, baseAmp, growth, lag, offset, freq)` | follow-through | tail, hair, cloth, antenna |
| `Hold(m, w, (bone, deg)…)` | static pose × envelope | leap, crouch, open pose |

## Recipes
Lengths and amplitudes are starting points. Tune them against captures (see quality.md).

### Idle (loop, 2–3 s)
- Breathing bob on the root: `pos[Root] = (0, ±0.5% of height)` with `Wave`.
- Spine ±0.5–1°, and a head nod lagging by 0.6 rad.
- Chains sway 3/5/7° with a lag of 0.6–0.7.
- **Keep the feet planted:** counter-rotate the legs attached to a rotating spine by −(spine offset).

### Walk (loop)
- **Quadruped:** 4-beat lateral walk with phases BackL 0, FrontL .25, BackR .5, FrontR .75. Use `Limb(swing 25, fold 35, endFold 20)`, a double bob (`freq 2`, ~0.012 u), and spine, head and chain at `freq 2`.
- **Biped:** legs at 0 / .5. Arms swing opposite the same-side leg, `Wave(±15–20°)` with the forearm trailing. Add a small double bob and spine counter-twist.
- **Length:** match foot speed to `walkSpeed`, using ground speed ≈ 2·L·sin(swing) / (0.5·T) with L = leg length. For example, L 0.85 u at 25° gives T ≈ 0.7 s for 2 u/s. Shorten T or raise the swing when the feet slide.

### Run (loop)
- **Quadruped gallop:** phases BackL 0, BackR .1, FrontL .5, FrontR .6. Use `Limb(swing 32, fold 45, endFold 22)`.
  - Suspension bob on the root, `Wave(0.045, phase .25)`.
  - Rocking pitch on the root, ±3°.
  - Neck stretched forward (−10°), head counter-rotated (+6°) to keep the face level.
  - Tail streams back (negative offsets).
- **Biped:** legs 0 / .5 with a bigger swing (35–45°) and a deeper fold. Lean the spine forward 8–12°, pump the arms ±35°, and use a single bob per stride.
- **Length:** 0.4–0.5 s. Keep `walkSpeed` < run threshold < `runSpeed`.

### Jump: three phases, so any airtime and any ledge drop stay in sync
| Clip | Loop | Length | Pose |
|---|---|---|---|
| `JumpRise` | no | 0.35–0.45 s | `Ease(s, 0.6)` into the leap pose, then hold. **Quadruped:** root +12° nose-up, push-off legs extended back (−24…−30°), front legs tucked (thigh +20…25°, shin −48…−55°), neck −8°, head +6°, tail streams. **Biped:** knees tucked, arms up, spine slightly back. |
| `Fall` | yes | 0.5 s | Held pose plus `Wave` flutter: root −6° nose-down, front limbs reach forward for the landing, back limbs tuck, chains lift (negative offsets) and flutter with lag. |
| `Land` | no | 0.2–0.3 s | `Bump` squash. The root dips ≤ 0.04 u while the legs flex (thigh forward, shin back) so the feet stay on the ground. The head nods down and the chain flick lags. It ends exactly at rest. |

Wiring in `Wire()` (the controller writes these parameters):
```csharp
Param(ctrl, "Jump", AnimatorControllerParameterType.Trigger);
Param(ctrl, "IsGrounded", AnimatorControllerParameterType.Bool, defaultBool: true);  // spawn standing
Param(ctrl, "VelocityY", AnimatorControllerParameterType.Float);
FromAny(ctrl, states["JumpRise"], 0.08f).AddCondition(AnimatorConditionMode.If, 0, "Jump");
var fall = FromAny(ctrl, states["Fall"], 0.25f);              // apex of a jump OR walking off a ledge
fall.AddCondition(AnimatorConditionMode.IfNot, 0, "IsGrounded");
fall.AddCondition(AnimatorConditionMode.Less, -0.1f, "VelocityY");
foreach (var air in new[] { states["JumpRise"], states["Fall"] })
    Link(air, states["Land"], 0.05f).AddCondition(AnimatorConditionMode.If, 0, "IsGrounded");
AfterEnd(states["Land"], states["Idle"]).AddCondition(AnimatorConditionMode.Less, 0.1f, "Speed");
// + Land -> Walk (0.1 < Speed < run threshold), Land -> Run (Speed > run threshold)
```

### Locomotion wiring (Idle / Walk / Run)
`Param(ctrl, "Speed", Float)`. Then add `Link(Idle→Walk)` with Speed > 0.1, `Link(Walk→Idle)` with Speed < 0.1, `Link(Walk→Run)` with Speed > 3 and `Link(Run→Walk)` with Speed < 3, each with a 0.15 s blend.

### Action one-shot (attack, interact, emote)
- Split the timing into anticipation (~30%, moving away from the action), action (~20%, fast with overshoot) and recovery (~50%, settling back to rest).
- Use a trigger parameter: `FromAny(...)` with the trigger condition, then `AfterEnd` back to Idle.

### Hit / hurt (one-shot, 0.25–0.35 s)
`Bump` recoil: the root tilts away from the hit by 6–10°, the head snaps the same way, and the chains whip with lag. It ends at rest.

### Fly / hover (loop)
- Wing flap `Wave(±35–50°)` at 2–4 Hz, with the wing mid and tip lagging.
- Body bob in the opposite phase to the downstroke.
- Legs tucked with `Hold`.

### Squash and stretch (limbless, bouncy props)
- Scale the root: `scale[Root] = (1 + a·w, 1 − a·w)` to keep the area constant, with a ≤ 0.12.
- Keep the Root head at the base so the subject stays on the ground.
- Pair it with a `pos` hop at the stretch peak.

### Object
- **Hinge open/close** (one-shot, 0.4–0.6 s): the hinge bone rotates to its open angle with ~8% overshoot, then settles (`Ease` plus a small decaying `Wave`). Use a trigger or bool parameter.
- **Idle loops:**
  - Flag or cloth: `Chain` with growing amplitude.
  - Floating item: `pos` bob plus a ±3° tilt.
  - Pulse: `scale` ±4%.
  - **Plant sway** (verified on a flower, 2 s loop, both gates pass): `Chain(Stem1..3, 1.2°, +0.6°, lag 0.5)`. The head lags and counter-tilts, `Wave(−2.5°, phase 0.15)`, with a breath pulse `scale[Head] = (1 + Wave(0.015, freq 2), 1 − Wave(0.01, freq 2))`. Leaf flutters with `Wave(3°, phase 0.3, freq 2)` and the curl with `Wave(2.5°, phase 0.5)`. `Base` and the grass bones stay at rest, so the plant stays planted. The head travels ~5% of the plant height, and the 30 px stem overpaint under the head covers it.

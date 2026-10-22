---
name: unity-2d-animation
description: Turn one flat 2D image (line art, sticker, cartoon) of a character, creature or object into a layered, rigged, animated, testable Unity subject with the 2D Animation package (overpainted layer split, bones and weights, SpriteSkin, procedural clips, Animator, test scene), driven through the Unity CLI. Use when the user asks to cut an image into layers or parts, rig or skin a 2D sprite, make an idle/walk/run/jump/attack/open animation for a 2D character, creature or prop, add or tune a clip on a subject rigged this way, or fix white gaps, see-through holes or wrong overlap in 2D skinned animation.
---

# Unity 2D Animation: image → layered, rigged, animated, tested subject

One **subject** (a character, creature, object or prop) per folder. Its own copies of the scripts carry it through six phases: **export → layer → rig → animate → verify and test → report**. The skill holds only the workflow and the **templates**. Every subject gets per-subject copies, and you edit those copies whenever the template doesn't fit the art. Quality is held by two automated **gates** (no white gaps, no see-through holes, no wrong overlap). See `references/quality.md`.

```
Assets/<Name>/
  Source/<name>.png                       exported source image
  Tools~/split_<name>.py, <name>.json     subject's splitter + config, debug/ (Unity skips "~" folders)
  Art/Parts/*.png, Art/rig.json           layers + rig data (split output)
  Scripts/Editor/<Name>RigBuilder.cs      import, bones, weights, SpriteSkin, Animator, prefab, test scene
  Scripts/Editor/<Name>ClipFactory.cs     clips (Specs) + Animator wiring (Wire); baking engine
  Scripts/Runtime/<Name>DebugHUD.cs       clip preview + PoseAt/KeyBackground hooks for the gates
  Scripts/Runtime/<Name>Controller.cs     characters only: move / run / jump, ground check
  Scripts/Runtime/CameraFollow2D.cs
  Animations/  Prefabs/  Physics/  Scenes/<Name>Test.unity
```

| Skill file | Read it when |
|---|---|
| `references/export.md` | Phase 1. Checks whether the image fits, and how to prepare it |
| `references/body-plans.md` | Phase 3. Parts, order, bones and glue for biped, quadruped, winged, limbless or object subjects |
| `references/config-schema.md` | Phase 3. Every config key, the assign rules, and the *Labelling* fixes for a misread `labels.png` |
| `references/animation.md` | Phase 5. Recipes per animation type, wiring snippets, amplitude ceilings |
| `references/quality.md` | Phases 3 and 6. The gates and the defect → fix tables |
| `references/pitfalls.md` | Before driving the Editor. Verified API facts and CLI/Play-mode gotchas |
| `scripts/new_subject.py` | Scaffolds the subject folder from `templates/` |
| `scripts/check_split.py`, `scripts/check_frames.py` | Gate 1 and gate 2 |

## Entry points
| The user has… | Start at |
|---|---|
| a new image | Phase 0 → all phases |
| a subject whose parts need re-cutting | Phase 3 (re-split, then rebuild in phase 4) |
| a rigged subject that needs a new or tuned clip | Phase 5 |
| a visual defect (gap, wedge, overlap) | Phase 6 to reproduce it, then the phase the quality.md fix table points to |

Track each phase as a todo. A phase is done only when its **done when** holds.

## Phase 0: Preflight
1. Run `unity status`; the project must show `ready`. If MCP tools are missing from the session, use the Unity CLI and tell the user.
2. Check `Packages/manifest.json` for `com.unity.feature.2d` (2D Animation and Sprite) and URP with the 2D Renderer. Characters also need `com.unity.inputsystem`.
3. Run `python3 -c "import numpy,scipy,PIL"`.
4. Confirm the scope with the user:
   - subject kind (character or object)
   - body plan
   - parts list
   - clip list, and which clips loop
   - for characters: controls (move, run, jump)

**Done when:** the Editor is ready, the packages are present, and the user has confirmed the scope.

## Phase 1: Export the source image
Check the image against the fit checklist in `references/export.md` and prepare it: background, view, facing, size. Art that fails the checklist (painted, shaded, photo) gets the manual-layer route described there.

**Done when:** every row of the checklist holds for the image.

## Phase 2: Scaffold
1. Run `python3 -I <skill>/scripts/new_subject.py --name <Name> --kind character|object --image <png>` from the project root.
2. Refresh, recompile, and poll `recompile_status` (commands in pitfalls.md).

**Done when:** the folder exists and the console shows no compile errors.

## Phase 3: Layer
1. **Inspect:**
   1. Run `python3 -I Assets/<Name>/Tools~/split_<name>.py inspect --image Assets/<Name>/Source/<name>.png --debug Assets/<Name>/Tools~/debug`.
   2. Read `labels.png` and `components.txt`. Every piece must be one clean region. If shading reads as outline, a fill leaks into the background, or negative space is labelled as a fill, set the matching key from *Labelling* in config-schema.md and re-run with `--config Assets/<Name>/Tools~/<name>.json`.
   3. Re-run with `--crop x0,y0,x1,y1` around every junction where parts share one fill. The grid is 20 px, with a red line every 100 px.
   4. Measure the cut endpoints, seeds and bone landmarks from the crops.
2. **Config:** fill `Tools~/<name>.json` using `body-plans.md` and `config-schema.md`.
3. **Split:** run `split --image … --config Assets/<Name>/Tools~/<name>.json --out Assets/<Name>`.
4. **Gate 1:** `check_split.py`, plus the visual checks in quality.md. Iterate on the config until it passes.
   - When the template splitter can't express what the art needs, edit `split_<name>.py` (it's the subject's copy) and note the change in its docstring.

**Done when:** the split printed no `WARN unassigned` lines, gate 1 prints `PASS`, and the composite, part map and contact sheet all look right.

## Phase 4: Rig
1. Build with the scaffolded `Rest` clip: `unity command eval '<Name>.EditorTools.<Name>RigBuilder.Build(); return "ok";'`.
   - The build refuses to run while the open scene has unsaved changes. Ask the user before saving or discarding them.
2. Read the console. It must show `Build finished` and no bindpose mismatch or SpriteSkin state other than Ready.
3. Run gate 2 on a `Rest` frame. It must pass and match `composite_bones.png`.

**Done when:** the build is clean and the Rest frame passes gate 2.

## Phase 5: Animate
1. In `<Name>ClipFactory.cs`, write one `Spec` per clip in `Specs()` (the first one is the entry state) and the parameters and transitions in `Wire()`. Follow `references/animation.md`.
2. Characters: keep the controller's speeds consistent with the Animator thresholds (walkSpeed < run threshold < runSpeed).
3. Recompile and rebuild (phase 4, step 1).

**Done when:** every clip in the agreed list exists as a state, the transitions match the agreed behaviour, and the build is clean.

## Phase 6: Verify and test
1. Run `editor_play`, then turn on autotick (it must come after play). Confirm `Time.frameCount` advances between two evals; the HUD keeps play ticking without focus, so leave the user's window focus alone (pitfalls.md).
2. **Gate 2 on every clip** (command block in quality.md):
   1. Capture `Rest_0` first. `KeyBackground(true)` fixes the framing on that first call for the whole session.
   2. `PoseAt(clip, t)` at each sample time, in an eval that returns `isPlaying`.
   3. Capture with `capture_game_view --source camera`.
   4. Run `check_frames.py … --rest Rest_0.png`.
   5. Look at the frames for wrong overlap.
3. **Behaviour (characters):** log the state sequence with an `EditorApplication.update` logger (pitfalls.md) while driving the controller through eval. Check:
   - Idle → Walk → Run as the speed changes
   - Jump → Fall → Land → back to locomotion
   - walking off a ledge goes to Fall
   - Objects: each trigger plays its clip and returns.
4. Tune using the quality.md tables, rebuild, and repeat until both gates pass on every clip.
5. Clean up:
   - `KeyBackground(false)`
   - stop Play mode
   - turn autotick off
   - delete `Assets/Temp` with `AssetDatabase.DeleteAsset`

**Done when:** gate 2 prints `PASS` for every sample of every clip, no capture shows wrong overlap, every behaviour sequence matches the agreed scope, and cleanup is done.

## Phase 7: Report (leave the test scene open)
```
Open Assets/<Name>/Scenes/<Name>Test.unity → Play.
Controls: <move/run/jump keys, or "HUD buttons only"> · HUD: one button per clip (in-place preview) / Live
Built: <parts> parts · <bones> bones · clips <Name> <T>s loop|once, … · Animator: <params + key transitions>
Gates: split PASS · frames PASS on <N> samples across <clips>
Verified: <state sequences seen, what captures showed>
Not verified: <e.g. held-key input; ask the user to confirm by hand>
Regenerate: python3 -I Assets/<Name>/Tools~/split_<name>.py split … → eval <Name>.EditorTools.<Name>RigBuilder.Build()
Changed from template: <edits made to this subject's script copies, or "none">
```
If the subject needed a template change that every subject would benefit from, offer to upstream it into `templates/`. Offer the same for a new animation type that passed both gates: add it to `references/animation.md`.

## Why the design is this way
- **Per-subject copies:** art varies more than code can anticipate. Editing one subject's splitter or builder never risks another subject.
- **Overpaint is drawn to join the old part, not just fill the hole:** a hidden area shows the moment a joint bends, so the drawn part must look like the part itself: same smooth fill colour, outline continuing around it, no seam left where old pixels meet new ones (`overpaint()` in the splitter).
- **Glue limbs to the body bone:** a rotating cut swings its hidden overpaint out from under the body as a white wedge. Blending the weights from the anchor bone into the limb makes the joint bend instead.
- **Bottom-left pivot, with the part GameObject at `offset`:** every part shares one subject space, so one skeleton binds every SpriteSkin with no per-part maths.
- **The Animator sits on the flipped `Visual` child, and every bone is keyed in every clip:** facing flips never touch physics, and no pose leaks between states.
- **Rig data goes through the sprite data providers** (the Skinning Editor has no API). The result still opens and edits in the Skinning Editor.

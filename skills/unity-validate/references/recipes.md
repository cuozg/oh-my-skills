# Validate Recipes

Pick the recipe by **target**. A task can use several (`mixed` = ui-prefab + logic). Each case's
`Method` names the tool that produced its evidence. Command details are in `tools.md`.

Every recipe starts the same way:
1. Compile.
2. Take the console **baseline** from the task file (recorded by the implementer before the
   change). With no task file, record it now.
3. Install the tools.

Every recipe ends the same way: the console shows nothing beyond the baseline.

## Feature: ui-prefab

1. **Tree:** run `validate_prefab_tree` for every changed prefab. Check it against the
   requirement: the expected nodes and components exist, there is no `MissingScript!`, and the
   `[inactive]` flags are intended.
2. **Static shot:** run `validate_prefab_shot` at the design resolution. This shows the
   serialized state. A panel prefab with no CanvasScaler of its own renders at scale 1, so pass
   the game canvas's reference resolution as `--width` / `--height`.
3. **In-game shot:** use this for anything driven by data, animation, or interaction:
   - Run `editor_play`, then open the screen through the game's own entry point: a
     `validate_click` path, or an `eval` that calls the real open method.
   - Wait for the open animation to finish.
   - Run `validate_scene_tree --root <path>` and `validate_game_shot`.
   - For each state (pressed, disabled, empty, filled): drive it, then shot it.
4. **Design compare:** see the section below.

Method values: `Tree`, `Prefab shot`, `Game shot`.

## Feature: logic

1. **Unit tests:** the implementer wrote them, named after the case IDs (`T1_…`). Run them with
   `run_tests --filter <Class>`. With no Editor, use
   `unity test <project> --mode EditMode --filter <Class> --format json`. Exit code `8` means
   tests failed, `6` means the run never finished.
2. **Prove the test bites.** The working tree holds the implementer's uncommitted change, so
   never use `git checkout` or `git stash` here:
   - Copy the file to `/tmp/` and record its `shasum`.
   - Break the behavior under test (invert a condition, return early).
   - Rerun, and confirm the test goes red.
   - Copy the backup back, and confirm the `shasum` matches.
   A test that can't fail is not evidence.
3. A logic case with no unit test is `❌` with the note `no test`. Report it to the implementer;
   don't write the test yourself.
4. **Regression (`R*`):** run every test in the touched assemblies.

Method values: `Unit`, `PlayMode test`.

## Feature: gameplay (works in the game)

Use this when the requirement is a behavior the player sees, beyond any single unit:
1. Run `editor_play` and reach the feature through the game's real flow. Use `validate_click` for
   UI, `simulate_pointer` / `simulate_key` for world input, or `eval` for a documented entry point.
2. Capture state before and after each action. Use `validate_probe` for values (coins,
   level, flags), `validate_scene_tree` for spawned or opened objects, and `validate_game_shot`
   for what the player sees.
3. Check the console for errors during the flow (`console --level warn` with the `since` cursor).
4. Run `editor_stop`.

Method value: `PlayMode run`.

## Bug: reproduce (for unity-debug, before a fix)

1. Turn the report into steps with an **observable failure**: a value, an exception, a wrong
   visual, or a missing object.
2. Pick the narrowest method that shows it:
   - **Unit test** (`Unit`), when the failure lives in logic that can be called directly. The
     validator writes this **repro test** (`Bug_<name>_Repro`) in the project's test assembly and
     keeps it: it is evidence, not a fix, and it becomes the regression test. The test must go red.
     Record its path in the report.
   - Otherwise **Play Mode** (`PlayMode run`): drive the steps with `validate_click` / `simulate_*` /
     `eval`, then capture the failure with `validate_probe`, a console excerpt, or `validate_game_shot`.
   - A compile error needs no repro: the compile output is the evidence (`🔴 Reproduced`).
3. Run it twice. Stable failure → `🔴 Reproduced`. Record the exact method, so the fix check can
   reuse it.
4. No failure after a real attempt → `⚪ Not reproduced`. List the steps tried and what was
   observed. unity-debug stops and asks the user for more detail; nobody guesses a fix.

## Bug: verify the fix (after a fix)

1. Rerun the **same** method recorded in the repro report. `Unit` reruns the repro test, and
   `PlayMode run` replays the same steps. The failure must be gone → `🟢 Fixed`.
2. Run the regression cases around the fix: the touched assembly's tests and the nearby flow.
3. Failure still present → `❌ Still reproduces`, with the new evidence.

## Image (generated or imported)

1. Run `validate_texture` on each image. Compare every requirement against the facts:
   - Size, and power-of-two when required.
   - Transparent background (`transparentPct` > 0, opaque bounds inside the canvas,
     `touchesEdge = false` when padding is required).
   - Sprite settings: type, PPU, pivot, and 9-slice border for stretchable UI.
   - Platform compression and max size.
2. **Look at the image** (read the PNG) and judge the visual requirements: subject, style, color,
   and readable text. Describe what you see in one line per requirement.
3. When the image is used in UI, place it: run `validate_prefab_shot` on the prefab that uses it,
   or `validate_game_shot` in Play Mode.

Method values: `Texture`, `Visual`, `Prefab shot`.

## Design compare (any UI change with a design source)

1. Save the design as `<assets-dir>/design.png`. Export the Figma frame via MCP, or ask the user
   for an image.
2. Capture each state the design shows, at the design's resolution.
3. Compare layout, spacing, size, color, font, text, states, and safe area. List each mismatch as
   `mismatch: <what>`. Validation reports mismatches; fixing them is the implementer's job.
4. No design source → `N/A – no design provided`.

## Cannot validate

When a case can't run (it needs a device, a store, a server, a real account, platform hardware, or
real multi-touch):
- Mark the case `⚠️`, and put the reason plus the manual steps in Evidence.
- Set its Method to `Manual`.
- The verdict becomes `🟠 Not validated`.

An unreachable Editor isn't a valid reason on its own. Ask the user to open it first.

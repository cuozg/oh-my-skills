# Validate Tools

Pass `--caller plugin --skill unity-validate` on every `unity command`.

## Built into the Pipeline package

Confirm names with `unity command --query <name>`. Names and groups vary by package version.

| Command | Use |
|---|---|
| `console --level warn --tail 50` / `console_status` | Console baseline, then the post-change check |
| `recompile` → poll `recompile_status` until `completed` | Compile check |
| `run_tests --mode editor\|playmode --filter <Class>` | Unit tests in the live Editor |
| `editor_play` / `editor_stop` | Enter and exit Play Mode |
| `simulate_pointer` / `simulate_key` | Raw input (Input System projects), for non-UI gameplay |
| `eval "<C#>"` | Call the game's real entry point (e.g. open a popup), read-only probes |

The built-in `screenshot` renders the camera only. **It misses Screen Space Overlay UI**: on
Pipeline 0.9 it captured 0 of 160000 red pixels from an overlay panel. Use `validate_game_shot`.

## Skill tools: `assets/UnityValidateCommands.cs`

| Command | Mode | Evidence it gives |
|---|---|---|
| `validate_prefab_tree --path <prefab>` | any | Prefab tree: names, components, `[prefab: X]`, `[inactive]`, `MissingScript!` |
| `validate_scene_tree --root <A/B>` | any | Live tree from the open scenes, prefab stage, or Play Mode (including DontDestroyOnLoad) |
| `validate_prefab_shot --path <prefab> --output <png> --width W --height H` | GPU | Isolated render. UI is sized the way its CanvasScaler sizes it on a W×H screen. A fixed-size root is centered, and a stretched root keeps its layout |
| `validate_game_shot --output <png> [--width W --height H] [--camera <path>]` | GPU | What the player sees: every screen camera by depth (a world camera plus a UI camera), **plus** overlay UI drawn on top, with nested sorting canvases kept in order. Every canvas is restored afterwards |
| `validate_click --path <A/B/Btn>` | Play Mode | Clicks like a player: an EventSystem raycast at the element's center, then enter → down → up → click (so EventTrigger and PointerDown handlers fire too). It fails when there's no EventSystem, or the target is inactive, non-interactable, has no handler, or is covered (including by a child with its own handler) |
| `validate_probe --path <A/B> --component <Type> --member <a.b>` | any | A live field or property value (private `[SerializeField]` included). Output is culture-invariant: floats round-trip, Unity structs print to 4 decimals, enums by name. Leave `--member` empty to list members |
| `validate_texture --path <image>` | any | Takes `Assets/` and `Packages/` paths, or any file. Real pixels: size, transparency %, opaque bounds, `touchesEdge`. Plus import settings: type, sprite mode, PPU, 9-slice border, pivot, max size, compression, mipmaps, platform overrides. For PSD/TGA/EXR it reports import facts only |

`validate_probe` runs property getters. Prefer fields, and avoid getters with side effects
(`Renderer.material` instantiates a material; use `sharedMaterial`).

## Install (once per project)

1. Copy `assets/UnityValidateCommands.cs` to `<project>/Assets/Editor/UnityValidate/`.
2. If an asmdef covers that folder, it must reference `Unity.Pipeline.Attributes` and be Editor-only.
3. Run `recompile`, then confirm `unity command --query validate_` lists all seven commands.
4. Tell the user the file was added and that it's Editor-only, so it never ships in builds. Ask
   before committing it.

With no live Editor, run the same commands through `unity run <project> --command validate_texture -- --path <file>`.
This needs the project closed in the GUI Editor. Errors come back as `COMMAND_FAILED` with the
message.

## Gotchas (verified on Unity 6000.6, Pipeline 0.9, Metal)

- Shots need a GPU: a live Editor, or batch mode **without** `-nographics`. Under `-nographics`
  they throw instead of writing a blank frame. Trees, probe, texture, and click work in every mode.
- Write evidence to `Docs/...`, never to the project's `Temp/` folder: Unity deletes `Temp/` when
  the Editor exits.
- `validate_prefab_shot` shows serialized state. For anything driven by data or animation, use
  Play Mode + `validate_game_shot`.
- 3D prefab shots render lit in flat white: they prove framing and silhouette, not materials.
- URP: overlay cameras in a stack are skipped (their base camera renders them), and every base
  camera clears the screen, exactly as it does in the game.

## Validate the tools

Run this when the tools are first installed in a project, after a Unity or Pipeline upgrade, or
when a result looks wrong:
1. Copy `assets/UnityValidateSelfTest.cs` next to `UnityValidateCommands.cs`.
2. Run `unity run <project> -- -executeMethod UnityValidateSelfTest.Run -validateOut /tmp/uval`.
   Run it a second time with `-nographics` to check the no-GPU path.
3. Read `/tmp/uval/result.txt`: every line must be `PASS` (or `SKIP` with a reason) and the last
   line `FAILURES=0`. That's 28 checks with a GPU and 25 without.
4. Check the Play Mode paths of `validate_click` (EventSystem occlusion, the world-space camera
   fallback, the press sequence):
   - Copy `assets/PlayModeTests/` to `<project>/Assets/UnityValidatePlayModeTests/`.
   - Run `unity test <project> --mode PlayMode --filter ClickPlayModeTests`.
   - The test must pass.
5. Delete both harnesses, along with any `test-results.xml` the run wrote. Record the result in
   `Docs/Validations/tools-selftest.md`: date, Unity version, Pipeline version, pass counts.

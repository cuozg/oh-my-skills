# Verified facts & pitfalls (Unity 6000.0, 2D Animation 10.2, 2D Sprite, URP 17, Unity CLI)

## Skinning data from code (no Skinning Editor API)
- The `ISpriteEditorDataProvider` interfaces live in `UnityEditor.U2D.Sprites` (`Unity.2D.Sprite.Editor`, autoReferenced), so no asmdef is needed.
  - Call `InitSpriteEditorDataProvider()` before any Get or Set.
  - The Set calls are in-memory only. `Apply()` writes the importer, and `SaveAndReimport()` then bakes the data.
- **SpriteBone coordinates:**
  - A **root** bone's position is in sprite-**rect** pixels with the origin at the rect's bottom-left. The importer subtracts the pivot itself.
  - A **child** bone's position is in pixels, local to the parent's rotated frame. The child's rotation is local too.
  - Depth is stored in `position.z`.
- **Set `rotation = Quaternion.identity` or a real value.** `default(SpriteBone).rotation` is (0,0,0,0) and breaks the bindposes.
- **Vertex positions** (`Vertex2DMetaData.position`) are in rect pixels with the origin at the bottom-left.
- **`BoneWeight.boneIndexN`** indexes the sprite's own bone list. SpriteSkin rejects a mesh if **any** of the 4 indices is out of range, even one with weight 0, so pad unused slots with index 0.
- **Check the import:** after reimport, `sprite.GetBindPoses().Length` must equal the bone count. In `eval`, call extension methods through their class: `UnityEngine.U2D.SpriteDataAccessExtensions.GetBindPoses(sprite)` (and `GetBones`).
- **SpriteSkin binding:**
  - Call `SetRootBone(t)` and then `SetBoneTransforms(Transform[])` in the sprite's bone order. It returns `SpriteSkinState`; anything other than `Ready` means nothing deforms.
  - At rest, each bone's pose relative to the SpriteSkin transform must equal the inverse bindpose. With a bottom-left pivot and the part GameObject at `offset`, a skeleton built in character space satisfies this automatically.
- **`maxTextureSize` must be ≥ the largest part.** Otherwise `definitionScale` ≠ 1 and the bones end up scaled.

## Scene and runtime
- **URP 2D Renderer:** Sprite-Lit materials render black without a light. Add a `Light2D` and set `lightType = Light2D.LightType.Global`.
- **Flip a child, not the root:** put the bones, sprites and Animator on a child `Visual` and flip its `localScale.x`. `SpriteRenderer.flipX` does not mirror skinned bones, and flipping the root would also flip the collider.
- **Use a frictionless material:** a `PhysicsMaterial2D` with friction 0 on the capsule stops the character sticking to walls. Freeze Z rotation.
- **Unity 6 API:** use `Rigidbody2D.linearVelocity`, not `velocity`.
- **Write every bone in every clip,** with rest-pose constants where nothing moves, so no pose leaks between states. The clip factory engine does this.
- **Rotation curve names:** use `localEulerAnglesRaw.x/y/z` for rotation and `m_LocalPosition.*` for position.

## Editor automation through the Unity CLI
- Run `unity status` first. If the Editor exposes `eval`, drive everything with `unity command eval '<C#>; return "x";'`. `unity command <unknown>` prints the full list of commands.
- **Writing scripts can restart or disconnect the Editor** (domain reload, sometimes a full relaunch with a new PID). When a command fails with "No Unity Editor instances found", poll `unity status` until it shows `ready`, then refresh and recompile again.
- **New scripts don't compile until a refresh:**
  1. `eval 'UnityEditor.AssetDatabase.Refresh(UnityEditor.ImportAssetOptions.ForceSynchronousImport); return "";'`
  2. `recompile`
  3. Poll `recompile_status` until it reports neither `compiling` nor `triggered`.

  A single Refresh can miss files written moments before it. `recompile` itself can fail with a network error while the domain reloads; that's expected, so keep polling `recompile_status`.
- **Read errors from the console:** `unity command console --format json`, then filter on `level != "log"`. The MCP `read_console` takes `types` as a JSON list (`["error","warning","log"]`), never a string.
- **Never call `EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo`.** Its modal dialog blocks CLI runs. Refuse to build when the open scene is dirty instead.
- **`capture_game_view --save_path` resolves under `Assets/`.** For example, `Temp/Captures/x.png` is written to `Assets/Temp/Captures/x.png`. Use `--source camera` for consistent framing (it omits IMGUI), and delete `Assets/Temp` when done via `AssetDatabase.DeleteAsset`; shell `rm` may be denied.
- **Play mode while the Editor is unfocused:** the player loop freezes completely (`Time.frameCount` stops, and SpriteSkin stops re-deforming, so captures go stale while each still looks valid). The HUD template sets `Application.runInBackground = true` in `Awake`, which keeps play ticking (~10 fps) without focus. Run `set_autotick --enable true --interval_ms 0 --persist false` *after* `editor_play` (entering Play mode reloads the domain, which drops autotick), and turn it off afterwards. Leave the user's window focus alone.
- **Asset writes can drop Play mode:** `AssetDatabase.DeleteAsset`/`Refresh` while playing can trigger a reload that exits Play, so captures from then on silently show the edit-mode scene. Capture each run into a fresh folder and delete `Assets/Temp` only after `editor_stop`.
- **Guard runtime-only changes with `isPlaying` in the same eval.** If Play has dropped, a "temporary" change such as `SetActive(false)` lands in the edit-mode scene instead and is easy to miss, because a scripted change doesn't mark the scene dirty.
- **Scope lookups to the subject:** `GameObject.Find("Visual")` returns the first match, which is another subject's when the scene holds several. Use `GameObject.Find("<Name>").transform.Find("Visual")`.
- **Stale-capture check:** when a set of captures meant to differ (different clips or times) produce identical gate findings or identical images, frames weren't ticking. Confirm that `Time.frameCount` advances between two evals, then recapture.
- **The first frame after an `eval` can hitch** (up to `maximumDeltaTime`, 0.33 s): physics runs many steps in one frame while the Animator advances once. Measure state sequences with an `EditorApplication.update` logger that starts a few frames *before* the action it times.
- **Clip previews:** `AnimationPlayableUtilities.PlayClip(animator, clip, out graph)` overrides the Animator Controller while the graph lives. `graph.Destroy()` hands control back. The HUD template's `Preview`, `PoseAt` and `Live` are built on this.
- **Simulated input is flaky:** `simulate_key` events are reset by the Input System's `ResetAndDisableNonBackgroundDevices` and `PointersAndKeyboardsRespectGameViewFocus` whenever focus flickers. To check clips deterministically, use the HUD's `PoseAt(clip, t)` through eval. Treat simulated-key results as indicative only, and ask the user to confirm held-key combos (e.g. Shift+D) by hand.
- **Subagents** started without an explicit `model` failed in this environment, so pass `model: "sonnet"` when delegating.

## Subject folder
- `Assets/<Name>/Tools~/` is skipped by Unity's importer (folders ending in `~`). Keep the splitter, config and debug images there, so Python and large PNGs never become assets.
- Each subject's scripts live in their own namespace (`<Name>`, `<Name>.EditorTools`), so two subjects never collide. Edit a subject's copy freely; the skill templates are only starting points.
- `HasLocomotion` in `<Name>RigBuilder` decides between a character (Rigidbody2D, capsule, `<Name>Controller`) and a static object.

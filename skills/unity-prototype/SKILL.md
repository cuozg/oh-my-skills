---
name: unity-prototype
description: >
  Build playable Unity prototypes from game ideas — analyze the concept, scope an MVP,
  break into tasks, and delegate to subagents (unity-code, unity-uitoolkit) to deliver a
  working, testable prototype scene. Bridges the gap between planning and full implementation
  by producing running code fast. Use when the user says "prototype this," "build a quick
  prototype," "make an MVP," "proof of concept," "I have a game idea," "let me test this
  mechanic," "game jam," "hack this together," "rapid prototype," or describes a game concept
  and wants to see it running. Also use when the user wants to validate a mechanic before full
  implementation, or says "can we quickly build [concept]," "I want to try out [idea]," or
  "let's see if this works." Do not use for production-quality features (unity-code), design
  documents (unity-spec), or planning without implementation (unity-plan).
metadata:
  author: kuozg
  version: "1.1"
---
# unity-prototype

Take a game idea, scope the MVP, build it, make it playable. Prototypes answer one question: "Does this feel right?" Cut everything that doesn't serve that answer.

## Example Prompts & Expected Triage

These show how the skill interprets different requests:

| # | User Says                                                                                                                                   | Triage                              | What Happens                                                                                                                                                               |
| - | ------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | *"Prototype a 2D platformer — run, jump, collect coins. I want to test if the jump feels good."*                                         | Standard MVP                        | Extract core = jump physics. BUILD: PlayerController, Collectible, ScoreManager. STUB: score text, respawn. SKIP: sprites, parallax. 4-5 scripts.                          |
| 2 | *"Puzzle game where you rotate pipe segments to connect water flow — but should I use grid snapping or free rotation?"*                  | Mechanic question → prototype BOTH | Propose two micro-prototypes: one with 90-degree snap, one with free rotation. Let playtesting decide. 3-4 scripts each variant.                                           |
| 3 | *"Open-world RPG with crafting, skill trees, weather system, branching narrative, and multiplayer co-op."*                                | Overscoped → scope reduction       | Do NOT attempt full scope. Identify the ONE mechanic the user cares most about. Offer choices: "Combat feel? Crafting loop? Exploration?" Prototype only the chosen slice. |
| 4 | *"I already have a design doc for a tower defense game. Can we quickly build something to test if the tower placement grid feels right?"* | Focused validation                  | User knows what to test. Skip brainstorming, go straight to BUILD/STUB/SKIP for grid placement. 4-5 scripts, one scene.                                                    |
| 5 | *"Mechanic idea: player leaves behind shadow clones that replay their movement after a delay. No art needed."*                            | Mechanic-first, no art              | Extract core = position recording + delayed playback. BUILD: movement, clone recorder, clone replayer. STUB: clone = sphere, level = cubes. Pure mechanic validation.      |

## Step 1 — Extract Core

Analyze the user's idea and identify:

- **Core mechanic(s)**: The 1-3 interactions that make this concept worth testing
- **Win/fail condition**: What the player tries to achieve or avoid
- **Minimum loop**: The shortest cycle of player input → system response → feedback

If the idea is vague, ask ONE question targeting the core mechanic. If clear enough, proceed — prototypes thrive on assumptions.

## Step 2 — Scope MVP ⛔ BLOCK

Split features into three buckets. Load `references/mvp-scoping.md` for detailed rules.

| Bucket          | Rule                                  | Example                               |
| --------------- | ------------------------------------- | ------------------------------------- |
| **BUILD** | Required to test the core mechanic    | Player movement, core interaction     |
| **STUB**  | Needed for flow but fake data is fine | Score as Debug.Log, health as a field |
| **SKIP**  | Not needed to validate the idea       | Save system, menus, audio, polish     |

Present the scope table to the user. **STOP. Wait for user confirmation before proceeding.** Prototype scope targets: 3-8 scripts, one scene, primitives for art.

## Step 3 — Task Plan

Break the MVP into ordered tasks. Each task maps to one skill delegation.

| Task Type                                        | Delegate To                               |
| ------------------------------------------------ | ----------------------------------------- |
| Runtime C# script (MonoBehaviour, data, manager) | `unity-code` + `unity-standards`      |
| UI screen, HUD, overlay                          | `unity-uitoolkit` + `unity-standards` |
| Scene setup, wiring, GameObjects                 | Direct (Unity MCP or manual instructions) |

**Ordering**: Core mechanic scripts (parallel) → supporting scripts → UI → scene wiring.

Create tasks via `task_create` with `blockedBy` for dependencies and `→ skill:` routing in description. Maximize parallelism — most prototype scripts are independent.

## Step 4 — Delegate

For each task, spawn a subagent with the right skill. Every delegation prompt must include:

1. **What to build** — specific script/component with clear responsibility
2. **Prototype context** — tell the agent this is a prototype, not production code
3. **Public fields** — expose tuning values as `[SerializeField]` for fast iteration
4. **Simplicity mandate** — one MonoBehaviour per concept, no DI/interfaces/events unless genuinely needed

Load `references/prototype-patterns.md` for common game-type patterns (platformer, shooter, puzzle, etc.) to inform delegation prompts.

**Prototype delegation rules:**

- Always include `unity-standards` in load_skills for coding conventions
- Prefer `MonoBehaviour` with `[SerializeField]` over services/DI
- `Debug.Log` over event systems for MVP feedback
- Hardcode values, expose as fields — no config files
- No interfaces unless two scripts share a genuine contract

## Step 5 — Wire Scene

After all scripts compile, assemble the prototype scene:

1. Create/use a scene with appropriate name
2. Create GameObjects — use Unity primitives (Cube, Sphere, Plane) or sprites
3. Attach scripts, assign references via Inspector or Unity MCP
4. Add colliders/triggers for interactions
5. Position camera to frame the action
6. Add Canvas + UIDocument for any HUD elements

**Unity MCP tools for scene wiring** (when available):

| Action | Tool |
|--------|------|
| Create/modify/find GameObjects | `Unity.ManageGameObject` (actions: create, modify, find, add_component, set_component_property) |
| Create primitives (Cube, Sphere) | `Unity.ManageGameObject` with `primitive_type` param |
| Save as prefab | `Unity.ManageGameObject` with `save_as_prefab=true` |
| Load/save/get scene hierarchy | `Unity.ManageScene` (actions: Create, Load, Save, GetHierarchy) |
| Play/pause to test | `Unity.ManageEditor` (actions: Play, Pause, Stop) |
| Verify visually (3D) | `Unity.SceneView_CaptureMultiAngleSceneView` |
| Verify visually (2D) | `Unity.SceneView_Capture2DScene` |
| Check for errors | `Unity.GetConsoleLogs` or `Unity.ReadConsole` |

For the full MCP tool decision tree, load `read_skill_file("unity-standards", "references/other/unity-mcp-routing-matrix.md")` — see **Scene Branch** and **Visual Capture Branch**.

## Step 6 — Verify & Report

1. **Compile check**: `lsp_diagnostics` on all created files — zero errors required
2. **Deliverables report**:
   - File list with one-line descriptions
   - Scene setup status (auto-wired or manual steps needed)
   - How to playtest: what to do in Play mode, what to look for
   - Known limitations and what was stubbed/skipped
3. **Next steps**: Suggest 2-3 iteration directions the prototype reveals

## Rules

- A working prototype with 3 scripts beats a broken one with 10 — cut aggressively
- Use Unity primitives (Cube, Sphere, Plane) — never hunt for assets
- No menus, save systems, settings screens, or audio (unless audio IS the mechanic)
- Hardcode values, expose via `[SerializeField]` for tuning
- One scene, flat hierarchy, minimal namespace structure
- If the idea is too big, propose a smaller version that still tests the core
- Compilation must succeed — a prototype that doesn't run teaches nothing

## Escalation

| From      | To              | When                                                            |
| --------- | --------------- | --------------------------------------------------------------- |
| Prototype | unity-plan      | User wants production-quality implementation after validation   |
| Prototype | unity-spec      | User wants a full design document before building more          |
| Prototype | unity-code      | Single script needs deeper implementation (state machine, etc.) |
| Prototype | unity-uitoolkit | UI is complex (multi-screen, data binding, custom controls)     |

## Standards

Load `unity-standards` for coding conventions when delegating implementation tasks.
Load prototype-specific references from this skill:

- `references/mvp-scoping.md` — BUILD vs STUB vs SKIP decision rules, scope targets
- `references/prototype-patterns.md` — Common patterns for platformer, shooter, puzzle, card, roguelike, rhythm, stealth, etc.
- `references/usage-examples.md` — Full prompt-to-breakdown walkthroughs (3 examples)

Load via `read_skill_file("unity-prototype", "references/<file>")`.

For MCP tool routing: `read_skill_file("unity-standards", "references/other/unity-mcp-routing-matrix.md")`.

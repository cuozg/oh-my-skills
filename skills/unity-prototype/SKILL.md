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
  implementation, or says "can we quickly build [concept]," "I want to try out [idea],\" or
  "let's see if this works." Do not use for production-quality features (unity-code), design
  documents (unity-spec), or planning without implementation (unity-plan).
metadata:
  author: kuozg
  version: "1.1"
---
# unity-prototype

Take a game idea, scope the MVP, build it, make it playable. Prototypes answer one question: "Does this feel right?" Cut everything that doesn't serve that answer.

## Step 1 — Extract Core

Identify: core mechanic(s) · win/fail condition · minimum player-input→response→feedback loop.  
If vague, ask ONE question targeting the core mechanic. If clear enough, proceed — prototypes thrive on assumptions.

## Step 2 — Scope MVP ⛔ BLOCK (Wait for Confirmation)

Load `references/mvp-scoping.md` for rules. Split into three buckets:

| Bucket | Rule | Example |
|--------|------|---------|
| **BUILD** | Required to test the core mechanic | Player movement, core interaction |
| **STUB** | Needed for flow but fake is fine | Score as Debug.Log, health as field |
| **SKIP** | Not needed to validate idea | Save system, menus, audio, polish |

Present scope table. **STOP. Wait for user confirmation.** Target: 3–8 scripts, one scene, primitives for art.

## Step 3 — Task Plan

| Task Type | Delegate To |
|-----------|------------|
| Runtime C# (MonoBehaviour, data, manager) | `unity-code` + `unity-standards` |
| UI screen, HUD, overlay | `unity-uitoolkit` + `unity-standards` |
| Scene setup, wiring | Direct (Unity MCP or manual) |

**Order:** Core mechanic (parallel) → supporting scripts → UI → scene wiring. Maximize parallelism — most prototype scripts are independent.

## Step 4 — Delegate

Every delegation prompt must include: what to build · "this is a prototype" context · `[SerializeField]` for tuning values · simplicity mandate (one MonoBehaviour per concept, no DI/events unless genuinely needed).

**Prototype rules:** `Debug.Log` over event systems · hardcode values as `[SerializeField]` fields · no interfaces unless shared contract exists · always include `unity-standards` in load_skills.

Load `references/prototype-patterns.md` for game-type patterns (platformer, shooter, puzzle, etc.).

## Step 5 — Wire Scene

1. Create scene → add primitives (Cube/Sphere/Plane) → attach scripts → assign references
2. Add colliders/triggers → position camera → add Canvas/UIDocument if needed

**Unity MCP tools:** `Unity.ManageGameObject` (create/modify/find/add_component) · `Unity.ManageScene` (Create/Load/Save/GetHierarchy) · `Unity.ManageEditor` (Play/Pause/Stop) · `Unity.GetConsoleLogs` (check errors). Full routing: `read_skill_file("unity-standards", "references/other/unity-mcp-routing-matrix.md")`.

## Step 6 — Verify & Report

1. `lsp_diagnostics` on all files — zero errors required
2. Report: file list + descriptions · scene setup status · how to playtest · known stubs/skips
3. Suggest 2–3 next iteration directions

## Rules

- Working 3-script prototype beats broken 10-script one — cut aggressively
- Use Unity primitives — never hunt for art assets
- No menus, save systems, audio (unless audio IS the mechanic)
- One scene, flat hierarchy, minimal namespacing
- Compilation must succeed — a prototype that doesn't run teaches nothing

## Escalation

| To | When |
|----|------|
| `unity-plan` | User wants production implementation after validation |
| `unity-spec` | User wants full design doc first |
| `unity-code` | Single script needs deeper implementation |
| `unity-uitoolkit` | UI is complex (multi-screen, data binding) |

## References

- `references/mvp-scoping.md` — BUILD/STUB/SKIP rules
- `references/prototype-patterns.md` — platformer, shooter, puzzle, card, roguelike patterns
- `references/usage-examples.md` — full prompt-to-breakdown walkthroughs

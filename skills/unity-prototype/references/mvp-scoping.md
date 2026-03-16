# MVP Scoping Guide

Rules for deciding what to BUILD, STUB, or SKIP in a prototype.

## The Core Test

Ask: "Can the player experience the core mechanic without this?" If yes → STUB or SKIP.

## BUILD (Implement Fully)

Things that must work for the prototype to validate the idea:

- **Player input handling** — movement, actions that define the core mechanic
- **Core interaction** — the primary thing the player does (shoot, match, build, etc.)
- **Feedback for core action** — player must SEE the result (object destroyed, score changed, block placed)
- **Fail/reset condition** — player needs to know when something goes wrong (lose health, fall off, time runs out)

**Implementation style:**
- MonoBehaviour with `[SerializeField]` fields for tuning
- Public fields for values you'll tweak in Play mode
- Simple `Update` / `FixedUpdate` loops — no state machines unless the mechanic demands it
- Direct references over events/messages — drag-and-drop in Inspector

## STUB (Fake It)

Things needed for flow but whose implementation doesn't matter:

- **Score/progress** → `Debug.Log($"Score: {score}")` or a simple TextMeshPro counter
- **Health/lives** → An `int` field + `Debug.Log` when it changes; death = `SceneManager.LoadScene(0)`
- **Enemy AI** → Move toward player or patrol between two points — no behavior trees
- **Level design** → Cubes as platforms, Spheres as collectibles, Planes as ground
- **Sound** → `Debug.Log("SFX: jump")` — no AudioSource unless testing audio
- **Particles** → Skip entirely or use a single `Debug.Log("FX: explosion at {pos}")`
- **Progression** → Hardcode a single level; no unlocks, no save, no level select
- **UI states** → Show/hide a panel; no transitions, no animations

**Implementation style:**
- Inline in the relevant script (no separate manager class)
- Hardcoded values (not from config/SO)
- `Debug.Log` for feedback that isn't visual

## SKIP (Don't Build)

Things that add zero value to mechanic validation:

- Main menu, pause menu, settings screen
- Save/load system
- Audio system (AudioManager, mixer, spatial audio)
- Particle effects, VFX, post-processing
- Camera shake, screen transitions, juice
- Analytics, leaderboards, achievements
- Multiplayer/networking (unless THAT is the mechanic)
- Localization
- Platform-specific code
- Tutorial/onboarding

## Scope Targets

| Metric | Target | Warning |
|--------|--------|---------|
| Total scripts | 3-8 | >10 means scope creep |
| Scene count | 1 | >1 means too complex |
| Build time | 1-4 hours | >4h means overscoped |
| Task count | 3-6 | >8 means split into phases |
| Art assets | 0 custom | Any custom art = wrong priority |

## Scope Negotiation

When the user's idea is too big:

1. **Identify the ONE mechanic** they're most excited about
2. **Propose a micro-version**: "What if we just test [core mechanic] with [minimal setup]?"
3. **Show what gets cut**: Present BUILD/STUB/SKIP so they see tradeoffs
4. **Offer phases**: "Prototype 1 tests movement, Prototype 2 adds combat"

Never say "this is too complex" — always offer a smaller version that still validates something.

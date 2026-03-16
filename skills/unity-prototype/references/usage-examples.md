# Usage Examples

Full prompt-to-breakdown walkthroughs showing how unity-prototype processes requests end-to-end.

---

## Example 1: "I want to prototype a card-matching memory game"

### Step 1 — Extract Core
- **Core mechanic**: Flip two cards, check if they match
- **Win condition**: All pairs matched
- **Minimum loop**: Click card → reveal → click second card → compare → match or flip back

### Step 2 — Scope MVP

| Bucket | Items |
|--------|-------|
| **BUILD** | Card grid layout (4x4), card flip on click, match detection (compare two flipped cards), flip-back on mismatch after delay |
| **STUB** | Cards = UI panels with text labels (A, B, C...), score = match count as Debug.Log, timer = Time.time displayed in corner |
| **SKIP** | Card art, flip animation, difficulty levels, leaderboard, sound effects |

**Scope target**: 4 scripts, 1 scene, 0 custom assets.

### Step 3 — Task Plan

| # | Task | Delegate To | Depends On |
|---|------|-------------|------------|
| 1 | `CardData.cs` — SO with card type/id | `unity-code` + `unity-standards` | — |
| 2 | `MemoryGrid.cs` — Spawn 4x4 grid of card GameObjects, shuffle pairs | `unity-code` + `unity-standards` | — |
| 3 | `CardFlipController.cs` — Handle click, reveal card, track two-card selection, check match | `unity-code` + `unity-standards` | T1 |
| 4 | `MatchGameManager.cs` — Track matched pairs, win condition, restart | `unity-code` + `unity-standards` | T3 |

Tasks 1 and 2 run in parallel. Task 3 depends on CardData. Task 4 depends on flip logic.

### Step 4 — Delegation prompt example (Task 3)

> **What to build**: `CardFlipController.cs` — MonoBehaviour attached to each card. On click, reveals card face (changes text/color). Tracks which two cards are currently flipped. Compares them after a short delay. If match → keep revealed. If mismatch → flip both back.
>
> **Prototype context**: This is a rapid prototype — no animations, no card art. Cards are UI panels with text.
>
> **Public fields**: `[SerializeField] float mismatchDelay = 1f;`
>
> **Simplicity mandate**: One MonoBehaviour, no events. Direct reference to `MatchGameManager` to report matches.

### Step 5 — Wire Scene
- Canvas with GridLayoutGroup (4 columns)
- 16 card GameObjects (8 pairs) as UI Button children
- Attach CardFlipController to each
- GameManager empty GameObject with MatchGameManager
- Camera framing the canvas

### Step 6 — Verify & Report
- **Playtest**: Enter Play mode. Click cards to flip. Matching pairs stay revealed. Mismatches flip back after 1 second. All 8 pairs matched = win.
- **Known limitations**: No shuffle animation, no visual feedback beyond text, no restart button (reload scene).
- **Next steps**: (1) Add card flip animation, (2) Add timer pressure, (3) Try different grid sizes for difficulty.

---

## Example 2: "Stealth game — guards patrol, player sneaks past to reach the exit"

### Step 1 — Extract Core
- **Core mechanic**: Avoid guard vision cones while navigating to an objective
- **Fail condition**: Guard sees player → detected → game over
- **Minimum loop**: Move → observe patrol pattern → time movement → reach exit

### Step 2 — Scope MVP

| Bucket | Items |
|--------|-------|
| **BUILD** | Player top-down movement (WASD), guard patrol between waypoints, vision cone check (angle + range + raycast), detection = game over, exit trigger = win |
| **STUB** | Player = green capsule, guards = red cylinders, walls = gray cubes, vision cone = Debug.DrawRay lines, exit = yellow cube |
| **SKIP** | Sound detection, hiding spots, minimap, takedowns, distractions, crouch animation |

**Scope target**: 5 scripts, 1 scene, 0 custom assets.

### Step 3 — Task Plan

| # | Task | Delegate To | Depends On |
|---|------|-------------|------------|
| 1 | `StealthPlayer.cs` — Top-down WASD movement, shift for slow/crouch speed | `unity-code` + `unity-standards` | — |
| 2 | `PatrolGuard.cs` — Walk between waypoint transforms, pause at each | `unity-code` + `unity-standards` | — |
| 3 | `VisionCone.cs` — Angle + range + raycast detection of player | `unity-code` + `unity-standards` | — |
| 4 | `AlertSystem.cs` — On detection: pause, show "DETECTED", restart option | `unity-code` + `unity-standards` | T3 |
| 5 | `ExitZone.cs` — OnTriggerEnter, show "ESCAPED", win state | `unity-code` + `unity-standards` | — |

Tasks 1, 2, 3, 5 run in parallel. Task 4 depends on VisionCone interface.

### Step 5 — Wire Scene
- Floor Plane at y=0
- Wall cubes forming a small maze (L-shaped corridors)
- 2 guards with waypoint empties marking patrol routes
- Player capsule at spawn point
- Exit cube at maze end with trigger collider
- Top-down camera (rotation 90,0,0)

### Step 6 — Verify & Report
- **Playtest**: Move with WASD. Watch guard patrol patterns (drawn as debug rays). Time your movement to slip past. Reach yellow exit cube = win. Get spotted = "DETECTED" overlay.
- **Known limitations**: No sound-based detection, vision cone is debug lines only (no mesh visual), only 2 guards.
- **Next steps**: (1) Add cone mesh visualization, (2) Add hiding spots (trigger zones that block LOS), (3) More complex patrol routes with variable pause times.

---

## Example 3: "Rhythm game — notes fall to a beat and you press keys in time"

### Step 1 — Extract Core
- **Core mechanic**: Press keys in sync with music beats
- **Win condition**: Complete song with accuracy above threshold
- **Minimum loop**: See note approaching → press key at right time → get scored (Perfect/Good/Miss)

### Step 2 — Scope MVP

| Bucket | Items |
|--------|-------|
| **BUILD** | Beat timeline (BPM + note timestamps), note spawner + scrolling notes, input judge with timing windows (perfect ±50ms, good ±120ms, miss beyond), score tally |
| **STUB** | Song = any included AudioClip at known BPM, notes = colored quads falling in one lane, score = text counter, no combo multiplier |
| **SKIP** | Multiple lanes, long-press/hold notes, custom songs, visual effects, difficulty settings |

**Scope target**: 5 scripts, 1 scene, 1 AudioClip (any music file).

### Step 3 — Task Plan

| # | Task | Delegate To | Depends On |
|---|------|-------------|------------|
| 1 | `BeatMap.cs` — SO with BPM, float[] noteTimestamps | `unity-code` + `unity-standards` | — |
| 2 | `SongPlayer.cs` — Play AudioClip, expose current time via AudioSource.time | `unity-code` + `unity-standards` | — |
| 3 | `NoteSpawner.cs` — Read beatmap, spawn note objects scrolling toward hit zone | `unity-code` + `unity-standards` | T1 |
| 4 | `InputJudge.cs` — On keypress, find nearest note, compare timing, return result | `unity-code` + `unity-standards` | T1, T2 |
| 5 | `ScoreDisplay.cs` — Count Perfect/Good/Miss, show via UIDocument | `unity-uitoolkit` + `unity-standards` | — |

Tasks 1, 2, 5 run in parallel. Tasks 3 and 4 depend on BeatMap data shape.

### Step 5 — Wire Scene
- Empty scene with Camera facing a "highway" (vertical Plane or Quad)
- Hit zone indicator at bottom (colored line or quad)
- Notes spawn at top, scroll down
- UIDocument overlay for score text
- AudioSource on SongPlayer with a test clip
- BeatMap SO asset with 8-10 hand-placed timestamps matching the clip's beats

### Step 6 — Verify & Report
- **Playtest**: Enter Play mode. Music plays. Notes fall. Press Space when note reaches the hit line. "Perfect" / "Good" / "Miss" flashes. Score tallies at end.
- **Known limitations**: Single lane only, no visual polish on notes, timing calibration may need tweaking per machine (expose offset as SerializeField).
- **Next steps**: (1) Add 3-4 lanes with different keys (D/F/J/K), (2) Add hold notes, (3) Build a simple beatmap editor that records key presses during playback.

# Prototype Patterns by Game Type

Common patterns for prototyping different game types. Use these to inform task breakdowns and delegation prompts.

## 2D Platformer

**Core mechanic**: Jump and navigate platforms
**BUILD**: PlayerController (Rigidbody2D, ground check, variable jump height), simple level geometry (BoxCollider2D on sprites/primitives), collectible trigger, death zone
**STUB**: Score as UI text, respawn = reload scene, coins = colored circles
**SKIP**: Animated sprites, parallax, checkpoints, multiple levels

**Typical scripts** (4-5):
- `PlayerController.cs` — Movement + jump via Rigidbody2D
- `Collectible.cs` — OnTriggerEnter2D, increment score, destroy self
- `DeathZone.cs` — OnTriggerEnter2D, reload scene
- `GameManager.cs` — Score tracking, UI update
- HUD via UIDocument (score display)

## Top-Down Shooter

**Core mechanic**: Move and shoot
**BUILD**: Player movement (WASD), aiming (mouse), projectile spawning, enemy that can be hit
**STUB**: Enemy = moves toward player, health = int field, waves = spawn N every X seconds
**SKIP**: Weapon variety, power-ups, enemy types, boss fights

**Typical scripts** (5-6):
- `PlayerMovement.cs` — WASD movement, rotate toward mouse
- `Shooter.cs` — Instantiate bullet on click, set velocity
- `Bullet.cs` — Move forward, destroy on hit/timeout
- `Enemy.cs` — Move toward player, take damage, die
- `Spawner.cs` — Instantiate enemies at intervals
- HUD via UIDocument (health, wave count)

## Puzzle / Match-3

**Core mechanic**: Select and match elements on a grid
**BUILD**: Grid data structure, element placement, match detection, input handling
**STUB**: Elements = colored sprites/cubes, score = text, no animations for matching
**SKIP**: Special gems, combos, cascading, level progression

**Typical scripts** (4-5):
- `GridManager.cs` — 2D array, spawn elements, check matches
- `GridElement.cs` — Type/color, grid position, click handling
- `MatchChecker.cs` — Row/column scanning, return matched sets
- `GameController.cs` — Score, turn management, win condition
- HUD via UIDocument (score, moves remaining)

## Endless Runner

**Core mechanic**: Auto-move and dodge obstacles
**BUILD**: Player auto-movement, lane switching or jump, obstacle spawning, collision detection
**STUB**: Obstacles = cubes, distance = score, death = reload
**SKIP**: Power-ups, themes, daily challenges, cosmetics

**Typical scripts** (4):
- `PlayerRunner.cs` — Auto-forward, lane switch or jump input
- `ObstacleSpawner.cs` — Instantiate at intervals, randomize position
- `Obstacle.cs` — Move toward player (or player moves), destroy offscreen
- `ScoreTracker.cs` — Distance-based score, display, game over

## Physics Sandbox

**Core mechanic**: Interact with physics objects
**BUILD**: Spawn objects, apply forces, define goal state
**STUB**: Objects = primitives with Rigidbody, goal = overlap trigger
**SKIP**: Undo, material variety, custom meshes

**Typical scripts** (3-4):
- `ObjectSpawner.cs` — Click to spawn, physics material assignment
- `ForceApplier.cs` — Click-drag to launch, or catapult mechanic
- `GoalZone.cs` — Detect object entering trigger, track completion
- `GameManager.cs` — Level state, reset, score

## Tower Defense

**Core mechanic**: Place towers, enemies follow path
**BUILD**: Waypoint path, enemy follows path, tower placement on grid, tower shoots nearest enemy
**STUB**: Towers = cylinders, enemies = spheres, bullets = small cubes, health = float
**SKIP**: Tower upgrades, multiple tower types, economy, waves UI

**Typical scripts** (5-6):
- `Waypoint.cs` — Transform marker for path nodes
- `PathFollower.cs` — Enemy moves along waypoints, has health
- `TowerPlacer.cs` — Click grid to place tower, check placement validity
- `Tower.cs` — Find nearest enemy in range, shoot at interval
- `Projectile.cs` — Move toward target, deal damage
- `WaveManager.cs` — Spawn N enemies, delay between spawns

## Card Game (Matching / Deck-Building)

**Core mechanic**: Draw, play, and match cards
**BUILD**: Card data model (suit/value or effect), hand management (draw/discard), play area with card placement, match/combo detection logic
**STUB**: Cards = UI panels with text labels (no art), deck = shuffled List<T>, opponent = plays random card each turn
**SKIP**: Animations, card flipping effects, deck editor, multiplayer, card art, undo system

**Typical scripts** (5):
- `CardData.cs` — ScriptableObject with card type, value, effect text
- `DeckManager.cs` — Shuffle, draw, discard pile, reshuffle when empty
- `HandController.cs` — Display hand, select/play card, fan layout via RectTransform
- `PlayArea.cs` — Accept played cards, check match/combo rules, resolve turn
- `GameFlowController.cs` — Turn order, win/lose check, score tracking

**Tips**: Use UI Toolkit or Canvas for card display — cards are UI elements, not 3D objects. Keep card effects as simple int modifiers (damage, heal, draw N) rather than scriptable behaviors for the prototype.

## Roguelike (Turn-Based Dungeon)

**Core mechanic**: Move through grid, fight enemies, pick up items
**BUILD**: Tile-based grid with player movement (turn-based), enemy placement and simple AI (move toward player), item pickup on tile, attack/damage resolution
**STUB**: Dungeon = hardcoded 2D array of walkable/wall tiles rendered as colored quads, items = health potion (+HP) and weapon (+damage), enemies = take turns after player
**SKIP**: Procedural generation, fog of war, inventory UI, permadeath/meta-progression, stairs/multiple floors

**Typical scripts** (5):
- `GridManager.cs` — 2D int array for map, spawn tiles as quads, track occupancy
- `TurnManager.cs` — Player moves first, then all enemies, repeat
- `PlayerEntity.cs` — Grid position, WASD moves one tile per turn, attack adjacent enemy
- `EnemyEntity.cs` — Simple chase: move one tile toward player on its turn, deal damage if adjacent
- `Pickup.cs` — Sits on tile, apply effect on player overlap, destroy self

**Tips**: Turn-based is simpler than real-time for prototyping — no physics needed. Use a 2D int array (0=floor, 1=wall) and instantiate quads. Color-code: green=player, red=enemy, yellow=item, gray=wall.

## Rhythm Game

**Core mechanic**: Hit inputs in sync with beats
**BUILD**: Beat timeline system (fixed BPM, beat markers at known times), input detection with timing window (perfect/good/miss), visual note highway or falling notes, score based on accuracy
**STUB**: Song = AudioClip playing at known BPM, notes = serialized list of beat timestamps, visual = colored blocks falling down lanes
**SKIP**: Custom song editor, multiple difficulties, combo multipliers, particle effects, note skins

**Typical scripts** (5):
- `BeatMap.cs` — ScriptableObject with BPM, list of note timestamps and lane assignments
- `SongPlayer.cs` — Play AudioClip, expose `AudioSource.time` as current song position
- `NoteSpawner.cs` — Read beatmap, spawn note objects ahead of beat, scroll toward hit zone
- `InputJudge.cs` — Compare input time to expected beat time, return Perfect/Good/Miss
- `ScoreDisplay.cs` — Track hits/misses, show accuracy text, combo counter

**Tips**: The key prototype question is "does the timing feel tight?" Use `AudioSettings.dspTime` for precise audio sync instead of `Time.time`. Define timing windows as `[SerializeField] float perfectWindow = 0.05f, goodWindow = 0.12f`. Start with just one lane and 4-8 notes to test feel before expanding.

## Stealth Game

**Core mechanic**: Avoid detection by patrolling enemies
**BUILD**: Player movement (crouch/walk speed toggle), enemy patrol along waypoints, vision cone detection (angle + range), alert state on detection (game over or chase)
**STUB**: Player = capsule with two speeds, enemies = cylinders with a cone mesh child for FOV visual, walls = cubes, detection = cone angle check + raycast
**SKIP**: Sound detection, hiding spots, distraction items, security cameras, minimap, takedowns

**Typical scripts** (5):
- `StealthPlayer.cs` — WASD movement, shift to crouch (slower + smaller collider), interact key
- `PatrolGuard.cs` — Walk between waypoint transforms, pause at each, repeat
- `VisionCone.cs` — Check angle to player + distance + raycast for line-of-sight, trigger alert
- `AlertSystem.cs` — On detection: freeze game, show "DETECTED" text, offer restart
- `LevelSetup.cs` — Spawn guard routes, define patrol timing, place walls and objective

**Tips**: Vision cone check is: `Vector3.Angle(guard.forward, dirToPlayer) < halfAngle && distance < range && !Physics.Raycast(blocked)`. Make the cone visible with a mesh or `Debug.DrawRay` so the player can read the space. Slow patrol speeds + wide cones = easier to tune than fast guards.

## General Tips

- **Camera**: For 2D use `Camera.main` with orthographic. For 3D use Cinemachine if installed, otherwise static camera positioned to frame action.
- **Physics**: Use 2D physics (Rigidbody2D, Collider2D) for 2D prototypes — simpler and faster. Use 3D physics only when depth matters.
- **Input**: `Input.GetAxis("Horizontal")` / `Input.GetKeyDown(KeyCode.Space)` for prototype speed. New Input System only if analog precision matters.
- **Scene layout**: Ground plane at y=0 (or y=0 for 2D), spawn points at known positions, camera at z=-10 (2D ortho).
- **Prefab creation**: Create GameObjects in scene first, verify scripts work, THEN make prefabs for spawned objects.

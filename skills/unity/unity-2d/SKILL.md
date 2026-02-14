---
name: unity-2d
description: "(opencode-project - Skill) Unity 2D game development — sprites, tilemaps, 2D physics, 2D animation, sprite atlas, and 2D lighting. Covers SpriteRenderer setup and sorting layers, Tilemap workflow (Tile, TileBase, RuleTile), 2D physics (Rigidbody2D, Collider2D, ContactFilter2D), sprite animation (Animator + SpriteSheet), Sprite Atlas for draw call optimization, 2D lighting with URP, pixel-perfect camera, and 2D character controller patterns. Use when: (1) Building 2D games or game elements, (2) Working with sprites and sprite sheets, (3) Implementing tilemap levels with scripting, (4) Setting up 2D physics and collision, (5) Configuring 2D animation state machines, (6) Optimizing draw calls with Sprite Atlas, (7) Adding 2D lighting with URP. Triggers: '2D game', 'sprite', 'tilemap', '2D physics', 'Rigidbody2D', 'SpriteRenderer', 'sprite atlas', '2D animation', 'tile palette', '2D collider', '2D lighting', 'pixel perfect'."
---

# unity-2d — 2D Game Development

Build 2D games and game elements in Unity — covering sprite management, tilemap level design, 2D physics, animation, rendering configuration, and 2D lighting for polished 2D visuals.

## Purpose

Provide comprehensive guidance for 2D game development in Unity, from project setup (URP 2D Renderer, pixel-perfect camera) through sprite workflows, tilemap scripting, 2D physics with ContactFilter2D, animation state machines, Sprite Atlas optimization, and 2D lighting. Ensure pixel-perfect or smooth-vector visuals depending on art style, with performant physics and draw call–efficient rendering.

## Input

- **Required**: 2D game feature or system to implement (platformer physics, tilemap levels, sprite animation, etc.)
- **Optional**: Art style (pixel art vs vector), target resolution, existing sprite assets, physics requirements, target platform

## Output

Production-ready C# scripts, prefab configurations, and import settings for 2D game systems. All code compiles, follows `unity-code` quality standards, and uses proper 2D-specific patterns (Rigidbody2D, Collider2D, SpriteRenderer).

## Examples

| User Request | Skill Action |
|:---|:---|
| "Build a 2D platformer character controller" | Create physics-based controller with Rigidbody2D, coyote time, jump buffering, and better-jump gravity |
| "Set up tilemap levels with rule tiles" | Configure Tilemap palette with custom RuleTile, TilemapCollider2D + CompositeCollider2D, scripted tile placement |
| "Implement sprite animation for a character" | Configure sprite sheet import, create Animator Controller with cached parameter hashes, sprite flip on direction |
| "Optimize draw calls for 2D sprites" | Create Sprite Atlas, configure packing settings, verify batching in Frame Debugger |
| "Add 2D lighting to the scene" | Configure URP 2D Renderer, add Global Light 2D, Point Light 2D, and Sprite Lit materials |

## Workflow

1. **Configure project for 2D** — Set URP 2D Renderer, orthographic camera, Pixel Perfect Camera if needed
2. **Set up sprite import settings** — Configure pixels-per-unit, filter mode, compression based on art style
3. **Establish sorting layers** — Define rendering order: Background → Midground → Default → Foreground → UI
4. **Build levels with Tilemap** — Create Tilemap palette, RuleTiles, composite colliders, and scripted tile placement
5. **Add 2D physics** — Configure Rigidbody2D types, Collider2D shapes, ContactFilter2D for queries
6. **Create animations** — Import sprite sheets, build Animator Controller with transitions and cached hashes
7. **Optimize rendering** — Pack sprites into Sprite Atlas, verify batching, configure 2D lighting

---

## Code Patterns & Project Setup

> **Full code patterns and project setup**: See [2d-code-patterns.md](references/2d-code-patterns.md) — covers sorting layers, sprite import settings, PlatformerController2D, TilemapController, RuleTile, ContactFilter2D queries, SpriteAnimationController, 2D lighting (FlickerLight2D), pixel-perfect camera, and tilemap architecture with collider optimization.

## 2D Physics Reference

> **Full physics reference**: See [2d-physics-reference.md](references/2d-physics-reference.md) — covers Rigidbody2D type selection table (Dynamic/Kinematic/Static), collider choices per scenario, and Physics 2D project settings.

---

## Best Practices

### Do

- **Use Point filter for pixel art** — Bilinear filtering blurs pixel edges; Point preserves crisp pixels
- **Match PPU across all sprites in a set** — Mismatched PPU causes inconsistent visual scale
- **Use CompositeCollider2D for tilemaps** — Merges per-tile colliders into one efficient shape
- **Cache Animator parameter hashes** — `Animator.StringToHash()` in Awake, not in Update
- **Use ContactFilter2D for physics queries** — More efficient than multiple filtered OverlapCircle calls
- **Flip with `SpriteRenderer.flipX`** — Preserves transform scale, cheaper than negative scale
- **Use Sprite Atlas for draw call batching** — Pack related sprites to reduce draw calls
- **Freeze Rigidbody2D Z rotation** — Prevents 2D characters from tumbling on collision
- **Use `MovePosition` for Kinematic bodies** — Proper physics integration for moving platforms

### Do Not

- **Never use Bilinear filter on pixel art** — Creates blurry, smeared pixels
- **Never move Dynamic Rigidbody2D with `transform.position`** — Breaks physics simulation, causes tunneling
- **Never leave per-tile colliders on large tilemaps** — Thousands of individual colliders destroy performance
- **Never use string Animator parameters in Update** — Allocates string hash every frame (GC pressure)
- **Never use non-uniform scale on collider parents** — Distorts collision shapes unpredictably
- **Never ignore Sorting Layers** — Sprites on the same layer with same Z will Z-fight (flicker)
- **Never use `GetComponent<Collider2D>()` in FixedUpdate** — Cache in Awake to avoid repeated lookups

---

## Common Anti-Patterns

| Anti-Pattern | Why It Fails | Correct Pattern |
|:-------------|:-------------|:----------------|
| Bilinear filter on pixel art | Blurry, smeared pixels | Use Point (no filter) |
| Moving Dynamic rb via transform | Breaks physics, tunneling | `AddForce` (Dynamic) or `MovePosition` (Kinematic) |
| Per-tile colliders on tilemaps | Thousands of colliders, terrible perf | CompositeCollider2D to merge |
| String Animator params in Update | GC allocation every call | Cache with `Animator.StringToHash` |
| Z-fighting between sprites | Flickering, inconsistent draw | Sorting Layers + Order in Layer |
| Non-uniform scale on colliders | Distorted collision shapes | Scale the sprite, not the collider parent |
| Mismatched PPU across sprites | Inconsistent visual scale | Same PPU for all sprites in a set |

---

## Handoff & Boundaries

### Delegates To

| Skill | When |
|:------|:-----|
| `unity-code` | Gameplay logic, state machines, AI behavior beyond 2D-specific patterns |
| `unity-tech-art` | Custom 2D shaders, advanced visual effects, Shader Graph for 2D |
| `unity-optimize-performance` | Sprite Atlas deep optimization, draw call batching, profiling 2D games |

### Does Not Handle

- **3D rendering and physics** — 3D meshes, Rigidbody (3D), and 3D camera rigs are outside scope
- **Mixed 2D/3D rendering** — Forward+ renderer hybrid setups belong to rendering-specific guidance
- **Third-party 2D animation (Spine, DragonBones)** — Only Unity-native animation (Animator + SpriteSheet)
- **UI Toolkit for game UI** — HUD, menus, and UI elements belong to `ui-toolkit-*` skills
- **Networking for 2D games** — Multiplayer sync and server architecture belong to networking-specific code

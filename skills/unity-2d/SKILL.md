---
name: unity-2d
description: "(opencode-project - Skill) Unity 2D game development — sprites, tilemaps, 2D physics, 2D animation, sprite atlas, and 2D lighting. Covers SpriteRenderer setup and sorting layers, Tilemap workflow (Tile, TileBase, RuleTile), 2D physics (Rigidbody2D, Collider2D, ContactFilter2D), sprite animation (Animator + SpriteSheet), Sprite Atlas for draw call optimization, 2D lighting with URP, pixel-perfect camera, and 2D character controller patterns. Use when: (1) Building 2D games or game elements, (2) Working with sprites and sprite sheets, (3) Implementing tilemap levels with scripting, (4) Setting up 2D physics and collision, (5) Configuring 2D animation state machines, (6) Optimizing draw calls with Sprite Atlas, (7) Adding 2D lighting with URP. Triggers: '2D game', 'sprite', 'tilemap', '2D physics', 'Rigidbody2D', 'SpriteRenderer', 'sprite atlas', '2D animation', 'tile palette', '2D collider', '2D lighting', 'pixel perfect'."
---

# unity-2d — 2D Game Development

**Input**: 2D game feature or system to implement. Optional: art style (pixel art vs vector), target resolution, physics requirements, target platform.

**Output**: Production-ready C# scripts, prefab configurations, and import settings for 2D game systems.

## Workflow

1. **Configure**: URP 2D Renderer, orthographic camera, Pixel Perfect Camera if needed
2. **Sprite Import**: Set pixels-per-unit, filter mode, compression per art style
3. **Sorting Layers**: Background → Midground → Default → Foreground → UI
4. **Tilemap**: Create palette, RuleTiles, composite colliders, scripted tile placement
5. **2D Physics**: Configure Rigidbody2D types, Collider2D shapes, ContactFilter2D queries
6. **Animation**: Import sprite sheets, build Animator Controller with cached hashes
7. **Optimize**: Pack into Sprite Atlas, verify batching, configure 2D lighting

## References

- [2d-code-patterns.md](references/2d-code-patterns.md) — sorting layers, PlatformerController2D, TilemapController, RuleTile, ContactFilter2D, SpriteAnimationController, 2D lighting, pixel-perfect camera
- [2d-physics-reference.md](references/2d-physics-reference.md) — Rigidbody2D type selection, collider choices, Physics 2D settings

## Key Best Practices

- **Point filter for pixel art** — Bilinear blurs pixel edges
- **Match PPU across sprite sets** — Mismatched PPU = inconsistent scale
- **CompositeCollider2D for tilemaps** — Merges per-tile colliders into one shape
- **Cache Animator hashes** — `StringToHash()` in Awake, not Update
- **Flip with `SpriteRenderer.flipX`** — Cheaper than negative scale
- **Freeze Rigidbody2D Z rotation** — Prevents 2D characters from tumbling

## Common Anti-Patterns

| Anti-Pattern | Correct Pattern |
|:---|:---|
| Bilinear filter on pixel art | Point (no filter) |
| Moving Dynamic rb via transform | `AddForce` (Dynamic) or `MovePosition` (Kinematic) |
| Per-tile colliders on tilemaps | CompositeCollider2D |
| String Animator params in Update | Cache with `Animator.StringToHash` |
| Z-fighting between sprites | Sorting Layers + Order in Layer |
| Non-uniform scale on colliders | Scale the sprite, not the collider parent |

## Handoff

- **Delegates to**: `unity-code` (gameplay logic), `unity-tech-art` (custom 2D shaders), `unity-optimize-performance` (Sprite Atlas deep optimization)
- **Does NOT**: 3D rendering/physics, mixed 2D/3D, third-party animation (Spine/DragonBones), UI Toolkit, networking

---
name: phaser-coder
description: >
  Write, review, debug, or explain Phaser 3 code: game config, scenes, sprites,
  Arcade or Matter physics, tilemaps, animations, audio, input, cameras, tweens,
  particles, groups, and performance. Auto-triages Quick tasks like one feature,
  API question, or bug fix, and Deep tasks like full game scaffolds, multi-scene
  architecture, physics-heavy gameplay, or performance audits. MUST use for any
  Phaser request: creating a game, loading assets, physics, sprites, input,
  tilemaps, collisions, scene management, Phaser.Game, Phaser.Scene, this.physics,
  this.anims, preload/create/update, or help with a Phaser game. Target Phaser
  3.60+ unless Phaser 2/CE is explicitly requested.
metadata:
  author: cuongnp
  version: "1.0"
---
# phaser-coder

Phaser 3 game development specialist. Target v3.60+ APIs (latest stable v3.90). Never suggest Phaser 2/CE patterns unless asked about migration.

## Triage

**Quick** — Single-file: one feature, one API question, one bug fix.  
**Deep** — Multi-system: full scaffold, multi-scene architecture, physics-heavy gameplay, performance audit.

## Phaser 3 Essentials (Check Every Response)

1. **Config** — `new Phaser.Game({ type: Phaser.AUTO, width, height, scene, physics })`
2. **Lifecycle** — `init()` → `preload()` → `create()` → `update(time, delta)` — `delta` is ms since last frame
3. **`this` in scenes** — `this.add`, `this.physics`, `this.input`, `this.cameras`, `this.tweens`, `this.anims`, `this.time`, `this.sound`
4. **Asset loading** — ALL assets in `preload()` or via `this.load.start()`
5. **Arcade physics** — `this.physics.add.sprite()` for physics-enabled sprites; set `collideWorldBounds`, `setBounce`, `setVelocity` after creation
6. **Overlap vs Collide** — `this.physics.add.collider()` for physical; `this.physics.add.overlap()` for detection
7. **Groups** — `this.physics.add.group()` for physics; `this.add.group()` for display-only
8. **Animations** — Create globally via `this.anims.create({key, frames, frameRate, repeat})`; play via `sprite.anims.play('key')`
9. **Tilemap** — `this.make.tilemap({key})` → `addTilesetImage()` → `createLayer(layerName, tileset)`
10. **Camera** — `this.cameras.main.startFollow(player)`, `setBounds()`, `setZoom()`
11. **Input** — `this.input.keyboard.createCursorKeys()`, `this.input.keyboard.addKey('W')`, pointer via `this.input.on('pointerdown', cb)`
12. **Scene transitions** — `this.scene.start()` replaces; `this.scene.launch()` runs parallel
13. **Tweens** — `this.tweens.add({ targets, props, duration, ease, yoyo, repeat })`

## References (Load on Demand)

| File | Load when... |
|------|-------------|
| `references/game-config-and-scenes.md` | Game setup, scene lifecycle, multi-scene |
| `references/sprites-and-images.md` | Sprites, atlases, animation |
| `references/arcade-physics.md` | Physics bodies, velocity, gravity, collisions |
| `references/matter-physics.md` | Matter.js, complex bodies, constraints |
| `references/tilemaps.md` | Tiled import, tilemap layers |
| `references/input.md` | Keyboard, pointer, gamepad |
| `references/cameras-and-scenes.md` | Camera, multi-camera, transitions |
| `references/tweens-and-time.md` | Tweens, timers, timeline |
| `references/audio.md` | Sound manager, spatial audio |
| `references/particles.md` | Particle emitters (v3.60+ API) |
| `references/performance.md` | Object pooling, optimization |

## Response Pattern

**Quick:** inline answer, one code block, 1–3 gotchas.  
**Deep:** full scaffold, multiple labeled blocks, explain architectural choices.

```javascript
// Minimal Bootstrap
import Phaser from 'phaser';
class MainScene extends Phaser.Scene {
  constructor() { super('MainScene'); }
  preload() { this.load.image('logo', 'assets/logo.png'); }
  create() {
    this.tweens.add({ targets: this.add.image(400, 300, 'logo'),
      y: 250, duration: 1500, ease: 'Sine.easeInOut', yoyo: true, repeat: -1 });
  }
}
new Phaser.Game({ type: Phaser.AUTO, width: 800, height: 600, scene: MainScene });

// Scene Transition with Data
this.scene.start('GameScene', { level: 1 });
// In GameScene:  init(data) { this.level = data.level; }
```

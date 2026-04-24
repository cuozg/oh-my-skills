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

Phaser 3 game development specialist. Target v3.60+ APIs (latest stable v3.90). Never suggest Phaser 2/CE patterns unless explicitly asked about migration.

## Triage

**Quick** — Single-file answers: one feature, one API question, one bug fix, one snippet.
**Deep** — Multi-system: full game scaffold, multi-scene architecture, physics-heavy gameplay, tilemap integration, performance audit.

## Phaser 3 Essentials (Enforce These Always)

These are the most common mistakes and misunderstandings. Check every response:

1. **Game config** — `new Phaser.Game({ type: Phaser.AUTO, ... })` — always specify `width`, `height`, `scene`, and `physics` when physics is needed
2. **Scene lifecycle** — `init()` → `preload()` → `create()` → `update(time, delta)` — `delta` is ms since last frame, NOT a multiplier like PixiJS
3. **`this` in scenes** — Scene methods use `this` to access managers: `this.add`, `this.physics`, `this.input`, `this.cameras`, `this.tweens`, `this.anims`, `this.load`, `this.scene`, `this.time`, `this.sound`
4. **Asset loading** — ALL loading in `preload()` or via `this.load.start()` after adding files — never assume assets are ready in `create()` if loaded elsewhere
5. **Arcade physics** — `this.physics.add.sprite()` not `this.add.sprite()` for physics-enabled sprites; set `collideWorldBounds`, `setBounce`, `setVelocity` after creation
6. **Overlap vs Collide** — `this.physics.add.collider(a, b, callback)` for physical collision; `this.physics.add.overlap(a, b, callback)` for non-physical detection
7. **Groups** — `this.physics.add.group()` for physics groups, `this.add.group()` for display-only groups; group config sets defaults for children
8. **Animations** — Create via `this.anims.create({ key, frames, frameRate, repeat })` globally, play via `sprite.anims.play('key')` — anims are global, not per-sprite
9. **Tilemap** — `this.make.tilemap({ key })` then `addTilesetImage(tilesetName, imageKey)` then `createLayer(layerName, tileset)` — layer name must match Tiled export
10. **Camera** — `this.cameras.main.startFollow(player)` for follow cam; `setBounds()` to constrain; `setZoom()` for zoom
11. **Input** — `this.input.keyboard.createCursorKeys()` for arrow keys; `this.input.keyboard.addKey('W')` for specific keys; pointer via `this.input.on('pointerdown', cb)`
12. **Scene transitions** — `this.scene.start('SceneKey')` replaces; `this.scene.launch('SceneKey')` runs parallel; `this.scene.pause()`/`this.scene.resume()` for overlay patterns
13. **Texture atlases** — `this.load.atlas('key', 'png', 'json')` in preload; `this.add.sprite(x, y, 'key', 'frameName')` to use specific frames
14. **Tweens** — `this.tweens.add({ targets, props, duration, ease, yoyo, repeat })` — use `'Power2'`, `'Bounce.easeOut'`, `'Sine.easeInOut'` etc. for easing
15. **Data manager** — `sprite.setData('key', value)` and `sprite.getData('key')` for attaching game state to objects; `this.registry` for cross-scene data

## Reference Files

Load on demand — do NOT preload all:

| File | Load when... |
|------|-------------|
| `references/game-config-and-scenes.md` | Game setup, scene lifecycle, scene manager, multi-scene patterns |
| `references/sprites-and-images.md` | Sprites, images, texture atlases, sprite sheets, animation |
| `references/arcade-physics.md` | Arcade physics bodies, velocity, gravity, collisions, groups |
| `references/matter-physics.md` | Matter.js integration, complex bodies, constraints, sensors |
| `references/tilemaps.md` | Tiled import, tilemap layers, collision tiles, dynamic tiles |
| `references/input.md` | Keyboard, pointer, gamepad, drag, zones, interactive objects |
| `references/cameras-and-scenes.md` | Camera follow, bounds, effects, multi-camera, scene transitions |
| `references/tweens-and-time.md` | Tweens, timers, delays, timeline, easing functions |
| `references/audio.md` | Sound manager, Web Audio, spatial audio, audio sprites |
| `references/particles.md` | Particle emitters (v3.60+ API), zones, effects |
| `references/performance.md` | Object pooling, texture packing, render optimization, debugging |

## Response Pattern

```
[Triage: Quick/Deep]

[Load relevant reference file(s) if needed]

[Code — complete, runnable, Phaser 3 v3.60+]

[Gotchas — call out any common pitfalls relevant to this code]
```

For **Quick**: answer inline, one code block, note 1-3 gotchas.
For **Deep**: scaffold the full solution, multiple code blocks with file labels, explain architectural choices.

## Common Patterns to Emit

### Minimal Game Bootstrap
```javascript
import Phaser from 'phaser';

class MainScene extends Phaser.Scene {
  constructor() {
    super('MainScene');
  }

  preload() {
    this.load.image('logo', 'assets/logo.png');
  }

  create() {
    const logo = this.add.image(400, 300, 'logo');
    this.tweens.add({
      targets: logo,
      y: 250,
      duration: 1500,
      ease: 'Sine.easeInOut',
      yoyo: true,
      repeat: -1,
    });
  }
}

const config = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  backgroundColor: '#1a1a2e',
  scene: MainScene,
};

new Phaser.Game(config);
```

### Arcade Physics Platformer Setup
```javascript
create() {
  const platforms = this.physics.add.staticGroup();
  platforms.create(400, 580, 'ground').setScale(2).refreshBody();

  const player = this.physics.add.sprite(100, 450, 'player');
  player.setBounce(0.2);
  player.setCollideWorldBounds(true);

  this.physics.add.collider(player, platforms);

  this.cursors = this.input.keyboard.createCursorKeys();
  this.player = player;
}

update() {
  if (this.cursors.left.isDown) {
    this.player.setVelocityX(-160);
    this.player.anims.play('walk-left', true);
  } else if (this.cursors.right.isDown) {
    this.player.setVelocityX(160);
    this.player.anims.play('walk-right', true);
  } else {
    this.player.setVelocityX(0);
    this.player.anims.play('idle', true);
  }

  if (this.cursors.up.isDown && this.player.body.touching.down) {
    this.player.setVelocityY(-330);
  }
}
```

### Scene Transition
```javascript
// From MenuScene
this.scene.start('GameScene', { level: 1, difficulty: 'hard' });

// In GameScene
init(data) {
  this.level = data.level;
  this.difficulty = data.difficulty;
}
```

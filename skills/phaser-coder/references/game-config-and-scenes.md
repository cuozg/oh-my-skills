# Game Config & Scenes

## Game Configuration

```javascript
const config = {
  type: Phaser.AUTO,        // AUTO, WEBGL, or CANVAS
  width: 800,
  height: 600,
  parent: 'game-container', // DOM element id
  backgroundColor: '#000000',
  pixelArt: true,           // Disable anti-aliasing for pixel art
  scale: {
    mode: Phaser.Scale.FIT,           // FIT, RESIZE, ENVELOP, NONE
    autoCenter: Phaser.Scale.CENTER_BOTH,
  },
  physics: {
    default: 'arcade',
    arcade: { gravity: { y: 300 }, debug: false },
  },
  scene: [BootScene, MenuScene, GameScene, UIScene],
};

const game = new Phaser.Game(config);
```

### Scale Modes
- `FIT` — scale to fit parent, maintain aspect ratio (most common)
- `RESIZE` — resize canvas to fill parent (responsive)
- `ENVELOP` — scale to cover parent, may crop
- `NONE` — no scaling

## Scene Lifecycle

```
constructor() → init(data) → preload() → create() → update(time, delta) [loop]
```

- **`init(data)`** — receives data from `scene.start('Key', data)`, runs every time scene starts
- **`preload()`** — queue assets here; `create()` waits until all loaded
- **`create()`** — build game objects, set up physics, input, animations
- **`update(time, delta)`** — game loop; `time` = ms since game start, `delta` = ms since last frame

## Scene Manager Patterns

```javascript
// Replace current scene
this.scene.start('GameOver', { score: this.score });

// Launch parallel scene (overlay UI)
this.scene.launch('HUD');

// Pause/Resume
this.scene.pause('GameScene');
this.scene.resume('GameScene');

// Stop and remove from active
this.scene.stop('GameScene');

// Bring to top (rendering order)
this.scene.bringToTop('HUD');

// Sleep (pauses update but keeps rendered)
this.scene.sleep('Background');
this.scene.wake('Background');
```

### Cross-Scene Communication

```javascript
// Via events (preferred)
this.scene.get('HUD').events.emit('updateScore', 100);

// In HUD scene:
this.events.on('updateScore', (score) => { this.scoreText.setText(score); });

// Via registry (global data store)
this.registry.set('lives', 3);
this.registry.get('lives');
this.registry.events.on('changedata-lives', (parent, value) => { ... });
```

## Scene Class Template

```javascript
class GameScene extends Phaser.Scene {
  constructor() {
    super({ key: 'GameScene' });
  }

  init(data) {
    this.level = data.level || 1;
  }

  preload() {
    // Only if this scene has unique assets not loaded in Boot
  }

  create() {
    // Build world, player, enemies, UI
  }

  update(time, delta) {
    // Game logic, input handling
    // delta is in ms — multiply velocities by (delta / 1000) for frame-rate independence
    // OR use Arcade physics which handles this automatically
  }
}
```

## Common Gotchas

- Scene keys are strings, not class references — `this.scene.start('GameScene')` not `this.scene.start(GameScene)`
- `update()` delta is in **milliseconds**, not a normalized multiplier
- `init()` runs BEFORE `preload()` — don't access loaded assets there
- Launching a scene that's already running does nothing — stop it first or use restart
- Scene render order follows array order in config (or `bringToTop`/`sendToBack`)

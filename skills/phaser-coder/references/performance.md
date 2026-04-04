# Performance

## Object Pooling

The most important optimization in Phaser games. Reuse objects instead of creating/destroying.

```javascript
// Physics group with pooling
const bullets = this.physics.add.group({
  classType: Bullet,
  maxSize: 50,
  runChildUpdate: true,
});

function fire(x, y, direction) {
  const bullet = bullets.get(x, y);
  if (!bullet) return; // pool exhausted
  bullet.setActive(true).setVisible(true);
  bullet.body.enable = true;
  bullet.setVelocityX(direction * 600);
}

// In Bullet class update():
update(time, delta) {
  if (this.x < -50 || this.x > 850) {
    this.setActive(false).setVisible(false);
    this.body.enable = false;
  }
}
```

## Texture Atlases

Bundle sprites into atlases to reduce draw calls and HTTP requests:

- Use **TexturePacker** or **Free Texture Packer**
- One atlas per "domain" (player, enemies, UI, tiles)
- Power-of-two dimensions for GPU efficiency (512, 1024, 2048)

```javascript
// One draw call for all sprites from same atlas
this.load.atlas('game', 'assets/game.png', 'assets/game.json');
```

## Render Optimization

```javascript
// Pixel art: disable smoothing
const config = {
  pixelArt: true,       // sets antialias: false, roundPixels: true
  render: {
    antialias: false,
    batchSize: 4096,    // increase if many sprites (default 4096)
  },
};

// Static elements: use images, not sprites (no animation overhead)
this.add.image(x, y, 'background');

// Off-screen culling: automatic for tilemaps, manual for others
// Objects outside camera bounds still update — disable manually:
if (!cam.worldView.contains(enemy.x, enemy.y)) {
  enemy.setActive(false);
}
```

## Physics Optimization

```javascript
// Use Arcade over Matter when possible — 10x faster
// Disable physics on inactive objects
sprite.body.enable = false;

// Reduce collision checks
// Bad: collider between two large groups (O(n*m))
// Good: spatial partitioning or manual distance checks first

// Static bodies are cheaper — use staticGroup for platforms
const platforms = this.physics.add.staticGroup();
```

## Memory Management

```javascript
// Destroy unused objects
sprite.destroy();

// Clear scene caches on shutdown
this.events.on('shutdown', () => {
  this.tweens.killAll();
  this.time.removeAllEvents();
});

// Texture management — remove unused textures
this.textures.remove('temporary-texture');
```

## Profiling

```javascript
// FPS display
const config = {
  fps: { target: 60, forceSetTimeOut: false },
};

// In-game FPS counter
this.fpsText = this.add.text(10, 10, '', { fontSize: '14px', color: '#0f0' });
// In update():
this.fpsText.setText(`FPS: ${Math.round(this.game.loop.actualFps)}`);

// Scene-level stats
console.log(this.sys.displayList.length);  // render count
console.log(this.physics.world.bodies.entries.length); // physics bodies
```

## Common Performance Killers

1. **Creating/destroying objects every frame** → use object pooling
2. **Too many physics bodies** → disable inactive, use groups wisely
3. **Large uncompressed textures** → use atlases, compress PNGs
4. **Text objects updated every frame** → cache and only update on change
5. **Matter.js with many bodies** → switch to Arcade if possible
6. **No dead zone on camera follow** → causes constant re-render of tilemap
7. **Debug mode left on** → `debug: true` in physics has significant overhead

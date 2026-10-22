# Performance — PixiJS v8

## Batching — How PixiJS Draws

PixiJS batches consecutive objects that share the same texture and blend mode into a single draw call. A "batch break" occurs when:
- Texture changes between adjacent objects
- Blend mode changes
- A filter is applied
- An object is a Mesh with a custom shader

**Goal**: Minimize texture switches. Use texture atlases / sprite sheets.

```typescript
// BAD — different textures = 3 draw calls:
stage.addChild(new Sprite(texA));
stage.addChild(new Sprite(texB));
stage.addChild(new Sprite(texA)); // starts new batch

// GOOD — atlas = 1 draw call for all three:
const atlas = await Assets.load('/atlas/game.json'); // spritesheet
stage.addChild(Sprite.from('hero.png'));
stage.addChild(Sprite.from('enemy.png'));
stage.addChild(Sprite.from('coin.png'));
```

## Texture Atlases

Always pack sprites into atlases (TexturePacker, ShoeBox, Shoebox, Free Texture Packer):
```typescript
// Load the atlas (one load, one GPU texture, many sprites)
await Assets.load('/sprites/game-atlas.json');

const hero = Sprite.from('hero_idle_001.png');   // from atlas
const enemy = Sprite.from('enemy_walk_001.png'); // from atlas
```

## Object Pooling

Never `new` inside a loop or each frame. Pool and reuse:

```typescript
class SpritePool {
  private pool: Sprite[] = [];
  private texture: Texture;

  constructor(texture: Texture, prealloc = 50) {
    this.texture = texture;
    for (let i = 0; i < prealloc; i++) {
      this.pool.push(this.createNew());
    }
  }

  private createNew(): Sprite {
    const s = new Sprite(this.texture);
    s.visible = false;
    return s;
  }

  get(): Sprite {
    const s = this.pool.pop() ?? this.createNew();
    s.visible = true;
    return s;
  }

  release(sprite: Sprite) {
    sprite.visible = false;
    sprite.parent?.removeChild(sprite);
    this.pool.push(sprite);
  }
}
```

## RenderGroup — Layer-Level Optimization

```typescript
// Container with isRenderGroup = true gets its own GPU transform matrix
// Moving it = one uniform update instead of recalculating all children
const hudLayer = new Container();
hudLayer.isRenderGroup = true;
stage.addChild(hudLayer);

// All HUD elements benefit — moving the HUD is essentially free
hudLayer.alpha = 0.8; // applies to whole group without rebatch
```

## Culling — Not Automatic in v8

v8 does NOT auto-cull off-screen objects. You must do it manually:

```typescript
import { Culler, Container } from 'pixi.js';

// Manual per-frame culling
const viewBounds = app.renderer.screen;
app.ticker.add(() => {
  Culler.shared.cull(app.stage, viewBounds);
});

// Or use the CullerPlugin extension (auto-culls every frame)
import { extensions, CullerPlugin } from 'pixi.js';
extensions.add(CullerPlugin);
// Now culling happens automatically before each render
```

## cacheAsTexture — Complex Static Containers

If a container has complex content that rarely changes (a game board, a city block):

```typescript
const staticScene = new Container();
// ... add many children ...

// Render to texture once — subsequent renders use cached GPU texture
staticScene.cacheAsTexture(true);

// If something changes, force refresh:
staticScene.updateCacheTexture();

// Disable
staticScene.cacheAsTexture(false);
```

## sortableChildren — Use Sparingly

```typescript
// Sorting is O(n log n) per frame
parent.sortableChildren = true; // avoid unless needed

// Prefer addChildAt() for fixed ordering, or use RenderGroup layers
// Only enable sortableChildren if objects frequently change zIndex
```

## Render Profiling Checklist

1. Open Chrome DevTools → Performance tab
2. Open `app.renderer.plugins.accessibility` — enable PixiJS Stats (if installed)
3. Check: `app.renderer.renderPipes.batch.batchCount` — high = too many batches
4. Watch GPU frame time vs CPU frame time
5. Profile with [Stats.js](https://github.com/mrdoob/stats.js) or [pixi-stats](https://github.com/mweststrate/pixi-stats)

```typescript
// Quick draw call logging (dev only)
app.ticker.add(() => {
  // After render
  console.log('Draw calls:', (app.renderer as any)._drawCallCount);
});
```

## Memory Management

```typescript
// Destroy sprites when done
sprite.destroy();
sprite.destroy({ texture: false }); // keep texture (pooling)
sprite.destroy({ texture: true, textureSource: true }); // full cleanup

// Destroy entire tree
container.destroy({ children: true, texture: true });

// Unload assets
await Assets.unload('hero');
await Assets.unloadBundle('level-1');
```

## Tips at a Glance

| Tip | Impact |
|---|---|
| Use texture atlases | ⬆⬆⬆ Reduces draw calls dramatically |
| Pool Sprites/Particles | ⬆⬆ Eliminates GC pressure |
| Set `eventMode='none'` on non-interactive objects | ⬆ Skips hit-test |
| Use `RenderGroup` for large stable layers | ⬆ Cheap layer transforms |
| `cacheAsTexture` for complex static containers | ⬆⬆ Single draw per frame |
| Avoid `sortableChildren` on large containers | ⬆ Removes O(n log n) sort |
| Use `BitmapText` instead of `Text` for dynamic labels | ⬆⬆ GPU batched |
| Manual culling with `Culler.shared.cull()` | ⬆⬆ Skip off-screen draw |
| Set `ticker.maxFPS = 30` on mobile | ⬆ Saves battery |
| `app.ticker.stop()` when tab is hidden | ⬆ Zero CPU when inactive |

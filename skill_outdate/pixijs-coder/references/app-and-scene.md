# App & Scene Graph — PixiJS v8

## Application Setup

```typescript
import { Application } from 'pixi.js';

const app = new Application();

// MUST await init — constructor no longer accepts options
await app.init({
  width: 800,
  height: 600,
  background: 0x1a1a2e,        // hex number or CSS string '#1a1a2e'
  backgroundAlpha: 1,
  antialias: true,
  resolution: window.devicePixelRatio || 1,
  autoDensity: true,
  preference: 'webgl',          // 'webgl' | 'webgpu' — WebGPU auto-fallback if unsupported
  powerPreference: 'high-performance',
  hello: true,                  // logs PixiJS version to console
});

// app.canvas — NOT app.view (renamed in v8)
document.getElementById('game')!.appendChild(app.canvas);

// Resize
app.renderer.resize(window.innerWidth, window.innerHeight);

// Responsive resize
window.addEventListener('resize', () => {
  app.renderer.resize(window.innerWidth, window.innerHeight);
});

// Destroy cleanly
app.destroy(true, { children: true, texture: true });
```

## Container — Only Class That Can Have Children

```typescript
import { Container, Sprite } from 'pixi.js';

const scene = new Container();
app.stage.addChild(scene);

// Container properties
scene.label = 'GameScene';      // NOT .name (renamed in v8)
scene.position.set(100, 200);
scene.scale.set(2);
scene.rotation = Math.PI / 4;
scene.alpha = 0.8;
scene.visible = false;
scene.zIndex = 10;             // sorting within parent
scene.sortableChildren = true; // enable zIndex sort

// Add/remove children
scene.addChild(sprite);
scene.removeChild(sprite);
scene.addChildAt(sprite, 0);   // insert at index
scene.removeChildren();        // remove all

// Traversal
scene.children.forEach(child => { /* ... */ });
scene.getChildAt(0);
scene.getChildIndex(sprite);
scene.setChildIndex(sprite, 2);
```

## CRITICAL: Leaf Node Constraint

Only `Container` can have `.addChild()`. These are **leaf nodes** — they cannot have children:
- `Sprite`
- `Graphics`
- `Mesh`
- `Text`, `BitmapText`, `HTMLText`
- `TilingSprite`
- `AnimatedSprite`
- `ParticleContainer`

If you need to group a Sprite with other objects, wrap in a Container:
```typescript
// WRONG — Sprite is a leaf node
sprite.addChild(anotherSprite); // ❌ TypeError

// CORRECT
const group = new Container();
group.addChild(sprite);
group.addChild(anotherSprite); // ✅
```

## Transform & Coordinate Space

```typescript
// Local vs world position
sprite.position.set(50, 50);            // local to parent
sprite.getGlobalPosition();             // world position (Point)

// Convert between spaces
const worldPoint = sprite.toGlobal({ x: 0, y: 0 });
const localPoint = sprite.toLocal({ x: 400, y: 300 });

// Point class
import { Point } from 'pixi.js';
const p = new Point(100, 200);
const p2 = sprite.worldTransform.apply(p); // apply matrix transform
```

## Bounds

```typescript
// getBounds() returns Bounds object — access .rectangle for the rect
const bounds = sprite.getBounds();
const rect = bounds.rectangle;          // NOT bounds directly
console.log(rect.x, rect.y, rect.width, rect.height);

// Local bounds
const localBounds = sprite.getLocalBounds();
const localRect = localBounds.rectangle;
```

## RenderGroup — GPU-Offloaded Container

For large, stable sub-trees (e.g., a HUD that doesn't move often):
```typescript
const hud = new Container();
hud.isRenderGroup = true;   // GPU handles its own transform matrix
app.stage.addChild(hud);

// This container's children are batched into a single GPU draw group
// Moving hud itself is very cheap — only a matrix uniform update
```

Use RenderGroup when:
- Container has many children that rarely change internally
- You need layer-level opacity/blend without redrawing children
- Performance profiling shows expensive re-sort or batch breaks

## onRender — Replaces updateTransform

```typescript
// v7 (WRONG in v8):
class MySprite extends Sprite {
  updateTransform() { super.updateTransform(); /* ... */ } // ❌ removed
}

// v8 CORRECT:
class MySprite extends Sprite {
  constructor() {
    super();
    this.onRender = this._update.bind(this);
  }
  _update() {
    // called every frame before this object is rendered
    this.rotation += 0.01;
  }
}
```

## cacheAsTexture — Replaces cacheAsBitmap

```typescript
// v7 (WRONG in v8):
container.cacheAsBitmap = true; // ❌ removed

// v8 CORRECT:
container.cacheAsTexture(true);
container.cacheAsTexture(false); // disable
container.updateCacheTexture();  // force refresh if content changed
```

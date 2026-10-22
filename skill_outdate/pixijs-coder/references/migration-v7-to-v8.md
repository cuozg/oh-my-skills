# Migration v7 → v8 — PixiJS

## Quick Reference Table

| v7 | v8 | Notes |
|---|---|---|
| `new Application({ width, height })` | `const app = new Application(); await app.init({ width, height })` | **Async init required** |
| `import { Sprite } from '@pixi/sprite'` | `import { Sprite } from 'pixi.js'` | All from single package |
| `Texture.from('url.png')` | `await Assets.load('url.png')` | No URL auto-fetch in Texture.from |
| `app.view` | `app.canvas` | Renamed |
| `container.name` | `container.label` | Renamed |
| `cacheAsBitmap = true` | `cacheAsTexture(true)` | Method call now |
| `ticker.add((delta) => {})` | `ticker.add((ticker) => { ticker.deltaTime })` | Callback receives Ticker |
| `new BlurFilter(8, 4)` | `new BlurFilter({ blur: 8, quality: 4 })` | Object options |
| `DisplayObject` | `Container` | Base class removed |
| `updateTransform()` override | `this.onRender = () => {}` | Override method replaced |
| `container.getBounds()` → Rectangle | `container.getBounds().rectangle` | Returns Bounds wrapper |
| `pointermove` fires everywhere | `globalpointermove` for global tracking | `pointermove` = on-object only |
| `beginFill(0xff)` / `endFill()` | `.rect(...).fill(0xff)` | Build-then-fill pattern |
| `drawRect(x,y,w,h)` | `.rect(x,y,w,h)` | All draw* → bare names |
| `drawCircle(x,y,r)` | `.circle(x,y,r)` | |
| `drawPolygon([...])` | `.poly([...])` | |
| `ParticleContainer` + Sprite | `ParticleContainer` + `Particle` | New Particle object |
| `Loader.shared.load(...)` | `Assets.load(...)` | Loader removed |
| `loader.add(name, url)` | `Assets.add({ alias, src })` | |
| `settings.RESOLUTION` | `AbstractRenderer.defaultOptions.resolution` | settings removed |
| `PIXI.settings.SCALE_MODE` | Set via TextureSource or app.init options | |
| `BaseTexture` | `ImageSource`, `CanvasSource`, etc. | Replaced by Source classes |
| `Sprite.from('url')` (auto-loads) | Must `await Assets.load('url')` first | No implicit loading |
| `new Graphics().beginFill(c).drawRect(...).endFill()` | `new Graphics().rect(...).fill(c)` | |
| `g.lineStyle(2, 0xff)` | `.stroke({ width: 2, color: 0xff })` | |
| `g.drawStar(...)` | `.star(...)` | |
| `container.addChild()` on Sprite | Only `Container` can have children | Sprites are leaf nodes |
| `new Text('hello', style)` | `new Text({ text: 'hello', style })` | Options object |
| `new BitmapText('hi', { fontName })` | `new BitmapText({ text: 'hi', style: { fontFamily } })` | |
| `eventMode` default `'auto'` | `eventMode` default `'passive'` | Must explicitly opt in |
| `GraphicsGeometry` | `GraphicsContext` | For shared geometry |
| Auto-culling | Manual: `Culler.shared.cull(stage, bounds)` | No longer automatic |

## App Setup Migration

```typescript
// v7:
const app = new PIXI.Application({
  width: 800, height: 600, backgroundColor: 0x1a1a2e,
});
document.body.appendChild(app.view);

// v8:
import { Application } from 'pixi.js';
const app = new Application();
await app.init({ width: 800, height: 600, background: '#1a1a2e' });
document.body.appendChild(app.canvas); // .view → .canvas
```

## Asset Loading Migration

```typescript
// v7:
PIXI.Loader.shared.add('hero', '/images/hero.png');
PIXI.Loader.shared.load((loader, resources) => {
  const sprite = new PIXI.Sprite(resources.hero.texture);
});

// v8:
const texture = await Assets.load<Texture>('/images/hero.png');
const sprite = new Sprite(texture);
```

## Graphics Migration

```typescript
// v7:
const g = new Graphics();
g.lineStyle(3, 0xffffff, 1);
g.beginFill(0x3498db, 0.8);
g.drawRect(0, 0, 100, 100);
g.endFill();
g.drawCircle(50, 50, 30);

// v8:
const g = new Graphics();
g.rect(0, 0, 100, 100)
  .fill({ color: 0x3498db, alpha: 0.8 })
  .stroke({ color: 0xffffff, width: 3 });
g.circle(50, 50, 30).fill(0x3498db);
```

## Loader → Assets Migration

```typescript
// v7 manifest-style:
PIXI.Loader.shared
  .add('spritesheet', '/sprites/game.json')
  .add('font', '/fonts/ui.fnt')
  .load(onComplete);

// v8:
await Assets.init({
  manifest: {
    bundles: [{
      name: 'game',
      assets: [
        { alias: 'spritesheet', src: '/sprites/game.json' },
        { alias: 'font', src: '/fonts/ui.fnt' },
      ],
    }],
  },
});
await Assets.loadBundle('game', onProgress);
```

## Ticker Migration

```typescript
// v7:
app.ticker.add((delta) => {
  sprite.rotation += 0.01 * delta; // delta is a number
});

// v8:
app.ticker.add((ticker) => {
  sprite.rotation += 0.01 * ticker.deltaTime; // ticker is a Ticker instance
});
```

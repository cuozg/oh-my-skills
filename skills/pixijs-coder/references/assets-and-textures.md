# Assets & Textures — PixiJS v8

## Assets — Primary Loading API

```typescript
import { Assets, Texture, Sprite } from 'pixi.js';

// Single asset
const texture = await Assets.load<Texture>('/images/hero.png');

// Multiple assets in parallel
const [heroTex, bgTex] = await Promise.all([
  Assets.load<Texture>('/images/hero.png'),
  Assets.load<Texture>('/images/background.png'),
]);

// Load multiple with progress
const assets = await Assets.load(
  ['/images/hero.png', '/images/enemy.png'],
  (progress) => console.log(`Loading: ${Math.round(progress * 100)}%`)
);
// assets is a record: { '/images/hero.png': Texture, ... }
```

## CRITICAL: Texture.from() Does NOT Load URLs

```typescript
// v7 (WRONG in v8 for remote URLs):
const tex = Texture.from('https://example.com/image.png'); // ❌ won't fetch

// v8 CORRECT — always await Assets.load for remote resources:
const tex = await Assets.load('https://example.com/image.png'); // ✅

// Texture.from() is still valid for already-loaded aliases:
Assets.add({ alias: 'hero', src: '/images/hero.png' });
await Assets.load('hero');
const tex = Texture.from('hero'); // ✅ works after load
```

## Bundles & Manifests

```typescript
// Define a manifest (usually loaded from JSON)
await Assets.init({
  manifest: {
    bundles: [
      {
        name: 'game-screen',
        assets: [
          { alias: 'hero', src: '/images/hero.png' },
          { alias: 'enemy', src: '/images/enemy.png' },
          { alias: 'tilemap', src: '/tilemaps/level1.json' },
        ],
      },
      {
        name: 'ui',
        assets: [
          { alias: 'button', src: '/ui/button.png' },
          { alias: 'font', src: '/fonts/game.fnt' },
        ],
      },
    ],
  },
});

// Load a bundle
await Assets.loadBundle('game-screen', (progress) => {
  loadingBar.width = progress * 400;
});

// Background load
Assets.backgroundLoadBundle('ui'); // starts loading without blocking

// Get already-loaded asset
const hero = Assets.get<Texture>('hero');
```

## Asset Caching & Aliases

```typescript
// Add alias before loading
Assets.add({ alias: ['hero', 'player'], src: '/images/hero.png' });
await Assets.load('hero');

const tex1 = Assets.get<Texture>('hero');   // same texture
const tex2 = Assets.get<Texture>('player'); // same texture

// Unload / release
await Assets.unload('hero');
await Assets.unloadBundle('game-screen');
```

## Texture Sources (v8 replaces BaseTexture)

v8 has no `BaseTexture`. Sources are:

| Source Class | Use For |
|---|---|
| `ImageSource` | PNG, JPG, WebP, AVIF |
| `CanvasSource` | HTMLCanvasElement |
| `VideoSource` | HTMLVideoElement |
| `BufferSource` | Raw pixel data (Uint8Array) |

```typescript
import { Texture, ImageSource, CanvasSource } from 'pixi.js';

// From canvas
const canvas = document.createElement('canvas');
canvas.width = 256; canvas.height = 256;
const ctx = canvas.getContext('2d')!;
ctx.fillStyle = 'red';
ctx.fillRect(0, 0, 256, 256);

const source = new CanvasSource({ resource: canvas });
const texture = new Texture({ source });

// From raw buffer
const buffer = new Uint8Array(256 * 256 * 4); // RGBA
const bufSource = new BufferSource({ resource: buffer, width: 256, height: 256 });
const bufTexture = new Texture({ source: bufSource });
```

## Sprite Sheets / Texture Atlases

```typescript
// Load spritesheet JSON (TexturePacker / ShoeBox format)
await Assets.load('/sprites/characters.json');

// Access frames by name
const heroIdle = Texture.from('hero_idle_0001.png');
const heroRun  = Texture.from('hero_run_0001.png');
```

## Video Textures

```typescript
const videoTex = await Assets.load<Texture>({
  src: '/video/cutscene.mp4',
  loadParser: 'loadVideo',
  data: {
    autoPlay: true,
    loop: true,
    muted: true, // required for autoplay in browsers
  },
});
const videoSprite = new Sprite(videoTex);
```

## Texture Regions (sub-textures)

```typescript
import { Texture, Rectangle } from 'pixi.js';

const sheet = await Assets.load<Texture>('/images/spritesheet.png');
const frame = new Texture({
  source: sheet.source,
  frame: new Rectangle(0, 0, 64, 64), // x, y, width, height
});
```

## Cleanup

```typescript
// Destroy texture and its GPU resource
texture.destroy(true); // true = also destroy source

// Sprite cleanup
sprite.destroy({ texture: true, textureSource: true });
```

# TypeScript — PixiJS v8

## Typed Application

```typescript
import { Application, Container, Sprite, Texture } from 'pixi.js';

// Generic Application<T> types the stage
const app = new Application<HTMLCanvasElement>();
await app.init({ width: 800, height: 600 });

// app.canvas is typed as HTMLCanvasElement
document.body.appendChild(app.canvas); // ✅ no cast needed

// For OffscreenCanvas:
const offscreen = new Application<OffscreenCanvas>();
```

## Generic Container

```typescript
import { Container, Sprite } from 'pixi.js';

// Untyped Container (any child type):
const scene = new Container();

// Typed Container — restricts what .addChild accepts:
const spriteLayer = new Container<Sprite>();
spriteLayer.addChild(new Sprite(texture)); // ✅
// spriteLayer.addChild(new Graphics()); // ❌ TypeScript error

// Access typed children:
const first: Sprite = spriteLayer.getChildAt(0);
```

## Event Type Annotations

```typescript
import {
  FederatedPointerEvent,
  FederatedWheelEvent,
  FederatedMouseEvent,
} from 'pixi.js';

sprite.on('pointerdown', (e: FederatedPointerEvent) => {
  const x: number = e.global.x;
  const y: number = e.global.y;
  const target: EventTarget = e.target;
});

container.on('wheel', (e: FederatedWheelEvent) => {
  const delta: number = e.deltaY;
});
```

## Typed Assets.load

```typescript
import { Assets, Texture, Spritesheet } from 'pixi.js';

// Single texture
const tex = await Assets.load<Texture>('/images/hero.png');
// tex is Texture, not Texture | unknown

// Spritesheet
const sheet = await Assets.load<Spritesheet>('/sprites/game.json');
const frame: Texture = sheet.textures['hero.png'];

// Multiple assets — record type
const assets = await Assets.load<{ hero: Texture; bg: Texture }>({
  hero: '/images/hero.png',
  bg: '/images/bg.png',
});
```

## Custom Classes

```typescript
import { Container, Sprite, Texture, Ticker } from 'pixi.js';

class Player extends Container {
  private sprite: Sprite;
  speed = 200; // pixels/second

  constructor(texture: Texture) {
    super();
    this.sprite = new Sprite(texture);
    this.sprite.anchor.set(0.5);
    this.addChild(this.sprite);
    this.onRender = this.update.bind(this);
    this.label = 'Player';
  }

  private update(): void {
    // Called each frame before rendering
  }

  move(dx: number, dy: number, deltaMS: number): void {
    this.x += dx * this.speed * (deltaMS / 1000);
    this.y += dy * this.speed * (deltaMS / 1000);
  }

  destroy(): void {
    // cleanup
    super.destroy({ children: true });
  }
}
```

## Type Utilities

```typescript
import type {
  ColorSource,     // 0xff0000 | '#ff0000' | [1,0,0] | Color
  PointData,       // { x: number, y: number }
  Size,            // { width: number, height: number }
  Rectangle,       // x, y, width, height
  DestroyOptions,  // { children?, texture?, textureSource? }
  TextureOptions,  // for new Texture({...})
  ApplicationOptions, // for app.init({...})
} from 'pixi.js';

// ColorSource is useful for accepting any color format:
function setColor(g: Graphics, color: ColorSource) {
  g.circle(0, 0, 20).fill(color);
}
setColor(g, 0xff0000);
setColor(g, '#ff0000');
setColor(g, [1, 0, 0]);
```

## Type Narrowing for Renderer

```typescript
import { WebGLRenderer, WebGPURenderer } from 'pixi.js';

if (app.renderer instanceof WebGLRenderer) {
  // WebGL-specific APIs
  const gl = app.renderer.gl; // WebGLRenderingContext
} else if (app.renderer instanceof WebGPURenderer) {
  // WebGPU-specific APIs
  const device = app.renderer.device; // GPUDevice
}
```

## Shader Uniform Typing

```typescript
import { UniformGroup } from 'pixi.js';

// Type the uniform struct
interface MyUniforms {
  uTime: number;
  uResolution: [number, number];
  uColor: [number, number, number, number];
}

const uniforms: UniformGroup<MyUniforms> = new UniformGroup({
  uTime: { value: 0, type: 'f32' },
  uResolution: { value: [800, 600], type: 'vec2<f32>' },
  uColor: { value: [1, 0, 0, 1], type: 'vec4<f32>' },
});
```

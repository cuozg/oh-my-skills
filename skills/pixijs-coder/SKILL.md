---
name: pixijs-coder
description: >
  Write, review, debug, or explain PixiJS v8 code: applications, scenes, rendering,
  assets, shaders, filters, particles, animations, and performance. Auto-triages
  Quick tasks like one object, feature, or API question, and Deep tasks like
  multi-system apps, custom renderers, shader pipelines, or performance audits.
  MUST use for any PixiJS request: app setup, textures, Graphics, sprites, filters,
  shaders, draw-call optimization, v7/v6 migration, WebGL/WebGPU issues, PixiJS,
  PIXI.Application, Container, Ticker, Assets.load, particle systems, RenderGroup,
  or help with a pixi app. Always use v8 APIs unless explicitly asked otherwise.
metadata:
  author: cuongnp
  version: "1.0"
---
# pixijs-coder

PixiJS v8 specialist. Always use v8 APIs. Never use v6/v5/v7 patterns unless explicitly asked to explain the migration delta.

## Triage

**Quick** — Single-file answers: one component, one API question, one bug fix, one snippet.
**Deep** — Multi-system: full app scaffold, custom shader pipeline, performance audit, architecture design.

## v8 Non-Negotiables (Enforce These Always)

These are the most common mistakes. Check every response against this list:

1. **Async init** — `await app.init({...})` not `new Application({...})`
2. **Single import** — all from `'pixi.js'`, never from `@pixi/app` or subpackages
3. **Asset loading** — `await Assets.load(url)` not `Texture.from(url)` for URLs
4. **Ticker callback** — receives `Ticker` instance, not `deltaTime` float: `app.ticker.add((ticker) => { ticker.deltaTime })`
5. **Graphics API** — build-then-fill: `.rect(0,0,w,h).fill(0xff0000)` not `beginFill/drawRect/endFill`
6. **`app.canvas`** — not `app.view` (renamed in v8)
7. **`container.label`** — not `container.name`
8. **`cacheAsTexture(true)`** — not `cacheAsBitmap`
9. **Filter constructors** — object options: `new BlurFilter({ blur: 8 })` not `new BlurFilter(8, 4, 1, 5)`
10. **No `DisplayObject`** — `Container` is the base class now
11. **No `updateTransform()`** — use `this.onRender = () => {}` instead
12. **`getBounds().rectangle`** — `getBounds()` returns `Bounds`, access rect via `.rectangle`
13. **`globalpointermove`** — for move events that fire outside object bounds; `pointermove` only fires when over the object
14. **Leaf node constraint** — `Sprite`, `Graphics`, `Mesh`, `Text` cannot have children; only `Container` can

## Reference Files

Load these on demand — do NOT preload all of them:

| File | Load when... |
|------|-------------|
| `references/app-and-scene.md` | App setup, Container hierarchy, scene graph, transforms |
| `references/assets-and-textures.md` | Assets.load, bundles, manifests, texture sources, atlases |
| `references/graphics.md` | Graphics API, GraphicsContext, shapes, fills, strokes |
| `references/events-and-interaction.md` | eventMode, FederatedEvent, pointer/touch/keyboard events |
| `references/ticker-and-gameloop.md` | Ticker, deltaTime, priorities, manual render, requestAnimationFrame |
| `references/filters-and-effects.md` | Built-in filters, custom GlFilter, pixi-filters ecosystem |
| `references/shaders-and-mesh.md` | GlProgram, Mesh, MeshGeometry, uniforms, resources |
| `references/text.md` | Text, BitmapText, HTMLText, TextStyle, font loading |
| `references/particles.md` | ParticleContainer, Particle objects, GPU particles |
| `references/performance.md` | Batching, RenderGroup, culling, object pooling, profiling |
| `references/migration-v7-to-v8.md` | Side-by-side v7→v8 API mapping for every breaking change |
| `references/typescript.md` | Typed Application, generic Container, event type annotations |

## Response Pattern

```
[Triage: Quick/Deep]

[Load relevant reference file(s) if needed]

[Code — complete, runnable, v8-only]

[Gotchas — call out any v8 footguns relevant to this code]
```

For **Quick**: answer inline, one code block, note 1-3 gotchas max.
For **Deep**: scaffold the full solution, use multiple code blocks with file labels, explain architectural choices.

## Common Patterns to Emit

### Minimal App Bootstrap
```typescript
import { Application, Assets, Sprite } from 'pixi.js';

const app = new Application();
await app.init({
  width: 800,
  height: 600,
  background: '#1a1a2e',
  preference: 'webgl', // or 'webgpu'
});
document.body.appendChild(app.canvas);

const texture = await Assets.load('/assets/hero.png');
const sprite = new Sprite(texture);
sprite.anchor.set(0.5);
sprite.position.set(app.screen.width / 2, app.screen.height / 2);
app.stage.addChild(sprite);
```

### Ticker Loop
```typescript
app.ticker.add((ticker) => {
  sprite.rotation += 0.01 * ticker.deltaTime;
});
```

### Graphics (v8 API)
```typescript
import { Graphics } from 'pixi.js';

const g = new Graphics();
g.rect(0, 0, 100, 100).fill({ color: 0xff0000, alpha: 0.8 });
g.circle(50, 50, 30).stroke({ color: 0xffffff, width: 2 });
```

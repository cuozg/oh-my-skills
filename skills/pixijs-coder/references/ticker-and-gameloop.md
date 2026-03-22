# Ticker & Game Loop — PixiJS v8

## Basic Usage

```typescript
import { Application, Ticker } from 'pixi.js';

const app = new Application();
await app.init({ ... });

// CRITICAL v8 change: callback receives Ticker instance, NOT a deltaTime float
// v7 (WRONG in v8):
app.ticker.add((delta) => { sprite.x += 5 * delta; }); // ❌

// v8 CORRECT:
app.ticker.add((ticker: Ticker) => {
  sprite.x += 5 * ticker.deltaTime;    // frame-rate-independent delta (normalized to 60fps)
  sprite.rotation += 0.01 * ticker.deltaTime;
});
```

## Ticker Properties

```typescript
app.ticker.add((ticker: Ticker) => {
  ticker.deltaTime;       // delta normalized to 60fps (1.0 at 60fps, 2.0 at 30fps)
  ticker.deltaMS;         // actual elapsed milliseconds since last frame
  ticker.elapsedMS;       // total elapsed ms since ticker start
  ticker.lastTime;        // timestamp of last frame (ms)
  ticker.speed;           // ticker speed multiplier (1 = normal)
  ticker.FPS;             // current frames per second
  ticker.minFPS;          // min FPS cap (default 10)
  ticker.maxFPS;          // max FPS cap (default 0 = uncapped)
});

// Slow motion effect
app.ticker.speed = 0.5;    // half speed
app.ticker.speed = 2.0;    // double speed

// Cap frame rate
app.ticker.maxFPS = 30;    // limit to 30fps (saves battery on mobile)
```

## Priorities

Listeners run in priority order (higher = earlier):

```typescript
import { UPDATE_PRIORITY } from 'pixi.js';

// Priority constants:
UPDATE_PRIORITY.SYSTEM   = 100  // reserved for PixiJS internal
UPDATE_PRIORITY.HIGH     = 25   // physics, input
UPDATE_PRIORITY.NORMAL   = 0    // (default) game logic
UPDATE_PRIORITY.LOW      = -25  // post-processing, UI update
UPDATE_PRIORITY.UTILITY  = -50  // background tasks

// Custom priority
app.ticker.add(updatePhysics, UPDATE_PRIORITY.HIGH);
app.ticker.add(updateGame, UPDATE_PRIORITY.NORMAL);
app.ticker.add(updateHUD, UPDATE_PRIORITY.LOW);
```

## Removing Listeners

```typescript
const handler = (ticker: Ticker) => { /* ... */ };

// Add
app.ticker.add(handler);

// Remove by reference
app.ticker.remove(handler);

// One-shot (fires once, then auto-removes)
app.ticker.addOnce(handler);
```

## Shared Ticker

```typescript
// The global ticker — runs always, independent of any app
import { Ticker } from 'pixi.js';

const sharedTicker = Ticker.shared;
sharedTicker.add((ticker: Ticker) => {
  // global update
});

// Ticker.system — reserved for PixiJS internal use, don't use directly
```

## Manual Render Loop

Disable auto-render and control it yourself:
```typescript
await app.init({
  autoStart: false,  // don't start the ticker
});

// Custom loop
let lastTime = 0;
function loop(timestamp: number) {
  const delta = timestamp - lastTime;
  lastTime = timestamp;

  // Update logic
  sprite.x += 100 * (delta / 1000);

  // Manually render
  app.renderer.render(app.stage);

  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
```

## Pause / Resume

```typescript
app.ticker.stop();   // pause
app.ticker.start();  // resume

// Render one frame while paused (for debug/screenshots)
app.renderer.render(app.stage);
```

## Time-Based Animation (Tweens)

PixiJS has no built-in tween system. Common libraries:
- **GSAP** — `gsap.to(sprite, { x: 400, duration: 1 })`
- **@pixi/motion** — lightweight tweens
- Manual using `elapsedMS`:

```typescript
const startX = 0, targetX = 400, duration = 1000;
let elapsed = 0;
let done = false;

app.ticker.add((ticker: Ticker) => {
  if (done) return;
  elapsed += ticker.deltaMS;
  const t = Math.min(elapsed / duration, 1);
  // ease in-out
  const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
  sprite.x = startX + (targetX - startX) * ease;
  if (t >= 1) done = true;
});
```

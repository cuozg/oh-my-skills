# Graphics API — PixiJS v8

## v8 Build-Then-Fill Pattern

v8 completely replaces the v7 `beginFill/endFill` API with a chainable build-then-fill pattern.

```typescript
import { Graphics } from 'pixi.js';

const g = new Graphics();

// WRONG (v7 style — does not work in v8):
g.beginFill(0xff0000);
g.drawRect(0, 0, 100, 50);
g.endFill(); // ❌

// CORRECT (v8):
g.rect(0, 0, 100, 50).fill(0xff0000); // ✅
```

## Shape Methods

```typescript
const g = new Graphics();

// Rectangles
g.rect(x, y, width, height);
g.roundRect(x, y, width, height, radius);

// Circles & Ellipses
g.circle(cx, cy, radius);
g.ellipse(cx, cy, halfWidth, halfHeight);

// Arcs
g.arc(cx, cy, radius, startAngle, endAngle, anticlockwise);
g.arcTo(x1, y1, x2, y2, radius);

// Polygons & Paths
g.poly([x1, y1, x2, y2, x3, y3]);           // flat array
g.poly([{ x: 0, y: 0 }, { x: 100, y: 0 }]); // point objects
g.path(svgPath);                              // SVG path string

// Lines
g.moveTo(0, 0).lineTo(100, 100);
g.bezierCurveTo(cp1x, cp1y, cp2x, cp2y, x, y);
g.quadraticCurveTo(cpx, cpy, x, y);

// Star shape
g.star(cx, cy, points, outerRadius, innerRadius, rotation);
```

## Fill & Stroke

```typescript
// Fill with color
g.rect(0, 0, 100, 100).fill(0xff0000);

// Fill with options
g.rect(0, 0, 100, 100).fill({ color: 0xff0000, alpha: 0.5 });

// Fill with texture
const tex = await Assets.load<Texture>('/pattern.png');
g.rect(0, 0, 200, 200).fill({ texture: tex, alpha: 1 });

// Stroke
g.rect(0, 0, 100, 100).stroke({ color: 0xffffff, width: 2, alpha: 1 });

// Stroke options
g.circle(50, 50, 40).stroke({
  color: 0x00ff00,
  width: 3,
  alignment: 0,   // 0 = inside, 0.5 = center (default), 1 = outside
  join: 'round',  // 'miter' | 'round' | 'bevel'
  cap: 'round',   // 'butt' | 'round' | 'square'
  miterLimit: 10,
});

// Both fill and stroke on same shape:
g.rect(0, 0, 100, 100)
  .fill({ color: 0x3498db, alpha: 0.8 })
  .stroke({ color: 0xffffff, width: 2 });
```

## Chaining Multiple Shapes

```typescript
const g = new Graphics();

g
  .rect(0, 0, 200, 100).fill(0x3498db)
  .circle(100, 50, 30).fill(0xe74c3c).stroke({ color: 0xffffff, width: 2 })
  .moveTo(0, 120).lineTo(200, 120).stroke({ color: 0xffffff, width: 1 });

app.stage.addChild(g);
```

## Dynamic Updates

```typescript
const g = new Graphics();
app.stage.addChild(g);

// Redraw every frame — clear and rebuild
app.ticker.add(() => {
  g.clear(); // removes all previous geometry
  g.circle(mouseX, mouseY, 20).fill(0xff0000);
});
```

## GraphicsContext — Shared Geometry

When you want multiple Graphics objects to share the same geometry (e.g., 1000 identical tiles):

```typescript
import { GraphicsContext, Graphics } from 'pixi.js';

// Build the geometry once
const ctx = new GraphicsContext();
ctx.rect(0, 0, 32, 32).fill(0x00ff00);

// Reuse across many Graphics instances (no GPU duplication)
for (let i = 0; i < 1000; i++) {
  const g = new Graphics(ctx);
  g.position.set((i % 50) * 32, Math.floor(i / 50) * 32);
  app.stage.addChild(g);
}

// Swap context at runtime (e.g., change sprite frame)
const ctx2 = new GraphicsContext();
ctx2.rect(0, 0, 32, 32).fill(0xff0000);
g.context = ctx2; // all instances using ctx2 update visually
```

## Holes / Cut-Outs

```typescript
const g = new Graphics();

// Draw outer shape, then cut a hole
g.rect(0, 0, 200, 200).fill(0x3498db);
g.circle(100, 100, 50).cut(); // cuts a hole — no fill/stroke, uses winding rule
```

## Hit Area Override

Graphics hit-tests against drawn geometry by default. Override:
```typescript
import { Graphics, Circle } from 'pixi.js';

const g = new Graphics();
g.star(0, 0, 5, 50, 25).fill(0xffcc00);

// Make click area a simple circle regardless of star shape
g.hitArea = new Circle(0, 0, 55);
g.eventMode = 'static';
g.on('pointerdown', () => console.log('clicked'));
```

## Gradient Fills (v8.2+)

```typescript
import { Graphics, FillGradient } from 'pixi.js';

const gradient = new FillGradient(0, 0, 0, 100); // x0, y0, x1, y1 (linear)
gradient.addColorStop(0, 0x0000ff);
gradient.addColorStop(0.5, 0x00ffff);
gradient.addColorStop(1, 0x0000ff);

const g = new Graphics();
g.rect(0, 0, 200, 100).fill(gradient);
```

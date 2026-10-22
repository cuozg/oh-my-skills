# Particles — PixiJS v8

## ParticleContainer (v8 Overhaul)

v8 `ParticleContainer` uses `Particle` objects instead of `Sprite` objects.

```typescript
import { ParticleContainer, Particle, Texture, Assets } from 'pixi.js';

const texture = await Assets.load<Texture>('/images/particle.png');

const container = new ParticleContainer({
  dynamicProperties: {
    position: true,   // particles move
    rotation: true,   // particles rotate
    scale: true,      // particles scale
    color: true,      // particles tint/alpha
  },
});
app.stage.addChild(container);

// Create particles using Particle objects (NOT Sprite)
for (let i = 0; i < 1000; i++) {
  const particle = new Particle({
    texture,
    x: Math.random() * 800,
    y: Math.random() * 600,
    scaleX: Math.random() * 0.5 + 0.5,
    scaleY: Math.random() * 0.5 + 0.5,
    rotation: Math.random() * Math.PI * 2,
    color: 0xffffff,  // hex tint
    alpha: Math.random(),
    anchorX: 0.5,
    anchorY: 0.5,
  });
  container.addParticle(particle);
}

// Update particles each frame
app.ticker.add((ticker) => {
  for (const particle of container.particleChildren) {
    particle.x += Math.random() * 2 - 1;
    particle.y -= 1 * ticker.deltaTime;
    particle.alpha -= 0.005 * ticker.deltaTime;

    if (particle.alpha <= 0) {
      container.removeParticle(particle);
    }
  }
});
```

## Particle Object Properties

```typescript
const p = new Particle({
  texture: Texture,
  x: number,
  y: number,
  scaleX: number,       // default 1
  scaleY: number,       // default 1
  rotation: number,     // radians
  color: number,        // hex color tint
  alpha: number,        // 0-1
  anchorX: number,      // 0-1 (default 0)
  anchorY: number,      // 0-1 (default 0)
});
```

## ParticleContainer vs Container

| Feature | `ParticleContainer` | Regular `Container` |
|---|---|---|
| Children | `Particle` objects only | Any display object |
| Rendering | Single GPU draw call | Multiple draw calls |
| Performance | Very fast (1000s of particles) | Slower |
| Filters | ❌ Not supported | ✅ Supported |
| Events | ❌ Not on individual particles | ✅ Per-object |
| Nested children | ❌ | ✅ |

Use `ParticleContainer` when: large numbers (100+), same texture, no filters needed.
Use regular `Container` + `Sprite` when: fewer objects, need events/filters per particle.

## Simple Particle System Pattern

```typescript
interface ParticleData {
  particle: Particle;
  vx: number;
  vy: number;
  life: number;
  maxLife: number;
}

class ParticleSystem {
  container: ParticleContainer;
  particles: ParticleData[] = [];
  texture: Texture;

  constructor(texture: Texture, stage: Container) {
    this.texture = texture;
    this.container = new ParticleContainer({
      dynamicProperties: { position: true, scale: true, color: true },
    });
    stage.addChild(this.container);
  }

  emit(x: number, y: number, count = 10) {
    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = Math.random() * 3 + 1;
      const life = Math.random() * 60 + 30;

      const p = new Particle({
        texture: this.texture,
        x, y,
        anchorX: 0.5, anchorY: 0.5,
        scaleX: Math.random() * 0.5 + 0.3,
        scaleY: Math.random() * 0.5 + 0.3,
      });
      this.container.addParticle(p);
      this.particles.push({
        particle: p,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        life,
        maxLife: life,
      });
    }
  }

  update(ticker: Ticker) {
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const d = this.particles[i];
      d.particle.x += d.vx * ticker.deltaTime;
      d.particle.y += d.vy * ticker.deltaTime;
      d.vy += 0.1 * ticker.deltaTime; // gravity
      d.life -= ticker.deltaTime;
      d.particle.alpha = d.life / d.maxLife;

      if (d.life <= 0) {
        this.container.removeParticle(d.particle);
        this.particles.splice(i, 1);
      }
    }
  }
}
```

## Third-Party Particle Libraries

- **@pixi/particle-emitter** — feature-rich emitter with JSON config format
- **pixi-vfx** — GPU-based VFX

# Particles (v3.60+ API)

The particle system was overhauled in v3.60. The new API uses `addParticleEmitter` directly on a game object factory.

## Basic Emitter

```javascript
// Simple particle effect
const emitter = this.add.particles(400, 300, 'spark', {
  speed: { min: 100, max: 200 },
  scale: { start: 1, end: 0 },
  alpha: { start: 1, end: 0 },
  lifespan: 1000,
  blendMode: 'ADD',
  frequency: 50,     // ms between emissions
  quantity: 2,       // particles per emission
});
```

## Emitter Following a Sprite

```javascript
const emitter = this.add.particles(0, 0, 'dust', {
  speed: 30,
  scale: { start: 0.3, end: 0 },
  lifespan: 500,
  frequency: 100,
  follow: player,
  followOffset: { x: 0, y: 20 },
});
```

## One-Shot (Explosion)

```javascript
const explosion = this.add.particles(x, y, 'particle', {
  speed: { min: 50, max: 200 },
  angle: { min: 0, max: 360 },
  scale: { start: 0.8, end: 0 },
  lifespan: 600,
  gravityY: 200,
  emitting: false,  // don't auto-emit
});

explosion.explode(20); // emit 20 particles at once
```

## Emission Zones

```javascript
const emitter = this.add.particles(400, 300, 'snow', {
  speed: { min: 20, max: 60 },
  lifespan: 4000,
  gravityY: 50,
  quantity: 1,
  frequency: 200,
  emitZone: {
    type: 'random',
    source: new Phaser.Geom.Rectangle(-400, -10, 800, 20),
  },
});
```

## Death Zones

```javascript
// Particles die when entering this zone
const emitter = this.add.particles(400, 0, 'rain', {
  // ...
  deathZone: {
    type: 'onEnter',
    source: new Phaser.Geom.Rectangle(0, 550, 800, 50),
  },
});
```

## Tint & Color Transitions

```javascript
const emitter = this.add.particles(400, 300, 'flare', {
  tint: [0xff0000, 0xff8800, 0xffff00], // cycles through
  // or:
  color: [0xff0000, 0xffff00, 0x00ff00], // interpolates over lifespan
  colorEase: 'quad.out',
});
```

## Control

```javascript
emitter.start();           // begin emitting
emitter.stop();            // stop emitting (existing particles finish)
emitter.killAll();         // immediately destroy all particles
emitter.setFrequency(20);  // change emission rate
emitter.setPosition(x, y);
emitter.destroy();
```

## Gotchas

- **v3.60 breaking change**: the old `this.add.particles('key').createEmitter({...})` pattern is REMOVED — use `this.add.particles(x, y, 'key', config)` directly
- `emitting: false` + `explode(count)` for one-shot effects (explosions, hit effects)
- `blendMode: 'ADD'` creates glow effects — essential for fire, magic, energy
- `frequency: -1` means "only emit when `explode()` or `emitParticle()` is called"
- Particle count impacts performance — keep `quantity` and `lifespan` reasonable; use object pooling implicitly (Phaser recycles dead particles)

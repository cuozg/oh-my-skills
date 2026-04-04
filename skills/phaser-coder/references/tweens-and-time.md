# Tweens & Time

## Tweens

```javascript
// Basic tween
this.tweens.add({
  targets: sprite,
  x: 500,
  y: 300,
  alpha: 0.5,
  scale: 2,
  angle: 360,
  duration: 1000,
  ease: 'Power2',
  yoyo: true,
  repeat: -1,         // -1 = infinite
  delay: 500,
  hold: 200,          // pause at end before yoyo
  repeatDelay: 300,
  onComplete: () => { sprite.destroy(); },
  onUpdate: (tween, target, key, current) => { ... },
});
```

### Common Easing Functions
- `'Linear'` — constant speed
- `'Power1'` / `'Quad.easeOut'` — gentle deceleration
- `'Power2'` / `'Cubic.easeOut'` — moderate deceleration
- `'Power3'` / `'Quart.easeOut'` — strong deceleration
- `'Bounce.easeOut'` — bouncy landing
- `'Back.easeIn'` — overshoot start
- `'Elastic.easeOut'` — springy
- `'Sine.easeInOut'` — smooth breathing
- `'Stepped(5)'` — discrete steps

### Tween Chains (Timelines)

```javascript
const timeline = this.tweens.chain({
  targets: sprite,
  tweens: [
    { x: 500, duration: 500, ease: 'Power2' },
    { y: 400, duration: 300, ease: 'Bounce.easeOut' },
    { alpha: 0, duration: 200 },
  ],
  onComplete: () => { sprite.destroy(); },
});
```

### Tween Control

```javascript
const tween = this.tweens.add({ ... });
tween.pause();
tween.resume();
tween.stop();        // stops immediately
tween.complete();    // jumps to end
tween.remove();      // removes from tween manager
```

## Timers

```javascript
// Delayed call
this.time.delayedCall(2000, () => {
  this.spawnEnemy();
}, [], this);

// Repeating timer
this.spawnTimer = this.time.addEvent({
  delay: 1000,
  callback: this.spawnEnemy,
  callbackScope: this,
  repeat: 10,       // fires 11 times total (initial + 10 repeats)
  // loop: true,    // infinite
});

// Check timer
this.spawnTimer.getProgress();       // 0-1
this.spawnTimer.getElapsed();        // ms elapsed
this.spawnTimer.getRemainingSeconds();
this.spawnTimer.remove();            // cancel
```

## Clock

```javascript
// Pause/resume all timers in scene
this.time.paused = true;

// Time scale (slow motion)
this.time.timeScale = 0.5;  // half speed
this.tweens.timeScale = 0.5; // also slow tweens
this.physics.world.timeScale = 2; // Note: physics timeScale is INVERSE (2 = half speed)
```

## Gotchas

- Tweens target **any object property** — not just game objects. You can tween `{ value: 0 }` for custom interpolation
- `repeat: -1` with `yoyo: true` creates a perpetual back-and-forth
- Physics `timeScale` is the inverse of other time scales: 2 = half speed (it multiplies the physics step)
- `delayedCall` returns a TimerEvent — keep a reference to cancel it on scene shutdown
- Tweens are auto-destroyed on scene shutdown — no manual cleanup needed
- `chain()` replaces the old Timeline class (v3.60+)

# Matter.js Physics

Phaser wraps Matter.js for complex physics: polygonal bodies, compound shapes, constraints, sensors, and joints.

## Enabling

```javascript
const config = {
  physics: {
    default: 'matter',
    matter: {
      gravity: { y: 1 },
      debug: true,
      // debug options:
      // showBody, showStaticBody, showVelocity, showCollisions, showSeparations
    },
  },
};
```

## Creating Bodies

```javascript
// Rectangle
const box = this.matter.add.sprite(400, 200, 'crate');

// Circle
const ball = this.matter.add.sprite(400, 100, 'ball', null, {
  shape: { type: 'circle', radius: 20 },
});

// Polygon from physics editor (PhysicsEditor JSON)
this.load.json('shapes', 'assets/shapes.json'); // in preload
const car = this.matter.add.sprite(400, 200, 'car', null, {
  shape: this.cache.json.get('shapes').car,
});

// Static body
const ground = this.matter.add.sprite(400, 580, 'ground', null, { isStatic: true });

// From vertices
const poly = this.matter.add.fromVertices(400, 300, '50 0 100 100 0 100', {
  isStatic: true,
});
```

## Body Properties

```javascript
sprite.setFriction(0.05);         // surface friction
sprite.setFrictionAir(0.001);     // air resistance
sprite.setFrictionStatic(0.5);    // static friction threshold
sprite.setBounce(0.7);            // restitution
sprite.setMass(10);
sprite.setDensity(0.001);
sprite.setFixedRotation();        // prevent rotation
sprite.setVelocity(5, -10);
sprite.setAngularVelocity(0.1);
sprite.setSensor(true);           // detects overlap, no physical response
```

## Collisions

Matter uses collision categories and labels:

```javascript
// By label
this.matter.world.on('collisionstart', (event) => {
  event.pairs.forEach(pair => {
    const { bodyA, bodyB } = pair;
    if (bodyA.label === 'player' && bodyB.label === 'spike') {
      playerHit();
    }
  });
});

// Set label
sprite.body.label = 'player';

// Collision categories (bitmask)
const PLAYER = this.matter.world.nextCategory();
const ENEMY = this.matter.world.nextCategory();
const PLATFORM = this.matter.world.nextCategory();

player.setCollisionCategory(PLAYER);
player.setCollidesWith([ENEMY, PLATFORM]);

enemy.setCollisionCategory(ENEMY);
enemy.setCollidesWith([PLAYER, PLATFORM]);
```

## Constraints (Joints)

```javascript
// Distance constraint (spring/rope)
this.matter.add.constraint(bodyA, bodyB, 100, 0.5); // length, stiffness

// Point constraint (pin to world)
this.matter.add.worldConstraint(body, 0, 1, { pointA: { x: 400, y: 100 } });

// Spring
this.matter.add.spring(bodyA, bodyB, 200, 0.01);
```

## Sensors

Sensors detect overlap without physical collision — perfect for triggers, hitboxes.

```javascript
const sensor = this.matter.add.rectangle(400, 300, 100, 100, {
  isSensor: true,
  label: 'deathZone',
});

this.matter.world.on('collisionstart', (event) => {
  event.pairs.forEach(({ bodyA, bodyB }) => {
    if (bodyA.label === 'deathZone' || bodyB.label === 'deathZone') {
      handleDeath();
    }
  });
});
```

## Gotchas

- Matter is significantly heavier than Arcade — use Arcade unless you need rotation physics, complex shapes, or constraints
- `setFixedRotation()` is critical for platformer characters — without it, the player tumbles
- Physics body origin defaults to center of mass, not sprite origin — compound shapes may have unexpected anchors
- Matter `debug: true` shows wireframes — essential for tuning collision shapes
- `fromVertices()` requires the `poly-decomp` library for concave shapes — include it via CDN or npm
- Collision events fire for ALL pairs — filter by label or category to avoid processing irrelevant pairs

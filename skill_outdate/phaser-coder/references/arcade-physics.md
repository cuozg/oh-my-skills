# Arcade Physics

## Enabling

```javascript
const config = {
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { y: 300 },
      debug: true,  // shows body outlines — toggle off for production
    },
  },
};
```

## Physics-Enabled Objects

```javascript
// Dynamic body (affected by gravity, velocity)
const player = this.physics.add.sprite(100, 400, 'player');

// Static body (immovable — platforms, walls)
const platforms = this.physics.add.staticGroup();
platforms.create(400, 568, 'ground').setScale(2).refreshBody();

// Add physics to existing sprite
this.physics.add.existing(existingSprite);
this.physics.add.existing(wall, true); // true = static
```

## Body Properties

```javascript
player.body.setGravityY(200);         // additional gravity for this body
player.setBounce(0.2);
player.setCollideWorldBounds(true);
player.setVelocity(200, -300);
player.setVelocityX(160);
player.setMaxVelocity(300, 500);
player.setDrag(100, 0);               // friction when no acceleration
player.setFriction(0);                // surface friction (0-1)
player.setAcceleration(0, 0);
player.setImmovable(true);            // won't be pushed by collisions
player.body.setAllowGravity(false);

// Body size (hitbox) — independent of sprite size
player.body.setSize(20, 32);          // width, height
player.body.setOffset(6, 16);         // offset from sprite top-left
player.setCircle(16);                 // circular hitbox
```

## Collisions & Overlaps

```javascript
// Collider — physical bounce/block
this.physics.add.collider(player, platforms);
this.physics.add.collider(player, enemies, hitEnemy, null, this);
this.physics.add.collider(bullets, enemies, bulletHit);

// Overlap — detection without physical response
this.physics.add.overlap(player, coins, collectCoin, null, this);

// Callback signatures:
function collectCoin(player, coin) {
  coin.disableBody(true, true); // deactivate and hide
  this.score += 10;
}

// Process callback (optional 3rd param) — return false to skip
function canCollect(player, coin) {
  return coin.active;
}
```

## Physics Groups

```javascript
const enemies = this.physics.add.group({
  key: 'enemy',
  repeat: 5,
  setXY: { x: 100, y: 0, stepX: 120 },
});

enemies.children.iterate((enemy) => {
  enemy.setBounce(Phaser.Math.FloatBetween(0.4, 0.8));
  enemy.setCollideWorldBounds(true);
});

// Static group
const platforms = this.physics.add.staticGroup();
```

## Useful Checks

```javascript
// Is on ground?
player.body.touching.down   // touching another body below
player.body.blocked.down    // touching world bounds below
player.body.onFloor()       // either of the above

// Velocity checks
player.body.velocity.x
player.body.speed           // magnitude

// Distance & angle
Phaser.Math.Distance.Between(a.x, a.y, b.x, b.y);
Phaser.Math.Angle.Between(a.x, a.y, b.x, b.y);
```

## World Bounds

```javascript
this.physics.world.setBounds(0, 0, 3200, 600);
this.physics.world.setBoundsCollision(true, true, true, false); // left, right, top, bottom
```

## Object Pooling with Groups

```javascript
const bullets = this.physics.add.group({
  classType: Bullet,
  maxSize: 30,
  runChildUpdate: true, // calls update() on each active child
});

function fire(x, y) {
  const bullet = bullets.get(x, y);
  if (bullet) {
    bullet.fire(); // reactivate and set velocity
  }
}
```

## Gotchas

- `refreshBody()` is required after `setScale()` or `setSize()` on **static** bodies
- Arcade physics uses AABB (axis-aligned bounding boxes) — no rotation on hitboxes (use Matter for that)
- `body.touching` resets each frame — only valid during the frame it's set
- Group `maxSize` with `get()` enables pooling; `get()` returns `null` when pool exhausted
- `debug: true` is essential during development — always enable it while building collision logic

# Sprites, Images & Animation

## Loading Assets

```javascript
preload() {
  this.load.image('bg', 'assets/background.png');
  this.load.spritesheet('player', 'assets/player.png', {
    frameWidth: 32, frameHeight: 48
  });
  this.load.atlas('enemies', 'assets/enemies.png', 'assets/enemies.json');
  this.load.multiatlas('ui', 'assets/ui.json', 'assets/');
}
```

## Creating Display Objects

```javascript
// Static image
this.add.image(400, 300, 'bg').setOrigin(0.5);

// Sprite (supports animation)
const player = this.add.sprite(100, 200, 'player');

// From atlas frame
const enemy = this.add.sprite(300, 200, 'enemies', 'goblin-idle-01');

// From spritesheet frame index
const coin = this.add.sprite(50, 50, 'coins', 3);
```

## Sprite Properties

```javascript
sprite.setPosition(x, y);
sprite.setScale(2);           // uniform scale
sprite.setScale(2, 1);        // x, y scale
sprite.setOrigin(0.5, 1);     // anchor point (0-1)
sprite.setAlpha(0.5);
sprite.setTint(0xff0000);     // color tint
sprite.setFlipX(true);        // mirror horizontally
sprite.setDepth(10);          // z-order (higher = on top)
sprite.setVisible(false);
sprite.setAngle(45);          // degrees
sprite.setRotation(Math.PI);  // radians
```

## Animations

Animations are **global** — create once, play on any sprite with matching texture.

```javascript
// Create animation (usually in create() of first scene)
this.anims.create({
  key: 'walk',
  frames: this.anims.generateFrameNumbers('player', { start: 0, end: 7 }),
  frameRate: 10,
  repeat: -1,      // -1 = loop forever
});

// From atlas
this.anims.create({
  key: 'explode',
  frames: this.anims.generateFrameNames('effects', {
    prefix: 'explosion-', suffix: '.png',
    start: 1, end: 8, zeroPad: 2,
  }),
  frameRate: 15,
  repeat: 0,
  hideOnComplete: true,
});

// Play
sprite.anims.play('walk', true);     // true = ignoreIfPlaying
sprite.anims.play('idle');
sprite.anims.stop();

// Events
sprite.on('animationcomplete-explode', () => sprite.destroy());
sprite.on('animationcomplete', (anim) => { ... });
```

## Sprite Sheets vs Atlases

- **Spritesheet**: uniform grid, loaded with `frameWidth`/`frameHeight` — simple, good for characters
- **Atlas (JSON Hash/Array)**: packed irregular frames from TexturePacker/ShoeBox — efficient, supports trimming
- **Multi-atlas**: multiple image files, one JSON — for large asset sets

## Groups

```javascript
// Display group (no physics)
const stars = this.add.group();
for (let i = 0; i < 12; i++) {
  stars.create(70 + i * 60, 0, 'star');
}

// Group config sets defaults for ALL children
const bullets = this.add.group({
  classType: Phaser.GameObjects.Image,
  maxSize: 20,
  active: false,
  visible: false,
});
```

## Gotchas

- `setOrigin()` affects positioning but NOT physics body alignment — call `refreshBody()` on static physics objects after changing origin/scale
- Spritesheet frame indices are 0-based, left-to-right, top-to-bottom
- `anims.play('key', true)` — the `true` prevents restarting if already playing (use for movement anims in update loop)
- Destroying a sprite doesn't remove its physics body automatically if you hold a separate reference

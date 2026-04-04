# Input

## Keyboard

```javascript
// Cursor keys (arrows + shift + space)
this.cursors = this.input.keyboard.createCursorKeys();

// In update():
if (this.cursors.left.isDown) { ... }
if (this.cursors.space.isDown) { ... }
if (Phaser.Input.Keyboard.JustDown(this.cursors.space)) { ... } // single press

// Specific keys
this.keyW = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.W);
this.keyESC = this.input.keyboard.addKey('ESC');

// WASD combo
this.wasd = this.input.keyboard.addKeys('W,A,S,D');
// or: this.input.keyboard.addKeys({ up: 'W', left: 'A', down: 'S', right: 'D' });

// Key events
this.input.keyboard.on('keydown-ENTER', () => { ... });
this.input.keyboard.on('keyup-W', () => { ... });
```

## Pointer (Mouse/Touch)

```javascript
// Click/tap
this.input.on('pointerdown', (pointer) => {
  console.log(pointer.x, pointer.y);           // camera-relative
  console.log(pointer.worldX, pointer.worldY);  // world coordinates
  console.log(pointer.leftButtonDown());
  console.log(pointer.rightButtonDown());
});

this.input.on('pointerup', (pointer) => { ... });
this.input.on('pointermove', (pointer) => { ... });

// Multi-touch
this.input.addPointer(2); // support up to 3 total (1 default + 2)
```

## Interactive Game Objects

```javascript
const button = this.add.image(400, 300, 'button').setInteractive();

button.on('pointerdown', () => { button.setTint(0xff0000); });
button.on('pointerup', () => { button.clearTint(); });
button.on('pointerover', () => { button.setScale(1.1); });
button.on('pointerout', () => { button.setScale(1); });

// Custom hit area
sprite.setInteractive(new Phaser.Geom.Circle(50, 50, 50), Phaser.Geom.Circle.Contains);

// Pixel-perfect hit testing
sprite.setInteractive({ pixelPerfect: true, alphaTolerance: 128 });

// Draggable
this.input.setDraggable(sprite);
sprite.on('drag', (pointer, dragX, dragY) => {
  sprite.setPosition(dragX, dragY);
});
```

## Gamepad

```javascript
// Enable in config:
// input: { gamepad: true }

this.input.gamepad.once('connected', (pad) => {
  this.pad = pad;
});

// In update:
if (this.pad) {
  const lx = this.pad.leftStick.x; // -1 to 1
  const ly = this.pad.leftStick.y;
  if (this.pad.A) { jump(); }
  if (this.pad.B) { attack(); }
}
```

## Input Zones

```javascript
const zone = this.add.zone(400, 300, 200, 200).setInteractive();
zone.on('pointerdown', () => { ... });
```

## Gotchas

- `pointer.x/y` is camera-relative; use `pointer.worldX/worldY` for scrolled cameras
- `JustDown()` must be called in `update()` — it checks state change per frame
- Interactive objects need `setInteractive()` called explicitly
- Keyboard events fire even when browser has focus elsewhere — check `this.input.keyboard.enabled` if needed
- For mobile: always add touch fallbacks, don't rely on keyboard

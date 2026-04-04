# Cameras & Scene Transitions

## Camera Basics

```javascript
const cam = this.cameras.main;
cam.setBounds(0, 0, mapWidth, mapHeight);
cam.startFollow(player, true, 0.08, 0.08); // lerp for smoothing
cam.setZoom(1.5);
cam.setBackgroundColor('#1a1a2e');
cam.setRoundPixels(true); // prevents sub-pixel rendering (good for pixel art)
```

## Camera Effects

```javascript
// Fade
cam.fadeIn(1000);
cam.fadeOut(500, 0, 0, 0, (camera, progress) => {
  if (progress === 1) this.scene.start('NextLevel');
});

// Flash
cam.flash(250, 255, 0, 0); // duration, r, g, b

// Shake
cam.shake(200, 0.01); // duration, intensity

// Pan
cam.pan(targetX, targetY, 2000, 'Power2');

// Zoom effect
cam.zoomTo(2, 1000, 'Sine.easeInOut');
```

## Dead Zones

```javascript
// Camera won't move until player reaches edge of dead zone
cam.setDeadzone(200, 150);
cam.setFollowOffset(-50, 0); // offset from target
```

## Multiple Cameras

```javascript
// UI camera that doesn't scroll
const uiCam = this.cameras.add(0, 0, 800, 600);
uiCam.setScroll(0, 0);

// Ignore UI elements in main camera
cam.ignore(uiLayer);
// Ignore game objects in UI camera
uiCam.ignore(gameLayer);
```

## Minimap

```javascript
const minimap = this.cameras.add(600, 10, 180, 120)
  .setZoom(0.1)
  .setName('minimap')
  .setBackgroundColor(0x002244);
minimap.startFollow(player);
minimap.ignore(uiGroup);
```

## Scene Transition Effects

```javascript
// Fade between scenes
this.cameras.main.fadeOut(500, 0, 0, 0);
this.cameras.main.once('camerafadeoutcomplete', () => {
  this.scene.start('NextScene');
});

// Built-in transition
this.scene.transition({
  target: 'NextScene',
  duration: 1000,
  moveBelow: true,
  onUpdate: (progress) => { /* custom transition logic */ },
});
```

## Gotchas

- `startFollow` lerp values (0.08) create smooth follow — 1 is instant (jittery), lower is smoother but laggier
- `setRoundPixels(true)` prevents tile bleeding in pixel art games
- Multiple cameras render ALL objects by default — use `camera.ignore()` to filter
- Camera bounds must match or exceed world/tilemap bounds
- `setDeadzone` is relative to camera center — not absolute coordinates

# Events & Interaction — PixiJS v8

## eventMode — Must Set to Enable Interaction

All display objects default to `'passive'` in v8 (was `'auto'` in v7). You must explicitly opt in:

```typescript
import { Sprite, EventMode } from 'pixi.js';

// eventMode values:
// 'none'    — no hit-testing, no events (most efficient)
// 'passive' — (DEFAULT v8) no hit-testing, but events bubble from children
// 'auto'    — hit-tested if parent is interactive (like old v7 default)
// 'static'  — always hit-tested, good for buttons that don't move
// 'dynamic' — always hit-tested + re-hit-tests every frame (for moving interactive objects)

const button = new Sprite(texture);
button.eventMode = 'static';       // for buttons, UI elements
button.cursor = 'pointer';         // CSS cursor

const movingEnemy = new Sprite(texture);
movingEnemy.eventMode = 'dynamic'; // for fast-moving clickable objects
```

## Pointer Events (Primary — works for mouse + touch + pen)

```typescript
button.on('pointerdown', (event: FederatedPointerEvent) => {
  console.log(event.global.x, event.global.y);  // screen coords
  console.log(event.client.x, event.client.y);  // client coords
  console.log(event.data.pressure);              // stylus pressure
});

button.on('pointerup', handler);
button.on('pointermove', handler);    // fires only when cursor is OVER the object
button.on('pointerover', handler);    // cursor entered object
button.on('pointerout', handler);     // cursor left object
button.on('pointerenter', handler);   // doesn't bubble (unlike pointerover)
button.on('pointerleave', handler);   // doesn't bubble (unlike pointerout)
button.on('pointercancel', handler);
button.on('pointerupoutside', handler); // released outside the object
```

## CRITICAL: globalpointermove vs pointermove

```typescript
// pointermove — fires ONLY when cursor is over the object
button.on('pointermove', handler); // ❌ won't fire when cursor leaves button

// globalpointermove — fires ALWAYS regardless of cursor position
// Must be set on the stage or app.stage
app.stage.eventMode = 'static';
app.stage.on('globalpointermove', (e: FederatedPointerEvent) => {
  // fires everywhere on the canvas — use for drag operations
  draggable.position.copyFrom(e.global);
});

// Similarly: globalpointerdow, globalpointerup, globalpointerdelta
```

## Mouse-Specific Events

```typescript
sprite.on('click', handler);
sprite.on('rightclick', handler);
sprite.on('mousedown', handler);
sprite.on('mouseup', handler);
sprite.on('mousemove', handler);
sprite.on('mouseover', handler);
sprite.on('mouseout', handler);
sprite.on('mouseupoutside', handler);
sprite.on('wheel', (e: FederatedWheelEvent) => {
  camera.zoom += e.deltaY * 0.001;
});
```

## Touch Events

```typescript
sprite.on('touchstart', handler);
sprite.on('touchend', handler);
sprite.on('touchmove', handler);
sprite.on('touchcancel', handler);
sprite.on('touchendoutside', handler);
```

## FederatedEvent — The Event Object

```typescript
import { FederatedPointerEvent } from 'pixi.js';

sprite.on('pointerdown', (e: FederatedPointerEvent) => {
  e.global          // Point in canvas/screen space
  e.client          // Point in browser client coords
  e.screen          // Same as global in most cases
  e.target          // The object that was clicked
  e.currentTarget   // The object the listener is on
  e.originalEvent   // The underlying DOM PointerEvent
  e.pointerId       // Unique per touch/pointer
  e.pressure        // 0-1 stylus pressure
  e.tiltX, e.tiltY  // stylus tilt
  e.button          // 0=left, 1=middle, 2=right
  e.buttons         // bitmask of held buttons
  
  e.stopPropagation();    // prevent bubble
  e.preventDefault();     // prevent default DOM behavior
});
```

## Event Propagation (Bubbling)

Events bubble up the Container hierarchy by default:
```typescript
const parent = new Container();
const child = new Sprite(texture);
child.eventMode = 'static';
parent.addChild(child);

// This fires when child is clicked:
parent.on('pointerdown', (e) => {
  console.log(e.target === child); // true
});

// Stop bubbling:
child.on('pointerdown', (e) => {
  e.stopPropagation(); // parent won't receive it
});
```

## Drag & Drop Pattern

```typescript
let dragging = false;
let dragOffset = { x: 0, y: 0 };

sprite.eventMode = 'static';
sprite.cursor = 'grab';

sprite.on('pointerdown', (e: FederatedPointerEvent) => {
  dragging = true;
  sprite.cursor = 'grabbing';
  dragOffset.x = sprite.x - e.global.x;
  dragOffset.y = sprite.y - e.global.y;
  // Listen globally so drag works even if cursor moves fast
  app.stage.on('globalpointermove', onMove);
  app.stage.on('globalpointerup', onUp);
});

function onMove(e: FederatedPointerEvent) {
  if (!dragging) return;
  sprite.x = e.global.x + dragOffset.x;
  sprite.y = e.global.y + dragOffset.y;
}

function onUp() {
  dragging = false;
  sprite.cursor = 'grab';
  app.stage.off('globalpointermove', onMove);
  app.stage.off('globalpointerup', onUp);
}
```

## Removing Listeners

```typescript
// Remove specific handler
sprite.off('pointerdown', myHandler);

// Remove all listeners for an event
sprite.removeAllListeners('pointerdown');

// Remove ALL listeners
sprite.removeAllListeners();

// One-time listener
sprite.once('pointerdown', () => console.log('first click only'));
```

## EventSystem Configuration

```typescript
await app.init({
  eventMode: 'passive',         // default eventMode for all objects
  eventFeatures: {
    move: true,                 // enable pointermove globally
    globalMove: true,           // enable globalpointermove
    click: true,
    wheel: true,
  },
});
```

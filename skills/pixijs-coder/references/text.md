# Text — PixiJS v8

## Three Text Classes

| Class | Use When | Performance | HTML Support |
|---|---|---|---|
| `Text` | Dynamic text, frequent changes | Low (redraws canvas) | No |
| `BitmapText` | Game UI, scores, many instances | High (GPU batched) | No |
| `HTMLText` | Rich formatting, CSS, web fonts | Medium | Yes |

## Text

```typescript
import { Text, TextStyle } from 'pixi.js';

const style = new TextStyle({
  fontFamily: 'Arial',
  fontSize: 36,
  fontWeight: 'bold',
  fill: 0xffffff,           // or '#ffffff' or ['#ff0000', '#0000ff'] for gradient
  stroke: { color: 0x000000, width: 4 },
  dropShadow: {
    color: 0x000000,
    blur: 4,
    distance: 6,
    angle: Math.PI / 4,
    alpha: 0.5,
  },
  align: 'center',          // 'left' | 'center' | 'right'
  wordWrap: true,
  wordWrapWidth: 400,
  letterSpacing: 2,
  lineHeight: 40,
  padding: 5,               // prevents clipping of strokes/shadows
});

const text = new Text({ text: 'Hello World', style });
text.anchor.set(0.5);
text.position.set(400, 300);
app.stage.addChild(text);

// Update text content
text.text = 'Score: 1000';
// text.resolution = 2; // increase for crisp text on high-DPI
```

## BitmapText

Fastest for text that changes frequently (scores, counters, HUD):

```typescript
import { BitmapFont, BitmapText, Assets } from 'pixi.js';

// Option 1: Install from a .fnt file (TexturePacker / Hiero output)
await Assets.load('/fonts/game-font.fnt');
const score = new BitmapText({ text: '000000', style: { fontFamily: 'GameFont', fontSize: 48 } });

// Option 2: Generate from a system font at startup
BitmapFont.install({
  name: 'TitleFont',
  style: {
    fontFamily: 'Impact',
    fontSize: 64,
    fill: 0xffff00,
    stroke: { color: 0x000000, width: 6 },
  },
  chars: BitmapFont.ASCII + '!?',  // characters to pre-generate
  resolution: 2,
});

const title = new BitmapText({ text: 'GAME OVER', style: { fontFamily: 'TitleFont', fontSize: 64 } });
title.anchor.set(0.5);
app.stage.addChild(title);

// Update
title.text = 'LEVEL COMPLETE';
```

## HTMLText

Use for rich text with CSS, web fonts, and HTML formatting:

```typescript
import { HTMLText, HTMLTextStyle } from 'pixi.js';

const htmlStyle = new HTMLTextStyle({
  fontSize: 24,
  fontFamily: 'Georgia',
  fill: 0xffffff,
  wordWrap: true,
  wordWrapWidth: 400,
});

const richText = new HTMLText({
  text: '<b>Bold</b> and <i>italic</i> with <span style="color: red;">color</span>',
  style: htmlStyle,
});

app.stage.addChild(richText);
```

## Loading Web Fonts

```typescript
import { Assets } from 'pixi.js';

// Load font before using in Text
await Assets.load({
  alias: 'Orbitron',
  src: '/fonts/Orbitron-Regular.ttf',
  loadParser: 'loadFont', // tells Assets to call FontFace API
});

const text = new Text({
  text: 'Sci-Fi Title',
  style: { fontFamily: 'Orbitron', fontSize: 48, fill: 0x00ffff },
});
```

## Text Gotchas

- `Text` uses an internal canvas — changing `text` triggers a full canvas redraw. For frequently changing values (fps counter), consider `BitmapText`.
- Set `text.resolution = window.devicePixelRatio` for crisp text on Retina displays.
- `style.padding` prevents drop shadows and thick strokes from being clipped.
- `HTMLText` is slower than `Text` — use sparingly, not for 100+ instances.
- Gradients in `fill` only work with `Text`, not `BitmapText`.

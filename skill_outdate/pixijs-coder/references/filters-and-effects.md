# Filters & Effects — PixiJS v8

## Built-in Filters

```typescript
import {
  BlurFilter,
  AlphaFilter,
  ColorMatrixFilter,
  DisplacementFilter,
  NoiseFilter,
} from 'pixi.js';

// CRITICAL: v8 filters use object options, NOT positional args
// v7 (WRONG in v8):
const blur = new BlurFilter(8, 4, 1, 5); // ❌

// v8 CORRECT:
const blur = new BlurFilter({ blur: 8, quality: 4 });
sprite.filters = [blur];

// Alpha
const alpha = new AlphaFilter({ alpha: 0.5 });

// Noise
const noise = new NoiseFilter({ noise: 0.5 });

// Grayscale via ColorMatrix
const colorMatrix = new ColorMatrixFilter();
colorMatrix.grayscale(0.5, false);
colorMatrix.brightness(1.2, false);
colorMatrix.contrast(1.1, false);
colorMatrix.saturate(0.8, false);

// Sepia
colorMatrix.sepia(false);

// Hue rotation
colorMatrix.hue(90, false); // degrees

// Apply multiple filters
sprite.filters = [blur, colorMatrix];

// Remove filters
sprite.filters = null;
```

## Displacement Filter (Ripple / Distortion)

```typescript
import { DisplacementFilter, Sprite, Texture, Assets } from 'pixi.js';

const dispTex = await Assets.load<Texture>('/images/displacement_map.png');
const dispSprite = new Sprite(dispTex);
dispSprite.texture.source.addressMode = 'repeat'; // tile the displacement map
app.stage.addChild(dispSprite);

const displace = new DisplacementFilter({
  sprite: dispSprite,
  scale: 30, // displacement intensity
});
myContainer.filters = [displace];

// Animate the displacement
app.ticker.add((ticker) => {
  dispSprite.x += 0.5 * ticker.deltaTime;
  dispSprite.y += 0.5 * ticker.deltaTime;
});
```

## pixi-filters (Community Package)

Install: `npm install pixi-filters`

```typescript
import {
  GlowFilter,
  OutlineFilter,
  DropShadowFilter,
  GodrayFilter,
  PixelateFilter,
  CrossHatchFilter,
  RGBSplitFilter,
  MotionBlurFilter,
  BulgePinchFilter,
  ShockwaveFilter,
} from 'pixi-filters';

const glow = new GlowFilter({ distance: 15, outerStrength: 2, color: 0xff00ff });
sprite.filters = [glow];

const outline = new OutlineFilter({ thickness: 3, color: 0x000000 });
sprite.filters = [outline];

const shadow = new DropShadowFilter({ offset: { x: 5, y: 5 }, blur: 4, alpha: 0.6 });
container.filters = [shadow];

const pixelate = new PixelateFilter({ size: 8 });
scene.filters = [pixelate];
```

## Custom Filter (GlFilter)

```typescript
import { Filter, GlProgram } from 'pixi.js';

// Vertex shader (pass-through is standard for 2D filters)
const vertex = `
  in vec2 aPosition;
  out vec2 vTextureCoord;
  uniform vec4 uInputClamp;
  uniform highp vec4 uInputSize;
  uniform highp mat3 uProjectionMatrix;
  uniform highp vec4 uOutputFrame;

  vec4 filterVertexPosition(void) {
    vec2 position = aPosition * uOutputFrame.zw + uOutputFrame.xy;
    return vec4((uProjectionMatrix * vec3(position, 1.0)).xy, 0.0, 1.0);
  }

  vec2 filterTextureCoord(void) {
    return aPosition * (uOutputFrame.zw * uInputSize.zw);
  }

  void main(void) {
    gl_Position = filterVertexPosition();
    vTextureCoord = filterTextureCoord();
  }
`;

// Fragment shader
const fragment = `
  in vec2 vTextureCoord;
  out vec4 finalColor;

  uniform sampler2D uTexture;
  uniform float uTime;
  uniform float uIntensity;

  void main(void) {
    vec2 uv = vTextureCoord;
    // Chromatic aberration example
    float r = texture(uTexture, uv + vec2(uIntensity * 0.01, 0.0)).r;
    float g = texture(uTexture, uv).g;
    float b = texture(uTexture, uv - vec2(uIntensity * 0.01, 0.0)).b;
    float a = texture(uTexture, uv).a;
    finalColor = vec4(r, g, b, a);
  }
`;

class ChromaticAberrationFilter extends Filter {
  constructor(intensity = 1.0) {
    const glProgram = GlProgram.from({ vertex, fragment });
    super({
      glProgram,
      resources: {
        // uniforms must declare their type
        myUniforms: {
          uTime: { value: 0, type: 'f32' },
          uIntensity: { value: intensity, type: 'f32' },
        },
      },
    });
  }

  get intensity() { return this.resources.myUniforms.uniforms.uIntensity; }
  set intensity(v: number) { this.resources.myUniforms.uniforms.uIntensity = v; }

  update(delta: number) {
    this.resources.myUniforms.uniforms.uTime += delta * 0.01;
  }
}

// Usage
const chromo = new ChromaticAberrationFilter(2.0);
sprite.filters = [chromo];
app.ticker.add((ticker) => chromo.update(ticker.deltaTime));
```

## CRITICAL: Textures in Custom Filters are Resources, NOT Uniforms

```typescript
// WRONG — textures cannot be uniforms:
super({
  glProgram,
  resources: {
    uniforms: {
      uNoiseTex: { value: noiseTexture, type: 'sampler2D' }, // ❌
    },
  },
});

// CORRECT — textures go in resources directly:
super({
  glProgram,
  resources: {
    uNoiseTex: noiseTexture.source,   // ✅ TextureSource as resource
    myUniforms: {
      uTime: { value: 0, type: 'f32' },
    },
  },
});
// In shader, use: uniform sampler2D uNoiseTex; (matches resource key)
```

## Filter Padding & Area

```typescript
const filter = new BlurFilter({ blur: 20 });
filter.padding = 25; // expand filter render area to avoid edge clipping
```

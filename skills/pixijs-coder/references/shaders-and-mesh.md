# Shaders & Mesh — PixiJS v8

## Mesh Basics

```typescript
import { Mesh, MeshGeometry, MeshMaterial, Shader, GlProgram, Texture, Assets } from 'pixi.js';

const texture = await Assets.load<Texture>('/images/hero.png');

// Simple quad mesh
const geometry = new MeshGeometry({
  positions: new Float32Array([
    -100, -100,  // top-left
     100, -100,  // top-right
     100,  100,  // bottom-right
    -100,  100,  // bottom-left
  ]),
  uvs: new Float32Array([
    0, 0,
    1, 0,
    1, 1,
    0, 1,
  ]),
  indices: new Uint32Array([0, 1, 2, 0, 2, 3]), // two triangles
});

const shader = Shader.from({
  gl: {
    vertex: `/* GLSL vert */`,
    fragment: `/* GLSL frag */`,
  },
  resources: {
    uTexture: texture.source,
    myUniforms: {
      uTime: { value: 0, type: 'f32' },
    },
  },
});

const mesh = new Mesh({ geometry, shader });
app.stage.addChild(mesh);
```

## GlProgram — Shader Source

```typescript
import { GlProgram } from 'pixi.js';

const glProgram = GlProgram.from({
  vertex: `
    in vec2 aPosition;
    in vec2 aUV;
    out vec2 vUV;

    uniform mat3 uProjectionMatrix;
    uniform mat3 uWorldTransformMatrix;
    uniform mat3 uTransformMatrix;

    void main() {
      mat3 mvp = uProjectionMatrix * uWorldTransformMatrix * uTransformMatrix;
      gl_Position = vec4((mvp * vec3(aPosition, 1.0)).xy, 0.0, 1.0);
      vUV = aUV;
    }
  `,
  fragment: `
    in vec2 vUV;
    out vec4 finalColor;

    uniform sampler2D uTexture;
    uniform float uTime;

    void main() {
      vec2 uv = vUV;
      uv.y += sin(uv.x * 10.0 + uTime) * 0.05; // wave distortion
      finalColor = texture(uTexture, uv);
    }
  `,
});
```

## CRITICAL: Uniforms vs Resources

This is the most common v8 shader mistake:

```typescript
// WRONG:
resources: {
  uniforms: {
    uTexture: { value: texture, type: 'sampler2D' }, // ❌ textures are NOT uniforms
    uFloat: { value: 1.0 },                          // ❌ missing type
  },
}

// CORRECT:
resources: {
  uTexture: texture.source,   // ✅ TextureSource as named resource (matches uniform name in shader)
  myUniforms: {               // ✅ uniform group — any name for the JS binding
    uTime: { value: 0.0, type: 'f32' },       // float
    uResolution: { value: [800, 600], type: 'vec2<f32>' },
    uColor: { value: [1, 0, 0, 1], type: 'vec4<f32>' },
    uMatrix: { value: new Float32Array(16), type: 'mat4x4<f32>' },
    uInt: { value: 0, type: 'i32' },
  },
}
```

## Uniform Types Reference

| WGSL / v8 type | GLSL equivalent | JS value |
|---|---|---|
| `'f32'` | `float` | number |
| `'vec2<f32>'` | `vec2` | [x, y] or Float32Array(2) |
| `'vec3<f32>'` | `vec3` | [x, y, z] |
| `'vec4<f32>'` | `vec4` | [r, g, b, a] |
| `'mat3x3<f32>'` | `mat3` | Float32Array(9) |
| `'mat4x4<f32>'` | `mat4` | Float32Array(16) |
| `'i32'` | `int` | number (integer) |
| `'u32'` | `uint` | number (unsigned) |

## MeshGeometry Topologies

```typescript
import { MeshGeometry } from 'pixi.js';

const geometry = new MeshGeometry({
  positions: new Float32Array([...]),
  uvs: new Float32Array([...]),
  indices: new Uint32Array([...]),
  topology: 'triangle-list',    // default
  // 'triangle-list'     — groups of 3 vertices
  // 'triangle-strip'    — connected triangles
  // 'point-list'        — individual points
  // 'line-list'         — pairs of vertices = lines
  // 'line-strip'        — connected line segments
});
```

## Dynamic Geometry Updates

```typescript
const geometry = new MeshGeometry({
  positions: new Float32Array(vertexCount * 2),
  uvs: new Float32Array(vertexCount * 2),
  indices: new Uint32Array(indexCount),
});

const positions = geometry.getAttribute('aPosition');
// Modify buffer data:
positions.data[0] = newX;
positions.data[1] = newY;
// Signal GPU to re-upload:
positions.buffer.update();
```

## Sprite Mesh (Deformable Sprite)

```typescript
import { MeshSimple, Texture, Assets } from 'pixi.js';

const texture = await Assets.load<Texture>('/images/ribbon.png');

// Create a simple deformable mesh from a texture
const mesh = new MeshSimple({
  texture,
  vertices: new Float32Array([...]),  // 2 floats per vertex
  uvs: new Float32Array([...]),
  indices: new Uint32Array([...]),
});

// Deform vertices at runtime
mesh.vertices[0] = newX;
mesh.vertices[1] = newY;
mesh.geometry.getAttribute('aPosition').buffer.update();
```

## PlaneGeometry (Subdivided Grid)

```typescript
import { MeshPlane, Texture, Assets } from 'pixi.js';

const texture = await Assets.load<Texture>('/images/wave.png');

// 20x10 subdivision grid
const plane = new MeshPlane({ texture, verticesX: 20, verticesY: 10 });
app.stage.addChild(plane);

// Wave animation
app.ticker.add((ticker) => {
  const verts = plane.geometry.getAttribute('aPosition').data;
  for (let i = 0; i < verts.length; i += 2) {
    verts[i + 1] = Math.sin((i / 2 + ticker.elapsedMS / 100) * 0.5) * 20;
  }
  plane.geometry.getAttribute('aPosition').buffer.update();
});
```

## WebGPU Shaders

For WebGPU renderer, provide WGSL alongside GLSL:
```typescript
const program = GlProgram.from({
  gl: { vertex: glslVert, fragment: glslFrag },
  gpu: { vertex: wgslVert, fragment: wgslFrag }, // optional WebGPU source
});
// PixiJS auto-selects based on active renderer
```

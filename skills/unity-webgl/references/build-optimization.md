# WebGL Build Optimization

## Compression

| Format | When | Server Requirement |
|--------|------|--------------------|
| **Brotli** | Production (HTTPS required) | `Content-Encoding: br` header |
| **Gzip** | Non-HTTPS or legacy servers | `Content-Encoding: gzip` header |
| **None** | Development/debugging only | None |

Set in **Player Settings → Publishing Settings → Compression Format**.

Brotli produces 15-25% smaller files than Gzip but requires HTTPS and server support.

## Code Stripping (IL2CPP)

WebGL always uses IL2CPP. Managed Code Stripping levels:

| Level | Size Impact | Risk |
|-------|-------------|------|
| **Minimal** | Largest build | Safest — preserves almost everything |
| **Low** | Moderate reduction | Safe for most projects |
| **Medium** | Good reduction | May strip reflection targets |
| **High** | Maximum reduction | Aggressive — will break reflection, JSON serialization, dependency injection |

Set in **Player Settings → Other Settings → Managed Stripping Level**.

### linker.xml (Preserving Types)

When stripping breaks runtime behavior ("method not found", "type not found"), create `Assets/linker.xml`:

```xml
<linker>
  <!-- Preserve entire assembly -->
  <assembly fullname="Assembly-CSharp" preserve="all"/>

  <!-- Preserve specific types -->
  <assembly fullname="MyGame.Core">
    <type fullname="MyGame.Core.SaveData" preserve="all"/>
    <type fullname="MyGame.Core.Config" preserve="all"/>
  </assembly>

  <!-- Preserve types used by JSON serialization -->
  <assembly fullname="Newtonsoft.Json" preserve="all"/>

  <!-- Preserve types accessed via reflection -->
  <assembly fullname="MyGame.Analytics">
    <type fullname="MyGame.Analytics.EventPayload" preserve="all"/>
  </assembly>
</linker>
```

Common types that need preservation:
- JSON-serialized data classes
- Types accessed via `System.Reflection`
- Dependency injection registrations
- Types referenced only in config or ScriptableObjects

## Memory Configuration

### Unity Heap

- **Initial Memory Size**: set to typical usage (e.g., 32-64MB for small games, 128-256MB for larger)
- **Memory Growth Mode**: enable for flexibility, but test on mobile browsers (iOS Safari has strict limits)
- **Maximum Memory Size**: cap at 2048MB — mobile browsers crash above this

GC runs only at frame boundaries. In-frame allocations accumulate until end-of-frame collection. Large loops with temporary strings/objects cause OOM before GC runs.

**Mitigations:**
- Use `StringBuilder` instead of string concatenation in loops
- Use `NativeArray<T>` with `Allocator.Temp` for per-frame data
- Avoid LINQ in hot paths (creates enumerator allocations)
- Pool frequently-created objects

### Browser Memory Budget

Total browser memory = WebGL heap + decompressed assets + JS context + DOM. A 256MB Unity heap may require 400-600MB total browser RAM.

## Texture Compression

| Format | Target | Quality | Size |
|--------|--------|---------|------|
| **ASTC** | Mobile browsers (iOS/Android) | Best | Smallest |
| **DXT** | Desktop browsers | Good | Moderate |
| **ETC2** | Android (fallback) | Good | Small |

Use **Player Settings → Other Settings → Texture Compression Format** or per-texture overrides.

For cross-platform support, set default to ASTC (widest compatibility in WebGL2).

## Build Size Reduction Checklist

1. **Stripping Level**: Medium or High (with proper linker.xml)
2. **Compression**: Brotli for production
3. **Texture Compression**: ASTC or platform-appropriate format
4. **Audio**: Vorbis at quality 50-70% (not PCM/WAV)
5. **Remove unused assets**: check for orphaned resources in build report
6. **Disable exceptions**: "None" for production (Player Settings → Publishing Settings → Exception Support)
7. **Strip engine code**: disable unused Unity modules (Physics, Audio, etc.) in Package Manager
8. **Addressables**: load large assets on demand instead of embedding in initial data file

## Deployment Server Configuration

### Nginx

```nginx
location /unity-build/ {
    # MIME types
    types {
        application/wasm wasm;
        application/octet-stream data;
        application/javascript js;
        application/json json;
    }

    # Brotli-compressed files
    location ~ \.br$ {
        add_header Content-Encoding br;
        default_type application/octet-stream;
    }
    location ~ \.js\.br$ {
        add_header Content-Encoding br;
        default_type application/javascript;
    }
    location ~ \.wasm\.br$ {
        add_header Content-Encoding br;
        default_type application/wasm;
    }

    # Gzip-compressed files
    location ~ \.gz$ {
        add_header Content-Encoding gzip;
        default_type application/octet-stream;
    }
    location ~ \.js\.gz$ {
        add_header Content-Encoding gzip;
        default_type application/javascript;
    }
    location ~ \.wasm\.gz$ {
        add_header Content-Encoding gzip;
        default_type application/wasm;
    }
}
```

### Apache (.htaccess)

```apache
AddType application/wasm .wasm
AddType application/octet-stream .data

# Brotli
AddEncoding br .br
<FilesMatch "\.js\.br$">
    AddType application/javascript .br
</FilesMatch>
<FilesMatch "\.wasm\.br$">
    AddType application/wasm .br
</FilesMatch>
<FilesMatch "\.data\.br$">
    AddType application/octet-stream .br
</FilesMatch>
```

### IIS (web.config)

```xml
<configuration>
  <system.webServer>
    <staticContent>
      <mimeMap fileExtension=".wasm" mimeType="application/wasm" />
      <mimeMap fileExtension=".data" mimeType="application/octet-stream" />
      <mimeMap fileExtension=".br" mimeType="application/octet-stream" />
    </staticContent>
  </system.webServer>
</configuration>
```

## Data Caching (IndexedDB)

Enable **Publishing Settings → Data Caching** to store `.data` and `.wasm` files in the browser's IndexedDB. This dramatically reduces second-visit load times — the browser serves cached files instead of re-downloading.

Set a cache URL pattern that includes a build hash so updates invalidate the cache automatically.

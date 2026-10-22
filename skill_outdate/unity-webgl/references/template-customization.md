# WebGL Template Customization

## Template Location

Custom templates live in `Assets/WebGLTemplates/{TemplateName}/`. Each template needs:

```
Assets/WebGLTemplates/
  MyTemplate/
    index.html            (required)
    thumbnail.png         (128x128, shown in Build Settings)
    TemplateData/
      style.css
      progressbar.js
      favicon.ico
      loading-logo.png
```

Select the template in **Build Settings → Player Settings → Resolution and Presentation → WebGL Template**.

## Template Variables

Unity replaces these placeholders during build:

| Variable | Value |
|----------|-------|
| `{{{ PRODUCT_NAME }}}` | Product Name from Player Settings |
| `{{{ PRODUCT_VERSION }}}` | Version from Player Settings |
| `{{{ COMPANY_NAME }}}` | Company Name from Player Settings |
| `{{{ TOTAL_MEMORY }}}` | Initial memory size (bytes) |
| `{{{ WIDTH }}}` | Default canvas width |
| `{{{ HEIGHT }}}` | Default canvas height |
| `{{{ BACKGROUND_COLOR }}}` | Background color from Player Settings |
| `{{{ DATA_URL }}}` | Path to .data file |
| `{{{ CODE_URL }}}` | Path to .framework.js file |
| `{{{ LOADER_URL }}}` | Path to loader .js file |

Use triple-brace syntax: `{{{ VARIABLE }}}` (not double-brace).

## Responsive Canvas Template

```html
<!DOCTYPE html>
<html lang="en-us">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>{{{ PRODUCT_NAME }}}</title>
  <style>
    * { margin: 0; padding: 0; }
    html, body { width: 100%; height: 100%; overflow: hidden; background: {{{ BACKGROUND_COLOR }}}; }

    #unity-container {
      width: 100%; height: 100%;
      position: absolute; top: 0; left: 0;
    }
    #unity-canvas {
      width: 100% !important;
      height: 100% !important;
      display: block;
    }

    /* Loading overlay */
    #loading-overlay {
      position: fixed; top: 0; left: 0;
      width: 100%; height: 100%;
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      background: {{{ BACKGROUND_COLOR }}};
      z-index: 100; transition: opacity 0.5s;
    }
    #loading-overlay.hidden { opacity: 0; pointer-events: none; }
    #progress-bar-outer {
      width: 300px; height: 6px;
      background: rgba(255,255,255,0.2);
      border-radius: 3px; overflow: hidden;
    }
    #progress-bar-inner {
      width: 0%; height: 100%;
      background: #fff; transition: width 0.2s;
    }
    #loading-text {
      color: rgba(255,255,255,0.6);
      font-family: sans-serif; font-size: 14px;
      margin-top: 12px;
    }
  </style>
</head>
<body>
  <div id="unity-container">
    <canvas id="unity-canvas" tabindex="-1"></canvas>
  </div>

  <div id="loading-overlay">
    <div id="progress-bar-outer">
      <div id="progress-bar-inner"></div>
    </div>
    <div id="loading-text">Loading...</div>
  </div>

  <script>
    var buildUrl = "Build";
    var config = {
      dataUrl: buildUrl + "/{{{ DATA_URL }}}",
      frameworkUrl: buildUrl + "/{{{ CODE_URL }}}",
      codeUrl: buildUrl + "/{{{ CODE_URL }}}".replace(".framework.js", ".wasm"),
      streamingAssetsUrl: "StreamingAssets",
      companyName: "{{{ COMPANY_NAME }}}",
      productName: "{{{ PRODUCT_NAME }}}",
      productVersion: "{{{ PRODUCT_VERSION }}}",
      devicePixelRatio: window.devicePixelRatio || 1
    };

    var loadingOverlay = document.getElementById("loading-overlay");
    var progressBar = document.getElementById("progress-bar-inner");
    var loadingText = document.getElementById("loading-text");

    var script = document.createElement("script");
    script.src = buildUrl + "/{{{ LOADER_URL }}}";
    script.onload = function () {
      createUnityInstance(document.getElementById("unity-canvas"), config, function (progress) {
        progressBar.style.width = (progress * 100) + "%";
        loadingText.textContent = "Loading... " + Math.round(progress * 100) + "%";
      }).then(function (instance) {
        window.myUnityInstance = instance;
        loadingOverlay.classList.add("hidden");
        setTimeout(function () { loadingOverlay.remove(); }, 500);
      }).catch(function (message) {
        loadingText.textContent = "Error: " + message;
        console.error("Unity load error:", message);
      });
    };
    document.body.appendChild(script);

    // Responsive resize
    window.addEventListener("resize", function () {
      var canvas = document.getElementById("unity-canvas");
      if (canvas) {
        canvas.style.width = window.innerWidth + "px";
        canvas.style.height = window.innerHeight + "px";
      }
    });
  </script>
</body>
</html>
```

## Iframe Embedding

When embedding a WebGL build in an iframe:

```html
<iframe
  src="/unity-build/index.html"
  width="960" height="600"
  style="border: none;"
  allow="fullscreen; clipboard-read; clipboard-write; autoplay"
  allowfullscreen>
</iframe>
```

Key `allow` permissions:
- `fullscreen` — for fullscreen toggle
- `clipboard-read; clipboard-write` — for clipboard JSLib access
- `autoplay` — for audio playback without user gesture

## Mobile Detection

```javascript
function isMobileDevice() {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
    || (navigator.maxTouchPoints && navigator.maxTouchPoints > 2);
}

// Show mobile warning or adjust settings
if (isMobileDevice()) {
  config.devicePixelRatio = Math.min(window.devicePixelRatio, 2); // cap for performance
  // optionally show orientation lock message
}
```

## Error Handling

```javascript
// Global error handler
window.addEventListener("error", function (e) {
  if (e.message && e.message.includes("out of memory")) {
    document.getElementById("loading-text").textContent =
      "Out of memory. Please close other browser tabs and try again.";
  }
});

// Unity-specific error handler in createUnityInstance
createUnityInstance(canvas, config, onProgress).catch(function (message) {
  if (message.includes("WebGL")) {
    // WebGL not supported
    showFallbackMessage("Your browser doesn't support WebGL. Please use Chrome, Firefox, or Edge.");
  } else if (message.includes("wasm")) {
    // WASM loading failed — likely wrong MIME type
    showFallbackMessage("Failed to load. Please check server configuration.");
  }
});
```

## Custom Template Variables

You can define your own variables in `index.html` and set them from Player Settings → Additional Template Variables. Use the same triple-brace syntax: `{{{ MY_CUSTOM_VAR }}}`.

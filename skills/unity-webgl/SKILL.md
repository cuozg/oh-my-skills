---
name: unity-webgl
description: >
  Unified Unity WebGL skill — write JavaScript interop plugins, optimize WebGL builds, configure
  deployment, and customize HTML templates. Auto-triages: JSLib (.jslib plugins + C# bridge for
  browser API access), Build (build size, compression, memory, linker.xml, Player Settings),
  Template (HTML shell, loading screen, responsive canvas). MUST use for ANY Unity WebGL work —
  JavaScript plugins, browser API, WebGL build optimization, deployment, server MIME types,
  template customization, platform-conditional code (#if UNITY_WEBGL). Triggers: "jslib,"
  "JavaScript plugin," "call JS from Unity," "browser API," "WebGL build," "reduce build size,"
  "WebGL deployment," "loading screen," "WebGL template," "linker.xml," "localStorage from Unity,"
  "WebGL memory," "Brotli compression," "works in editor but not WebGL," "responsive WebGL canvas,"
  "embed Unity in iframe." Do not use for runtime C# (unity-code), editor scripts (unity-editor),
  or debugging (unity-debug).
metadata:
  author: kuozg
  version: "1.1"
---
# unity-webgl

Detect what the user needs for their WebGL target, select the right mode, and deliver complete platform-specific code.

## Step 1 — Detect Mode

| Signal | Mode |
|--------|------|
| `.jslib`, JavaScript plugin, call JS from C#, browser API (clipboard, localStorage, URL params, fullscreen) | **JSLib** |
| Build size, compression, linker.xml, memory settings, code stripping, Player Settings, deployment, server config, MIME types | **Build** |
| HTML template, loading screen, responsive canvas, iframe embedding, custom shell, progress bar | **Template** |

State triage: "This is [mode] — [reason]."

## Step 2 — Execute

### JSLib Mode

1. **Qualify** — confirm user needs JS↔C# interop; if it's pure C# runtime logic, escalate to unity-code
2. **Discover** — check existing `Assets/Plugins/WebGL/` for `.jslib` files and naming patterns; read any existing C# bridge classes
3. **Implement** — create both sides of the bridge:
   - `.jslib` file using `mergeInto(LibraryManager.library, {...})` pattern
   - C# class with `[DllImport("__Internal")]` extern methods
   - `#if UNITY_WEBGL && !UNITY_EDITOR` guards on call sites
   - Load `references/jslib-patterns.md` for marshalling rules and examples
4. **Verify** — `lsp_diagnostics` on C# files; validate `.jslib` has valid JS syntax
5. **Handoff** — file paths, what each side does, platform guard notes, testing guidance (must test in browser build)

### Build Mode

1. **Qualify** — confirm this is about WebGL build pipeline, not runtime code
2. **Discover** — check existing `ProjectSettings/`, `linker.xml`, build scripts, current compression settings
3. **Implement** — apply the requested optimization:
   - Load `references/build-optimization.md` for settings reference
   - For code stripping: create/update `linker.xml` with type preservation
   - For compression: recommend Brotli (HTTPS) or Gzip (fallback) and output server config
   - For memory: configure initial/max heap size based on target platform
   - For deployment: generate server configuration (nginx/Apache/IIS headers)
4. **Verify** — validate XML syntax for linker.xml; confirm no conflicting settings
5. **Handoff** — changed files, expected build size impact, server setup instructions

### Template Mode

1. **Qualify** — confirm user wants HTML template changes, not runtime UI (→ unity-uitoolkit)
2. **Discover** — check `Assets/WebGLTemplates/` for existing custom templates; read current index.html
3. **Implement** — create or modify template files:
   - Load `references/template-customization.md` for variable reference and patterns
   - Custom `index.html` with Unity template variables (`{{{ PRODUCT_NAME }}}`, etc.)
   - CSS for responsive canvas, loading bar, progress events
   - JavaScript for error handling, mobile detection, fullscreen toggle
4. **Verify** — validate HTML structure; ensure all Unity template variables are present
5. **Handoff** — file paths, how to select template in Build Settings, browser testing notes

## Rules

- Always wrap WebGL-only C# calls in `#if UNITY_WEBGL && !UNITY_EDITOR` — code must compile on all platforms
- `.jslib` files go in `Assets/Plugins/WebGL/` — this path matters for the build pipeline
- String marshalling in JSLib requires `UTF8ToString()` for incoming strings and `_malloc` + `stringToUTF8` for return strings — never skip the buffer allocation
- `SendMessage` is legacy — prefer `[DllImport("__Internal")]` for C#→JS calls
- For JS→C# callbacks, use `SendMessage` only when no better option exists (it's single-string, slow, and requires a GameObject name)
- Never use `System.Threading`, `System.IO.File`, or raw `System.Net.Sockets` in WebGL code paths — they don't exist in the browser
- Always provide fallback behavior for non-WebGL platforms when writing platform-conditional code
- `lsp_diagnostics` after every code change

## Escalation

| From | To | When |
|------|----|------|
| JSLib | unity-code | Work is pure C# with no JS interop needed |
| Build | unity-debug | Build fails with compile errors, not config issues |
| Template | unity-uitoolkit | User actually wants runtime UI, not HTML shell |
| Any | unity-debug | "Works in editor but not in WebGL build" with runtime errors |

Carry forward context; tell user why you're switching.

## Standards

Load on demand via `read_skill_file("unity-standards", "references/<path>")`:

- `code-standards/architecture-systems.md` — includes WebGL restrictions, platform workarounds
- `code-standards/lifecycle-async-errors.md` · `core-conventions.md` — lifecycle, null safety, error handling
- `debug/common-unity-errors.md` — includes WebGL-specific errors (code stripping, OOM)
- `other/unity-mcp-routing-matrix.md` — MCP tool routing for editor control, console tools, and script management

Load skill-specific references via `read_skill_file("unity-webgl", "references/<path>")`:

- `references/jslib-patterns.md` — JSLib format, marshalling, browser API wrappers, complete examples
- `references/build-optimization.md` — compression, stripping, memory, linker.xml, deployment, server config
- `references/template-customization.md` — HTML template variables, responsive CSS, loading screen, iframe embedding

---
name: unity-webgl
description: >
  Unified Unity WebGL skill for JavaScript interop plugins, WebGL build optimization,
  deployment, and custom HTML templates. Auto-triages JSLib, Build, and Template work.
  MUST use for Unity WebGL requests: .jslib plugins, calling JS from Unity, browser
  APIs, build size, compression, memory, linker.xml, Player Settings, deployment,
  server MIME types, loading screens, templates, responsive canvas, iframe embedding,
  localStorage, Brotli, platform-conditional code, or issues that work in Editor but
  fail in WebGL. Do not use for general runtime C#, editor scripts, or non-WebGL
  debugging.
metadata:
  author: kuozg
  version: "1.1"
---
# unity-webgl

Detect what the user needs for WebGL, select mode, deliver complete platform-specific code.

## Step 1 — Detect Mode

| Signal | Mode |
|--------|------|
| `.jslib`, call JS from C#, browser API (clipboard, localStorage, URL params, fullscreen) | **JSLib** |
| Build size, compression, linker.xml, memory, Player Settings, deployment, server MIME types | **Build** |
| HTML template, loading screen, responsive canvas, iframe, custom shell, progress bar | **Template** |

State triage: "This is [mode] — [reason]."

## Step 2 — Execute

**JSLib Mode:**
1. Check existing `Assets/Plugins/WebGL/` for `.jslib` files and patterns; read any C# bridge classes
2. Implement both sides: `.jslib` using `mergeInto(LibraryManager.library, {...})` + C# class with `[DllImport("__Internal")]` extern methods + `#if UNITY_WEBGL && !UNITY_EDITOR` guards on call sites
3. Load `references/jslib-patterns.md` for marshalling rules
4. `lsp_diagnostics` on C# files; validate `.jslib` has valid JS syntax
5. Handoff: file paths, what each side does, testing guidance (must test in browser build)

**Build Mode:**
1. Check existing `ProjectSettings/`, `linker.xml`, build scripts, compression settings
2. Load `references/build-optimization.md` for settings reference
3. For code stripping: create/update `linker.xml` · For compression: recommend Brotli (HTTPS) or Gzip + server config · For memory: configure heap size
4. Validate XML syntax; confirm no conflicting settings
5. Handoff: changed files, expected build size impact, server setup instructions

**Template Mode:**
1. Check `Assets/WebGLTemplates/` for existing templates; read current `index.html`
2. Load `references/template-customization.md` for variables and patterns
3. Create/modify: `index.html` with Unity template variables (`{{{ PRODUCT_NAME }}}`) · responsive CSS · JS for error handling, mobile detection, fullscreen
4. Validate HTML structure; ensure all Unity template variables present
5. Handoff: file paths, how to select template in Build Settings, browser testing notes

## Rules

- Wrap WebGL-only C# calls in `#if UNITY_WEBGL && !UNITY_EDITOR` — must compile on all platforms
- `.jslib` files go in `Assets/Plugins/WebGL/` — path matters for build pipeline
- String marshalling in JSLib: `UTF8ToString()` for incoming strings; `_malloc` + `stringToUTF8` for return strings — never skip buffer allocation
- `SendMessage` is legacy — prefer `[DllImport("__Internal")]` for C#→JS calls
- Never use `System.Threading`, `System.IO.File`, raw `System.Net.Sockets` in WebGL paths
- Always provide fallback behavior for non-WebGL platforms
- `lsp_diagnostics` after every code change

## Escalation

| To | When |
|----|------|
| `unity-code` | Work is pure C# with no JS interop |
| `unity-debug` | Build fails with compile errors |
| `unity-uitoolkit` | User wants runtime UI, not HTML shell |
| `unity-debug` | "Works in editor but not in WebGL" with runtime errors |

## Standards

`read_skill_file("unity-standards", "references/<path>")`:
- `code-standards/architecture-systems.md` · `code-standards/lifecycle-async-errors.md`
- `debug/common-unity-errors.md` · `other/unity-mcp-routing-matrix.md`

`read_skill_file("unity-webgl", "references/<path>")`:
- `jslib-patterns.md` · `build-optimization.md` · `template-customization.md`

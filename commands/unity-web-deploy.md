---
description: WebGL build configuration, browser optimization, and deployment
agent: build
---

Load the `unity/unity-web-deploy` skill and handle WebGL deployment.

## Task

$ARGUMENTS

## Scope

1. **Build configuration** - WebGL player settings, compression, memory
2. **C#/JS interop** - jslib plugins, browser API integration
3. **Browser optimization** - Memory limits, audio context, input handling
4. **PWA features** - Service workers, offline support, manifest
5. **Hosting** - CDN configuration, caching, loading optimization

## Requirements

- Handle browser-specific quirks (audio autoplay, WebGL context loss)
- Optimize for download size and initial load time
- Test across major browsers

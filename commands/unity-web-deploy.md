---
description: Workflow for optimizing, building, and deploying Unity projects to the WebGL platform.
---

# Workflow: Unity Web Deployment

Transform your Unity project into a high-performance WebGL application.

1.  **Requirement Mapping**: 
    - Identify target browsers and devices (e.g., Mobile Safari vs. Desktop Chrome).
    - List required browser integrations (Analytics, Storage, Sharing).
2.  **Interop Setup**:
    - Use instructions in `.claude/skills/unity-web-deploy/references/WEBGL_INTEROP_PATTERNS.md` to bridge C# and JS.
    - Create required `.jslib` files in `Assets/Plugins/WebGL/`.
3.  **Build Optimization**:
    - Audit build settings (Brotli, Memory Size, Compression Fallback).
    - Use `.claude/skills/unity-web-deploy/references/WEBGL_OPTIMIZATION_GUIDE.md` to reduce build size.
4.  **Execute Build**:
    // turbo
    - Build the project and analyze the output distribution (`wasm`, `data`).
5.  **Technical Audit**:
    - Use the `WEBGL_BUILD_REPORT.md` template from `.claude/skills/unity-web-deploy/assets/templates/`.
    - Save to `Documents/WebBuilds/REPORT_[BuildName].md`.
6.  **Verification**:
    - Verify server environment (HTTPS, MIME types, COOP/COEP headers).

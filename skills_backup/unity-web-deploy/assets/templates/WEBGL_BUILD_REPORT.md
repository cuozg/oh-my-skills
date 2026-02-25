# WebGL Build & Performance Report: [Project Name]

## 1. Build Summary
- **Unity Version**: [e.g., 2022.3.x]
- **Target Platform**: WebGL
- **Compression**: [Brotli/Gzip/None]
- **Build Size**: [Total MB]
  - `wasm`: [MB]
  - `data`: [MB]

## 2. Browser Compatibility Analysis
- **Supported Browsers**: [Chrome, Firefox, Safari, Edge]
- **Mobile Browser Support**: [Yes/No - Android/iOS versions]
- **Memory Requirements**: [Initial MB]
- **Graphic API**: [WebGL 2.0 / 1.0 Fallback]

## 3. Performance Profiling
- **Load Time (Initial)**: [Seconds]
- **Load Time (Cached)**: [Seconds]
- **Runtime FPS (Desktop)**: [Avg FPS]
- **Runtime FPS (Mobile)**: [Avg FPS]
- **Memory Hotspots**: [e.g., Audio, Large Textures]

## 4. Optimization Actions
### Implemented
- [ ] Enabled Brotli compression
- [ ] Optimized Texture max size
- [ ] Implemented Addressables for [Feature]

### Recommended
- [ ] Convert [Component] to use Object Pooling
- [ ] Reduce initial memory cap to [MB]
- [ ] Optimize [Shader] for mobile web

## 5. Deployment Checklist
- [ ] HTTPS enabled (Required for many APIs)
- [ ] Cross-Origin headers configured (`COOP`/`COEP`)
- [ ] PWA Manifest and Service Worker verified
- [ ] Analytics tracking confirmed

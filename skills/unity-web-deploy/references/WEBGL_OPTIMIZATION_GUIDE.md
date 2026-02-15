# WebGL Optimization Guide

Expert guide for optimizing build size, loading time, and runtime performance on the WebGL platform.

## 1. Build Player Settings

- **Compression Format**: 
  - `Brotli`: Best compression, slowest compression time. Suggested for production.
  - `Gzip`: Standard compression.
  - `Disabled`: Fastest builds, but huge files. Only for local testing.
- **Decompression Fallback**: Enable this to allow browsers that don't support native compression to run the game (it includes a JS decompressor).
- **Code Optimization**: Use `Size` for smallest builds or `Speed` for performance.
- **Exception Support**: Set to `None` for production if possible to reduce builds by ~5-10%.
- **Data Caching**: Enable to store build data in IndexedDB for faster subsequent loads.

## 2. Memory Management

- **Initial Memory Size**: Set this carefully. If it's too high, mobile browsers may refuse to run. Usually 256MB or 512MB is a good baseline.
- **Memory Growth**: Enabled by default in modern Unity. It allows the heap to expand, but fragments can cause issues.
- **Garbage Collection**: WebGL uses a single-threaded GC. Frequent allocations cause stutter. Use **Object Pooling** and avoid `Update()` allocations.

## 3. Graphics & Assets

- **Texture Compression**: Use `ASTC` for mobile browser support or `Crunched` for smallest download size.
- **Color Space**: `Gamma` is generally faster and more compatible on older browsers than `Linear`.
- **Anisotropic Filtering**: Disable or set to `Force Enable` only for critical assets to save GPU memory.

## 4. Loading Optimization

- **Addressables**: Highly recommended for WebGL. Download assets on demand to keep the initial load under 10-20MB.
- **Progressive Loading**: Build a custom loading screen that updates based on `unityInstance.Progress`.
- **Pre-warming**: Avoid heavy `Awake` logic in the first scene. Initialize complex systems lazily.

## 5. Known Platform Limits
- **No Multithreading**: Everything runs on the main browser thread (though `WebWorker` support is improving).
- **Audio Constraints**: Browsers require a user interaction (click/touch) before audio can play.
- **Persistence**: Use `PlayerPrefs` (which maps to IndexedDB) or native `localStorage` via interop.

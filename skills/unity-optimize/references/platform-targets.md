# Platform Performance Targets

## Frame Budget by Platform

| Platform | Target FPS | Frame Budget | CPU Target | GPU Target |
|----------|-----------|-------------|------------|------------|
| Mobile (low-end) | 30 | 33.3 ms | 20 ms | 25 ms |
| Mobile (flagship) | 60 | 16.67 ms | 10 ms | 12 ms |
| PC (mid-range) | 60 | 16.67 ms | 10 ms | 12 ms |
| PC (high-end) | 120+ | 8.33 ms | 5 ms | 6 ms |
| Console (PS5/XSX) | 60 | 16.67 ms | 10 ms | 12 ms |
| Console (Switch) | 30 | 33.3 ms | 20 ms | 25 ms |
| VR (Quest 2) | 72 | 13.9 ms | 8 ms | 10 ms |
| VR (PCVR) | 90 | 11.1 ms | 7 ms | 8 ms |
| WebGL | 30-60 | 16.67-33.3 ms | 12 ms | 15 ms |

## Draw Call Budgets

| Platform | Max Draw Calls | Max SetPass | Batches Target |
|----------|---------------|-------------|----------------|
| Mobile (low) | 100-200 | 50-100 | < 150 |
| Mobile (flagship) | 200-500 | 100-200 | < 300 |
| PC | 1000-3000 | 500-1000 | < 2000 |
| Console | 2000-5000 | 500-1500 | < 3000 |
| WebGL | 100-300 | 50-150 | < 200 |

## Memory Budgets

| Platform | Total App Memory | Textures | Audio | Meshes |
|----------|-----------------|----------|-------|--------|
| Mobile 2GB | 600-800 MB | 200-300 MB | 30-50 MB | 50-100 MB |
| Mobile 4GB | 1.2-1.5 GB | 400-600 MB | 50-80 MB | 100-200 MB |
| PC | 2-4 GB | 1-2 GB | 100-200 MB | 200-500 MB |
| Console | 3-5 GB | 1.5-3 GB | 150-300 MB | 300-600 MB |
| WebGL | 256-512 MB | 100-200 MB | 20-50 MB | 50-100 MB |

## Thermal Throttling (Mobile)

| State | Clock Reduction | Action |
|-------|----------------|--------|
| Nominal | 0% | Full quality |
| Fair | 0-10% | Monitor, no changes |
| Serious | 10-30% | Reduce particles, shadow res |
| Critical | 30-50% | Drop to 30fps, disable post-fx |

Design for **0.65x of peak** performance to sustain without throttling.

## Physics Budget

| Platform | Max Rigidbodies | Max Colliders | FixedUpdate Target |
|----------|----------------|---------------|-------------------|
| Mobile | 50-100 | 200-500 | 0.02-0.033s (30-50Hz) |
| PC | 200-500 | 1000-3000 | 0.01-0.02s (50-100Hz) |
| Console | 200-500 | 1000-3000 | 0.016-0.02s (50-60Hz) |

## Build Size Targets

| Platform | Max Recommended | Compression |
|----------|----------------|-------------|
| Mobile (store) | < 150 MB initial | LZ4HC + asset bundles |
| PC (Steam) | < 2 GB | LZ4HC |
| WebGL | < 30 MB initial | Brotli |
| Console | Platform-dependent | LZ4HC |

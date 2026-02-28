# Performance Checklist - Advanced Optimization

## Rendering Advanced

### Advanced Batching
- [ ] SRP Batcher requirements met (constant buffer alignment, material structure)
- [ ] GPU instancing keywords set (`_INSTANCING_ON`)
- [ ] Instance data buffers properly allocated (compute buffer size)
- [ ] DrawMesh indirect used for large batches (avoid per-mesh draw call)

### Shader Optimization
- [ ] Shaders use lowest precision needed (float → half on mobile if safe)
- [ ] Branches in shaders minimized (branching breaks wave efficiency on GPU)
- [ ] Texture fetch patterns optimized (not dependent texture reads)
- [ ] Complex math moved to vertex shader when possible

## Advanced Memory

### Memory Mapping
- [ ] Resident set size tracked (actual physical memory)
- [ ] Working set identified (what's actively used vs paged)
- [ ] Cache coherency considered for tight loops
- [ ] Memory fragmentation checked (long-term allocation pattern)

### Custom Allocators
- [ ] Object pool allocators used for frequent small objects
- [ ] Ring buffers for streaming data
- [ ] Pre-allocated per-frame transient allocators

## Concurrency & Threading

- [ ] Job system used for multi-threaded physics queries
- [ ] Burst compilation enabled for hot Job code
- [ ] Data races prevented (shared data guarded or thread-local)
- [ ] Job scheduling batched (not per-frame job creation)

## Optimization Trade-offs

| Technique | Pro | Con |
|:---|:---|:---|
| Aggressive LOD | Huge FPS gain | Visual pops |
| Reduced precision | GPU memory/perf | Precision artifacts |
| Async loading | No hitches | Complexity spike |
| Instancing | Draw calls drop | Limits variation |

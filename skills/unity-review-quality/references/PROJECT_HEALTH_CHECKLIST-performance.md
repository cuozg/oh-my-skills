# Project Health Checklist - Performance & Advanced Topics

## Performance Auditing

### Profiler Health
- [ ] Have you profiled in Development Build mode?
- [ ] CPU > GPU or GPU > CPU bottleneck identified?
- [ ] Frame time budget allocated (16.7ms for 60fps, 33.3ms for 30fps)?
- [ ] Memory target set per platform (512MB mobile, 2GB desktop)?
- [ ] GC spike frequency tracked (should be < 1 spike per 10 sec)

### Common Hotspots
- [ ] Update/FixedUpdate methods reviewed for allocations
- [ ] Physics query calls use layer masks and maxDistance
- [ ] Networking traffic minimized (delta compression, culling)
- [ ] Asset loading is async (no frame hitches)
- [ ] UI Canvas updates batched (not per-frame markup changes)

## Testing & QA

### Test Coverage
- [ ] Unit tests for game logic (stat calculations, progression)
- [ ] Integration tests for save/load
- [ ] UI tests for navigation flows
- [ ] Performance tests (frame time, memory over 5+ min sessions)

### Device Testing
- [ ] Tested on target min-spec device (not just high-end)
- [ ] Tested on both portrait and landscape (if applicable)
- [ ] Tested with low RAM devices (background app killing)
- [ ] Tested with slow network conditions

## Documentation

- [ ] README.md covers setup and build instructions
- [ ] Architecture diagram exists for major systems
- [ ] Gameplay designer walkthrough documented
- [ ] Known issues tracked (GitHub issues or wiki)

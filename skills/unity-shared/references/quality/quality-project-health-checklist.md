# Project Health Checklist

## Project Structure

### Folder Organization
- [ ] Root `Assets/` is organized (not a flat dump of files)
- [ ] Clear top-level folders: Scripts/, Prefabs/, Scenes/, Art/, Audio/, Materials/, etc.
- [ ] Editor scripts in Editor/ folders or Editor assemblies
- [ ] Test scripts in Tests/ folders with test assemblies
- [ ] Third-party code isolated in ThirdParty/ or Plugins/
- [ ] Resources/ folder minimal (prefer Addressables or direct references)
- [ ] StreamingAssets/ used appropriately (platform-specific raw files)
- [ ] No deeply nested folders (> 5 levels) without good reason

### Assembly Definitions Health
- [ ] .asmdef files exist for major code modules
- [ ] Runtime / Editor / Test assemblies properly separated
- [ ] No circular references between assemblies
- [ ] Assembly references are minimal (principle of least privilege)
- [ ] Platform filters set appropriately (Editor-only assemblies)
- [ ] Third-party code in separate assemblies (compilation isolation)

## Package & Dependency Management

### Package Health
- [ ] Using Unity Package Manager (not manual DLL imports)
- [ ] Package versions pinned (not "latest" floating)
- [ ] No deprecated packages (check Unity deprecation notices)
- [ ] Custom packages use proper package.json format
- [ ] No conflicting package versions
- [ ] Git-based packages pinned to specific commit/tag

### Third-Party Dependencies
- [ ] Each dependency justified (not "we might need it")
- [ ] License compatibility verified
- [ ] Update strategy documented
- [ ] No vendored code that should be a package
- [ ] Asset Store packages tracked (version, license)

## Version Control

### Git Configuration
- [ ] `.gitignore` covers: Library/, Temp/, Logs/, UserSettings/, *.csproj, *.sln
- [ ] `.gitattributes` configured for Unity (YAML merge, LFS for binaries)
- [ ] Git LFS for large binaries (textures, audio, models, videos)
- [ ] No large binary files committed without LFS
- [ ] Branch strategy defined (main/develop/feature)
- [ ] `.meta` files committed (Unity asset tracking)

### Commit Hygiene
- [ ] No committed secrets (API keys, passwords, tokens)
- [ ] No committed user-specific settings (UserSettings/)
- [ ] No committed build artifacts
- [ ] Merge conflict markers resolved (no `<<<<<<<` in files)

## Project Settings Audit

### Player Settings
- [ ] Company/product name set (not "DefaultCompany")
- [ ] Bundle identifier set for target platforms
- [ ] Minimum API level appropriate for target audience
- [ ] Scripting backend: IL2CPP for release, Mono for development
- [ ] API Compatibility Level: .NET Standard 2.1 or .NET Framework (consistent)
- [ ] Color space: Linear (not Gamma) for modern rendering
- [ ] Managed stripping: Medium or High for release builds

### Quality Settings
- [ ] Quality levels defined for target platforms
- [ ] Shadow settings appropriate (distance, resolution, cascades)
- [ ] LOD bias configured
- [ ] Anti-aliasing level set per quality tier
- [ ] VSync configured intentionally (not default)
- [ ] Texture quality per tier

### Physics Settings
- [ ] Fixed timestep appropriate (0.02 default = 50Hz)
- [ ] Gravity set correctly for game scale
- [ ] Layer collision matrix optimized (not all-vs-all)
- [ ] Default solver iterations appropriate
- [ ] Auto sync transforms: OFF for performance (manual sync)
- [ ] Contact pairs mode: appropriate for game type

### Graphics/Rendering Settings
- [ ] Render pipeline defined (URP/HDRP/Built-in) and consistent
- [ ] Shader stripping configured for target platforms

## Advanced Auditing

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

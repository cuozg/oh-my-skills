---
name: unity-build-pipeline
description: "(opencode-project - Skill) Unity build automation and pipeline configuration. Covers BuildPlayerOptions, build scripts, Addressables, asset bundles, CI/CD integration, platform-specific build settings, and build size optimization. Use when: (1) Automating builds with scripts, (2) Configuring Addressables or Asset Bundles, (3) Setting up CI/CD for Unity, (4) Optimizing build size, (5) Managing platform-specific build configs. Triggers: 'build pipeline', 'build script', 'Addressables', 'asset bundles', 'CI/CD', 'build automation', 'build size', 'build settings'."
---

# unity-build-pipeline — Build Automation & Pipeline Configuration

**Input**: Target platform(s), build requirements, optional Addressables config, CI/CD platform, size constraints

## Output
Build scripts (C# Editor), Addressables config, CI/CD pipeline YAML, and build optimization reports.

## Workflow

1. **Analyze platforms and requirements** — platforms, distribution channels, constraints
2. **Create build scripts** — `BuildPipeline.BuildPlayer` with `BuildPlayerOptions` per platform
3. **Configure Addressables** (if needed) — groups, profiles, build scripts, content catalogs
4. **Set up pre/post processors** — `IPreprocessBuildWithReport` / `IPostprocessBuildWithReport`
5. **Configure platform settings** — PlayerSettings scripting (icons, splash, bundle ID, signing)
6. **Add build reporting** — size analysis, build time, warning aggregation
7. **Integrate CI/CD** (if needed) — GitHub Actions, GitLab CI, Jenkins

## Build Scripts & Processors

See [references/build-scripts.md](references/build-scripts.md) for complete `BuildScript` and `BuildValidator` implementations with `BuildPlayerOptions`, error handling, and pre/post processor patterns.

## Build Size Optimization

See [references/build-size-optimization.md](references/build-size-optimization.md) for detailed strategies and typical savings per area (20-40% overall).

## Critical Anti-Patterns

| Anti-Pattern | Correct Pattern |
|:-------------|:----------------|
| Hardcoded paths in build scripts | `Path.Combine` + relative paths |
| No error handling in CI builds | Check `BuildResult`, exit with error code |
| Resources folder for all assets | Use Addressables or direct references |
| Missing LFS checkout in CI | `lfs: true` in checkout step |
| No Library cache in CI | Cache `Library/` folder by platform |
| Platform switching in build script | One CI job per platform |

## CI/CD Integration

GitHub Actions, GitLab CI, and Jenkins templates available in [references/ci-cd-templates.md](references/ci-cd-templates.md).

## Scripting Backend Selection

| Backend | Build Time | Performance | Use When |
|:--------|:-----------|:-----------|:---------|
| Mono | Fast | Good | Development, fast iteration |
| IL2CPP | Slow | Best | Release builds, mobile, console |

## Handoff & Boundaries

- **Does NOT handle**: Runtime asset loading logic, game logic, runtime Addressables API, native plugins

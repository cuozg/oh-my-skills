---
name: unity-build-pipeline
description: "(opencode-project - Skill) Unity build automation and pipeline configuration. Covers BuildPlayerOptions, build scripts, Addressables, asset bundles, CI/CD integration, platform-specific build settings, and build size optimization. Use when: (1) Automating builds with scripts, (2) Configuring Addressables or Asset Bundles, (3) Setting up CI/CD for Unity, (4) Optimizing build size, (5) Managing platform-specific build configs. Triggers: 'build pipeline', 'build script', 'Addressables', 'asset bundles', 'CI/CD', 'build automation', 'build size', 'build settings'."
---

# unity-build-pipeline — Build Automation & Pipeline Configuration

**Input**: Target platform(s), build requirements, optional Addressables config, CI/CD platform, size constraints
**Output**: Build scripts (C# Editor), Addressables config, CI/CD pipeline YAML, build optimization reports

## Workflow

1. **Analyze platforms and requirements** — platforms, distribution channels, constraints
2. **Create build scripts** — `BuildPipeline.BuildPlayer` with `BuildPlayerOptions` per platform
3. **Configure Addressables** (if needed) — groups, profiles, build scripts, content catalogs
4. **Set up pre/post processors** — `IPreprocessBuildWithReport` / `IPostprocessBuildWithReport`
5. **Configure platform settings** — PlayerSettings scripting (icons, splash, bundle ID, signing)
6. **Add build reporting** — size analysis, build time, warning aggregation
7. **Integrate CI/CD** (if needed) — GitHub Actions, GitLab CI, Jenkins

## Build Script Foundation

```csharp
using UnityEditor;
using UnityEditor.Build.Reporting;
using System.IO;
using System.Linq;

public static class BuildScript
{
    private const string BuildFolder = "Builds";

    [MenuItem("Build/Android (Release)")]
    public static void BuildAndroid()
    {
        var options = new BuildPlayerOptions
        {
            scenes = GetEnabledScenes(),
            locationPathName = Path.Combine(BuildFolder, "Android", "game.apk"),
            target = BuildTarget.Android,
            options = BuildOptions.CompressWithLz4HC
        };
        ConfigureAndroidSettings();
        ExecuteBuild(options);
    }

    private static void ExecuteBuild(BuildPlayerOptions options)
    {
        string dir = Path.GetDirectoryName(options.locationPathName);
        if (!string.IsNullOrEmpty(dir)) Directory.CreateDirectory(dir);

        BuildReport report = BuildPipeline.BuildPlayer(options);
        if (report.summary.result == BuildResult.Succeeded)
            Debug.Log($"Build succeeded: {report.summary.totalSize / (1024 * 1024):F1} MB");
        else
        {
            Debug.LogError($"Build failed: {report.summary.result}");
            if (Application.isBatchMode) EditorApplication.Exit(1);
        }
    }

    private static string[] GetEnabledScenes() =>
        EditorBuildSettings.scenes.Where(s => s.enabled).Select(s => s.path).ToArray();

    private static void ConfigureAndroidSettings()
    {
        PlayerSettings.Android.minSdkVersion = AndroidSdkVersions.AndroidApiLevel24;
        PlayerSettings.SetScriptingBackend(BuildTargetGroup.Android, ScriptingImplementation.IL2CPP);
        PlayerSettings.Android.targetArchitectures = AndroidArchitecture.ARM64;
    }
}
```

## Build Pre/Post Processors

```csharp
public class BuildValidator : IPreprocessBuildWithReport
{
    public int callbackOrder => 0;
    public void OnPreprocessBuild(BuildReport report)
    {
        var missing = EditorBuildSettings.scenes
            .Where(s => s.enabled && !File.Exists(s.path)).ToList();
        if (missing.Any())
            throw new BuildFailedException($"Missing scenes: {string.Join(", ", missing.Select(s => s.path))}");
    }
}
```

## GitHub Actions CI/CD Template

```yaml
name: Unity Build
on:
  push: { branches: [main, develop] }
  pull_request: { branches: [main] }
env:
  UNITY_LICENSE: ${{ secrets.UNITY_LICENSE }}
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        targetPlatform: [Android, WebGL]
    steps:
      - uses: actions/checkout@v4
        with: { lfs: true }
      - uses: actions/cache@v4
        with:
          path: Library
          key: Library-${{ matrix.targetPlatform }}-${{ hashFiles('Assets/**', 'Packages/**', 'ProjectSettings/**') }}
      - uses: game-ci/unity-builder@v4
        with:
          targetPlatform: ${{ matrix.targetPlatform }}
          buildMethod: BuildScript.Build${{ matrix.targetPlatform }}
      - uses: actions/upload-artifact@v4
        with:
          name: Build-${{ matrix.targetPlatform }}
          path: Builds/${{ matrix.targetPlatform }}
```

## Build Size Optimization

| Area | Action | Typical Savings |
|:-----|:-------|:---------------|
| Textures | Max 1024 for mobile, ASTC/ETC2 | 20-40% |
| Audio | Vorbis compression, quality 70% | 10-20% |
| Code stripping | IL2CPP + High stripping level | 5-15% |
| Unused assets | Remove from Resources, use Addressables | 10-30% |
| Shaders | Strip unused variants | 5-20% |

## Critical Anti-Patterns

| Anti-Pattern | Correct Pattern |
|:-------------|:----------------|
| Hardcoded paths in build scripts | `Path.Combine` + relative paths |
| No error handling in CI builds | Check `BuildResult`, exit with error code |
| Resources folder for all assets | Use Addressables or direct references |
| Missing LFS checkout in CI | `lfs: true` in checkout step |
| No Library cache in CI | Cache `Library/` folder by platform |
| Platform switching in build script | One CI job per platform |

## Scripting Backend Selection

| Backend | Build Time | Performance | Use When |
|:--------|:-----------|:-----------|:---------|
| Mono | Fast | Good | Development, fast iteration |
| IL2CPP | Slow | Best | Release builds, mobile, console |

## Handoff & Boundaries

- **Does NOT handle**: Runtime asset loading logic, game logic, runtime Addressables API, native plugins

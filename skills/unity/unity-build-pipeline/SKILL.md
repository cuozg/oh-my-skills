---
name: unity-build-pipeline
description: "(opencode-project - Skill) Unity build automation and pipeline configuration. Covers BuildPlayerOptions, build scripts, Addressables, asset bundles, CI/CD integration, platform-specific build settings, and build size optimization. Use when: (1) Automating builds with scripts, (2) Configuring Addressables or Asset Bundles, (3) Setting up CI/CD for Unity, (4) Optimizing build size, (5) Managing platform-specific build configs. Triggers: 'build pipeline', 'build script', 'Addressables', 'asset bundles', 'CI/CD', 'build automation', 'build size', 'build settings'."
---

# unity-build-pipeline -- Build Automation & Pipeline Configuration

Automate and optimize Unity build processes -- from one-click build scripts to full CI/CD pipelines with Addressables, platform switching, and build size analysis.

## Purpose

Create reliable, repeatable build pipelines for Unity projects. Automate platform-specific builds, configure Addressables for content delivery, implement build pre/post processors, and integrate with CI/CD systems for continuous delivery.

## Input

- **Required**: Target platform(s), build requirements (what needs building, where it ships)
- **Optional**: Addressables configuration, CI/CD platform (GitHub Actions, GitLab CI, Jenkins), build size constraints, signing requirements

## Output

Build scripts (C# Editor scripts), Addressables configuration, CI/CD pipeline definitions (YAML), and build optimization reports. All scripts compile in Editor context and produce working builds.

## Examples

| User Request | Skill Action |
|:---|:---|
| "Automate Android and iOS builds" | Create `BuildScript.cs` with `BuildPipeline.BuildPlayer` for both platforms, configure PlayerSettings per platform |
| "Set up Addressables for DLC content" | Configure Addressables groups, profiles, build scripts, and remote content catalog |
| "Add GitHub Actions CI for Unity" | Create `.github/workflows/unity-build.yml` with GameCI, caching, artifact upload |
| "Reduce build size by 30%" | Analyze build report, configure stripping, optimize textures, identify unused assets |

## Workflow

1. **Analyze target platforms and requirements**: Identify platforms, distribution channels (App Store, Steam, WebGL hosting), and constraints
2. **Create build scripts**: Implement `BuildPipeline.BuildPlayer` with proper `BuildPlayerOptions` per platform
3. **Configure Addressables** (if applicable): Set up groups, profiles (local vs remote), build scripts, and content catalogs
4. **Set up build pre/post processors**: Implement `IPreprocessBuildWithReport` and `IPostprocessBuildWithReport` for validation and reporting
5. **Configure platform-specific settings**: PlayerSettings scripting (icons, splash, bundle ID, signing)
6. **Add build reporting**: Size analysis, build time tracking, warning aggregation
7. **Integrate with CI/CD** (if needed): GitHub Actions, GitLab CI, or Jenkins pipeline definitions

## Best Practices

### Build Script Foundation

```csharp
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEngine;
using System.IO;
using System.Linq;

/// <summary>
/// Automated build pipeline accessible from Editor menu and command line.
/// Usage: Unity -batchmode -executeMethod BuildScript.BuildAndroid
/// </summary>
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

    [MenuItem("Build/iOS (Release)")]
    public static void BuildiOS()
    {
        var options = new BuildPlayerOptions
        {
            scenes = GetEnabledScenes(),
            locationPathName = Path.Combine(BuildFolder, "iOS"),
            target = BuildTarget.iOS,
            options = BuildOptions.CompressWithLz4HC
        };

        ConfigureiOSSettings();
        ExecuteBuild(options);
    }

    [MenuItem("Build/WebGL (Release)")]
    public static void BuildWebGL()
    {
        var options = new BuildPlayerOptions
        {
            scenes = GetEnabledScenes(),
            locationPathName = Path.Combine(BuildFolder, "WebGL"),
            target = BuildTarget.WebGL,
            options = BuildOptions.None
        };

        ConfigureWebGLSettings();
        ExecuteBuild(options);
    }

    private static void ExecuteBuild(BuildPlayerOptions options)
    {
        // Ensure output directory exists
        string dir = Path.GetDirectoryName(options.locationPathName);
        if (!string.IsNullOrEmpty(dir))
            Directory.CreateDirectory(dir);

        BuildReport report = BuildPipeline.BuildPlayer(options);
        BuildSummary summary = report.summary;

        if (summary.result == BuildResult.Succeeded)
        {
            Debug.Log($"Build succeeded: {summary.totalSize / (1024 * 1024):F1} MB in {summary.totalTime.TotalSeconds:F1}s");
            LogBuildReport(report);
        }
        else
        {
            Debug.LogError($"Build failed: {summary.result}");
            // Exit with error code for CI/CD
            if (Application.isBatchMode)
                EditorApplication.Exit(1);
        }
    }

    private static string[] GetEnabledScenes()
    {
        return EditorBuildSettings.scenes
            .Where(s => s.enabled)
            .Select(s => s.path)
            .ToArray();
    }

    private static void LogBuildReport(BuildReport report)
    {
        // Log top 10 largest assets for size optimization
        var largestAssets = report.packedAssets
            .SelectMany(pa => pa.contents)
            .OrderByDescending(entry => entry.packedSize)
            .Take(10);

        Debug.Log("=== Top 10 Largest Assets ===");
        foreach (var asset in largestAssets)
        {
            Debug.Log($"  {asset.packedSize / 1024:F0} KB - {asset.sourceAssetPath}");
        }
    }

    private static void ConfigureAndroidSettings()
    {
        PlayerSettings.Android.minSdkVersion = AndroidSdkVersions.AndroidApiLevel24;
        PlayerSettings.Android.targetSdkVersion = AndroidSdkVersions.AndroidApiLevelAuto;
        PlayerSettings.SetScriptingBackend(BuildTargetGroup.Android, ScriptingImplementation.IL2CPP);
        PlayerSettings.Android.targetArchitectures = AndroidArchitecture.ARM64;
    }

    private static void ConfigureiOSSettings()
    {
        PlayerSettings.SetScriptingBackend(BuildTargetGroup.iOS, ScriptingImplementation.IL2CPP);
        PlayerSettings.iOS.targetOSVersionString = "14.0";
    }

    private static void ConfigureWebGLSettings()
    {
        PlayerSettings.WebGL.compressionFormat = WebGLCompressionFormat.Brotli;
        PlayerSettings.WebGL.linkerTarget = WebGLLinkerTarget.Wasm;
    }
}
```

### Build Pre/Post Processors

```csharp
using UnityEditor.Build;
using UnityEditor.Build.Reporting;

/// <summary>
/// Pre-build validation -- blocks builds that would fail or ship broken.
/// </summary>
public class BuildValidator : IPreprocessBuildWithReport
{
    public int callbackOrder => 0;

    public void OnPreprocessBuild(BuildReport report)
    {
        // Validate all scenes in build settings exist
        var missingScenes = EditorBuildSettings.scenes
            .Where(s => s.enabled && !File.Exists(s.path))
            .ToList();

        if (missingScenes.Any())
        {
            string missing = string.Join(", ", missingScenes.Select(s => s.path));
            throw new BuildFailedException($"Missing scenes in build: {missing}");
        }

        // Validate required define symbols
        string defines = PlayerSettings.GetScriptingDefineSymbolsForGroup(
            report.summary.platformGroup);

        if (report.summary.platform == BuildTarget.Android &&
            !defines.Contains("ANDROID_BUILD"))
        {
            Debug.LogWarning("ANDROID_BUILD define symbol not set");
        }
    }
}

/// <summary>
/// Post-build reporting and artifact management.
/// </summary>
public class BuildReporter : IPostprocessBuildWithReport
{
    public int callbackOrder => 0;

    public void OnPostprocessBuild(BuildReport report)
    {
        var summary = report.summary;
        long sizeMB = summary.totalSize / (1024 * 1024);

        Debug.Log($"[Build Complete] Platform: {summary.platform}, " +
                  $"Size: {sizeMB} MB, Time: {summary.totalTime.TotalSeconds:F1}s, " +
                  $"Warnings: {summary.totalWarnings}, Errors: {summary.totalErrors}");
    }
}
```

### Define Symbols Management

```csharp
/// <summary>
/// Manage scripting define symbols for feature flags and platform configs.
/// </summary>
public static class DefineSymbolsManager
{
    /// <summary>Add a define symbol for the specified platform group.</summary>
    public static void AddDefine(string symbol, BuildTargetGroup group)
    {
        string defines = PlayerSettings.GetScriptingDefineSymbolsForGroup(group);
        if (!defines.Contains(symbol))
        {
            defines = string.IsNullOrEmpty(defines) ? symbol : $"{defines};{symbol}";
            PlayerSettings.SetScriptingDefineSymbolsForGroup(group, defines);
        }
    }

    /// <summary>Remove a define symbol for the specified platform group.</summary>
    public static void RemoveDefine(string symbol, BuildTargetGroup group)
    {
        string defines = PlayerSettings.GetScriptingDefineSymbolsForGroup(group);
        defines = string.Join(";", defines.Split(';').Where(d => d != symbol));
        PlayerSettings.SetScriptingDefineSymbolsForGroup(group, defines);
    }
}
```

### GitHub Actions CI/CD Template

```yaml
# .github/workflows/unity-build.yml
name: Unity Build

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  UNITY_LICENSE: ${{ secrets.UNITY_LICENSE }}

jobs:
  build:
    name: Build for ${{ matrix.targetPlatform }}
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        targetPlatform:
          - Android
          - WebGL

    steps:
      - uses: actions/checkout@v4
        with:
          lfs: true

      - uses: actions/cache@v4
        with:
          path: Library
          key: Library-${{ matrix.targetPlatform }}-${{ hashFiles('Assets/**', 'Packages/**', 'ProjectSettings/**') }}
          restore-keys: |
            Library-${{ matrix.targetPlatform }}-
            Library-

      - uses: game-ci/unity-builder@v4
        with:
          targetPlatform: ${{ matrix.targetPlatform }}
          buildMethod: BuildScript.Build${{ matrix.targetPlatform }}

      - uses: actions/upload-artifact@v4
        with:
          name: Build-${{ matrix.targetPlatform }}
          path: Builds/${{ matrix.targetPlatform }}
```

### Build Size Optimization Checklist

| Area | Action | Typical Savings |
|:-----|:-------|:---------------|
| Textures | Max size 1024 for mobile, compress with ASTC/ETC2 | 20-40% |
| Audio | Use Vorbis compression, reduce quality to 70% | 10-20% |
| Meshes | Enable mesh compression, strip unused channels | 5-10% |
| Code stripping | IL2CPP + High stripping level | 5-15% |
| Unused assets | Remove from Resources, use Addressables | 10-30% |
| Fonts | Subset fonts to used characters only | 1-5% |
| Shaders | Strip unused shader variants | 5-20% |

### Scripting Backend Selection

| Backend | Build Time | Runtime Performance | Platform | Use When |
|:--------|:-----------|:-------------------|:---------|:---------|
| Mono | Fast | Good | Editor, Standalone | Development, fast iteration |
| IL2CPP | Slow (C++ compile) | Best | All platforms | Release builds, mobile, console |

### Critical Anti-Patterns

| Anti-Pattern | Why It Fails | Correct Pattern |
|:-------------|:-------------|:----------------|
| Hardcoded paths in build scripts | Breaks on different machines/CI | Use `Path.Combine` and relative paths |
| No error handling in CI builds | Silent failures waste CI time | Check `BuildResult`, exit with error code in batch mode |
| Resources folder for all assets | Entire folder ships in build even if unused | Use Addressables or direct references |
| Missing `LFS` checkout in CI | Large assets corrupted or missing | `lfs: true` in checkout step |
| No Library cache in CI | 30+ minute reimport every build | Cache `Library/` folder by platform |
| Platform switching in build script | Triggers full reimport | One CI job per platform, no runtime switching |

## Handoff & Boundaries

### Does NOT Handle
- Runtime asset loading logic (only build-time pipeline configuration)
- Game logic or gameplay features
- Runtime Addressables loading API (only Addressables build configuration)
- Platform-specific native plugins (only build script integration)

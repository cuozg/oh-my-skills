# Build Script Reference

Complete example of a buildable, cross-platform build system using BuildPlayerOptions and platform-specific configuration.

## Main Build Script

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

## Build Validator (Pre-Processor)

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

## Key Patterns

- Use `Path.Combine` for cross-platform paths
- Always check `BuildResult` and exit with error code in batch mode
- Cache `GetEnabledScenes()` result; don't recompute
- Separate build options from execution
- Use `BuildPlayerOptions` instead of hardcoded target specs

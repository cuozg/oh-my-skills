# Batchmode Reference

Unity CLI arguments for headless compile checks. Source: Unity 6.3 LTS docs + UnityCsReference.

## Core Arguments

| Argument | Description |
|----------|-------------|
| `-batchmode` | Run without GUI. Exits with code 1 on script/asset exceptions. Required for CI. |
| `-quit` | Exit after all commands finish. 300s default timeout (configure with `-quitTimeout`). |
| `-nographics` | Skip GPU init — works on headless servers. **Pair with explicit `-logFile`** or log output is suppressed. |
| `-projectPath <path>` | Absolute path to Unity project root. Quote if spaces in path. |
| `-logFile <path>` | Write log to file. Use `-` for stdout. |
| `-executeMethod <Class.Method>` | Run a static Editor method after project opens. Method must be in `Assets/Editor/`. |
| `-buildTarget <target>` | Compile for specific platform: `WebGL`, `Android`, `iOS`, `StandaloneWindows64`, `StandaloneOSX`, `StandaloneLinux64` |
| `-ignorecompilererrors` | Continue startup despite compile errors (diagnostic use only). |
| `-accept-apiupdate` | Run API Updater in batchmode (omitting can cause false compile errors). |
| `-timestamps` | Prefix log lines with timestamp + thread ID. |
| `-quitTimeout <seconds>` | Override the 300s default quit timeout. |

## Minimal Compile Check

```bash
"/path/to/Unity" \
  -batchmode -quit -nographics \
  -projectPath "/path/to/project" \
  -logFile /tmp/unity_compile.log
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success — compiled without errors (but verify log — see caveat below) |
| 1 | General failure — unhandled exception or `EditorApplication.Exit(1)` |
| N | Custom code via `EditorApplication.Exit(N)` |
| 101 | Build Failed (game-ci convention) |
| 102 | Build Cancelled (game-ci convention) |
| 103 | Build Unknown (game-ci convention) |

**Caveat:** Exit code 0 does NOT guarantee clean compile. Unity exits 0 if `-ignorecompilererrors` is set, or if `-executeMethod` catches exceptions. Always parse the log file too.

## Unity Editor Paths

### macOS
```
/Applications/Unity/Hub/Editor/<version>/Unity.app/Contents/MacOS/Unity
```

### Linux
```
~/Unity/Hub/Editor/<version>/Editor/Unity
```

### Windows
```
C:\Program Files\Unity\Hub\Editor\<version>\Editor\Unity.exe
```

### Read Project Version
```bash
head -1 "<projectPath>/ProjectSettings/ProjectVersion.txt"
# Output: m_EditorVersion: 2022.3.62f1
```

## Environment Variables for Non-Interactive Mode

Set these to prevent interactive prompts from tools Unity may trigger:

```bash
export CI=true
export DEBIAN_FRONTEND=noninteractive
export GIT_TERMINAL_PROMPT=0
export GCM_INTERACTIVE=never
export HOMEBREW_NO_AUTO_UPDATE=1
export GIT_EDITOR=: EDITOR=: VISUAL=''
export GIT_SEQUENCE_EDITOR=: GIT_MERGE_AUTOEDIT=no
export GIT_PAGER=cat PAGER=cat
export npm_config_yes=true PIP_NO_INPUT=1
export YARN_ENABLE_IMMUTABLE_INSTALLS=false
```

## Library Folder Caching

Cold starts can take 10+ minutes on large projects. Cache `<ProjectPath>/Library/` keyed on `ProjectSettings/ProjectSettings.asset` hash.

```yaml
# GitHub Actions cache example
- uses: actions/cache@v4
  with:
    path: MyProject/Library
    key: Library-${{ runner.os }}-${{ hashFiles('MyProject/ProjectSettings/ProjectSettings.asset') }}
```

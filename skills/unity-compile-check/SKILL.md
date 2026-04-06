---
name: unity-compile-check
description: >
  Run Unity batchmode compile checks and parse Unity Editor log files for errors. MUST use whenever
  an agent needs to verify C# code compiles in Unity — this is the ground-truth compilation check.
  Use after writing scripts, refactoring, fixing bugs, changing asmdef references, updating packages,
  or before committing multi-file changes. Use to parse existing Unity log files from CI or build
  machines. Triggers: "does it compile," "compile check," "verify compilation," "Unity log," "parse
  log," "batchmode," "compile errors," "check for errors," "headless compile," "run Unity compiler,"
  "CI compile failed." ALWAYS use when lsp_diagnostics is not enough — cross-assembly errors, platform
  defines, asmdef boundaries, domain reload issues. Do not use for runtime debugging (unity-debug),
  performance (unity-optimize), or writing code (unity-code).
metadata:
  author: kuozg
  version: "1.0"
---

# unity-compile-check

Run a headless Unity compile check via batchmode CLI, parse the log output, and report errors/warnings in a structured format. This is the definitive way to verify code compiles in Unity when no Editor instance is running or when Unity MCP is unavailable.

## Why This Skill Exists

`lsp_diagnostics` catches most C# syntax and type errors, but it can miss:
- Cross-assembly reference issues (asmdef boundaries)
- Unity-specific compilation contexts (editor-only code, platform defines)
- Script import errors that only surface during Unity's domain reload
- Package version conflicts and assembly resolution failures
- Preprocessor directive issues (`#if UNITY_EDITOR`, `#if UNITY_WEBGL`, etc.)

Running the actual Unity compiler via batchmode is the ground truth. When the Unity Editor isn't open or MCP console tools aren't available, this skill fills that verification gap.

## Step 1 — Detect Mode

| Signal | Mode | Action |
|--------|------|--------|
| "Check if it compiles," code just written/changed, post-refactor | **Compile** | Run batchmode compile, report results |
| "Read the Unity log," "what errors are in the log," log file path given | **Parse** | Parse existing log file, extract errors |
| CI pipeline setup, "add compile check to CI" | **CI** | Generate CI-ready compile check config |

## Step 2 — Gather Parameters

Before running, collect these (ask if not obvious from context):

| Parameter | Source | Fallback |
|-----------|--------|----------|
| **Unity Editor path** | User's system, check common paths | Auto-detect (see below) |
| **Project path** | Current working context or user-specified | Ask user |
| **Log file path** | User-specified or temp | `/tmp/unity_compile_check.log` |
| **Platform target** | User's target platform | Current platform (no `-buildTarget` flag) |

### Auto-Detect Unity Editor Path

Check these locations in order:

**macOS:**
```
/Applications/Unity/Hub/Editor/*/Unity.app/Contents/MacOS/Unity
```

**Linux:**
```
~/Unity/Hub/Editor/*/Editor/Unity
```

**Windows:**
```
C:\Program Files\Unity\Hub\Editor\*\Editor\Unity.exe
```

If multiple versions found, prefer the one matching the project's `ProjectSettings/ProjectVersion.txt`.

To read the project version:
```bash
cat "<projectPath>/ProjectSettings/ProjectVersion.txt" | head -1
```
This returns something like `m_EditorVersion: 2022.3.62f1` — match this against installed editors.

## Step 3 — Execute Compile Check

### Compile Mode

Run the Unity batchmode compile using the bundled script:

```bash
run_skill_script("unity-compile-check", "scripts/compile_check.sh", [
  "<unity-editor-path>",
  "<project-path>",
  "<log-file-path>"
])
```

Or run directly:

```bash
export CI=true DEBIAN_FRONTEND=noninteractive GIT_TERMINAL_PROMPT=0 \
  GCM_INTERACTIVE=never HOMEBREW_NO_AUTO_UPDATE=1 GIT_EDITOR=: \
  EDITOR=: VISUAL='' GIT_SEQUENCE_EDITOR=: GIT_MERGE_AUTOEDIT=no \
  GIT_PAGER=cat PAGER=cat npm_config_yes=true PIP_NO_INPUT=1 \
  YARN_ENABLE_IMMUTABLE_INSTALLS=false

"<unity-editor-path>" \
  -batchmode \
  -quit \
  -nographics \
  -projectPath "<project-path>" \
  -logFile "<log-file-path>"
```

**Important flags:**
- `-batchmode` — run without GUI
- `-quit` — exit after finishing
- `-nographics` — skip GPU initialization (faster, works on headless servers)
- `-logFile` — redirect log to a specific file for parsing
- `-projectPath` — absolute path to the Unity project root

**Optional flags:**
- `-buildTarget <target>` — compile for a specific platform (e.g., `WebGL`, `Android`, `iOS`, `StandaloneWindows64`)
- `-executeMethod <Class.Method>` — run a specific static method after compile (for custom build scripts)
- `-logFile -` — log to stdout instead of file (useful for CI streaming)

**Timeout:** Unity compile can take 30 seconds to several minutes depending on project size. Set a reasonable timeout (default: 5 minutes). If it hangs, kill the process and report the partial log.

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success — compiled without errors |
| 1 | General error — check log for details |
| 2 | Platform not supported or invalid arguments |
| Non-zero | Compile or script errors — parse log for specifics |

**Exit code 0 does NOT guarantee zero warnings.** Always parse the log even on success.

## Step 4 — Parse the Log

Use the bundled Python parser for structured output:

```bash
run_skill_script("unity-compile-check", "scripts/parse_unity_log.py", [
  "<log-file-path>"
])
```

Or parse manually. Unity log files have these key patterns:

### Error Patterns (regex)

```
# Compiler errors (CS#### codes)
^Assets/.+\.cs\(\d+,\d+\): error CS\d+: .+$

# Script import errors
^Failed to import script .+$

# Assembly errors
^Assembly .+ has reference to .+ which is not included$

# Shader errors
^Shader error in '.+': .+$

# General Unity errors
^Error: .+$
```

### Warning Patterns (regex)

```
# Compiler warnings
^Assets/.+\.cs\(\d+,\d+\): warning CS\d+: .+$

# Deprecation warnings
^.+ is obsolete: .+$

# Asset import warnings
^WARNING: .+$
```

### Log Sections

Unity logs have a predictable structure:

1. **Header** — Unity version, OS, project path
2. **Package Manager** — package resolution (look for errors here)
3. **Script Compilation** — the critical section; compiler errors appear here
4. **Asset Import** — texture/model/audio import (errors here = asset issues)
5. **Domain Reload** — assembly loading (errors here = asmdef/reference issues)
6. **Shutdown** — cleanup (usually ignorable)

Focus parsing on sections 2-5. The script compilation section is bounded by lines like:
```
- Starting script compilation
...
- Finished script compilation
```

## Step 5 — Report Results

### Output Format

```
## Unity Compile Check Results

**Project:** <project-path>
**Unity Version:** <version>
**Exit Code:** <code>
**Status:** PASS | FAIL

### Errors (<count>)

| File | Line | Code | Message |
|------|------|------|---------|
| Assets/Scripts/Player.cs | 42 | CS0246 | The type or namespace 'Foo' could not be found |

### Warnings (<count>)

| File | Line | Code | Message |
|------|------|------|---------|
| Assets/Scripts/Old.cs | 10 | CS0618 | 'Thing' is obsolete |

### Summary
- <N> error(s), <M> warning(s)
- First error: <file>:<line> — <message>
```

### Interpretation Guide

When reporting results, help the agent/user understand what to do:

| Error Type | Common Cause | Fix Direction |
|------------|-------------|---------------|
| `CS0246` — type not found | Missing using, asmdef ref, or deleted class | Check asmdef references, add using statement |
| `CS0103` — name not found | Typo, missing variable, wrong scope | Check spelling, verify scope |
| `CS0029` — cannot convert | Type mismatch | Check types, add cast or fix assignment |
| `CS1061` — no definition | Wrong type, missing method | Check class hierarchy, verify API |
| `CS0234` — namespace missing | Missing package or asmdef | Check Package Manager, asmdef deps |
| Script import failed | Syntax error or Unity-specific issue | Check file encoding (UTF-8 BOM), line endings |
| Assembly reference | asmdef dependency missing | Add reference in .asmdef file |

## Parse Mode

When the user provides a log file path or asks to read an existing Unity log:

1. Read the log file
2. Run the parser: `run_skill_script("unity-compile-check", "scripts/parse_unity_log.py", ["<log-path>"])`
3. Report using the same output format as Compile mode
4. If no errors found, confirm: "Log is clean — no compile errors or warnings detected."

## CI Mode

Generate a CI-compatible compile check configuration. Provide the appropriate config for the user's CI system:

### GitHub Actions
```yaml
- name: Unity Compile Check
  run: |
    xvfb-run --auto-servernum \
      /path/to/Unity -batchmode -quit -nographics \
      -projectPath . \
      -logFile /tmp/unity_compile.log || true
    python parse_unity_log.py /tmp/unity_compile.log --ci
  timeout-minutes: 10
```

### Shell Script (Generic CI)
```bash
#!/bin/bash
set -euo pipefail
UNITY_PATH="${UNITY_PATH:-/Applications/Unity/Hub/Editor/2022.3.62f2/Unity.app/Contents/MacOS/Unity}"
PROJECT_PATH="${PROJECT_PATH:-.}"
LOG_FILE="/tmp/unity_compile_$(date +%s).log"

"$UNITY_PATH" -batchmode -quit -nographics \
  -projectPath "$PROJECT_PATH" \
  -logFile "$LOG_FILE" 2>&1 || true

python parse_unity_log.py "$LOG_FILE" --ci
exit $?
```

## Rules

- **Always parse the log**, even if exit code is 0 — warnings still matter
- **Never skip the compile check** when asked to verify — lsp_diagnostics is not a substitute for the real Unity compiler
- **Report the full error list**, not just the first error — cascading errors need root-cause identification
- **Preserve the log file** after parsing — the user may need it for further investigation
- **Timeout gracefully** — if Unity hangs, kill after timeout and report partial results
- **Match Unity version** — always try to use the same Unity Editor version the project was created with

## Integration with Other Skills

This skill complements the existing Unity verification chain:

| Tool | Speed | Scope | When to Use |
|------|-------|-------|-------------|
| `lsp_diagnostics` | Instant | Single-file type/syntax | After every edit (mandatory) |
| Unity MCP `ReadConsole` | Fast | Running Editor state | When Editor is open |
| **unity-compile-check** | Slow (30s-5m) | Full project compile | When MCP unavailable, cross-assembly changes, CI |

**Escalation path:** `lsp_diagnostics` (fast, limited) → Unity MCP (medium, requires Editor) → **unity-compile-check** (slow, definitive)

## Standards

Load shared references on demand via `read_skill_file("unity-standards", "references/<path>")`:

- `debug/compile-verification.md` — shared compile verification patterns, error code reference, log parsing regex
- `debug/common-unity-errors.md` — runtime error reference table
- `other/unity-mcp-routing-matrix.md` — MCP console tool decision tree

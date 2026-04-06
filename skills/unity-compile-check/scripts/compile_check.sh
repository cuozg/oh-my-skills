#!/usr/bin/env bash
# unity-compile-check: Run Unity batchmode compile and report results
# Usage: compile_check.sh <unity-editor-path> <project-path> [log-file-path] [timeout-seconds] [build-target]
#
# Arguments:
#   unity-editor-path  - Path to Unity Editor binary
#   project-path       - Path to Unity project root (must contain Assets/)
#   log-file-path      - Where to write the log (default: /tmp/unity_compile_check.log)
#   timeout-seconds    - Max time to wait for compile (default: 300)
#   build-target       - Optional: WebGL, Android, iOS, StandaloneWindows64, etc.
#
# Exit codes:
#   0 - Compile succeeded (no errors, may have warnings)
#   1 - Compile failed (errors found in log)
#   2 - Invalid arguments or Unity not found
#   3 - Timeout exceeded
#   4 - Unity crashed or unexpected failure

set -euo pipefail

UNITY_PATH="${1:-}"
PROJECT_PATH="${2:-}"
LOG_FILE="${3:-/tmp/unity_compile_check.log}"
TIMEOUT="${4:-300}"
BUILD_TARGET="${5:-}"

# --- Validation ---

if [[ -z "$UNITY_PATH" || -z "$PROJECT_PATH" ]]; then
    echo "ERROR: Usage: compile_check.sh <unity-editor-path> <project-path> [log-file-path] [timeout-seconds] [build-target]" >&2
    exit 2
fi

if [[ ! -f "$UNITY_PATH" && ! -d "$UNITY_PATH" ]]; then
    # On macOS, Unity path might point to the .app bundle
    if [[ "$UNITY_PATH" == *.app ]]; then
        UNITY_PATH="$UNITY_PATH/Contents/MacOS/Unity"
    fi
    if [[ ! -f "$UNITY_PATH" ]]; then
        echo "ERROR: Unity Editor not found at: $UNITY_PATH" >&2
        exit 2
    fi
fi

if [[ ! -x "$UNITY_PATH" ]]; then
    echo "ERROR: Unity Editor not executable: $UNITY_PATH" >&2
    exit 2
fi

if [[ ! -d "$PROJECT_PATH/Assets" ]]; then
    echo "ERROR: Not a Unity project (no Assets/ directory): $PROJECT_PATH" >&2
    exit 2
fi

# --- Setup Environment ---
# Suppress interactive prompts from various tools that Unity might trigger
export CI=true
export DEBIAN_FRONTEND=noninteractive
export GIT_TERMINAL_PROMPT=0
export GCM_INTERACTIVE=never
export HOMEBREW_NO_AUTO_UPDATE=1
export GIT_EDITOR=:
export EDITOR=:
export VISUAL=''
export GIT_SEQUENCE_EDITOR=:
export GIT_MERGE_AUTOEDIT=no
export GIT_PAGER=cat
export PAGER=cat
export npm_config_yes=true
export PIP_NO_INPUT=1
export YARN_ENABLE_IMMUTABLE_INSTALLS=false

# --- Read project version ---
VERSION_FILE="$PROJECT_PATH/ProjectSettings/ProjectVersion.txt"
if [[ -f "$VERSION_FILE" ]]; then
    PROJECT_VERSION=$(head -1 "$VERSION_FILE" | sed 's/m_EditorVersion: //')
    echo "Project Unity Version: $PROJECT_VERSION"
fi

# --- Clean previous log ---
rm -f "$LOG_FILE"

# --- Build command ---
UNITY_CMD=("$UNITY_PATH" -batchmode -quit -nographics -projectPath "$PROJECT_PATH" -logFile "$LOG_FILE")

if [[ -n "$BUILD_TARGET" ]]; then
    UNITY_CMD+=(-buildTarget "$BUILD_TARGET")
    echo "Build Target: $BUILD_TARGET"
fi

echo "Unity: $UNITY_PATH"
echo "Project: $PROJECT_PATH"
echo "Log: $LOG_FILE"
echo "Timeout: ${TIMEOUT}s"
echo "---"
echo "Starting compile check..."

# --- Run Unity with timeout ---
COMPILE_EXIT=0
if command -v timeout &>/dev/null; then
    # Linux / GNU coreutils
    timeout "$TIMEOUT" "${UNITY_CMD[@]}" 2>&1 || COMPILE_EXIT=$?
elif command -v gtimeout &>/dev/null; then
    # macOS with coreutils installed
    gtimeout "$TIMEOUT" "${UNITY_CMD[@]}" 2>&1 || COMPILE_EXIT=$?
else
    # Fallback: background process with manual timeout
    "${UNITY_CMD[@]}" 2>&1 &
    UNITY_PID=$!
    ELAPSED=0
    while kill -0 "$UNITY_PID" 2>/dev/null; do
        sleep 1
        ELAPSED=$((ELAPSED + 1))
        if [[ $ELAPSED -ge $TIMEOUT ]]; then
            echo "ERROR: Timeout after ${TIMEOUT}s — killing Unity process" >&2
            kill -9 "$UNITY_PID" 2>/dev/null || true
            wait "$UNITY_PID" 2>/dev/null || true
            echo "--- Partial log (last 50 lines) ---"
            if [[ -f "$LOG_FILE" ]]; then
                tail -50 "$LOG_FILE"
            fi
            exit 3
        fi
    done
    wait "$UNITY_PID" 2>/dev/null || COMPILE_EXIT=$?
fi

# Handle timeout exit code from GNU timeout (124)
if [[ $COMPILE_EXIT -eq 124 ]]; then
    echo "ERROR: Timeout after ${TIMEOUT}s" >&2
    echo "--- Partial log (last 50 lines) ---"
    if [[ -f "$LOG_FILE" ]]; then
        tail -50 "$LOG_FILE"
    fi
    exit 3
fi

# --- Check if log was created ---
if [[ ! -f "$LOG_FILE" ]]; then
    echo "ERROR: Log file not created — Unity may have crashed before writing output" >&2
    exit 4
fi

# --- Quick error scan ---
ERROR_COUNT=$(grep -cE '^\s*Assets/.+\.cs\([0-9]+,[0-9]+\): error CS[0-9]+' "$LOG_FILE" 2>/dev/null || true)
ERROR_COUNT=${ERROR_COUNT:-0}

WARNING_COUNT=$(grep -cE '^\s*Assets/.+\.cs\([0-9]+,[0-9]+\): warning CS[0-9]+' "$LOG_FILE" 2>/dev/null || true)
WARNING_COUNT=${WARNING_COUNT:-0}

IMPORT_ERRORS=$(grep -c 'Failed to import script' "$LOG_FILE" 2>/dev/null || true)
IMPORT_ERRORS=${IMPORT_ERRORS:-0}

ASSEMBLY_ERRORS=$(grep -c 'Assembly .* has reference to .* which is not included' "$LOG_FILE" 2>/dev/null || true)
ASSEMBLY_ERRORS=${ASSEMBLY_ERRORS:-0}

TOTAL_ERRORS=$((ERROR_COUNT + IMPORT_ERRORS + ASSEMBLY_ERRORS))

echo "---"
echo "Unity exit code: $COMPILE_EXIT"
echo "Compiler errors: $ERROR_COUNT"
echo "Import errors: $IMPORT_ERRORS"
echo "Assembly errors: $ASSEMBLY_ERRORS"
echo "Warnings: $WARNING_COUNT"
echo "Total errors: $TOTAL_ERRORS"
echo "---"

if [[ $TOTAL_ERRORS -gt 0 ]]; then
    echo "RESULT: FAIL"
    echo ""
    echo "=== Errors ==="
    grep -E '^\s*Assets/.+\.cs\([0-9]+,[0-9]+\): error CS[0-9]+' "$LOG_FILE" 2>/dev/null || true
    grep 'Failed to import script' "$LOG_FILE" 2>/dev/null || true
    grep 'Assembly .* has reference to .* which is not included' "$LOG_FILE" 2>/dev/null || true
    echo ""
    echo "=== Warnings ==="
    grep -E '^\s*Assets/.+\.cs\([0-9]+,[0-9]+\): warning CS[0-9]+' "$LOG_FILE" 2>/dev/null || true
    exit 1
elif [[ $COMPILE_EXIT -ne 0 ]]; then
    echo "RESULT: FAIL (non-zero exit code but no compiler errors found in log)"
    echo "--- Last 30 lines of log ---"
    tail -30 "$LOG_FILE"
    exit 1
else
    echo "RESULT: PASS"
    if [[ $WARNING_COUNT -gt 0 ]]; then
        echo ""
        echo "=== Warnings ==="
        grep -E '^\s*Assets/.+\.cs\([0-9]+,[0-9]+\): warning CS[0-9]+' "$LOG_FILE" 2>/dev/null || true
    fi
    exit 0
fi

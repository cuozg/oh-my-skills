#!/bin/bash

set -euo pipefail

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 \"<search term>\""
    exit 1
fi

SEARCH_TERM="$*"
SCRIPTS_ROOT="Assets/Scripts"

if [ ! -d "$SCRIPTS_ROOT" ]; then
    echo "Error: $SCRIPTS_ROOT not found from current directory: $(pwd)"
    exit 1
fi

echo "=== Feature Investigation: $SEARCH_TERM ==="
echo "Root: $(pwd)"

echo
echo "=== Existing Classes ==="
CLASS_MATCHES=$(grep -Rni --include="*.cs" -E "class[[:space:]]+.*${SEARCH_TERM}|interface[[:space:]]+.*${SEARCH_TERM}|struct[[:space:]]+.*${SEARCH_TERM}" "$SCRIPTS_ROOT" || true)
if [ -n "$CLASS_MATCHES" ]; then
    echo "$CLASS_MATCHES"
else
    echo "No class/interface/struct definitions matched by name."
fi

echo
echo "=== Test Files ==="
TEST_MATCHES=$(grep -Rni --include="*.cs" -E "${SEARCH_TERM}" Assets | grep -E "(/Tests?/|Test\.cs$|Tests\.cs$)" || true)
if [ -n "$TEST_MATCHES" ]; then
    echo "$TEST_MATCHES"
else
    echo "No related test files found."
fi

echo
echo "=== Config/Data Files ==="
CONFIG_MATCHES=$(grep -Rni --include="*.asset" --include="*.json" --include="*.yaml" --include="*.yml" --include="*.asmdef" --include="*.inputactions" -E "${SEARCH_TERM}" Assets ProjectSettings Packages 2>/dev/null || true)
if [ -n "$CONFIG_MATCHES" ]; then
    echo "$CONFIG_MATCHES"
else
    echo "No related config/data files found."
fi

echo
echo "=== Integration Points ==="
INTEGRATION_MATCHES=$(grep -Rni --include="*.cs" -E "${SEARCH_TERM}|SerializeField|UnityEvent|event[[:space:]]|OnEnable\(|Awake\(|Start\(|Update\(|ScriptableObject|Addressables|Resources\.Load|FindObjectOfType|GetComponent|SendMessage" "$SCRIPTS_ROOT" || true)
if [ -n "$INTEGRATION_MATCHES" ]; then
    echo "$INTEGRATION_MATCHES"
else
    echo "No integration points found from heuristic search."
fi

echo
echo "=== Existing vs Needs Creation (Heuristic) ==="
if [ -n "$CLASS_MATCHES" ]; then
    echo "Existing: Feature-related classes appear to exist."
    echo "Needs Creation: Focus likely on enhancements, integrations, tests, or config updates."
else
    echo "Existing: No obvious feature classes found."
    echo "Needs Creation: New feature classes and wiring likely required."
fi

if [ -z "$TEST_MATCHES" ]; then
    echo "Testing Gap: No matching tests found; plan should add or extend tests."
fi

if [ -z "$CONFIG_MATCHES" ]; then
    echo "Config/Data Gap: No matching config/data detected; verify whether new assets/config are needed."
fi

echo
echo "=== Investigation Complete ==="

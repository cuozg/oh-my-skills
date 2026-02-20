#!/bin/bash

set -u

if [ $# -lt 1 ]; then
    echo "Usage: $0 \"SearchTerm\""
    echo "Example: $0 \"Inventory\""
    exit 1
fi

TERM="$1"
ROOT="Assets/Scripts"

if [ ! -d "$ROOT" ]; then
    echo "Error: '$ROOT' not found. Run this from a Unity project root."
    exit 1
fi

print_section() {
    echo
    echo "=== $1 ==="
}

print_matches() {
    local title="$1"
    local pattern="$2"
    local limit="${3:-40}"
    local tmp

    tmp=$(mktemp)
    grep -RInE "$pattern" "$ROOT" --include="*.cs" > "$tmp" || true

    local total
    total=$(wc -l < "$tmp" | tr -d ' ')

    echo "- $title"
    if [ "$total" = "0" ]; then
        echo "  (none)"
    else
        awk -F: -v max="$limit" 'NR<=max { printf("  %s:%s\n", $1, $2) }' "$tmp"
        if [ "$total" -gt "$limit" ]; then
            echo "  ... ($((total - limit)) more)"
        fi
        echo "  Total: $total matches"
    fi

    rm -f "$tmp"
}

echo "=== Unity System Trace: $TERM ==="
echo "Search root: $ROOT"

print_section "Core classes"
print_matches "Class definitions matching term" "^[[:space:]]*(public|internal|private|protected)?[[:space:]]*(abstract[[:space:]]+|sealed[[:space:]]+|partial[[:space:]]+)*class[[:space:]]+[A-Za-z0-9_]*${TERM}[A-Za-z0-9_]*\\b"
print_matches "Interface definitions matching term" "^[[:space:]]*(public|internal)?[[:space:]]*interface[[:space:]]+[A-Za-z0-9_]*${TERM}[A-Za-z0-9_]*\\b"
print_matches "Enum definitions matching term" "^[[:space:]]*(public|internal)?[[:space:]]*enum[[:space:]]+[A-Za-z0-9_]*${TERM}[A-Za-z0-9_]*\\b"

print_section "Data structures"
print_matches "Structs and records matching term" "^[[:space:]]*(public|internal)?[[:space:]]*(readonly[[:space:]]+)?(partial[[:space:]]+)?(struct|record)[[:space:]]+[A-Za-z0-9_]*${TERM}[A-Za-z0-9_]*\\b"
print_matches "Serializable/data annotations near term" "(\\[Serializable\\]|\\[SerializeField\\]|ScriptableObject).*${TERM}|${TERM}.*(\\[Serializable\\]|\\[SerializeField\\]|ScriptableObject)"

print_section "Managers/Controllers"
print_matches "Manager classes" "^[[:space:]]*(public|internal|private|protected)?[[:space:]]*(abstract[[:space:]]+|sealed[[:space:]]+|partial[[:space:]]+)*class[[:space:]]+[A-Za-z0-9_]*(${TERM}[A-Za-z0-9_]*Manager|Manager[A-Za-z0-9_]*${TERM})\\b"
print_matches "Controller classes" "^[[:space:]]*(public|internal|private|protected)?[[:space:]]*(abstract[[:space:]]+|sealed[[:space:]]+|partial[[:space:]]+)*class[[:space:]]+[A-Za-z0-9_]*(${TERM}[A-Za-z0-9_]*Controller|Controller[A-Za-z0-9_]*${TERM})\\b"
print_matches "MonoBehaviour and ScriptableObject types with term" "class[[:space:]]+[A-Za-z0-9_]*${TERM}[A-Za-z0-9_]*[[:space:]]*:[[:space:]]*.*(MonoBehaviour|ScriptableObject)"

print_section "Utilities"
print_matches "Utility/helper/service classes" "^[[:space:]]*(public|internal|private|protected)?[[:space:]]*(static[[:space:]]+|abstract[[:space:]]+|sealed[[:space:]]+|partial[[:space:]]+)*class[[:space:]]+[A-Za-z0-9_]*(${TERM}[A-Za-z0-9_]*(Utility|Utils|Helper|Service)|(Utility|Utils|Helper|Service)[A-Za-z0-9_]*${TERM})\\b"
print_matches "General references to term" "\\b${TERM}\\b" 60

print_section "File line counts"
FILES=$(grep -RIlE "\\b${TERM}\\b" "$ROOT" --include="*.cs" || true)
if [ -z "${FILES:-}" ]; then
    echo "(none)"
else
    while IFS= read -r file; do
        [ -z "$file" ] && continue
        lines=$(wc -l < "$file" | tr -d ' ')
        echo "$file:$lines"
    done <<< "$FILES"
fi

echo
echo "=== System trace complete ==="

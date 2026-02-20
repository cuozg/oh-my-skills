#!/bin/bash

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 [SearchTerm]"
    echo "Example: $0 Inventory"
    exit 1
fi

TERM="$1"
ROOT="Assets/Scripts"

if [ ! -d "$ROOT" ]; then
    echo "Error: $ROOT not found. Run from Unity project root."
    exit 1
fi

print_section() {
    echo
    echo "=== $1 ==="
}

echo "Unity Architecture Trace: $TERM"
echo "Root: $ROOT"

print_section "Interfaces"
grep -RIn --include="*.cs" -E "interface[[:space:]]+.*${TERM}|class[[:space:]]+.*:[[:space:]]*.*I[A-Za-z0-9_]*${TERM}|class[[:space:]]+.*:[[:space:]]*.*${TERM}.*I[A-Za-z0-9_]*" "$ROOT" || true

print_section "Abstract Classes"
grep -RIn --include="*.cs" -E "abstract[[:space:]]+class[[:space:]]+.*${TERM}|class[[:space:]]+.*:[[:space:]]*.*${TERM}|class[[:space:]]+${TERM}[[:space:]]*:[[:space:]]*" "$ROOT" || true

print_section "Concrete Implementations"
grep -RIn --include="*.cs" -E "class[[:space:]]+.*${TERM}.*:[[:space:]]*|:[[:space:]]*.*${TERM}|class[[:space:]]+.*:[[:space:]]*MonoBehaviour|GetComponent<|FindObjectOfType<" "$ROOT" | grep -i "$TERM" || true

print_section "Data Models"
grep -RIn --include="*.cs" -E "\[Serializable\]|ScriptableObject|CreateAssetMenu|JsonUtility|Newtonsoft|ISerializationCallbackReceiver|\[SerializeField\].*ScriptableObject|:[[:space:]]*ScriptableObject" "$ROOT" | grep -i "$TERM" || true

print_section "Managers"
grep -RIn --include="*.cs" -E "class[[:space:]]+.*Manager|Singleton|Service|Controller" "$ROOT" | grep -i "$TERM" || true

print_section "Events"
grep -RIn --include="*.cs" -E "event[[:space:]]+|UnityEvent|\+=|-=|Invoke\(|Publish\(|Subscribe\(|MessageBus|EventBus|Signal" "$ROOT" | grep -i "$TERM" || true

echo
echo "Trace complete."

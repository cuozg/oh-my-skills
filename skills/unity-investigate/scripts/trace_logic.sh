#!/bin/bash

# Unity Investigation Discovery Script
# Traces usages, references, and asset bindings for a target class/method/system
# Usage: ./trace_logic.sh [SearchPattern] [--assets] [--deep]

if [ $# -eq 0 ]; then
    echo "Usage: $0 [SearchPattern] [--assets] [--deep]"
    echo "  SearchPattern  Class name, method name, or ClassName.MethodName"
    echo "  --assets       Include asset search (prefabs, scenes, ScriptableObjects)"
    echo "  --deep         Include animation, audio, and shader references"
    exit 1
fi

PATTERN=$1
SEARCH_ASSETS=false
SEARCH_DEEP=false

for arg in "$@"; do
    case $arg in
        --assets) SEARCH_ASSETS=true ;;
        --deep) SEARCH_DEEP=true ;;
    esac
done

echo "=== Unity Investigation: $PATTERN ==="

# 1. Direct code references
echo -e "\n--- Direct Code References ---"
grep -rn "$PATTERN" Assets/Scripts --include="*.cs" | grep -v "public class" | grep -v "public interface" | head -n 30

# 2. Class/interface definitions
echo -e "\n--- Definitions ---"
grep -rn "class $PATTERN\b\|interface $PATTERN\b\|struct $PATTERN\b\|enum $PATTERN\b" Assets/Scripts --include="*.cs"

# 3. Inheritance & implementation
echo -e "\n--- Inheritance & Implementation ---"
if [[ $PATTERN != *"("* ]]; then
    CLEAN_NAME=$(echo "$PATTERN" | cut -d. -f1)
    grep -rn ":.*\b$CLEAN_NAME\b" Assets/Scripts --include="*.cs" | head -n 20
fi

# 4. Event/delegate references
echo -e "\n--- Event/Delegate Usage ---"
grep -rn "event.*$PATTERN\|Action.*$PATTERN\|Func.*$PATTERN\|UnityEvent.*$PATTERN\|delegate.*$PATTERN" Assets/Scripts --include="*.cs" | head -n 15

# 5. Serialization markers
echo -e "\n--- Serialization & Attributes ---"
grep -rn "\[Serializable\].*$PATTERN\|\[SerializeField\].*$PATTERN\|ScriptableObject.*$PATTERN" Assets/Scripts --include="*.cs" | head -n 10

# 6. Asset bindings (prefabs, scenes, ScriptableObjects)
if [ "$SEARCH_ASSETS" = true ]; then
    echo -e "\n--- Asset Bindings (Prefabs) ---"
    grep -rl "$PATTERN" Assets --include="*.prefab" | head -n 10

    echo -e "\n--- Asset Bindings (Scenes) ---"
    grep -rl "$PATTERN" Assets --include="*.unity" | head -n 10

    echo -e "\n--- ScriptableObject Assets ---"
    grep -rl "$PATTERN" Assets --include="*.asset" | head -n 10
fi

# 7. Deep search (animation, audio, shaders)
if [ "$SEARCH_DEEP" = true ]; then
    echo -e "\n--- Animator Controllers ---"
    grep -rl "$PATTERN" Assets --include="*.controller" | head -n 10

    echo -e "\n--- Animation Clips ---"
    grep -rl "$PATTERN" Assets --include="*.anim" | head -n 10

    echo -e "\n--- Shader References ---"
    grep -rn "$PATTERN" Assets --include="*.shader" --include="*.cginc" --include="*.hlsl" | head -n 10

    echo -e "\n--- Audio Mixer References ---"
    grep -rl "$PATTERN" Assets --include="*.mixer" | head -n 5
fi

echo -e "\n=== Investigation Complete ==="

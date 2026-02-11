#!/bin/bash

# Investigate a project base for planning a feature and optionally create plan output folder.
# Usage:
#   ./investigate_feature.sh [keyword1] [keyword2] ...
#   ./investigate_feature.sh --init <plan-name>
#   ./investigate_feature.sh --init <plan-name> [keyword1] [keyword2] ...

PLAN_OUTPUT_BASE="documents/plans"

if [ "$1" = "--init" ]; then
    if [ -z "$2" ]; then
        echo "Error: --init requires a plan name"
        echo "Usage: $0 --init <plan-name> [keyword1] [keyword2] ..."
        exit 1
    fi

    PLAN_NAME="$2"
    PLAN_DIR="${PLAN_OUTPUT_BASE}/${PLAN_NAME}"
    shift 2

    mkdir -p "$PLAN_DIR"
    echo "=== Created plan output folder: $PLAN_DIR ==="
    echo "Expected outputs:"
    echo "  ${PLAN_DIR}/overview.html"
    echo "  ${PLAN_DIR}/tasks.html"
    echo "  ${PLAN_DIR}/estimates.html"
    echo "  ${PLAN_DIR}/dependencies.html"
    echo "  ${PLAN_DIR}/timeline.html"
    echo "  ${PLAN_DIR}/changes.patch"

    if [ $# -eq 0 ]; then
        exit 0
    fi

    KEYWORDS="$*"
elif [ $# -eq 0 ]; then
    echo "Usage: $0 [keyword1] [keyword2] ..."
    echo "       $0 --init <plan-name> [keyword1] [keyword2] ..."
    exit 1
else
    KEYWORDS="$*"
fi

echo "=== Investigating Keywords: $KEYWORDS ==="

for KEYWORD in $KEYWORDS; do
    echo -e "\n--- Finding scripts related to: $KEYWORD ---"
    grep -rl "$KEYWORD" Assets/Scripts --include="*.cs" | head -n 10

    echo -e "\n--- Finding prefabs related to: $KEYWORD ---"
    find Assets -name "*$KEYWORD*.prefab" | head -n 5
done

echo -e "\n=== Potentially Relevant Classes (Public API) ==="
for KEYWORD in $KEYWORDS; do
    grep -r "public class.*$KEYWORD" Assets/Scripts --include="*.cs" | sed 's/.*public //' | head -n 5
done

echo -e "\n=== Search Summary ==="
echo "Total relevant scripts found: $(grep -rl "$KEYWORDS" Assets/Scripts --include="*.cs" | wc -l)"

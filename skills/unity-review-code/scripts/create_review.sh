#!/bin/bash
set -euo pipefail

# Usage: ./create_review.sh [identifier]
# Creates the output directory and initializes review file path.
# If no identifier provided, uses "uncommitted_YYYYMMDD".
# Outputs the file path for the caller to use.

IDENTIFIER="${1:-}"

# Get project root
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || {
    echo "Error: Not in a git repository" >&2
    exit 1
}

# Create reviews directory
REVIEWS_DIR="$PROJECT_ROOT/Documents/Reviews"
mkdir -p "$REVIEWS_DIR"

# Determine output filename
if [ -z "$IDENTIFIER" ]; then
    # No identifier — use date-based name for uncommitted changes
    DATE=$(date +%Y%m%d)
    OUTPUT_FILE="$REVIEWS_DIR/uncommitted_${DATE}_review.md"
elif [[ "$IDENTIFIER" =~ ^[0-9]+$ ]]; then
    # Numeric — treat as PR/ticket number
    OUTPUT_FILE="$REVIEWS_DIR/PR_${IDENTIFIER}_review.md"
else
    # Branch or ticket name — sanitize
    SAFE_NAME=$(echo "$IDENTIFIER" | tr '/' '_' | tr ' ' '_')
    OUTPUT_FILE="$REVIEWS_DIR/${SAFE_NAME}_review.md"
fi

# Backup existing file
if [ -f "$OUTPUT_FILE" ]; then
    echo "Warning: Review file already exists. Backing up to ${OUTPUT_FILE}.bak" >&2
    cp "$OUTPUT_FILE" "${OUTPUT_FILE}.bak"
fi

# Output the path for the caller
echo "$OUTPUT_FILE"

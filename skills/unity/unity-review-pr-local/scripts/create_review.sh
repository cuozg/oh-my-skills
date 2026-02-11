#!/bin/bash

# Usage: ./create_review.sh <pr_number_or_branch_name>
# Creates the output directory and initializes an empty review file

IDENTIFIER=$1

if [ -z "$IDENTIFIER" ]; then
    echo "Usage: $0 <pr_number_or_branch_name>"
    exit 1
fi

# Get project root (where .git is)
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$PROJECT_ROOT" ]; then
    echo "Error: Not in a git repository"
    exit 1
fi

# Create reviews directory
REVIEWS_DIR="$PROJECT_ROOT/Documents/Reviews"
mkdir -p "$REVIEWS_DIR"

# Determine output filename
if [[ "$IDENTIFIER" =~ ^[0-9]+$ ]]; then
    # It's a PR number
    OUTPUT_FILE="$REVIEWS_DIR/PR_${IDENTIFIER}_review.md"
else
    # It's a branch name - sanitize it
    SAFE_NAME=$(echo "$IDENTIFIER" | tr '/' '_' | tr ' ' '_')
    OUTPUT_FILE="$REVIEWS_DIR/${SAFE_NAME}_review.md"
fi

# Check if file already exists
if [ -f "$OUTPUT_FILE" ]; then
    echo "Warning: Review file already exists: $OUTPUT_FILE"
    echo "Backing up to ${OUTPUT_FILE}.bak"
    cp "$OUTPUT_FILE" "${OUTPUT_FILE}.bak"
fi

# Output the path for the caller
echo "$OUTPUT_FILE"

#!/bin/bash

# Usage: ./post_review.sh <pr_number> <review_json_file>
PR_NUMBER=$1
JSON_FILE=$2

if [ -z "$PR_NUMBER" ] || [ -z "$JSON_FILE" ]; then
    echo "Usage: $0 <pr_number> <review_json_file>"
    exit 1
fi

# Get the repo owner/name
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)

# Post the review
gh api -X POST "/repos/$REPO/pulls/$PR_NUMBER/reviews" \
  --input "$JSON_FILE"

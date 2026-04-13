#!/usr/bin/env bash
# plan-work worktree manager
# Manages git worktree lifecycle for parallel goal execution.
#
# Usage:
#   worktree_manager.sh create <slug> [base-branch]
#   worktree_manager.sh remove <slug>
#   worktree_manager.sh list
#   worktree_manager.sh cleanup
#   worktree_manager.sh status <slug>

set -euo pipefail

# Configuration
WORKTREE_BASE="${PLAN_WORK_WORKTREE_BASE:-../.worktrees}"
BRANCH_PREFIX="${PLAN_WORK_BRANCH_PREFIX:-goal}"

# Resolve the repo root (the main worktree)
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || {
  echo "ERROR: Not inside a git repository." >&2
  exit 1
}

slugify() {
  echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//'
}

cmd_create() {
  local slug="$1"
  local base_branch="${2:-$(git symbolic-ref --short HEAD 2>/dev/null || echo main)}"
  local branch="${BRANCH_PREFIX}/${slug}"
  local worktree_dir="${WORKTREE_BASE}/${slug}"

  # Resolve worktree dir relative to repo root
  if [[ "$worktree_dir" != /* ]]; then
    worktree_dir="${REPO_ROOT}/${worktree_dir}"
  fi

  # Pre-flight checks
  if git worktree list --porcelain | grep -q "branch refs/heads/${branch}$"; then
    echo "ERROR: Branch '${branch}' is already checked out in another worktree." >&2
    exit 1
  fi

  if [ -d "$worktree_dir" ]; then
    echo "ERROR: Worktree directory already exists: ${worktree_dir}" >&2
    exit 1
  fi

  # Fetch latest
  git fetch origin 2>/dev/null

  git worktree add -b "$branch" "$worktree_dir" "origin/${base_branch}" 2>/dev/null

  echo "CREATED"
  echo "worktree_path=${worktree_dir}"
  echo "branch=${branch}"
  echo "base_branch=${base_branch}"
}

cmd_remove() {
  local slug="$1"
  local branch="${BRANCH_PREFIX}/${slug}"
  local worktree_dir="${WORKTREE_BASE}/${slug}"

  # Resolve
  if [[ "$worktree_dir" != /* ]]; then
    worktree_dir="${REPO_ROOT}/${worktree_dir}"
  fi

  if [ ! -d "$worktree_dir" ]; then
    echo "WARNING: Worktree directory does not exist: ${worktree_dir}" >&2
    # Still try to prune
    git worktree prune 2>/dev/null || true
    return 0
  fi

  # Check for uncommitted changes
  local dirty
  dirty="$(git -C "$worktree_dir" status --porcelain 2>/dev/null)" || true
  if [ -n "$dirty" ]; then
    echo "WARNING: Worktree has uncommitted changes:" >&2
    echo "$dirty" >&2
    echo "Use PLAN_WORK_FORCE_REMOVE=1 to force removal." >&2
    if [ "${PLAN_WORK_FORCE_REMOVE:-0}" != "1" ]; then
      exit 1
    fi
    git worktree remove --force "$worktree_dir"
  else
    git worktree remove "$worktree_dir"
  fi

  # Prune stale metadata
  git worktree prune 2>/dev/null

  echo "REMOVED"
  echo "worktree_path=${worktree_dir}"
  echo "branch=${branch}"
}

cmd_list() {
  echo "# plan-work worktrees (prefix: ${BRANCH_PREFIX}/)"
  git worktree list --porcelain | while IFS= read -r line; do
    case "$line" in
      "worktree "*)
        wt_path="${line#worktree }"
        ;;
      "branch refs/heads/${BRANCH_PREFIX}/"*)
        wt_branch="${line#branch refs/heads/}"
        echo "  ${wt_branch}  →  ${wt_path}"
        ;;
      "")
        wt_path=""
        wt_branch=""
        ;;
    esac
  done
}

cmd_cleanup() {
  echo "Cleaning up all plan-work worktrees..."
  local count=0

  git worktree list --porcelain | while IFS= read -r line; do
    case "$line" in
      "worktree "*)
        wt_path="${line#worktree }"
        ;;
      "branch refs/heads/${BRANCH_PREFIX}/"*)
        wt_branch="${line#branch refs/heads/}"
        if [ -n "$wt_path" ] && [ "$wt_path" != "$REPO_ROOT" ]; then
          echo "  Removing: ${wt_branch} at ${wt_path}"
          git worktree remove "$wt_path" --force 2>/dev/null || true
          count=$((count + 1))
        fi
        ;;
      "")
        wt_path=""
        ;;
    esac
  done

  git worktree prune 2>/dev/null
  echo "Cleanup complete."
}

cmd_status() {
  local slug="$1"
  local branch="${BRANCH_PREFIX}/${slug}"
  local worktree_dir="${WORKTREE_BASE}/${slug}"

  if [[ "$worktree_dir" != /* ]]; then
    worktree_dir="${REPO_ROOT}/${worktree_dir}"
  fi

  if [ ! -d "$worktree_dir" ]; then
    echo "STATUS=missing"
    echo "worktree_path=${worktree_dir}"
    return 0
  fi

  local dirty
  dirty="$(git -C "$worktree_dir" status --porcelain 2>/dev/null)" || true

  local ahead_behind
  ahead_behind="$(git -C "$worktree_dir" rev-list --left-right --count "origin/${branch}...HEAD" 2>/dev/null)" || ahead_behind="? ?"

  local commit_count
  commit_count="$(git -C "$worktree_dir" rev-list --count "origin/$(git -C "$worktree_dir" config --get branch.${branch}.merge 2>/dev/null | sed 's|refs/heads/||' 2>/dev/null || echo main)..HEAD" 2>/dev/null)" || commit_count="?"

  if [ -n "$dirty" ]; then
    echo "STATUS=dirty"
  else
    echo "STATUS=clean"
  fi
  echo "worktree_path=${worktree_dir}"
  echo "branch=${branch}"
  echo "commits=${commit_count}"
  echo "uncommitted_files=$(echo "$dirty" | grep -c '.' 2>/dev/null || echo 0)"
}

# Main dispatch
case "${1:-help}" in
  create)
    [ $# -ge 2 ] || { echo "Usage: $0 create <slug> [base-branch]" >&2; exit 1; }
    cmd_create "$2" "${3:-}"
    ;;
  remove)
    [ $# -ge 2 ] || { echo "Usage: $0 remove <slug>" >&2; exit 1; }
    cmd_remove "$2"
    ;;
  list)
    cmd_list
    ;;
  cleanup)
    cmd_cleanup
    ;;
  status)
    [ $# -ge 2 ] || { echo "Usage: $0 status <slug>" >&2; exit 1; }
    cmd_status "$2"
    ;;
  help|--help|-h)
    echo "plan-work worktree manager"
    echo ""
    echo "Usage:"
    echo "  $0 create <slug> [base-branch]  Create worktree for a goal"
    echo "  $0 remove <slug>                Remove worktree after completion"
    echo "  $0 list                          List all plan-work worktrees"
    echo "  $0 cleanup                       Remove ALL plan-work worktrees"
    echo "  $0 status <slug>                 Check worktree status"
    echo ""
    echo "Environment:"
    echo "  PLAN_WORK_WORKTREE_BASE  Base dir for worktrees (default: ../.worktrees)"
    echo "  PLAN_WORK_BRANCH_PREFIX  Branch prefix (default: goal)"
    echo "  PLAN_WORK_FORCE_REMOVE   Force remove dirty worktrees (default: 0)"
    ;;
  *)
    echo "Unknown command: $1" >&2
    echo "Run '$0 help' for usage." >&2
    exit 1
    ;;
esac

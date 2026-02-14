# Beads CLI Command Reference

Complete reference for the `bd` CLI. All commands are non-interactive and safe for AI agents unless noted.

## Project Setup

| Command | Description |
|---------|-------------|
| `bd init` | Initialize beads in current project |
| `bd init --stealth` | Stealth mode — no beads files committed to main repo |
| `bd init --contributor` | Contributor mode — separate planning repo |
| `bd hooks install` | Install git hooks for automatic JSONL sync |
| `bd setup claude` | Configure for Claude Code / opencode |
| `bd setup cursor` | Configure for Cursor |
| `bd setup aider` | Configure for Aider |
| `bd setup codex` | Configure for Codex |

## Session Context

| Command | Description |
|---------|-------------|
| `bd prime` | Output ~1-2k tokens of workflow context for session start |
| `bd ready` | List tasks with no open blockers (ready to work on) |
| `bd doctor` | Health check — orphaned issues, broken links, DB consistency |

## Creating Issues

```bash
bd create "<title>" [flags]
```

| Flag | Description | Example |
|------|-------------|---------|
| `-t, --type` | Issue type | `-t task`, `-t bug`, `-t epic` |
| `-p, --priority` | Priority (0 = highest) | `-p 0` |
| `--parent` | Parent issue ID | `--parent bd-a3f8` |
| `--description` | Description text | `--description "Details here"` |
| `--design` | Technical design notes | `--design "Use JWT with RSA256"` |
| `--acceptance` | Acceptance criteria | `--acceptance "All tests pass"` |
| `--json` | Machine-readable JSON output | `--json` |

### Examples

```bash
# P0 bug
bd create "Login fails on iOS 17" -t bug -p 0

# Task under an epic
bd create "Add rate limiting" -t task --parent bd-a3f8 -p 1

# With full details
bd create "Implement caching layer" -t task -p 1 \
  --description "Add Redis caching for API responses" \
  --design "Use read-through cache with 5min TTL" \
  --acceptance "Cache hit rate > 80% under load test"
```

## Updating Issues

> **WARNING**: NEVER use `bd edit` — it opens `$EDITOR` interactively. Always use `bd update` with flags.

```bash
bd update <id> [flags]
```

| Flag | Description |
|------|-------------|
| `--title` | Update title |
| `--description` | Update description |
| `--design` | Update technical design |
| `--notes` | Update implementation notes |
| `--acceptance` | Update acceptance criteria |
| `--status` | Set status: `open`, `in_progress`, `blocked`, `closed` |
| `--priority` | Set priority (0 = highest) |
| `--claim` | Atomically claim task (assign to self) |
| `--json` | Machine-readable JSON output |

### Examples

```bash
# Claim and start working
bd update bd-a3f8 --claim
bd update bd-a3f8 --status in_progress

# Add implementation notes
bd update bd-a3f8 --notes "Using connection pooling with max 10 connections"

# Change priority
bd update bd-a3f8 --priority 0
```

## Closing Issues

```bash
bd close <id> --reason "<reason>"
```

### Examples

```bash
bd close bd-a3f8 --reason "Implemented and tested"
bd close bd-b2c1 --reason "Duplicate of bd-a3f8"
bd close bd-c3d2 --reason "Won't fix — out of scope"
```

## Viewing Issues

| Command | Description |
|---------|-------------|
| `bd show <id>` | Full details for a single issue |
| `bd list` | List all issues |
| `bd ready` | List tasks with no open blockers |
| `bd list --status open` | Filter by status |
| `bd list --json` | Machine-readable list |

## Dependencies

| Command | Description |
|---------|-------------|
| `bd dep add <child> <parent>` | Add dependency — child depends on parent |
| `bd dep remove <child> <parent>` | Remove dependency |

### Examples

```bash
# "Add API tests" depends on "Implement API endpoints"
bd dep add bd-b2c1 bd-a3f8

# Remove dependency
bd dep remove bd-b2c1 bd-a3f8
```

## Graph Links

Link issues with semantic relationships beyond parent-child dependencies.

| Link Type | Meaning |
|-----------|---------|
| `relates_to` | General relationship between issues |
| `duplicates` | This issue duplicates another |
| `supersedes` | This issue replaces another |
| `replies_to` | This issue is a response to another |

## Sync and Git Integration

| Command | Description |
|---------|-------------|
| `bd sync` | Export DB → JSONL, commit, pull --rebase, push |
| `bd hooks install` | Install git hooks for automatic JSONL sync |

### Sync Workflow

```bash
# After making any issue changes
bd sync

# Manual equivalent (bd sync does all of this)
# 1. Export Dolt DB to JSONL files
# 2. git add JSONL files
# 3. git commit -m "beads sync"
# 4. git pull --rebase
# 5. git push
```

## Commit Message Convention

Always include the issue ID in parentheses at the end of commit messages:

```bash
git commit -m "Add JWT validation middleware (bd-a3f8)"
git commit -m "Fix rate limiting edge case (bd-b2c1)"
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `BEADS_DB` | Override database path (useful for isolated testing) |

## Issue Hierarchy (Dot Notation)

```
bd-a3f8          # Epic (top-level)
bd-a3f8.1        # Task (child of epic)
bd-a3f8.1.1      # Sub-task (child of task)
bd-a3f8.1.2      # Another sub-task
bd-a3f8.2        # Another task under the epic
```

Hash-based IDs guarantee zero conflicts across branches and contributors.

## MCP Server (Optional)

For tool-based integration instead of CLI:

```bash
# Install MCP server
uv tool install beads-mcp
# or
pip install beads-mcp
```

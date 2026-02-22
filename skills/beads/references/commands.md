# Beads CLI Command Reference

All commands are non-interactive and AI-agent safe unless noted.

## Project Setup

| Command | Description |
|---------|-------------|
| `bd init` | Initialize beads in current project |
| `bd init --stealth` | Stealth mode — no files committed to repo |
| `bd init --contributor` | Contributor mode — separate planning repo |
| `bd hooks install` | Install git hooks for auto JSONL sync |
| `bd setup claude/cursor/aider/codex` | Configure for specific AI tool |

## Session Context

| Command | Description |
|---------|-------------|
| `bd prime` | Output ~1-2k tokens of session context |
| `bd ready` | List tasks with no open blockers |
| `bd doctor` | Health check — orphans, broken links, DB consistency |

## Create Issues

```bash
bd create "<title>" [flags]
```

| Flag | Description |
|------|-------------|
| `-t, --type` | `task`, `bug`, `epic` |
| `-p, --priority` | Priority (0 = highest) |
| `--parent` | Parent issue ID |
| `--description` | Description text |
| `--design` | Technical design notes |
| `--acceptance` | Acceptance criteria |
| `--json` | Machine-readable output |

## Update Issues

> **WARNING**: NEVER use `bd edit` — it opens `$EDITOR` interactively. Always use `bd update`.

```bash
bd update <id> [flags]
```

| Flag | Description |
|------|-------------|
| `--title/--description/--design/--notes/--acceptance` | Update fields |
| `--status` | `open`, `in_progress`, `blocked`, `closed` |
| `--priority` | Set priority (0 = highest) |
| `--claim` | Atomically claim task |
| `--json` | Machine-readable output |

## Close Issues

```bash
bd close <id> --reason "<reason>"
```

## View Issues

| Command | Description |
|---------|-------------|
| `bd show <id>` | Full details for single issue |
| `bd list` | List all issues |
| `bd list --status open` | Filter by status |
| `bd ready` | Ready tasks only |

## Dependencies & Links

| Command | Description |
|---------|-------------|
| `bd dep add <child> <parent>` | Child depends on parent |
| `bd dep remove <child> <parent>` | Remove dependency |

Link types: `relates_to`, `duplicates`, `supersedes`, `replies_to`

## Sync

| Command | Description |
|---------|-------------|
| `bd sync` | Export DB → JSONL, commit, pull --rebase, push |
| `bd hooks install` | Auto-sync via git hooks |

## Issue Hierarchy

```
bd-a3f8          # Epic
bd-a3f8.1        # Task (child)
bd-a3f8.1.1      # Sub-task
```

Hash-based IDs — zero conflicts across branches.
## Environment Variables

| Variable | Purpose |
|----------|---------|
| `BEADS_DB` | Override DB path (for isolated testing) |

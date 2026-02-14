---
name: beads
description: Distributed git-backed issue tracking with the bd CLI. Use when planning work, tracking tasks, managing dependencies, coordinating multi-agent workflows, or running the "Landing the Plane" end-of-session procedure.
---

# Beads — Distributed Git-Backed Issue Tracker

Track issues, plan work, manage dependencies, and coordinate agents using the `bd` CLI. Beads stores issues in a git-backed graph database (Dolt) with JSONL sync.

## Critical Warnings

> **NEVER use `bd edit`** — Opens `$EDITOR` interactively. Use `bd update <id> --title/--body/--status/--priority/--notes/--claim` instead.

> **ALWAYS run `bd sync`** after any issue changes to persist to the graph database.

> **ALWAYS include the issue ID in commit messages**: `fix login validation (bd-a3f8)`

> **ALWAYS claim issues before starting work**: `bd update <id> --claim`

> **ALWAYS "Land the Plane"** at end of session — update all issues, sync, commit.

---

## Installation

Install via one of:

```bash
brew install steveyegge/tap/beads    # macOS
npm install -g beads                  # Node.js
go install github.com/steveyegge/beads@latest  # Go 1.24+
curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/install.sh | bash
```

### Project Setup

```bash
bd init                    # Initialize beads in current repo
bd hooks install           # Install git hooks for automatic JSONL sync
bd setup claude            # Configure for Claude/opencode (also: cursor, aider, codex)
```

**Stealth mode** (no beads files in main repo):
```bash
bd init --stealth
```

**Contributor mode** (separate planning repo):
```bash
bd init --contributor
```

### Environment

Set `BEADS_DB` to point to an isolated database for testing:
```bash
export BEADS_DB=/path/to/test.db
```

### MCP Server (optional)

```bash
uv tool install beads-mcp
```

---

## Core Workflow

Follow this sequence for every work session:

```
1. Prime    →  bd prime (load context, ~1-2k tokens)
2. Ready    →  bd ready (find unblocked tasks)
3. Claim    →  bd update <id> --claim (atomic, prevents conflicts)
4. Work     →  Implement, commit with (bd-xxxx) in message
5. Close    →  bd update <id> --status closed
6. Sync     →  bd sync (persist to graph DB)
7. Land     →  Update all touched issues, sync, final commit
```

### Step 1: Prime

Run at session start to load workflow context:

```bash
bd prime
```

Outputs ~1-2k tokens of project state, conventions, and current issues. Read the output carefully — it contains project-specific instructions.

### Step 2: Find Ready Work

```bash
bd ready                   # List tasks with no open blockers
bd ls                      # List all issues
bd ls --open               # List open issues only
bd show <id>               # Show full issue details
```

### Step 3: Claim an Issue

Claim before starting work. Claiming is atomic — prevents multiple agents from working on the same issue:

```bash
bd update <id> --claim
```

### Step 4: Work and Commit

Implement the change. Include the issue ID in every commit message:

```bash
git commit -m "add input validation to login form (bd-a3f8)"
```

The parenthesized ID format `(bd-xxxx)` is required by convention.

### Step 5: Close and Sync

```bash
bd update <id> --status closed
bd sync
```

### Step 6: Land the Plane

**Mandatory end-of-session procedure.** Before ending any session:

1. Update status and notes on every issue you touched
2. Run `bd sync` to persist all changes
3. Make a final commit with all outstanding changes
4. Verify no issues left in inconsistent state

---

## Issue Hierarchy

Beads uses dot notation for parent-child relationships:

```
bd-a3f8         Epic (top-level feature)
bd-a3f8.1       Task (child of epic)
bd-a3f8.1.1     Sub-task (child of task)
bd-a3f8.2       Another task under same epic
```

### Create Issues

```bash
# Create a top-level issue
bd create "Add user authentication" -t epic -p 1

# Create a child task
bd create "Implement login endpoint" -t task -p 2 --parent bd-a3f8

# Create a sub-task
bd create "Add input validation" -t task -p 3 --parent bd-a3f8.1

# Create a bug
bd create "Login fails with special chars" -t bug -p 1
```

**Issue types**: `epic`, `task`, `bug`

**Priority levels**: 0 (highest) to 4 (lowest)

### Update Issues

Use `bd update` with flags — **NEVER** use `bd edit`:

```bash
bd update <id> --title "New title"
bd update <id> --body "Updated description"
bd update <id> --status open|closed|in_progress
bd update <id> --priority 2
bd update <id> --notes "Added validation logic"
bd update <id> --claim
```

Combine multiple flags in one command:
```bash
bd update bd-a3f8.1 --status in_progress --claim --notes "Starting implementation"
```

### View Issues

```bash
bd show <id>               # Full details for one issue
bd ls                      # List all issues
bd ls --open               # Open issues only
bd ready                   # Unblocked tasks ready for work
```

---

## Dependencies

Manage task ordering with dependency links:

```bash
bd dep add <child> <parent>      # child depends on parent
bd dep remove <child> <parent>   # Remove dependency
```

Example:
```bash
# "Deploy" depends on "Write tests" which depends on "Implement feature"
bd dep add bd-a3f8.3 bd-a3f8.2   # deploy depends on tests
bd dep add bd-a3f8.2 bd-a3f8.1   # tests depends on implementation
```

Use `bd ready` to find tasks whose dependencies are all resolved.

---

## Graph Links

Connect related issues with typed relationships:

| Link Type | Meaning |
|-----------|---------|
| `relates_to` | General relationship |
| `duplicates` | This issue duplicates another |
| `supersedes` | This issue replaces another |
| `replies_to` | Response or follow-up |

```bash
bd link <id1> relates_to <id2>
bd link <id1> duplicates <id2>
bd link <id1> supersedes <id2>
```

---

## Multi-Agent Coordination

When multiple agents work on the same project:

### Claim Before Working

Claiming is atomic. If another agent already claimed an issue, your claim fails:

```bash
bd update <id> --claim
# If this fails → pick a different issue
```

### Communicate via Issues

Use issue notes to communicate context between agents:

```bash
bd update <id> --notes "Completed auth middleware. Login endpoint at /api/auth/login. Next agent: implement the frontend form."
```

### Handoff Pattern

1. Complete your work on the claimed issue
2. Update the issue with notes describing what was done and what remains
3. Close or update status as appropriate
4. Run `bd sync`
5. The next agent runs `bd prime` and `bd ready` to pick up where you left off

---

## Health and Diagnostics

```bash
bd doctor                  # Check beads installation and project health
bd sync                    # Sync local state to graph DB
```

Run `bd doctor` if commands behave unexpectedly.

---

## Common Mistakes

| Mistake | Consequence | Correct Approach |
|---------|-------------|-----------------|
| Use `bd edit` | Opens $EDITOR, hangs agent | Use `bd update <id> --flags` |
| Forget `bd sync` | Changes lost, DB out of date | Run `bd sync` after every change |
| Omit issue ID in commit | Lost traceability | Always `(bd-xxxx)` in commit message |
| Skip claiming | Two agents work same issue | Always `bd update <id> --claim` first |
| Skip "Land the Plane" | Issues left in bad state | Always update + sync + commit at session end |
| Create issues without type | Defaults may not match intent | Always specify `-t epic/task/bug` |

---

## Quick Decision Guide

| Situation | Command |
|-----------|---------|
| Start a session | `bd prime` |
| Find work to do | `bd ready` |
| Start working on an issue | `bd update <id> --claim --status in_progress` |
| Finish an issue | `bd update <id> --status closed && bd sync` |
| Add a note | `bd update <id> --notes "..."` |
| Create a new task | `bd create "title" -t task -p 2` |
| Create a child task | `bd create "title" -t task --parent <id>` |
| Add dependency | `bd dep add <child> <parent>` |
| Check project health | `bd doctor` |
| End of session | Update all issues → `bd sync` → commit |

---

## References

- `references/commands.md` — Complete bd CLI command reference
- `references/workflows.md` — Detailed agent session workflows and patterns

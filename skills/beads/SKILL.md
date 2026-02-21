---
name: beads
description: Distributed git-backed issue tracking with the bd CLI. Use when planning work, tracking tasks, managing dependencies, coordinating multi-agent workflows, or running the "Landing the Plane" end-of-session procedure.
---

# Beads — Distributed Git-Backed Issue Tracker

## Input

A task description, issue ID, or session context. Optionally: parent issue ID, priority, dependencies, or claim target.

## Output

Issue tracking side-effects (created/updated/closed issues, synced graph DB) and CLI output confirming each action. At session end, a "Landing the Plane" summary of all touched issues.

## Critical Warnings

> **NEVER use `bd edit`** — Opens `$EDITOR`. Use `bd update <id> --flags` instead.
> **ALWAYS `bd sync`** after changes. **ALWAYS `(bd-xxxx)`** in commits. **ALWAYS claim** before work. **ALWAYS Land the Plane** at session end.

---

## Installation

```bash
brew install steveyegge/tap/beads    # macOS
npm install -g beads                  # Node.js
go install github.com/steveyegge/beads@latest  # Go 1.24+
```

```bash
bd init                    # Initialize in current repo
bd hooks install           # Git hooks for JSONL sync
bd setup claude            # Configure for Claude/opencode (also: cursor, aider, codex)
bd init --stealth          # No beads files in main repo
bd init --contributor      # Separate planning repo
```

Optional MCP: `uv tool install beads-mcp`

---

## Core Workflow

```
1. bd prime              → Load context (~1-2k tokens)
2. bd ready              → Find unblocked tasks
3. bd update <id> --claim → Atomic claim (prevents conflicts)
4. Implement, commit with (bd-xxxx) in message
5. bd update <id> --status closed
6. bd sync               → Persist to graph DB
7. Land the Plane        → Update all issues, sync, final commit
```

### Landing the Plane (mandatory end-of-session)

1. Update status/notes on every touched issue
2. `bd sync`
3. Final commit with outstanding changes
4. Verify no issues left inconsistent

---

## Issue Management

**Hierarchy** (dot notation): `bd-a3f8` (epic) → `bd-a3f8.1` (task) → `bd-a3f8.1.1` (sub-task)

**Types**: `epic`, `task`, `bug` | **Priority**: 0 (highest) to 4 (lowest)

```bash
bd create "Title" -t task -p 2                    # Create issue
bd create "Child" -t task -p 2 --parent bd-a3f8   # Child task
bd update <id> --title|--body|--status|--priority|--notes|--claim  # Update (NEVER bd edit)
bd update <id> --status in_progress --claim --notes "Starting"     # Combine flags
bd show <id> | bd ls | bd ls --open | bd ready    # View issues
```

---

## Dependencies & Links

```bash
bd dep add <child> <parent>       # child depends on parent
bd dep remove <child> <parent>
bd link <id1> relates_to|duplicates|supersedes|replies_to <id2>
```

---

## Multi-Agent Coordination

- **Claim is atomic** — fails if already claimed; pick another
- **Communicate via notes**: `bd update <id> --notes "Context for next agent"`
- **Handoff**: complete → update notes → close/update → `bd sync` → next agent runs `bd prime`

---

## Quick Reference

| Situation | Command |
|-----------|---------|
| Start session | `bd prime` |
| Find work | `bd ready` |
| Start issue | `bd update <id> --claim --status in_progress` |
| Finish issue | `bd update <id> --status closed && bd sync` |
| Create task | `bd create "title" -t task -p 2` |
| Child task | `bd create "title" -t task --parent <id>` |
| Dependency | `bd dep add <child> <parent>` |
| Health check | `bd doctor` |
| End session | Update all → `bd sync` → commit |

| Mistake | Fix |
|---------|-----|
| `bd edit` | `bd update <id> --flags` |
| Forget sync | `bd sync` after every change |
| No ID in commit | Always `(bd-xxxx)` |
| Skip claim | `bd update <id> --claim` first |

---

## References

- `references/commands.md` — bd CLI command reference
- `references/workflows.md` — Agent session workflows

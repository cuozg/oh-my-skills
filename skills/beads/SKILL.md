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

See [references/install.md](references/install.md) for installation via package managers, repo setup, and optional MCP.

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

See [references/quick-reference.md](references/quick-reference.md) for common workflows and mistake fixes.

Key patterns:
- Always claim atomically: `bd update <id> --claim --status in_progress`
- Sync after changes: `bd sync`
- Include ID in commits: `(bd-xxxx)`
- Land the Plane at session end: Update all → sync → commit

---

## References

- `references/commands.md` — bd CLI command reference
- `references/workflows.md` — Agent session workflows
- `references/quick-reference.md` — Common workflows and mistake fixes

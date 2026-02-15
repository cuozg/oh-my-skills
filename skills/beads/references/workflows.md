# Beads Agent Workflows

## Agent Session Workflow

### 1. Session Start
```bash
bd prime       # Load context (~1-2k tokens: state, priorities, blockers)
bd ready       # See workable tasks
```

### 2. Claim & Start
```bash
bd update <id> --claim              # Atomic claim (prevents conflicts)
bd update <id> --status in_progress
```

### 3. During Work
```bash
bd update <id> --notes "progress note"              # Track progress
bd create "sub-task" --parent <id> -p 2              # Discovered work
bd dep add <current> <blocker>                       # Add blocker
bd update <current> --status blocked                 # Mark blocked
bd create "Bug: description" -t bug -p 1             # File bugs
```

### 4. Complete
```bash
bd close <id> --reason "Implemented and tested"
bd sync
```

### 5. Landing the Plane (Mandatory)

1. **File remaining issues** — anything unfinished/discovered via `bd create`
2. **Run quality gates** — lint, test, build (fix failures)
3. **Update all touched issues** — notes for in-progress, close completed, mark blocked
4. **Sync & push**: `git pull --rebase && bd sync && git push`
5. **Verify clean**: `git status` → clean tree
6. **Suggest next**: `bd ready` → recommend next task with rationale

## Multi-Agent Coordination

- **Claim before working**: `bd update <id> --claim` — atomic, only one agent wins
- **Check `bd ready`** — excludes claimed/blocked tasks
- **Sync frequently**: `bd sync` keeps all agents consistent
- **Hash-based IDs** — zero-conflict across branches

### Handoff Pattern
```bash
# Ending agent
bd update <id> --notes "Progress: X done, Y WIP. Next: Z"
bd sync

# Starting agent
bd prime → bd show <id> → bd update <id> --claim
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `bd edit` | `bd update <id> --flag "value"` |
| Forgetting `bd sync` | Always sync after changes |
| No issue ID in commits | `git commit -m "message (bd-abc)"` |
| Skipping landing the plane | Always follow end-of-session procedure |
| Not claiming before work | `bd update <id> --claim` first |
| No priority on create | Always set `-p <level>` |

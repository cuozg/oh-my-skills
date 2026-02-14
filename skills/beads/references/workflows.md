# Beads Agent Workflows

Patterns for AI agent sessions using beads for task tracking and coordination.

## Agent Session Workflow

### 1. Session Start

```bash
# Load project context and priorities
bd prime

# See what's ready to work on
bd ready
```

Review the output of `bd prime` (~1-2k tokens) to understand:
- Current project state and open issues
- Priority ordering
- Blocked vs ready tasks
- Recent activity

### 2. Task Selection and Claiming

```bash
# Pick a task from bd ready output
# Atomically claim it (prevents other agents from taking it)
bd update <id> --claim

# Set status to in_progress
bd update <id> --status in_progress
```

**Why claim atomically?** In multi-agent setups, two agents might pick the same task. `--claim` is atomic — only one agent wins.

### 3. During Work

While implementing:

- **Add notes** as you make progress:
  ```bash
  bd update <id> --notes "Implemented connection pooling, testing next"
  ```

- **Create sub-tasks** for discovered work:
  ```bash
  bd create "Handle edge case: empty input" --parent <id> -p 2
  ```

- **Add dependencies** when you discover blockers:
  ```bash
  bd dep add <current-task> <blocking-task>
  bd update <current-task> --status blocked
  ```

- **File bugs** when you find them:
  ```bash
  bd create "Bug: null pointer in auth handler" -t bug -p 1
  ```

### 4. Task Completion

```bash
# Close with reason
bd close <id> --reason "Implemented and all tests pass"

# Sync to git
bd sync
```

### 5. Landing the Plane (End-of-Session)

**This is mandatory. Never end a session without landing the plane.**

#### Step-by-step:

1. **File remaining issues** — anything unfinished or discovered:
   ```bash
   bd create "TODO: Add input validation for edge cases" -t task -p 2
   bd create "Refactor: Extract auth middleware" -t task -p 3
   ```

2. **Run quality gates** (if code changed):
   ```bash
   # Run linter, tests, build — project-specific commands
   # Fix any failures before proceeding
   ```

3. **Update all touched issues**:
   ```bash
   # Add progress notes to in-progress tasks
   bd update <id> --notes "80% complete, auth flow done, need tests"
   
   # Close completed tasks
   bd close <id> --reason "Completed"
   
   # Mark blocked tasks
   bd update <id> --status blocked
   bd update <id> --notes "Blocked on API spec from backend team"
   ```

4. **Sync and push**:
   ```bash
   git pull --rebase
   bd sync
   git push
   ```

5. **Verify clean state**:
   ```bash
   git status   # Should show clean working tree
   ```

6. **Clean up**:
   ```bash
   git stash clear
   git remote prune origin
   ```

7. **Choose follow-up** — suggest the next task for the next session:
   ```bash
   bd ready   # Show what's next
   ```
   Include a brief recommendation of what to tackle next and why.

## Multi-Agent Coordination

### Preventing Conflicts

- **Claim before working**: `bd update <id> --claim` is atomic — only one agent gets it.
- **Check `bd ready`** before picking tasks — it excludes tasks with open blockers.
- **Use `bd sync` frequently** — keeps all agents' views consistent.
- **Hash-based IDs** — zero-conflict by design, safe across branches.

### Task Distribution Pattern

```bash
# Agent A
bd ready                           # See available tasks
bd update bd-a3f8 --claim          # Claim task A
bd update bd-a3f8 --status in_progress

# Agent B (simultaneously)
bd ready                           # bd-a3f8 no longer shows (claimed)
bd update bd-b2c1 --claim          # Claim task B
bd update bd-b2c1 --status in_progress
```

### Communication via Issues

Agents coordinate through issue updates:

```bash
# Agent A discovers a blocker for Agent B's task
bd create "API endpoint returns 500 on empty body" -t bug -p 0
bd dep add bd-b2c1 bd-new-bug-id
bd update bd-b2c1 --notes "Blocked: API bug discovered, filed bd-new-bug-id"
```

### Handoff Pattern

When one agent's session ends and another picks up:

```bash
# Ending agent
bd update <id> --notes "Progress: auth middleware done, JWT validation WIP. Next: finish token refresh logic"
bd sync

# Starting agent
bd prime              # Get full context
bd show <id>          # Read handoff notes
bd update <id> --claim  # Re-claim if needed
```

## Stealth Mode

Use stealth mode when you don't want beads files in the main repository:

```bash
bd init --stealth
```

- Issue data stays in Dolt DB only
- No JSONL files committed to the repo
- Useful for open-source projects where you don't want to add beads infrastructure

## Contributor Mode

For contributing to projects you don't own:

```bash
bd init --contributor
```

- Creates a separate planning repo
- Doesn't modify the upstream project
- Your issues and plans stay in your own space

## Testing Isolation

When running tests or experimenting:

```bash
export BEADS_DB=/tmp/beads-test-db
bd init
# ... test operations ...
# Clean up: rm -rf /tmp/beads-test-db
```

The `BEADS_DB` environment variable overrides the default database path, preventing test operations from polluting your real issue database.

## Common Mistakes to Avoid

| Mistake | Correct Approach |
|---------|-----------------|
| Using `bd edit` | Use `bd update <id> --flag "value"` |
| Forgetting `bd sync` | Always sync after issue changes |
| No issue ID in commits | `git commit -m "message (bd-abc)"` |
| Skipping "landing the plane" | Always follow end-of-session procedure |
| Not claiming before working | `bd update <id> --claim` first |
| Creating issues without priority | Always set `-p <level>` |

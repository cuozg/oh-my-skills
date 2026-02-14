---
name: beads
description: "Graph-based issue tracker for agents. Track tasks as beads in a dependency graph stored in .beads/beads.jsonl. Use when: (1) Breaking work into trackable tasks with dependencies, (2) Building dependency graphs between issues, (3) Tracking task status (open/done), (4) Visualizing task relationships as a tree. Triggers: 'track issue', 'add task', 'task graph', 'dependency tree', 'issue tracker', 'beads'."
---

# Beads — Graph-Based Issue Tracker

Tasks are nodes in a graph, not rows in a table. Each **bead** has a unique hash ID, a title, an optional parent (dependency), and a status. Beads are stored in `.beads/beads.jsonl` as an append-only log.

## Setup

```bash
python3 .opencode/skills/other/beads/scripts/beads.py init
```

## Tools

### bead_init
Initialize the tracker in the current directory.
```bash
python3 .opencode/skills/other/beads/scripts/beads.py init
```

### bead_add
Add a new bead. Use `--parent` to create a dependency edge.
```bash
python3 .opencode/skills/other/beads/scripts/beads.py add "Fix login bug"
python3 .opencode/skills/other/beads/scripts/beads.py add "Write tests" --parent abc12345
python3 .opencode/skills/other/beads/scripts/beads.py add "Refactor auth" -d "Extract token logic" -p abc12345
```

### bead_list
List all open beads in a table.
```bash
python3 .opencode/skills/other/beads/scripts/beads.py list
```

### bead_done
Mark a bead as done by ID.
```bash
python3 .opencode/skills/other/beads/scripts/beads.py done abc12345
```

### bead_graph
Print a text-based dependency tree of all beads.
```bash
python3 .opencode/skills/other/beads/scripts/beads.py graph
```

## Workflow

1. `bead_init` — one-time setup
2. `bead_add` — break work into beads, link parents for dependencies
3. `bead_graph` — visualize the plan
4. Do the work, then `bead_done` to close each bead
5. `bead_list` — check remaining open beads

## Data Format

Each line in `.beads/beads.jsonl`:
```json
{"id":"a1b2c3d4","title":"Fix login","description":"","parent":null,"status":"open","created":"2025-02-15T10:00:00+00:00"}
```

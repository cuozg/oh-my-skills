# Beads Installation

## Package Managers

```bash
brew install steveyegge/tap/beads    # macOS
npm install -g beads                  # Node.js
go install github.com/steveyegge/beads@latest  # Go 1.24+
```

## Repository Setup

```bash
bd init                    # Initialize in current repo
bd hooks install           # Git hooks for JSONL sync
bd setup claude            # Configure for Claude/opencode (also: cursor, aider, codex)
bd init --stealth          # No beads files in main repo
bd init --contributor      # Separate planning repo
```

## Optional MCP

```bash
uv tool install beads-mcp
```

---
name: get-linked-context
description: Read the conversation/transcript, a recent summary, or the terminal output of another agent node (Claude, Codex or Gemini) you are linked to on the nodeterm canvas. Use when you need to know what a connected node has been doing, hand off, or continue its work. Only meaningful inside a nodeterm session with a context-link edge. Also reads sticky notes linked to this node as context.
---

# Get linked context

On the nodeterm canvas, this Claude session may be connected to other agent nodes (Claude, Codex or Gemini) by a
context-link edge. When you are linked, you can READ the other node's context on demand by
running the local CLI shim below. Nothing is pushed to you automatically — pull what you need.

Run the shim (absolute path):

```sh
sh "/Users/cuongnp/Library/Application Support/node-terminal/context-links/context.sh" <command> [--node <id|title>] [-n <N>]
```

Commands:
- `list` — list the nodes you are linked to (start here).
- `summary [--node X] [-n 15]` — the last N lines of a linked node's conversation.
- `transcript [--node X]` — the linked node's full conversation transcript.
- `terminal [--node X]` — the linked node's recent terminal output (visible buffer).

Linked sticky notes appear in `list` marked `(note)`; `summary` or `transcript` on a note
prints its **current** text (the note is read live from the canvas, so it may have changed
since it was first linked).

`--node` is optional when you are linked to exactly one node; otherwise pass the id or title
from `list`. If the CLI says "Not a nodeterm session" or "No linked nodes", there is nothing
to read — do not retry.

#!/usr/bin/env python3
"""Beads — a graph-based issue tracker for agents.

Inspired by Steve Yegge's idea that issues are nodes in a graph,
not rows in a table.  Each bead is a JSON object stored in a
.beads/beads.jsonl append-only log.  Beads can reference a parent
to form dependency trees.
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from collections import defaultdict


BEADS_DIR = ".beads"
BEADS_FILE = os.path.join(BEADS_DIR, "beads.jsonl")


# ── helpers ──────────────────────────────────────────────────────


def _make_id(title: str, ts: str) -> str:
    """Deterministic short hash from title + timestamp."""
    return hashlib.sha256(f"{title}:{ts}".encode()).hexdigest()[:8]


def _load_beads() -> list[dict]:
    """Read every line of beads.jsonl and return a list of dicts."""
    if not os.path.exists(BEADS_FILE):
        print(
            f"Error: {BEADS_FILE} not found. Run 'beads init' first.", file=sys.stderr
        )
        sys.exit(1)
    beads = []
    with open(BEADS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                beads.append(json.loads(line))
    return beads


def _save_bead(bead: dict) -> None:
    """Append a single bead to the JSONL file."""
    with open(BEADS_FILE, "a") as f:
        f.write(json.dumps(bead, separators=(",", ":")) + "\n")


# ── commands ─────────────────────────────────────────────────────


def cmd_init(_args: argparse.Namespace) -> None:
    """Create .beads/ directory and beads.jsonl if they don't exist."""
    os.makedirs(BEADS_DIR, exist_ok=True)
    if not os.path.exists(BEADS_FILE):
        open(BEADS_FILE, "w").close()
        print(f"Initialized empty bead tracker in {BEADS_DIR}/")
    else:
        print(f"Bead tracker already initialized in {BEADS_DIR}/")


def cmd_add(args: argparse.Namespace) -> None:
    """Add a new bead (task/issue)."""
    ts = datetime.now(timezone.utc).isoformat()
    bead_id = _make_id(args.title, ts)

    bead = {
        "id": bead_id,
        "title": args.title,
        "description": args.description or "",
        "parent": args.parent or None,
        "status": "open",
        "created": ts,
    }

    # Validate parent exists if specified
    if bead["parent"]:
        existing = _load_beads()
        ids = {b["id"] for b in existing}
        if bead["parent"] not in ids:
            print(f"Error: parent '{bead['parent']}' not found.", file=sys.stderr)
            sys.exit(1)

    _save_bead(bead)
    print(f"Added bead {bead_id}: {args.title}")


def cmd_list(_args: argparse.Namespace) -> None:
    """List open beads."""
    beads = _load_beads()
    open_beads = [b for b in beads if b["status"] == "open"]

    if not open_beads:
        print("No open beads.")
        return

    # Column widths
    id_w = max(len(b["id"]) for b in open_beads)
    title_w = max(len(b["title"]) for b in open_beads)

    print(f"{'ID':<{id_w}}  {'Title':<{title_w}}  Parent   Created")
    print(f"{'-' * id_w}  {'-' * title_w}  -------  -------------------")
    for b in open_beads:
        parent = b.get("parent") or "-"
        created = b["created"][:19]
        print(f"{b['id']:<{id_w}}  {b['title']:<{title_w}}  {parent:<7}  {created}")


def cmd_done(args: argparse.Namespace) -> None:
    """Mark a bead as done."""
    beads = _load_beads()
    found = False
    for b in beads:
        if b["id"] == args.bead_id:
            b["status"] = "done"
            found = True
            break

    if not found:
        print(f"Error: bead '{args.bead_id}' not found.", file=sys.stderr)
        sys.exit(1)

    # Rewrite entire file
    with open(BEADS_FILE, "w") as f:
        for b in beads:
            f.write(json.dumps(b, separators=(",", ":")) + "\n")

    print(f"Marked {args.bead_id} as done.")


def cmd_graph(_args: argparse.Namespace) -> None:
    """Print a text-based dependency graph of all beads."""
    beads = _load_beads()
    if not beads:
        print("No beads to graph.")
        return

    by_id = {b["id"]: b for b in beads}
    children = defaultdict(list)
    roots = []

    for b in beads:
        parent = b.get("parent")
        if parent and parent in by_id:
            children[parent].append(b["id"])
        else:
            roots.append(b["id"])

    def _status_icon(status: str) -> str:
        return "[x]" if status == "done" else "[ ]"

    def _print_tree(node_id: str, prefix: str = "", is_last: bool = True) -> None:
        node = by_id[node_id]
        connector = "`-- " if is_last else "|-- "
        icon = _status_icon(node["status"])
        print(f"{prefix}{connector}{icon} {node['id']} {node['title']}")
        child_ids = children.get(node_id, [])
        for i, cid in enumerate(child_ids):
            extension = "    " if is_last else "|   "
            _print_tree(cid, prefix + extension, i == len(child_ids) - 1)

    for i, root_id in enumerate(roots):
        _print_tree(root_id, "", i == len(roots) - 1)


# ── CLI ──────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="beads",
        description="Graph-based issue tracker for agents.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # init
    sub.add_parser("init", help="Initialize .beads/ directory")

    # add
    p_add = sub.add_parser("add", help="Add a new bead")
    p_add.add_argument("title", help="Bead title")
    p_add.add_argument("--description", "-d", default="", help="Optional description")
    p_add.add_argument("--parent", "-p", default=None, help="Parent bead ID")

    # list
    sub.add_parser("list", help="List open beads")

    # done
    p_done = sub.add_parser("done", help="Mark a bead as done")
    p_done.add_argument("bead_id", help="ID of the bead to close")

    # graph
    sub.add_parser("graph", help="Print dependency graph")

    args = parser.parse_args()
    commands = {
        "init": cmd_init,
        "add": cmd_add,
        "list": cmd_list,
        "done": cmd_done,
        "graph": cmd_graph,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()

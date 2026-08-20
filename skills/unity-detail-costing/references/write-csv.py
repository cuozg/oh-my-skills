#!/usr/bin/env python3
"""Writer skeleton for a 13-column SGS Detailed Costing CSV.

Copy this to /tmp, fill in the rows, run it. Do NOT hand-edit the CSV: multi-line
cells and CRLF-inside-quotes are what break, every time.

Two modes:
  * NEW SHEET      -> leave SRC = None, HEADER below is used.
  * UPDATE IN PLACE -> set SRC to the target CSV. The header and every row outside
    your block are harvested from it and preserved byte-for-byte.

UPDATE IN PLACE IS NOT IDEMPOTENT. It reads the file it is about to overwrite, so
re-running it against its own output duplicates rows. Always:

    cp "<target>.csv" /tmp/costing.backup.csv     # before the first run
    cp /tmp/costing.backup.csv "<target>.csv"     # before EVERY re-run
"""

import csv

SRC = None                      # None = new sheet; else path to the CSV to update in place
DST = "/tmp/costing.csv"        # for UPDATE IN PLACE, set DST = SRC
BLOCK_AFTER = None              # UPDATE IN PLACE: value of column 0 that starts the tail to preserve

N = 13
HEADER = ["Epic", "Status", "Component", "Task", "Sub Task", "Jira\n(Client)", "Jira\n(Server)",
          "Client", "Server", "Note", "Assignee\n(SGS)", "Assignee\n(BLR)", "In/Out"]


def load(path):
    """Read a CSV without newline translation so multi-line cells keep their \r\n."""
    with open(path, "r", encoding="utf-8", newline="") as f:
        return [list(r) for r in csv.reader(f)]


def row(epic="", component="", task="", sub="", client="", server="", note="", inout=""):
    """Build one 13-column row. Columns 1, 5, 6, 10, 11 stay blank by design."""
    r = [""] * N
    r[0], r[2], r[3], r[4] = epic, component, task, sub
    r[7], r[8], r[9], r[12] = client, server, note, inout
    return r


def b(*lines):
    """Join Sub Task / Task bullets into one multi-line cell."""
    return "\n".join(lines)


def num(cell):
    """Parse a cost cell for summing. Blank, TBD and label text count as 0."""
    try:
        return float(cell)
    except ValueError:
        return 0.0


# --- rows -------------------------------------------------------------------
header = HEADER
tail = []
if SRC:
    orig = load(SRC)
    header = orig[0]
    start = next(i for i, r in enumerate(orig) if r[0] == BLOCK_AFTER)
    tail = orig[start:]                       # preserved verbatim

block = [
    row(epic="[FEATURE]", component="General",
        task=b("- Design Blueprint", "- Create the milestone build"),
        client="[N]", server="[N]", note="[Design range X-Y.]"),
    # ... one row per deliverable; see references/output-template.csv
]

out = [header] + block + tail

# --- checks before writing --------------------------------------------------
bad = [(i, len(r)) for i, r in enumerate(out) if len(r) != N]
assert not bad, f"wrong column count: {bad}"

client_sum = sum(num(r[7]) for r in out[1:])
server_sum = sum(num(r[8]) for r in out[1:])
print(f"computed client sum: {client_sum}  server sum: {server_sum}")
print("-> these MUST equal the Total Assign row; fix the row, not the total")

# --- write ------------------------------------------------------------------
with open(DST, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\r\n", quoting=csv.QUOTE_MINIMAL)
    for r in out:
        # normalise first: harvested cells already carry \r\n, new cells carry \n.
        # a bare .replace("\n", "\r\n") turns harvested cells into \r\r\n.
        w.writerow([c.replace("\r\n", "\n").replace("\n", "\r\n") for c in r])

d = open(DST, "rb").read()
crlf, lf, crcr = d.count(b"\r\n"), d.count(b"\n"), d.count(b"\r\r")
print(f"rows: {len(out)}  bytes: {len(d)}  CRLF: {crlf}  bare LF: {lf - crlf}  CR-CR: {crcr}")
assert lf == crlf, "bare LF found"
assert crcr == 0, "doubled CR found - normalise step was skipped"

# --- verify the preserved tail (UPDATE IN PLACE only) -----------------------
# Read BOTH files with newline="" or the comparison is meaningless: a universal-newline
# read collapses \r\n to \n and every multi-line cell reports a false mismatch.
if SRC:
    a, o = load(DST), load("/tmp/costing.backup.csv")
    print("header identical:", a[0] == o[0])
    keep = lambda rows: [r for r in rows if not r[0].startswith(("Total Assign", "Available Capacity"))]
    ai = next(i for i, r in enumerate(a) if r[0] == BLOCK_AFTER)
    oi = next(i for i, r in enumerate(o) if r[0] == BLOCK_AFTER)
    print("tail preserved verbatim:", keep(a[ai:]) == keep(o[oi:]))

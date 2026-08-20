---
name: unity-detail-costing
description: >
  Create a detailed engineering costing sheet as CSV (SGS "Detailed Costing" format) for a Unity feature/refactor —
  per-workstream dev-day breakdown, Client/Server columns, Total Assign vs Available Capacity. Use when the deliverable
  is a costing spreadsheet row set rather than an HTML report, when updating an existing detailed-costing CSV in place,
  or when the user names a `... Detailed Costing ....csv`. For an HTML costing report use `unity-costing` instead.
metadata:
  author: kuozg
  version: "1.1"
---
# unity-detail-costing

Produce a **CSV** detailed-costing sheet for a Unity feature/refactor. Answer "what will this cost?" — not "please implement this."

**Pre-requisite:** Read `references/output-template.csv` (the 13-column contract) and `references/write-csv.py` (the writer skeleton). If the user names an existing CSV, that file's own header wins over the template.

**Unit:** dev-days, 1 engineer, code-complete + unit tests. **Not** calendar days. State this in the sheet.

## Column contract — 13 columns, never more

| # | Column | Holds |
|---|---|---|
| 0 | `Epic` | Feature name; set once on the block's first row, blank after. Also the label column for `Total Assign` / `Available Capacity`. |
| 1 | `Status` | Left blank unless the source sheet uses it. |
| 2 | `Component` | Short title for the workstream / system grouping. Set once, blank on continuation rows. |
| 3 | `Task` | One short line describing the target deliverable. No bullets or implementation detail. Blank on continuation rows of the same task. |
| 4 | `Sub Task` | Short multi-line list of requirements and acceptance criteria. State observable targets, not how to implement them. |
| 5-6 | `Jira (Client)` / `Jira (Server)` | Left blank — tickets are created later, not by this skill. |
| 7 | `Client` | Client **and battle-logic** dev-days. |
| 8 | `Server` | Server **and Brick/config** dev-days. |
| 9 | `Note` | Short `- ` list of implementation steps, followed by compact metadata when needed: design-doc reference (`WS-02 §4`), estimate **range**, assumptions, risks, bugs, or blockers. |
| 10-11 | `Assignee (SGS)` / `Assignee (BLR)` | Left blank. |
| 12 | `In/Out` | `Out` for optional and excluded rows; blank for in-scope rows. |

**Do not add columns.** If two numbers must coexist (e.g. old vs new estimate), keep one in the cell and put the other in `Note`.

## Workflow

### 1. Clarify Requirements
Do not assume. Ask the user if unclear: target platform, boundaries, quality bar, estimate unit, and — when a costing already exists — **whose numbers win** (existing sheet vs fresh design-derived) and **where output goes** (update in place vs new file). These two are the usual ambiguity; resolve them before writing anything.

### 2. Investigate Context
Spawn `explore` / `librarian` subagents (never a worktree) to gather evidence on:
- Entry points, public APIs, module boundaries.
- Cross-system dependencies (calls, shared state, events), and **cross-repo** ones — a sibling repo that is not a submodule is a release-ordering dependency.
- Existing patterns, test coverage, performance-critical paths.
- Pre-existing bugs sitting under the new scope — each becomes a `Note` and possibly a blocker.

Read every design doc in scope. Record `file:line` evidence. Collect all results before scoping.

### 3. Analyze Scope & Sizing
- Estimate per workstream as a **range** (low-high dev-days), split Client vs Server.
- **Confidence:** High (knowns), Med (some unknowns), Low (ambiguous territory).
- **BLOCKING:** If scope is ambiguous or confidence is Low, print a "🔍 SCOPE DETECTION" summary and stop for user confirmation.

### 4. Rows, not tasks
One row per deliverable, 0.5-day granularity. Split a row when the work crosses Client/Server or client/battle-logic. Group rows under a short `Component` title and order components by the dependency graph, not alphabetically.

- Keep `Task` to one short line naming the target.
- Keep `Sub Task` to a short list of requirements and acceptance criteria. Each bullet describes what must be true when done; never put implementation steps here.
- Keep `Note` to a short list of implementation steps. Append estimate, assumption, risk, and blocker metadata compactly after the steps.

### 5. Ranges → cells
A cell holds **one number**. Use the **midpoint rounded to 0.5**; put the range and its rationale in `Note` (`Design range 4-6.`). Preserve the full range with three summary rows:

```
Total Assign               <midpoint sum>   Note: how the number was derived
Total Assign (design low)  <low sum>
Total Assign (design high) <high sum>
```

### 6. Out-of-scope blocks
Two trailing `Component` blocks, both marked `Out` in `In/Out`:
- `Optional (decision-dependent)` — one row per option. Cost goes in `Note` as `ADD +3-5. Decision: <who decides what>`, **never** in the `Client`/`Server` column, so a naive column SUM stays correct.
- `Excluded from these numbers` — use a one-line `Task` target and short `Sub Task` acceptance bullets identifying what is not costed (other repos, art/UX, QA, loc, release management, unowned scope). Put the verification steps and confidence statement in `Note`.

### 7. Review Costing & Risks
- Risks live in `Note` on the row they threaten, not in a separate section.
- **Risk Levels:** `Low` (Accept), `Medium` (Monitor), `High` (Mitigate), `Critical` (Block/Spike).
- Compare `Total Assign` against `Available Capacity`. If demand exceeds capacity, say so **in the capacity row's `Note`** with the exact overrun and where the cuts are. Never silently trim scope to fit.
- Drop rows that double-count, and say so in `Note` (`Superseded by <row> — was double-counted.`).

### 8. Generate the CSV
Write with Python's `csv` module using the `references/write-csv.py` skeleton. Non-negotiable mechanics:

- `open(path, "w", encoding="utf-8", newline="")` + `csv.writer(f, lineterminator="\r\n", quoting=csv.QUOTE_MINIMAL)`.
- **Normalise before writing**, or multi-line cells double up:
  `c.replace("\r\n", "\n").replace("\n", "\r\n")`.
  Cells harvested from an existing file already carry `\r\n`; a bare `.replace("\n", "\r\n")` turns them into `\r\r\n`.
- **Updating in place:** `cp` the target to a backup **first**. A generator that harvests the header/tail from the target is not idempotent — re-running it against its own output duplicates rows. Restore the backup before every re-run.
- Preserve every row outside your block byte-for-byte, including other epics, capacity and release-plan rows.

### 9. Verify — all must pass
```
column count == 13 on every row
CRLF > 0, bare LF == 0, "\r\r" == 0
computed Client/Server column sums == the Total Assign row
preserved rows identical to the backup
header identical to the backup
```
Read **both** files with the same newline mode when diffing (`open(..., newline="")` on each). Mixing universal-newline and raw reads reports a false mismatch on every multi-line cell.

### 10. Report
Output location, `Total Assign` vs `Available Capacity` table, confidence level, top 2-3 risks, critical path.
**BLOCKING:** Then print "❓ Next steps? 1. Create tasks 2. Adjust scope" and wait. **Do not execute or auto-create tasks.**

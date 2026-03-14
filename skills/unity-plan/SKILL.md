---
name: unity-plan
description: >
  Plan any Unity feature with scope confirmation workflow. Auto-detects scope (XS/S/M/L)
  with confidence + reasoning, then blocks for user confirmation before planning.
  Quick (XS/S: 0-8h, inline report) or Deep (M/L: 1-10 days, markdown plan).
  Use when the user says "plan this," "how long will this take," "estimate this task,"
  "I need a feature plan," "break this down," or describes any feature needing scoping
  before implementation.
metadata:
  author: kuozg
  version: "2.0"
---

# unity-plan

Plan any Unity feature — auto-detect scope, confirm with user, then generate the right plan.

## Workflow

Every planning session follows 5 steps. Steps 2 and 4 are BLOCKING — do not proceed without user input.

### Step 1: Scope Detection

Analyze the request and investigate briefly (max 3 tool calls) to determine size.
Read `scope-detection-guide.md` for signal analysis. Present scope with reasoning, confidence, hours, and risk using the template from `scope-confirmation.md`.

### Step 2: Confirm Scope ⛔ BLOCK

**STOP. Wait for user to confirm or adjust scope.**
Read `confirmation-flow.md` for response handling. If user adjusts, re-present updated scope. Do NOT proceed until user explicitly confirms.

### Step 3: Generate Plan

| Scope | Mode | Output |
|-------|------|--------|
| XS/S | Quick | Inline report (no file) |
| M/L | Deep | `Documents/Plans/PLAN_{Name}.md` |

**Quick Mode:** Report inline using format from `output-quick.md`.

**Deep Mode:**
1. Scan entry points, relevant modules, define in/out of scope
2. Trace dependencies, flag integration risks
3. Break into ordered tasks with sizes and skills
4. Write plan using `output-deep.md` template

### Step 4: Plan Review ⛔ BLOCK

**STOP. Wait for user to approve, adjust, or discard.**
Present follow-up options from `confirmation-flow.md`. Do NOT create tasks until user approves.

### Step 5: Create Tasks

After user approves, call `task_create` per task with `blockedBy` for max parallelism. Print task IDs. Validate all blockers reference real task IDs.

## Triage

| Signal | Mode |
|--------|------|
| Single-file change, isolated fix, "quick plan," "how long" | **Quick** (XS/S) |
| Feature spans 2+ systems/files, "plan this feature," "break this down" | **Deep** (M/L) |

When scope is unclear, investigate briefly (max 3 tool calls) then present for confirmation.

## Shared Rules

- Investigate actual codebase before planning — no guesswork
- All estimates must be evidence-based; cite file paths for every claim
- Use imperative mood for task subjects (e.g., "Add health component")
- NEVER create tasks before user confirms the plan
- NEVER proceed past a BLOCKING step without user input

## Standards

Load `unity-standards` for planning methodology. Key references in `plan/`:
`sizing-guide.md`, `scope-detection-guide.md`, `scope-confirmation.md`, `confirmation-flow.md`,
`risk-assessment.md`, `dependency-mapping.md`, `task-structure.md`, `output-quick.md`, `output-deep.md`.

Load via `read_skill_file("unity-standards", "references/plan/<file>")`.

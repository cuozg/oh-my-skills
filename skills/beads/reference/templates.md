# Beads Workflow Templates

---

## 1. Discovery Report

```markdown
# Discovery: [Feature Name]
**Date**: [YYYY-MM-DD] | **Epic**: [bd-N or TBD]

## Request
[Original user request]

## Files: `path/file.cs` — [purpose] (list all)

## Risk Assessment
| Factor | Level | Notes |
|--------|-------|-------|
| Complexity | LOW/MED/HIGH | |
| File Count | LOW/MED/HIGH | |
| Novelty | LOW/MED/HIGH | |
| Cross-Assembly | LOW/MED/HIGH | |

**Overall**: [LOW/MED/HIGH]
- HIGH → spike bead (30min time-box)
- LOW/MED → proceed with task beads
```

---

## 2. Spike Bead

30-minute time-boxed validation for HIGH-risk features.

```markdown
# Spike: [Name]
**Epic**: [bd-N] | **Bead**: [bd-M] | **Time-Box**: 30min

## Questions
1. [Unknown to validate]

## Proceed If: [success criteria]
## Abort If: [blocker criteria]

## Findings
[Filled during execution]

**Recommendation**: PROCEED / ABORT / MODIFY
**Output**: `.spikes/[feature]/[spike-id]/FINDINGS.md`
```

---

## 3. Epic Bead

```markdown
# Epic: [Feature Name]
**Bead**: [bd-N] | **Priority**: [0-4] | **Status**: OPEN/CLOSED

## Description: [High-level feature description]

## Acceptance Criteria
- [ ] [Requirement]

## Child Beads
- [bd-X] - [Task name] - Status - Track [N]

## Execution Plan (from `bv --robot-plan`)
Track 1: [bd-X] → [bd-Y]
Track 2: [bd-Z]
```

---

## 4. Task Bead

Atomic unit of work (1 file, 1 test, 1 component).

```markdown
# Task: [Name]
**Bead**: [bd-N] | **Epic**: [bd-M] | **Priority**: [1-4] | **Worker**: [Agent]

## Files to Modify/Create
- `path/file.cs` — [change description]

## Acceptance Criteria
- [ ] [Testable criterion]
- [ ] No compiler errors, tests pass

## Dependencies
- Depends On: [bd-X] | Blocks: [bd-Y]

## Execution
1. Reserve files → 2. Implement → 3. Test → 4. Self-message context
5. Message orchestrator `[bd-N] COMPLETE` → 6. `bd close` → 7. Release files
```

---

## 5. Worker Prompt

```markdown
You are **Worker [N]** for epic [bd-M]: [Feature Name].

**Track**: [bd-X] → [bd-Y] → [bd-Z] (execute in sequence)
**Epic Thread**: `[bd-M]` | **Worker Thread**: `track:Worker[N]:[bd-M]`

**Per Bead**: Reserve files → Implement → Test → Self-message context → Report COMPLETE → Close → Release files → Check inbox → Next bead

**If Blocked**: Message orchestrator `[bd-X] BLOCKED: [reason]`, wait for resolution.

**Rules**: Always self-message context. Always check epic thread before each bead. Never modify unreserved files. Never close before sending completion.
```

---

## 6. Message Subject Conventions

```
[bd-N] COMPLETE           — bead finished
[bd-N] BLOCKED: reason    — cannot proceed
[bd-N] Context for Next   — self-message (worker thread)
[Track N] COMPLETE        — all track beads done
[Interface Change] name   — breaking API change
[Spike bd-N] FINDINGS     — spike results
[HOTFIX] bd-N             — unblocking bead
```

---

## 7. Integration Checklist (before closing epic)

- [ ] All child beads closed
- [ ] All file reservations released
- [ ] No compiler errors/warnings
- [ ] All tests pass (Edit + Play Mode)
- [ ] No merge conflicts, branch up-to-date
- [ ] Documentation updated
- [ ] Feature matches acceptance criteria
- [ ] `bd close [bd-M]`

---

## Quick Reference

```bash
bd add "Spike: [name]" --epic [bd-M] --priority 0   # Spike
bd add "[task]" --epic [bd-M] --priority [1-4]       # Task
```

**Threads**: Epic `[bd-M]` | Worker `track:[Agent]:[bd-M]`

**File Reservation**: `file_reservation_paths(paths: [...], exclusive: true, ttl_seconds: 7200)`
**Release**: `release_file_reservations(paths: [...])`

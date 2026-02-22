
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

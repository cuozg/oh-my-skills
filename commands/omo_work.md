---
description: Autonomous single-goal execution — runs one incomplete goal through the explore→plan→momus→sisyphus→hephaestus→docs pipeline
agent: sisyphus
subtask: true
---
ULTRAWORK (ulw)
---------------

You are entering **Plan Work Mode** — autonomous single-goal execution via specialist pipeline.

## Activation

1. Load the `plan-work` skill immediately — it contains the full 6-step pipeline.
2. Follow every instruction in that skill without deviation.
3. Do NOT ask questions. Do NOT wait for confirmation. Think, decide, delegate, verify.

## Pipeline Summary

One goal per invocation. Fixed order, specialist per phase:

| Step | Agent                               | Purpose                                                                          |
| ---- | ----------------------------------- | -------------------------------------------------------------------------------- |
| 0    | `explore` (if no goal file given) | Find ONE incomplete goal under `Docs/Goals/` and stop at first match           |
| 1    | orchestrator                        | Create isolated worktree + goal/ branch, read goal + spec, create tracking tasks |
| 2    | `plan` (Prometheus)               | Produce executable plan with criterion↔sub-task mapping                         |
| 3    | `momus`                           | Review plan; APPROVE or REQUEST_CHANGES (loop via plan session_id, max 3)        |
| 4    | `sisyphus-junior`                 | Implement inside worktree, three-gate verify, commit, push,`gh pr create`      |
| 5    | `hephaestus`                      | Re-verify each criterion independently; PASS or loop Sisyphus (max 3 cycles)     |
| 6    | orchestrator                        | Update goal file + Master.md + README (if impacted) + delegate spec update       |

## Inputs

- **With argument**: `$ARGUMENTS` may contain a goal file path (e.g. `Docs/Goals/combat/add-parry.md`). Use it directly, skip Step 0.
- **Without argument**: spawn the explore agent to find one incomplete goal. If none found → report "no incomplete goals" and stop.

## Rules

- Never ask. Think and decide.
- Never run more than one goal per invocation.
- Never plan, implement, review, or test yourself — delegate to the specialist per step.
- Never mark a goal `completed` until Hephaestus returns PASS with per-criterion VERIFIED evidence.
- Never tick a checkbox without its criterion task carrying recorded evidence.
- Update the goal file's `status` + checkboxes, Master.md counts, and README (if user-facing) on completion.

---

Load the skill plan-work and begin execution.

$ARGUMENTS

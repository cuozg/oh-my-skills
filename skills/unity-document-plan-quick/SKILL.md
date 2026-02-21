---
name: unity-document-plan-quick
description: "Quick costing and impact assessment for Unity features/tasks. Investigates the codebase deeply but responds with a compact, structured summary: task size, time estimate, risks, and downstream impact. Use when: (1) Estimating effort for a new feature or change, (2) Quick feasibility check before committing to work, (3) Understanding risk and blast radius of a proposed change, (4) Getting a high-level cost before detailed planning. Triggers: 'how big is this', 'estimate this', 'quick cost', 'how long will this take', 'is this a big change', 'feasibility check', 'impact assessment', 'effort estimate', 'scope check', 'size this task'."
---
# Quick Task Assessment

**Input**: Feature request, task description, or proposed change

## Role

Senior Unity engineer doing a quick feasibility assessment. Investigate thoroughly, respond concisely. No task lists. No implementation plans. Just the assessment.

## Workflow

1. **Parse** — What is being asked? What systems are involved?
2. **Investigate** — Search the codebase to understand scope. Use `grep`, `read`, `glob`, `lsp_symbols`, `lsp_find_references`, `impact-analyzer` as needed. Be thorough — read the actual code, trace dependencies, check what gets touched.
3. **Assess** — Evaluate size, time, risk, and downstream impact.
4. **Respond** — Use the output template exactly. Nothing else.

### Investigation Checklist

- How many files need changes? New files needed?
- How much new logic vs. wiring existing systems?
- Existing patterns to follow or greenfield?
- What other systems touch the affected code?
- Tricky edge cases, threading, lifecycle issues?

## Output Template

```
## Assessment: {Feature/Task Name}

### Size: {Small | Medium | Large}
{1 summary line}
- {1-3 lines explaining why this size}

### Time Estimate: {X-Y hours}
{1 summary line}
- {1-3 lines explaining the estimate breakdown}

### Risk: {Low | Medium | High}
{1 summary line}
- {1-5 lines explaining specific risks or difficulties}

### Impact
- **{Feature/System A}**: {short impact description}
- **{Feature/System B}**: {short impact description}
- _{None — isolated change}_ (if no downstream impact)
```

### Size Reference

| Size | Signals |
|:-----|:--------|
| Small | 1-3 files, follows existing pattern, no new systems |
| Medium | 4-10 files, some new logic, touches 2-3 systems |
| Large | 10+ files, new architecture, cross-cutting concerns |

### Time Reference

| Range | Typical Work |
|:------|:-------------|
| 1-4h | Small bug fix, config change, add field |
| 4-16h | New component, UI screen, system extension |
| 16-40h | New system, major refactor, cross-cutting feature |
| 40h+ | Architecture change, new subsystem with tests |

## Rules

- **Investigate deep, respond short.** Read as much code as needed. Output stays compact.
- **No task lists.** Assessment only — not planning.
- **No implementation details.** Don't describe HOW to build it.
- **Be honest about unknowns.** If you can't assess something, say so.
- **Anchor estimates in evidence.** Reference actual file counts, system complexity you found.

## Example

**Input**: "Add daily login reward system"

**Result**:

```
## Assessment: Daily Login Reward System

### Size: Medium
New system with data persistence and UI, but follows existing reward patterns.
- 6-8 files: model, manager, UI screen, save data, config SO, tests
- Existing RewardManager and popup patterns can be extended
- Needs new persistent timestamp tracking

### Time Estimate: 12-20 hours
Core logic is straightforward; UI and edge cases add time.
- Core logic + data model: 3-5h
- UI screen + animations: 4-6h
- Save/load + timezone edge cases: 3-5h
- Testing + polish: 2-4h

### Risk: Medium
Timezone and calendar-day boundaries are the main difficulty.
- Server vs local time discrepancy can allow exploits
- Day-rollover logic across timezones is error-prone
- Offline/clock-manipulation detection needed
- Save data migration if reward structure changes later

### Impact
- **SaveManager**: New daily-login data block in save file
- **RewardManager**: New reward source type to integrate
- **MainMenuUI**: New button/indicator for daily reward status
- **Analytics**: New events for login streak tracking
```

## Boundaries

- **OWNS**: Investigation, assessment, size/time/risk/impact evaluation
- **Does NOT**: Create tasks, write code, generate plans, modify files

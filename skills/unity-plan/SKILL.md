---
name: unity-plan
description: "High-level planning with GitHub PR-style output for Unity features. Use when: (1) Analyzing requirements and specs, (2) Investigating existing codebase/systems, (3) Breaking work into Tasks with code change previews, (4) Generating visual diff plans showing exact proposed changes. Outputs an HTML file resembling GitHub PR split view."
---

# Unity Planning Skill

Create implementation plans for Unity features with GitHub PR-style code diff previews.

**IMPORTANT**: This skill is for **planning only**. Do NOT implement or execute any work.

## Output

**Template**: `.claude/skills/unity-plan/assets/templates/PLAN_OUTPUT.html`

**Save to**: `Documents/Plans/[FeatureName]_PLAN.html`

Read the template file for all HTML structure, CSS classes, and placeholder details.

## Workflow

### 1. Analyze Requirements
- Read the provided spec/requirements carefully
- Identify goals, constraints, and acceptance criteria
- Note any ambiguities or missing information
- **Ask clarifying questions** before proceeding if specs are unclear

### 2. Investigate Codebase

Use the **`unity-investigate-code`** skill to understand the related codebase:

```
Read and follow: .claude/skills/unity-investigate-code/SKILL.md
```

Focus on:
- Existing systems that will be affected
- Files that need modification
- Technical debt or constraints
- Reusable components
- Entry points and execution flows

### 3. Architecture Overview

**Show the architectural change** using simple before/after ASCII diagrams:

**Structure**:
- **OLD ARCHITECTURE**: Current state (problems highlighted)
- **NEW ARCHITECTURE**: Proposed state (with tree/hierarchy diagram)
- **Key Benefits**: Bullet list of architectural improvements

**Rules**:
- Keep diagrams simple and scannable (max 10-15 lines each)
- Use ASCII tree structure (`├──`, `└──`, `│`)
- Show data flow and object relationships
- Highlight the core structural change

See the template file for HTML structure and styling.

### 4. Technical Approach

**After Architecture Overview**, provide implementation steps:
- Explains **how** to implement the feature (not just what)
- Shows **key insights** from the investigation
- Keeps explanations **short and clear**

**Format**: Numbered bullet points with concise explanations

**Example**:
```markdown
## Technical Approach

1. Move remaining single-event state into `EventStateCache` (or a new `ActiveEventContext` struct)
2. Introduce an `_activeEventIds` list to track all currently active events
3. Keep `EventID` as `_focusedEventId` — the event the player is currently interacting with (UI context)
4. Add event-scoped overloads for `SelectDailyBossDifficulty()`, `SetCurrentBossHP()`, etc.
5. Mark old single-event methods `[Obsolete]` and delegate to the new event-scoped versions
6. Update callers progressively (foundation → non-breaking → breaking)
```

**Key elements to include**:
- Architecture decisions (patterns, data structures)
- Integration points with existing systems
- Migration strategy if touching legacy code
- Risk mitigation approach

### 5. High-Level Decomposition (Task Table)

Break down work into Tasks:

| # | Epic | Task | Description | Type | Cost |
|---|------|------|-------------|------|------|

**Types**: Logic, UI, Data, API, Asset, Test, Config

**Cost Sizing**:
| Size | Description |
|:----:|:------------|
| S | Simple, < 2 hours |
| M | Moderate, 2-4 hours |
| L | Complex, 4-8 hours |
| XL | Very complex, 1-2 days |

### 6. Walk Through Each Task with Code Changes

For each task, show **exact proposed code changes** in split-view format:

1. Identify affected files
2. Show before/after code side by side
3. Use the diff row classes from the template:
   - Deletions on left (red)
   - Additions on right (green)
   - Word-level highlights for inline changes

### 7. Acceptance Criteria

**After all code changes are defined**, generate Acceptance Criteria based on what you're planning to change. This section helps verify that all implementations work correctly.

**Format**: Checklist with testable criteria grouped by category

**Example**:
```markdown
## Acceptance Criteria

### Functional
- [ ] Multiple events can be active simultaneously without data conflicts
- [ ] Switching between events updates `_focusedEventId` correctly
- [ ] Old single-event methods still work via delegation to new overloads

### UI/UX
- [ ] Event list displays all active events
- [ ] Selected event is visually highlighted
- [ ] Switching events updates all UI elements

### Edge Cases
- [ ] Handle case when no events are active
- [ ] Handle case when focused event expires while viewing
- [ ] Handle rapid switching between events

### Debug Verification
- [ ] Log output confirms correct event scoping
- [ ] State inspector shows expected `_activeEventIds` values
- [ ] No null reference exceptions during event transitions
```

**Categories to include**:
- **Functional**: Core feature behavior
- **UI/UX**: Visual and interaction verification
- **Edge Cases**: Boundary conditions and error handling
- **Debug Verification**: Specific checks for debugging the implementation

### 8. Populate HTML Template

Read the template and replace all placeholders with actual data, including:
- `[ARCHITECTURE_OVERVIEW]` - The before/after diagrams from Step 3
- `[TECHNICAL_APPROACH]` - The bullet-pointed approach from Step 4
- `[ACCEPTANCE_CRITERIA]` - The checklist from Step 7

### 9. Summary

Provide a verbal summary:
- Total estimated effort
- Key risks or blockers
- Dependencies between tasks
- Recommended implementation order

## What This Skill Does NOT Do

❌ Write or modify actual code files  
❌ Create or edit Unity assets  
❌ Run implementations  
❌ Execute tasks from the plan  

This skill produces a **visual plan document** showing proposed changes only.

---
name: unity-plan
description: "High-level planning and costing for Unity features. Use when: (1) Analyzing requirements and specs, (2) Clarifying ambiguous specifications with the user, (3) Investigating existing codebase/systems, (4) Breaking work into Epics/Tasks, (5) Estimating high-level effort costs. This skill ONLY creates planning artifacts - it does NOT implement, code, or execute any tasks."
---

# Unity Planning Skill

Create high-level cost estimates and task breakdowns for Unity features.

**IMPORTANT**: This skill is for **planning only**. Do NOT implement, write code, or execute any work.

## Workflow

### 1. Analyze Requirements
- Read the provided spec/requirements carefully
- Identify goals, constraints, and acceptance criteria
- Note any ambiguities or missing information

### 2. Clarify Specifications
Ask the user to clarify if:
- Requirements are vague or incomplete
- Acceptance criteria are missing
- Dependencies are unclear
- Scope boundaries are undefined

**Always ask before assuming.** Use questions like:
- "What should happen when [edge case]?"
- "Is [Feature X] in scope or out of scope?"
- "What is the expected behavior for [scenario]?"

### 3. Investigate Codebase
Run: `.claude/skills/unity-plan/scripts/investigate_feature.sh [Keywords]`

Examine:
- Existing systems that will be affected
- Foundational files to modify
- Technical debt or constraints
- Reusable components

### 4. Break Down Work
Structure work into **Epics** (large features) and **Tasks** (atomic units):
- Each Task should be small and focused
- One responsibility per Task
- Clear deliverables

### 5. Estimate Costs
Use T-shirt sizing:
| Size | Description | Rough Estimate |
|:----:|:------------|:---------------|
| S | Simple, well-understood work | < 2 hours |
| M | Moderate complexity | 2-4 hours |
| L | Complex, multiple components | 4-8 hours |
| XL | Very complex, research needed | 1-2 days |

### 6. Output Task Table (REQUIRED)
**Always produce a Task Table as the final deliverable.**

| # | Epic | Task | Description | Type | Cost | Note |
|:-:|:-----|:-----|:------------|:----:|:----:|:-----|
| 1.1 | [Epic Name] | [Task Name] | [What needs to be done] | [Type] | [S/M/L/XL] | [Risks/Context] |

**Types**: Logic, UI, Data, API, Asset, Test, Config

### 7. Summarize
Provide:
- Total estimated effort (sum of T-shirt sizes)
- Key risks or blockers
- Dependencies between tasks
- Recommended implementation order

## Output Format

Save plan to: `Documents/Plans/IMPLEMENTATION_PLAN_[FeatureName].md`

Use template from: `assets/templates/IMPLEMENTATION_PLAN.md`

## What This Skill Does NOT Do

❌ Write or modify code  
❌ Create or edit Unity assets  
❌ Run implementations  
❌ Execute tasks from the plan  
❌ Make architectural decisions without user approval  

This skill produces a **plan document** only. Implementation is handled separately.

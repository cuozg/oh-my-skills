---
name: unity-plan
description: "High-level planning and costing for Unity features. Use when: (1) Analyzing requirements and specs, (2) Clarifying ambiguous specifications with the user, (3) Investigating existing codebase/systems, (4) Breaking work into Epics/Tasks, (5) Estimating high-level effort costs. This skill ONLY creates planning artifacts - it does NOT implement, code, or execute any tasks."
---

# Unity Planning Skill

Create high-level cost estimates and task breakdowns for Unity features.

**IMPORTANT**: This skill is for **planning only**. Do NOT implement, write code, or execute any work.

## Output Requirement (MANDATORY)

**Every plan MUST follow the template**: `assets/templates/IMPLEMENTATION_PLAN.md`

Save output to: `Documents/Plans/IMPLEMENTATION_PLAN_[FeatureName].md`

Read the template first, then populate all sections as described below.

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

### 6. Populate Template (REQUIRED)

Read template: `assets/templates/IMPLEMENTATION_PLAN.md`

Fill in **every section**:

#### Section 1: Executive Summary
- Brief overview of the feature
- Key requirements and goals
- High-level technical approach

#### Section 2: Project Base Investigation
- **Existing Systems**: List all systems involved (e.g., PlayerState, InventoryManager)
- **Foundational Files**: List key scripts, prefabs, or assets to modify
- **Technical Constraints**: Note known limitations, legacy debt, or risks

#### Section 3: High-Level Decomposition (Task Table)
Populate the Task Table:

| Number | Epic | Task | Description | Type | Cost | Note |
|:---:|:---|:---|:---|:---:|:---:|:---|

**Types**: Logic, UI, Data, API, Asset, Test, Config

#### Section 4: Total Estimated Costing
- **Total Duration**: Sum of T-shirt sizes converted to days
- **Resource Requirement**: Team composition needed
- **Risk Level**: Low/Medium/High with justification

#### Section 5: Implementation Workflow
Define the recommended phases:
1. **Setup Phase**: Base data structures and placeholders
2. **Logic Phase**: Core engine/system functionality
3. **UI/UX Phase**: Visuals and user interactions
4. **Validation Phase**: Testing and user verification
5. **Polishing/Optimization**: Final cleanup

#### Section 6: Definition of Done
Create a checklist of completion criteria, e.g.:
- [ ] Code passes all linting rules
- [ ] Unit tests cover core logic
- [ ] Feature verified in target scene
- [ ] Documentation updated

### 7. Summarize
After populating the template, provide a verbal summary:
- Total estimated effort
- Key risks or blockers
- Dependencies between tasks
- Recommended implementation order

## What This Skill Does NOT Do

❌ Write or modify code  
❌ Create or edit Unity assets  
❌ Run implementations  
❌ Execute tasks from the plan  
❌ Make architectural decisions without user approval  

This skill produces a **plan document** only. Implementation is handled separately.

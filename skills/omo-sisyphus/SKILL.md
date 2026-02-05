---
name: omo-sisyphus
description: "Orchestrator that delegates tasks to Sisyphus agent. CRITICAL: Always include load_skills parameter in delegate_task. Use for complex tasks requiring planning, delegation, code implementation, or multi-step work. Generates structured prompts following Sisyphus protocol."
---

# Sisyphus Orchestrator

**Role**: Generate Sisyphus-compatible prompts and delegate tasks to `@sisyphus`
**Reference**: [Sisyphus.ts](scripts/Sisyphus.ts) for prompt structure

---

## How Sisyphus Works

Sisyphus is a powerful AI orchestrator that:
- Plans obsessively with todos
- Assesses complexity before exploration
- Delegates via category + skills combinations
- Uses `@explore` for internal code, `@librarian` for external docs

> [!CAUTION]
> **CRITICAL REQUIREMENT: ALWAYS Include `load_skills` Parameter**
> 
> Every `delegate_task` call to Sisyphus **MUST** include the `load_skills` parameter:
> ```typescript
> delegate_task(
>   subagent_type="sisyphus",
>   load_skills=["skill-name"],  // <-- MANDATORY, even if empty []
>   prompt="..."
> )
> ```
> 
> **Missing `load_skills` = Skill not loaded = Task will fail!**

---

## ❌ WRONG vs ✅ RIGHT Delegation

**❌ WRONG - Missing `load_skills`:**
```typescript
delegate_task(
  subagent_type="sisyphus",
  description="Debug issue",  // ❌ This won't work!
  prompt="Debug the SS Tier..."
)
```
**Result**: Skill NOT loaded, task will likely fail!

**✅ RIGHT - With `load_skills`:**
```typescript
delegate_task(
  subagent_type="sisyphus",
  load_skills=["unity-debug"],  // ✅ Skill loaded!
  prompt="## Task\nDebug the SS Tier..."
)
```
**Result**: `unity-debug` skill loaded, task properly equipped!

---

## Workflow

> [!IMPORTANT]
> **When a skill is loaded, the prompt MUST explicitly tell Sisyphus to USE that skill:**
> 
> ```markdown
> ## Task
> [Task description]
> 
> **YOU MUST USE THE <skill-name> SKILL** that has been loaded for you.
> Follow the skill's instructions exactly.
> 
> ## Context
> - **Loaded skill**: <skill-name> - [brief description]
> 
> ## Requirements
> ### MUST DO:
> - **FOLLOW <skill-name> skill EXACTLY**
> - [other requirements from skill]
> ```
> 
> Simply passing `load_skills` is NOT enough - Sisyphus needs explicit instruction to use it!

### Step 1: Detect Skill Loading Mode

| User Input | Action |
|------------|--------|
| `use skill <skill-name> ...` | Extract skill name → `load_skills=[<skill-name>]` |
| No "use skill" keyword | Auto-detect appropriate skill from available skills |

### Explicit Skill Mode

When user says `use skill <skill-name>`:

```typescript
delegate_task(
  subagent_type="sisyphus",
  load_skills=["<skill-name>"],
  prompt="[user request without 'use skill' prefix]"
)
```

**Examples:**
- `use skill unity-review-pr PR #123` → `load_skills=["unity-review-pr"]`
- `use skill unity-plan create plan for feature X` → `load_skills=["unity-plan"]`

### Auto-Detect Skill Mode

When user does NOT say "use skill", analyze request and match to available skills:

| Request Type | Skill to Load |
|--------------|---------------|
| Review PR, check changes, PR link | `unity-review-pr` |
| Create plan, breakdown, estimate | `unity-plan` |
| Build/generate flatbuffer | `flatbuffer-builder` |
| Generate diagram, mermaid | `mermaid-generator` |
| Check bash script | `bash-check` |
| Other/unclear | No skill (Sisyphus decides) |

```typescript
delegate_task(
  subagent_type="sisyphus",
  load_skills=["<detected-skill>"],  // or [] if none detected
  prompt="[generated Sisyphus prompt]"
)
```

---

### Step 2: Analyze User Request

Classify the request type:

| Type | Signal | Sisyphus Action |
|------|--------|-----------------|
| **Trivial** | Single file, direct answer | Direct tools only |
| **Explicit** | Specific file/line, clear command | Execute directly |
| **Exploratory** | "How does X work?" | Fire explore + tools in parallel |
| **Open-ended** | "Improve", "Add feature" | Assess codebase first |
| **Ambiguous** | Unclear scope | Ask clarifying question |

### Step 3: Generate Sisyphus Prompt

Transform user request into structured Sisyphus prompt:

```markdown
## Task
[Clear, atomic description of what to accomplish]

## Expected Outcome
[Concrete deliverables with success criteria]

## Context
[Relevant file paths, patterns, constraints]

## Requirements
### MUST DO:
- [Exhaustive list of requirements]

### MUST NOT DO:
- [Forbidden actions]
```

### Step 4: Delegate to Sisyphus

**ALWAYS use `delegate_task` with `load_skills`:**

```typescript
delegate_task(
  subagent_type="sisyphus",
  load_skills=["<skill-name>"],  // From Step 1
  prompt="[generated Sisyphus prompt from Step 3]"
)
```

---

## Prompt Generation Rules

Based on [Sisyphus.ts](scripts/Sisyphus.ts):

### For Implementation Tasks

**When skill is loaded:**

```markdown
## Task
Implement [specific feature/fix]

**YOU MUST USE THE `[skill-name]` SKILL** that has been loaded for you.
Follow the skill's instructions exactly.

## Expected Outcome
- File(s) to create/modify: [paths]
- Success criteria: [what "done" looks like]

## Context
- Existing patterns: [reference files]
- Constraints: [tech stack, style]
- **Loaded skill**: `[skill-name]` - [brief description of what skill does]

## Requirements
### MUST DO:
- **FOLLOW `[skill-name]` skill instructions**
- Create todos BEFORE starting
- Mark tasks in_progress/completed
- Match existing codebase patterns
- Run lsp_diagnostics on changed files
- Verify build/tests pass

### MUST NOT DO:
- Ignore the loaded skill instructions
- Suppress type errors with as any, @ts-ignore
- Commit unless explicitly requested
- Refactor while fixing bugs
- Leave code in broken state
```

### For Exploration Tasks

**When skill is loaded:**

```markdown
## Task
Research/understand [topic]

**YOU MUST USE THE `[skill-name]` SKILL** that has been loaded for you.

## Expected Outcome
- Summary of findings
- Relevant code locations
- Recommendations

## Context
- Why needed: [reason]
- Scope: [boundaries]
- **Loaded skill**: `[skill-name]`

## Requirements
### MUST DO:
- **FOLLOW `[skill-name]` skill workflow**
- Use @explore for internal code (parallel)
- Use @librarian for external docs
- Stop when enough context found
- Cancel background tasks when done

### MUST NOT DO:
- Skip the skill instructions
- Over-explore (time is precious)
- Wait synchronously for explore/librarian
- Implement without understanding first
```

### For Review/Analysis Tasks

**When skill is loaded:**

```markdown
## Task
Review/analyze [target]

**YOU MUST USE THE `[skill-name]` SKILL** that has been loaded for you.
The skill contains the review template and submission instructions.

## Expected Outcome
- Assessment with severity levels
- Specific issues with locations
- Actionable recommendations

## Context
- Scope: [what to review]
- Standards: [conventions, patterns]
- **Loaded skill**: `[skill-name]` - Contains review format and submission script

## Requirements
### MUST DO:
- **FOLLOW `[skill-name]` skill EXACTLY**
- Check [specific areas from skill]
- Provide evidence for issues
- Suggest fixes
- Submit results using skill's method

### MUST NOT DO:
- Deviate from skill's format
- Miss [critical patterns from skill]
- Over-report minor issues
```

---

## Delegation Examples

### Example 1: Explicit Skill Mode

User: `use skill unity-review-pr Review PR #123`

```typescript
delegate_task(
  subagent_type="sisyphus",
  load_skills=["unity-review-pr"],
  prompt=`
## Task
Review PR #123 as expert Unity Developer

**YOU MUST USE THE unity-review-pr SKILL** that has been loaded for you.
Follow the skill's REVIEW_TEMPLATE.md format and submission instructions exactly.

## Expected Outcome
- Review posted to GitHub with inline comments
- Each issue as separate resolvable comment
- Submitted using post_review.sh script from skill

## Context
- **Loaded skill**: unity-review-pr - Contains review format, Unity patterns, and GitHub submission script

## Requirements
### MUST DO:
- **FOLLOW unity-review-pr skill EXACTLY**
- Use REVIEW_TEMPLATE.md format
- Check Unity-specific patterns (GetComponent in Update, etc.)
- Submit using scripts/post_review.sh

### MUST NOT DO:
- Deviate from REVIEW_TEMPLATE.md format
- Miss GetComponent in Update loops
- Combine multiple issues into one comment
- Skip GitHub submission
`
)
```

### Example 2: Auto-Detect Skill Mode

User: `Review PR #456` (no "use skill" keyword)

Auto-detected skill: `unity-review-pr` (matches "Review PR" trigger)

```typescript
delegate_task(
  subagent_type="sisyphus",
  load_skills=["unity-review-pr"],
  prompt=`
## Task
Review PR #456

**YOU MUST USE THE unity-review-pr SKILL** that has been loaded for you.

## Expected Outcome
- Complete review following REVIEW_TEMPLATE.md
- Inline comments for each issue
- Submitted to GitHub using post_review.sh

## Context
- **Loaded skill**: unity-review-pr

## Requirements
### MUST DO:
- **FOLLOW unity-review-pr skill workflow**
- Use templates and scripts from the skill
`
)
```

### Example 3: Feature Implementation (No Skill)

User: `Add user authentication to the API`

Auto-detected skill: None (general implementation task)

```typescript
delegate_task(
  subagent_type="sisyphus",
  load_skills=[],  // No specific skill, Sisyphus handles directly
  prompt=`
## Task
Implement user authentication for the API

## Expected Outcome
- Auth middleware created
- Login/logout endpoints
- JWT token handling
- Tests for auth flow

## Context
- API location: Assets/Scripts/API/
- Existing patterns: Check similar middleware

## Requirements
### MUST DO:
- Create todos BEFORE implementation
- Use existing error handling patterns
- Add unit tests
- Run lsp_diagnostics after changes

### MUST NOT DO:
- Store passwords in plain text
- Skip token expiration
- Leave endpoints unsecured
`
)

---

## Key Principles from Sisyphus.ts

1. **Always Plan First**: Create todos BEFORE non-trivial tasks
2. **Delegate Bias**: Work yourself ONLY when super simple
3. **Parallel Exploration**: explore/librarian = background + parallel
4. **Session Continuity**: Use session_id for follow-ups
5. **Verification Required**: lsp_diagnostics, build, tests
6. **No Evidence = Not Complete**: Every action needs verification

---

## Session Continuity

When continuing a task:

```
@sisyphus session_id="{previous_session_id}"

[Follow-up prompt]
```

Sisyphus has FULL context from previous session - no need to repeat.

---

## Anti-Patterns to Avoid

| Bad | Good |
|-----|------|
| ❌ Missing `load_skills` parameter | ✅ Always include `load_skills=["skill"]` or `[]` |
| ❌ Vague prompts | ✅ Exhaustive requirements |
| ❌ Missing MUST/MUST NOT | ✅ Explicit constraints |
| ❌ No expected outcome | ✅ Clear success criteria |
| ❌ Skipping todos | ✅ Plan before implement |
| ❌ Synchronous explore | ✅ Background + parallel |

---

## Critical Checklist

Before delegating to Sisyphus, verify:
- [ ] `load_skills` parameter is present (with skill name or empty `[]`)
- [ ] Prompt includes TASK, EXPECTED OUTCOME, REQUIREMENTS
- [ ] MUST DO and MUST NOT DO sections are complete
- [ ] Skill name matches auto-detect table (if applicable)

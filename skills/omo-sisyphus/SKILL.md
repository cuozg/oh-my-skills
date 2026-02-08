---
name: omo-sisyphus
description: "Orchestrator that delegates tasks to Sisyphus agent. CRITICAL: Always include load_skills parameter. Use for complex tasks requiring planning, delegation, or multi-step work. Generates structured prompts following Sisyphus protocol. Triggers: 'delegate to sisyphus', 'use sisyphus', complex multi-step requests."
---

# Sisyphus Orchestrator

**Purpose**: Generate Sisyphus-compatible prompts and delegate via `task()`.

---

## MANDATORY: `load_skills` Parameter

> [!CAUTION]
> **Every `task()` call MUST include `load_skills`**
> 
> ```typescript
> task(
>   category="quick",              // REQUIRED
>   load_skills=["skill-name"],    // MANDATORY, even if []
>   run_in_background=false,
>   prompt="..."
> )
> ```
> 
> **If no skill applies, justify:**
> ```
> load_skills=[]  // General implementation, no domain-specific skill applies
> ```

---

## Workflow

### Phase 1: Detect Skill Mode

| User Input | Action |
|------------|--------|
| `use skill <name> ...` | Extract → `load_skills=[<name>]` |
| No explicit skill | Auto-detect from request type |

**Auto-Detect Mapping:**

| Request Type | Skill |
|--------------|-------|
| Review PR, PR link | `unity-review-pr` |
| Create plan, estimate | `unity-plan` |
| Task with detail plan | `unity-plan-detail` |
| Execute task file | `unity-task-executor` |
| Generate flatbuffer | `flatbuffer-builder` |
| Generate diagram | `mermaid-generator` |
| Check bash script | `bash-check` |
| Other | `[]` (justify omission) |

---

### Phase 2: Pre-Delegation Planning (MANDATORY)

**BEFORE every `task()` call:**

```
I will use task() with:
- **category**: [quick|visual-engineering|deep|unspecified-high|...]
- **load_skills**: ["skill"] or []
- **Skill evaluation**:
  - unity-review-pr: OMIT - not a PR review
  - unity-plan: INCLUDE - user wants breakdown
- **Expected Outcome**: [success criteria]
```

> [!IMPORTANT]
> **When skill is loaded, prompt MUST explicitly instruct Sisyphus to USE it:**
> ```markdown
> **YOU MUST USE THE <skill-name> SKILL** that has been loaded.
> ```

---

### Phase 3: Generate Prompt

Use template: [DELEGATION_PROMPT.md](assets/templates/DELEGATION_PROMPT.md)

**Required sections:**

```markdown
## Task
[Atomic description - one action per delegation]

**YOU MUST USE THE `[skill-name]` SKILL** that has been loaded.

## Expected Outcome
[Concrete deliverables with success criteria]

## Context
- Existing patterns: [reference files]
- **Loaded skill**: `[skill-name]` - [description]

## Requirements
### MUST DO:
- Follow `[skill-name]` skill EXACTLY
- Create todos BEFORE starting
- Match existing codebase patterns
- Run lsp_diagnostics on changed files

### MUST NOT DO:
- Ignore loaded skill instructions
- Suppress type errors (as any, @ts-ignore)
- Commit unless requested
```

---

### Phase 4: Delegate

#### Background vs Sync

| Mode | When |
|------|------|
| `run_in_background=false` | Need result before next step |
| `run_in_background=true` | Parallel tasks, exploration |

```typescript
// Sync (blocking)
task(
  category="quick",
  run_in_background=false,
  load_skills=["<skill>"],
  prompt="..."
)

// Background (non-blocking)
task(
  category="quick",
  run_in_background=true,
  load_skills=["<skill>"],
  prompt="..."
)
// Collect later: background_output(task_id="...")
```

#### Session Continuity

**Reuse `session_id` for follow-ups:**

```typescript
// First call → get session_id
result = task(..., prompt="Implement feature")
// result.session_id = "ses_abc123"

// Follow-up with context preserved
task(session_id="ses_abc123", prompt="Fix type error on line 42")
```

---

## Examples

### Example 1: Explicit Skill

User: `use skill unity-review-pr Review PR #123`

```
I will use task() with:
- **category**: quick
- **load_skills**: ["unity-review-pr"]
- **Expected Outcome**: Review posted to GitHub
```

```typescript
task(
  category="quick",
  run_in_background=false,
  load_skills=["unity-review-pr"],
  prompt=`
## Task
Review PR #123 as expert Unity Developer.

**YOU MUST USE THE unity-review-pr SKILL** that has been loaded.

## Expected Outcome
- Review posted with inline comments

## Context
- **Loaded skill**: unity-review-pr

## Requirements
### MUST DO:
- Follow unity-review-pr skill EXACTLY
- Check Unity patterns (GetComponent in Update, etc.)

### MUST NOT DO:
- Skip GitHub submission
`
)
```

### Example 2: No Skill Needed

User: `Add user authentication to the API`

```
Skill evaluation:
- unity-review-pr: OMIT - not PR review
- unity-plan: OMIT - wants implementation, not planning
- DECISION: load_skills=[] - general implementation
```

```typescript
task(
  category="unspecified-high",
  run_in_background=false,
  load_skills=[],  // Justified above
  prompt=`
## Task
Implement user authentication

## Expected Outcome
- Auth middleware
- Login/logout endpoints
- JWT handling

## Requirements
### MUST DO:
- Create todos BEFORE implementation
- Follow existing patterns

### MUST NOT DO:
- Store plain text passwords
`
)
```

### Example 3: Parallel Exploration

```typescript
// Fire parallel background explorations
task(
  subagent_type="explore",
  run_in_background=true,
  load_skills=[],
  prompt="Find auth patterns in codebase"
)

task(
  subagent_type="explore",
  run_in_background=true,
  load_skills=[],
  prompt="Find caching implementations"
)

// Continue working, collect later with background_output()
```

---

## Anti-Patterns

| ❌ Bad | ✅ Good |
|-------|--------|
| Missing `load_skills` | Always include `load_skills=[]` or `[skill]` |
| `load_skills=[]` without justification | Evaluate each skill, justify omission |
| Loading skill without instruction | "YOU MUST USE skill" in prompt |
| Vague prompts | MUST DO / MUST NOT DO sections |
| Sync explore agents | Use `run_in_background=true` for explore |

---

## Checklist

- [ ] `load_skills` present
- [ ] Skills evaluated, omissions justified
- [ ] Prompt has: TASK, EXPECTED OUTCOME, CONTEXT, REQUIREMENTS
- [ ] MUST DO includes skill reference if loaded
- [ ] MUST NOT DO anticipates rogue behavior
- [ ] Background vs sync intentional

---
name: omo-sisyphus
description: "Orchestrator that delegates tasks to Sisyphus agent. CRITICAL: Always include load_skills parameter in delegate_task. Use for complex tasks requiring planning, delegation, code implementation, or multi-step work. Generates structured prompts following Sisyphus protocol. Supports v3.3.0 features: task transparency/inspectability, ctx.metadata(), storeToolMetadata(), session continuity, and enhanced CLI flags (--port, --attach, --session-id, --on-complete, --json)."
---

# Sisyphus Orchestrator

**Role**: Generate Sisyphus-compatible prompts and delegate tasks to `@sisyphus`

---

## Output Requirement (MANDATORY)

**Every delegation prompt MUST follow the template**: [DELEGATION_PROMPT.md](.claude/skills/omo-sisyphus/assets/templates/DELEGATION_PROMPT.md)

The generated prompt is passed directly to `delegate_task()`. No file save required.

Read the template first, then populate all sections.

## Your Role as Orchestrator

<Role>
You are invoking "Sisyphus" - Powerful AI Agent with orchestration capabilities.

**Why Sisyphus?**: Humans roll their boulder every day. So does Sisyphus. Code should be indistinguishable from a senior engineer's.

**Sisyphus Identity**: SF Bay Area engineer. Work, delegate, verify, ship. No AI slop.

**Core Competencies**:
- Parsing implicit requirements from explicit requests
- Adapting to codebase maturity (disciplined vs chaotic)
- Delegating specialized work to the right subagents
- Parallel execution for maximum throughput
- Follows user instructions - NEVER starts implementing unless explicitly requested

**Operating Mode**: Sisyphus NEVER works alone when specialists are available. Frontend work → delegate. Deep research → parallel background agents. Complex architecture → consult Oracle.
</Role>

---

## Task Transparency & Inspectability (v3.3.0)

> **Subagents are NO LONGER black boxes.** Every delegated `delegate_task` call is clickable and inspectable in the UI.

Each delegation exposes:
- **Full prompt** sent to the subagent
- **Description** of the task
- **Model** used for execution
- **Session ID** for continuity
- **Complete execution story** (inputs, outputs, tool calls)

**Implications for prompt quality**: Since every delegation is now fully visible and inspectable, prompts MUST be:
- Clear and self-documenting (users will read them)
- Well-structured with explicit sections
- Free of ambiguous or lazy instructions

### Metadata Documentation (v3.3.0)

Use `ctx.metadata()` and `storeToolMetadata()` to document delegation context:

```typescript
// Store structured metadata about what you're delegating and why
ctx.metadata({
  delegationReason: "PR review requires Unity-specific pattern checks",
  selectedSkills: ["unity-review-pr"],
  skillJustification: "Task is a PR review targeting Unity codebase",
  expectedOutcome: "Review posted to GitHub with inline comments",
})

// Document tool calls, not just execute them
storeToolMetadata({
  tool: "delegate_task",
  purpose: "Review PR #123 for Unity anti-patterns",
  category: "quick",
  skills: ["unity-review-pr"],
  sessionId: "ses_abc123",
})
```

**When to use metadata:**
- ALWAYS before `delegate_task()` calls — document intent
- When selecting/omitting skills — record justification
- When continuing sessions — link to previous session context

---

## CRITICAL: Always Include `load_skills`

> [!CAUTION]
> **MANDATORY: Every `delegate_task` call MUST include `load_skills` parameter**
> 
> ```typescript
> delegate_task(
>   subagent_type="sisyphus",
>   run_in_background=false,     // ← REQUIRED for task delegation
>   load_skills=["skill-name"],  // ← MANDATORY, even if empty []
>   prompt="..."
> )
> ```
> 
> **Missing `load_skills` = Skill not loaded = Task will fail!**
> 
> **If no skill applies, you MUST justify why:**
> ```
> load_skills=[]  // Justified: No skill matches this general implementation task
> ```

---

## Enhanced CLI Capabilities (v3.3.0)

New flags available for fine-grained control:

| Flag | Purpose | Example |
|------|---------|---------|
| `--port <N>` | Connect to specific OpenCode instance | `--port 3001` |
| `--attach` | Attach to running session interactively | `--attach --session-id ses_abc` |
| `--session-id <id>` | Resume specific session (critical for continuity) | `--session-id ses_abc123` |
| `--on-complete <cmd>` | Run command after task completes | `--on-complete "notify-send 'Done'"` |
| `--json` | Output structured JSON for programmatic use | `--json` |

**Use in delegation context:**
```typescript
// Resume a previous session with new instructions
delegate_task(
  session_id="ses_abc123",   // ← --session-id equivalent
  prompt="Fix the type error from previous attempt"
)

// Background task with structured output
delegate_task(
  subagent_type="explore",
  run_in_background=true,    // ← async execution
  load_skills=[],
  prompt="Find all auth patterns in codebase"
)
```

---

## Workflow

### Phase 0: Detect Skill Loading Mode

| User Input | Action |
|------------|--------|
| `use skill <skill-name> ...` | Extract skill name → `load_skills=[<skill-name>]` |
| No "use skill" keyword | Auto-detect skill from request type |

**Auto-Detect Mapping:**

| Request Type | Skill to Load |
|--------------|---------------|
| Review PR, check changes, PR link | `unity-review-pr` |
| Create plan, breakdown, estimate | `unity-plan` |
| Build/generate flatbuffer | `flatbuffer-builder` |
| Generate diagram, mermaid | `mermaid-generator` |
| Check bash script | `bash-check` |
| Other/unclear | `[]` (justify omission) |

---

### Phase 1: Pre-Delegation Planning (MANDATORY)

**BEFORE every `delegate_task` call, EXPLICITLY declare your reasoning:**

```
I will use delegate_task with:
- **load_skills**: ["skill-name"] or []
- **Skill evaluation**:
  - unity-review-pr: OMIT - not a PR review task
  - unity-plan: INCLUDE - user wants task breakdown
  - [evaluate each potentially relevant skill]
- **Expected Outcome**: [what success looks like]
```

**Then** make the delegate_task call.

> [!IMPORTANT]
> **When a skill is loaded, the prompt MUST explicitly tell Sisyphus to USE it:**
> 
> ```markdown
> ## Task
> [Task description]
> 
> **YOU MUST USE THE <skill-name> SKILL** that has been loaded.
> Follow the skill's instructions exactly.
> 
> ## Context
> - **Loaded skill**: <skill-name> - [brief description]
> ```

---

### Phase 2: Generate Sisyphus Prompt

Transform user request into structured Sisyphus prompt with ALL 6 sections:

```markdown
## Task
[Clear, atomic description - one action per delegation]

**YOU MUST USE THE `[skill-name]` SKILL** that has been loaded.

## Expected Outcome
[Concrete deliverables with success criteria]

## Context
- Existing patterns: [reference files]
- **Loaded skill**: `[skill-name]` - [what it does]

## Requirements
### MUST DO:
- **FOLLOW `[skill-name]` skill EXACTLY**
- Create todos BEFORE starting (2+ steps)
- Mark tasks in_progress/completed
- Match existing codebase patterns
- Run lsp_diagnostics on changed files
- Verify build/tests pass

### MUST NOT DO:
- Ignore the loaded skill instructions
- Suppress type errors (as any, @ts-ignore)
- Commit unless explicitly requested
- Refactor while fixing bugs
- Leave code in broken state
```

---

### Phase 3: Delegate to Sisyphus

#### Background vs Sync Delegation (v3.3.0)

| Mode | `run_in_background` | Use When |
|------|---------------------|----------|
| **Sync** | `false` | Task requires immediate result before next step |
| **Background** | `true` | Parallel tasks, exploration, non-blocking work |

**Prefer background** for:
- Multiple independent explorations (fire all in parallel)
- Long-running tasks where you can continue other work
- Explore/librarian agents (ALWAYS background)

**Use sync** for:
- Implementation tasks that block your next action
- Tasks where you need the result to make a decision
- Final verification/review steps

```typescript
// Sync delegation (blocking - wait for result)
delegate_task(
  subagent_type="sisyphus",
  run_in_background=false,
  load_skills=["<skill-name>"],  // From Phase 0
  prompt="[generated prompt from Phase 2]"
)

// Background delegation (non-blocking - continue working)
delegate_task(
  subagent_type="sisyphus",
  run_in_background=true,
  load_skills=["<skill-name>"],
  prompt="[generated prompt from Phase 2]"
)
// Collect later: background_output(task_id="...")
```

#### Session Continuity (v3.3.0)

Every `delegate_task()` output includes a `session_id`. **ALWAYS store and reuse it.**

```typescript
// First delegation → get session_id
result = delegate_task(subagent_type="sisyphus", run_in_background=false,
  load_skills=["unity-implement-logic"], prompt="Implement auth middleware")
// result.session_id = "ses_abc123"

// Follow-up using session_id → full context preserved
delegate_task(session_id="ses_abc123",
  prompt="Fix: Type error on line 42 in auth.ts")

// Verification using session_id → agent knows what it built
delegate_task(session_id="ses_abc123",
  prompt="Run lsp_diagnostics on all changed files and fix any errors")
```

**Why session_id is CRITICAL:**
- Subagent retains FULL conversation context
- No repeated file reads, exploration, or setup
- Saves 70%+ tokens on follow-ups
- Subagent knows what it already tried/learned

---

## Delegation Examples

### Example 1: Explicit Skill Mode (with metadata)

User: `use skill unity-review-pr Review PR #123`

```typescript
// Document delegation intent (v3.3.0 transparency)
ctx.metadata({
  delegationReason: "Explicit skill request: unity-review-pr",
  selectedSkills: ["unity-review-pr"],
  expectedOutcome: "Review posted to GitHub with inline comments",
})

delegate_task(
  subagent_type="sisyphus",
  run_in_background=false,
  load_skills=["unity-review-pr"],
  prompt=`
## Task
Review PR #123 as expert Unity Developer

**YOU MUST USE THE unity-review-pr SKILL** that has been loaded.
Follow the skill's REVIEW_TEMPLATE.md format and submission instructions.

## Expected Outcome
- Review posted to GitHub with inline comments
- Each issue as separate resolvable comment

## Context
- **Loaded skill**: unity-review-pr - Contains review format and Unity patterns

## Requirements
### MUST DO:
- **FOLLOW unity-review-pr skill EXACTLY**
- Check Unity-specific patterns (GetComponent in Update, etc.)
- Submit using .claude/skills/omo-sisyphus/scripts/post_review.sh

### MUST NOT DO:
- Deviate from REVIEW_TEMPLATE.md format
- Skip GitHub submission
`
)
```

### Example 2: No Skill Needed (with justification and metadata)

User: `Add user authentication to the API`

```
Skill evaluation:
- unity-review-pr: OMIT - not a PR review
- unity-plan: OMIT - user wants implementation, not planning
- flatbuffer-builder: OMIT - unrelated to auth
- DECISION: load_skills=[] - general implementation task
```

```typescript
// Store skill evaluation metadata (v3.3.0)
storeToolMetadata({
  tool: "delegate_task",
  purpose: "Implement user authentication",
  skillEvaluation: {
    omitted: ["unity-review-pr", "unity-plan", "flatbuffer-builder"],
    reason: "General implementation task, no domain-specific skill applies"
  },
})

delegate_task(
  subagent_type="sisyphus",
  run_in_background=false,
  load_skills=[],  // Justified above
  prompt=`
## Task
Implement user authentication for the API

## Expected Outcome
- Auth middleware created
- Login/logout endpoints
- JWT token handling

## Context
- API location: Assets/Scripts/API/

## Requirements
### MUST DO:
- Create todos BEFORE implementation
- Use existing error handling patterns
- Run lsp_diagnostics after changes

### MUST NOT DO:
- Store passwords in plain text
- Skip token expiration
`
)
```

### Example 3: Parallel Background Delegation (v3.3.0)

User: `Investigate how auth and caching work, then implement rate limiting`

```typescript
// Phase 1: Fire parallel background explorations
const authTask = delegate_task(
  subagent_type="explore",
  run_in_background=true,
  load_skills=[],
  prompt="Find all authentication middleware, patterns, and credential validation in this codebase."
)

const cacheTask = delegate_task(
  subagent_type="explore",
  run_in_background=true,
  load_skills=[],
  prompt="Find caching implementations, cache invalidation patterns, and TTL configurations."
)

// Phase 2: Continue with immediate work while background tasks run
// ... (prepare rate limiting plan)

// Phase 3: Collect results when needed
const authResult = background_output(task_id=authTask.task_id)
const cacheResult = background_output(task_id=cacheTask.task_id)

// Phase 4: Delegate implementation with gathered context
delegate_task(
  subagent_type="sisyphus",
  run_in_background=false,
  load_skills=[],  // Justified: general implementation
  prompt=`
## Task
Implement rate limiting middleware

## Context
- Auth patterns found: [from authResult]
- Caching patterns found: [from cacheResult]
...
`
)

// Cleanup
background_cancel(all=true)
```

---

## Communication Style for Prompts

Sisyphus expects:
- **Concise**: No preamble, start with task
- **No Flattery**: Don't praise the request
- **Explicit**: MUST DO and MUST NOT DO sections
- **Evidence Required**: Every action needs verification

---

## Anti-Patterns

| ❌ Bad | ✅ Good |
|-------|--------|
| Missing `load_skills` parameter | Always include `load_skills=[]` or `["skill"]` |
| `load_skills=[]` without justification | Evaluate each skill and justify omission |
| Loading skill without "YOU MUST USE" instruction | Explicit instruction to follow skill |
| Vague prompts | Exhaustive requirements with MUST/MUST NOT |
| No expected outcome | Clear success criteria |
| No metadata on delegation | `ctx.metadata()` before every `delegate_task()` |
| Starting fresh session when follow-up | Reuse `session_id` for continuity |
| Sync explore/librarian agents | ALWAYS use `run_in_background=true` for explore/librarian |
| Sequential independent explorations | Fire parallel background agents |

---

## Checklist Before Delegating

- [ ] `load_skills` parameter is present
- [ ] Skills evaluated and omissions justified
- [ ] Prompt includes: TASK, EXPECTED OUTCOME, CONTEXT, REQUIREMENTS
- [ ] MUST DO includes skill reference if skill loaded
- [ ] MUST NOT DO anticipates rogue behavior
- [ ] `ctx.metadata()` documents delegation intent (v3.3.0)
- [ ] `session_id` stored for potential follow-ups (v3.3.0)
- [ ] Background vs sync decision is intentional (v3.3.0)

---
name: omo-sisyphus
description: "Orchestrator that delegates tasks to Sisyphus agent. CRITICAL: Subagent MUST load skill before ANY action. Use for complex tasks requiring planning, delegation, or multi-step work. Generates structured prompts following Sisyphus protocol. Triggers: 'delegate to sisyphus', 'use sisyphus', complex multi-step requests."
---

# Sisyphus Orchestrator

**Purpose**: Generate Sisyphus-compatible prompts and delegate via `task()`.

---

## MANDATORY: Load Skill BEFORE Any Action

> [!CAUTION]
> **The subagent MUST load the appropriate skill BEFORE doing any work.**
> 
> The prompt MUST explicitly instruct the subagent:
> ```markdown
> ## FIRST: Load Required Skill
> **BEFORE you do anything**, read and follow this skill:
> `.claude/skills/[skill-name]/SKILL.md`
> ```
>
> **Skill selection by action type:**
>
> | Action | Skill to Load |
> |--------|---------------|
> | Write/implement code | `unity-code` |
> | Plan/estimate/breakdown | `unity-plan` |
> | Test/write tests | `unity-test` |
> | Review PR | `unity-review-pr` |
> | Execute task file | `unity-plan-executor` |
> | Detail task plan | `unity-plan-detail` |
> | Investigate codebase | `unity-investigate` |
> | Fix compilation errors | `unity-fix-errors` |
> | Debug issues | `unity-debug` |
> | Generate flatbuffer | `flatbuffers-coder` |
> | Generate diagram | `mermaid` |
> | Check bash script | `bash-check` |
> | General (no specific skill) | Justify omission |

---

## Workflow

### Phase 1: Detect Skill by Action Type

| User Intent | Primary Action | Skill |
|-------------|----------------|-------|
| "implement feature X" | Write code | `unity-code` |
| "create a plan for X" | Plan | `unity-plan` |
| "write tests for X" | Test | `unity-test` |
| "review PR #123" | Review | `unity-review-pr` |
| "execute task from file" | Execute | `unity-plan-executor` |
| "investigate how X works" | Investigate | `unity-investigate` |
| "fix compilation errors" | Fix | `unity-fix-errors` |
| "debug this issue" | Debug | `unity-debug` |
| `use skill <name> ...` | User-specified | `<name>` |

---

### Phase 2: Pre-Delegation Planning (MANDATORY)

**BEFORE every `task()` call:**

```
I will use task() with:
- **Primary action**: [code|plan|test|review|execute|investigate|fix|debug|...]
- **load_skills**: ["skill-name"]
- **Skill justification**: 
  - Action is "code" → unity-code (write C# for Unity)
- **Expected Outcome**: [success criteria]
```

---

### Phase 3: Generate Prompt

**Every prompt MUST include the skill loading instruction as the FIRST section:**

```markdown
## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
`.claude/skills/[skill-name]/SKILL.md`

This skill contains the rules, patterns, and workflow you MUST use.

---

## Task
[Atomic description - one action per delegation]

## Expected Outcome
[Concrete deliverables with success criteria]

## Context
- Existing patterns: [reference files]
- **Required skill**: `[skill-name]` - you loaded this above

## Requirements
### MUST DO:
- Follow `[skill-name]` skill EXACTLY as loaded above
- Create todos BEFORE starting
- Match existing codebase patterns
- Run lsp_diagnostics on changed files

### MUST NOT DO:
- Skip loading the skill first
- Ignore skill instructions
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

---

## Examples

### Example 1: Implementing Code

User: `Add a health bar to the player`

```
I will use task() with:
- **Primary action**: code (write C# implementation)
- **load_skills**: ["unity-code"]
- **Expected Outcome**: PlayerHealthBar.cs created with proper patterns
```

```typescript
task(
  category="unspecified-high",
  run_in_background=false,
  load_skills=["unity-code"],
  prompt=`
## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
\`.claude/skills/unity-code/SKILL.md\`

This skill contains Unity C# patterns, anti-patterns to avoid, and the pre-completion checklist.

---

## Task
Implement a health bar UI component for the player.

## Expected Outcome
- PlayerHealthBar.cs in Assets/Scripts/UI/
- Follows SCRIPT_TEMPLATE from unity-code skill
- Updates visually when player takes damage

## Context
- Player uses PlayerHealth component with OnHealthChanged event
- UI uses Unity UI system (Canvas, Image)

## Requirements
### MUST DO:
- Follow unity-code skill EXACTLY as loaded above
- Cache component references in Awake
- Subscribe in OnEnable, unsubscribe in OnDisable
- Add XML docs and comments

### MUST NOT DO:
- Use GetComponent in Update
- Skip the pre-completion checklist
- Ignore unity-code patterns
`
)
```

### Example 2: Creating a Plan

User: `Create a plan for implementing multiplayer`

```
I will use task() with:
- **Primary action**: plan
- **load_skills**: ["unity-plan"]
- **Expected Outcome**: Plan documents in documents/plans/multiplayer/
```

```typescript
task(
  category="deep",
  run_in_background=false,
  load_skills=["unity-plan"],
  prompt=`
## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
\`.claude/skills/unity-plan/SKILL.md\`

This skill contains the planning workflow, templates, and output format.

---

## Task
Create an implementation plan for adding multiplayer support.

## Expected Outcome
- HTML plan files in documents/plans/multiplayer/
- Overview, tasks, estimates, dependencies, timeline
- Patch file with all code changes

## Context
- Single-player game using Unity 6
- Need to support 2-4 players

## Requirements
### MUST DO:
- Follow unity-plan skill EXACTLY as loaded above
- Read all templates before generating
- Generate all 6 HTML files + patch

### MUST NOT DO:
- Implement any code (planning only)
- Skip any template file
- Output to assets/templates/ instead of documents/plans/
`
)
```

### Example 3: Writing Tests

User: `Write unit tests for PlayerHealth class`

```
I will use task() with:
- **Primary action**: test
- **load_skills**: ["unity-test"]
- **Expected Outcome**: Test file with comprehensive coverage
```

```typescript
task(
  category="quick",
  run_in_background=false,
  load_skills=["unity-test"],
  prompt=`
## FIRST: Load Required Skill

**BEFORE you do anything**, you MUST read and follow this skill:
\`.claude/skills/unity-test/SKILL.md\`

This skill contains test generation rules, naming conventions, and the output template.

---

## Task
Write comprehensive unit tests for PlayerHealth class.

## Expected Outcome
- Test file in Tests/EditMode/
- Covers: TakeDamage, Heal, death event, edge cases
- All tests pass

## Context
- PlayerHealth has TakeDamage(int), Heal(int), OnDeath event
- Pure logic, no MonoBehaviour lifecycle needed

## Requirements
### MUST DO:
- Follow unity-test skill EXACTLY as loaded above
- Use proper test naming convention
- Cover happy path + edge cases + error conditions

### MUST NOT DO:
- Skip the code analysis checklist
- Write Play Mode tests when Edit Mode suffices
- Leave tests without proper cleanup
`
)
```

---

## Anti-Patterns

| ❌ Bad | ✅ Good |
|-------|--------|
| Missing skill load instruction | "FIRST: Load Required Skill" section at top |
| `load_skills=[]` without justification | Evaluate action type, select skill |
| Generic prompt without skill reference | Prompt references loaded skill in MUST DO |
| Same skill for all tasks | Match skill to action type |
| Skill loaded but not used | "Follow skill EXACTLY as loaded above" |

---

## Checklist

- [ ] Action type identified (code/plan/test/review/etc)
- [ ] Correct skill selected for action type
- [ ] `load_skills` matches skill in prompt
- [ ] Prompt has "FIRST: Load Required Skill" section
- [ ] Skill path is `.claude/skills/[name]/SKILL.md`
- [ ] MUST DO includes "Follow skill EXACTLY as loaded above"
- [ ] MUST NOT DO includes "Skip loading the skill first"
- [ ] Background vs sync intentional

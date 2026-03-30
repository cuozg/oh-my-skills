# Delegation Prompt Templates

Templates for dispatching subagents during goal execution. The controller (sisyphus-work) provides all context upfront — subagents should never need to read the goal file themselves.

---

## Implementer Prompt Template

Use when delegating a sub-task to an implementer subagent.

```
1. TASK: Implement [sub-task subject]

2. EXPECTED OUTCOME:
   [Specific deliverables — files created/modified, behavior changes, observable results]

3. REQUIRED TOOLS:
   [Explicit tool whitelist — e.g., "read, write, edit, bash, lsp_diagnostics"]

4. MUST DO:
   - [Acceptance criterion 1 from the goal, verbatim]
   - [Acceptance criterion 2, if this sub-task addresses it]
   - Follow existing codebase patterns and conventions
   - Write tests if the project has test infrastructure
   - Self-review before reporting (see checklist below)

5. MUST NOT DO:
   - Do not modify files outside the scope of this sub-task
   - Do not add features not specified in the acceptance criteria
   - Do not suppress type errors (no `as any`, `@ts-ignore`, empty catches)
   - Do not refactor unrelated code

6. CONTEXT:
   - Project type: [Unity/Flutter/Web/General]
   - Relevant files: [list specific file paths]
   - Architecture: [brief description of how this fits into the system]
   - Dependencies: [what must exist before this sub-task]
   - Conventions: [naming patterns, file organization, error handling patterns]
   - Feature spec: [If a spec exists in Docs/Specs/, include relevant sections — especially Systems Design, Data Model, and Events. This defines the target architecture to follow. If no spec exists, state "No spec — implement based on acceptance criteria and codebase conventions."]
```

### Self-Review Checklist (include in every implementer prompt)

Before reporting back, the implementer should verify:

**Completeness:**
- Did I implement everything specified?
- Did I miss any requirements?
- Are there edge cases I didn't handle?

**Quality:**
- Are names clear and accurate?
- Is the code clean and maintainable?
- Does it follow existing patterns?

**Discipline:**
- Did I avoid overbuilding (YAGNI)?
- Did I only build what was requested?

**Testing:**
- Do tests verify behavior (not just mock behavior)?
- Are tests comprehensive?

---

## Implementer Status Protocol

Implementers MUST report one of four statuses:

| Status | Meaning | Controller Action |
|--------|---------|-------------------|
| **DONE** | Task completed, all requirements met | Proceed to spec review |
| **DONE_WITH_CONCERNS** | Completed but has doubts | Read concerns, address if needed, then review |
| **NEEDS_CONTEXT** | Missing information to proceed | Provide context via `session_id` continuation |
| **BLOCKED** | Cannot complete the task | Assess blocker, re-dispatch or escalate |

### Handling Each Status

**DONE** — Proceed directly to spec compliance review.

**DONE_WITH_CONCERNS** — Read the concerns carefully:
- Correctness/scope concerns → address before review
- Observations (e.g., "file is getting large") → note and proceed to review

**NEEDS_CONTEXT** — Provide the missing information via `session_id` continuation. Don't re-dispatch from scratch — the subagent already has partial context.

**BLOCKED** — Escalate based on blocker type:
1. Context problem → provide more context, re-dispatch same agent
2. Task too complex → re-dispatch with more capable model/category
3. Task too large → break into smaller sub-tasks
4. Plan is wrong → create new sub-tasks with corrected approach

**Never** ignore a BLOCKED status or force the same approach without changes.

---

## Spec Compliance Review Template

After an implementer reports DONE, dispatch a spec review to verify the implementation matches requirements.

```
You are reviewing whether an implementation matches its specification.

## What Was Requested
[FULL TEXT of the sub-task requirements and relevant acceptance criteria]

## What Implementer Claims They Built
[From implementer's status report]

## CRITICAL: Do Not Trust the Report

The implementer may be incomplete, inaccurate, or optimistic. Verify everything independently.

DO NOT:
- Take their word for what they implemented
- Trust their claims about completeness
- Accept their interpretation of requirements

DO:
- Read the actual code they wrote
- Compare implementation to requirements line by line
- Check for missing pieces they claimed to implement
- Look for extra features they didn't mention

## Your Job

Read the implementation code and verify:

**Missing requirements:**
- Did they implement everything requested?
- Are there requirements they skipped or missed?

**Extra/unneeded work:**
- Did they build things that weren't requested?
- Did they over-engineer or add unnecessary features?

**Misunderstandings:**
- Did they interpret requirements differently than intended?
- Did they solve the wrong problem?

Report:
- APPROVED — if everything matches after code inspection
- ISSUES — [list specifically what's missing or extra, with file:line references]
```

---

## Code Quality Review Template

Only dispatch AFTER spec compliance passes. Checks that the implementation is well-built.

```
You are reviewing code quality for a completed implementation.

## What Was Implemented
[Summary from implementer + spec reviewer approval]

## Files Changed
[List of files to review]

## Review Criteria

1. **Code Quality:**
   - Clean, readable, maintainable?
   - Proper error handling?
   - Type safety? No suppressions?
   
2. **Patterns:**
   - Follows existing codebase conventions?
   - Each file has one clear responsibility?
   - Well-defined interfaces between units?
   
3. **Testing:**
   - Tests verify behavior, not implementation details?
   - Edge cases and error paths covered?
   
4. **Architecture:**
   - Proper separation of concerns?
   - No unnecessary coupling introduced?

Report:
- Strengths: [what was done well]
- Issues: [Critical (must fix) | Important (should fix) | Minor (nice to have)]
- Assessment: APPROVED | NEEDS_FIXES
```

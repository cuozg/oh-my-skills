# Beads Workflow Templates

Copy-paste templates for common bead workflow operations.

---

## 1. Discovery Report Template

Use after Phase 1 codebase exploration, before creating beads.

```markdown
# Discovery Report: [Feature Name]

**Date**: [YYYY-MM-DD]  
**Explorer**: [Agent Name]  
**Epic ID**: [bd-N or TBD]

## Feature Request

[Original user request verbatim]

## Current State

### Relevant Files
- `path/to/file1.cs` - [Purpose]
- `path/to/file2.cs` - [Purpose]
- `path/to/prefab.prefab` - [Purpose]

### Key Components
- **[ComponentName]**: [What it does, where it's attached]
- **[SystemName]**: [Responsibilities, dependencies]

### Data Flow
[How data moves through the system]

```
User Input → [Component] → [Manager] → [Data Store]
                              ↓
                         [Side Effects]
```

## Dependencies

### Internal
- **[System A]**: [Dependency relationship, why needed]
- **[Class B]**: [Dependency relationship, why needed]

### External
- **Unity Package**: [Package name, version, usage]
- **Asset Store**: [Asset name, integration point]

## Risk Assessment

| Risk Factor | Level | Rationale |
|-------------|-------|-----------|
| **Complexity** | [LOW/MED/HIGH] | [Why] |
| **File Count** | [LOW/MED/HIGH] | [N files affected] |
| **Novelty** | [LOW/MED/HIGH] | [New patterns? Known territory?] |
| **Cross-Assembly** | [LOW/MED/HIGH] | [Affects multiple assemblies?] |
| **Test Coverage** | [LOW/MED/HIGH] | [Existing tests? Need new tests?] |

**Overall Risk**: [LOW/MEDIUM/HIGH]

## Recommended Approach

[Proposed implementation strategy based on risk level]

### If HIGH Risk:
- Create spike bead: `[spike-name]` (30-minute time-box)
- Questions to answer: [List unknowns]
- Success criteria: [What validates proceed vs. abort]

### If MEDIUM/LOW Risk:
- Proceed directly with task beads
- Decomposition strategy: [How to break into beads]

## Open Questions

1. [Question requiring clarification]
2. [Technical uncertainty]
3. [Design decision pending]

## Next Steps

- [ ] Review with orchestrator
- [ ] Create epic bead
- [ ] Create spike bead (if HIGH risk)
- [ ] Create task beads
- [ ] Run `bv --robot-plan`
```

---

## 2. Risk Assessment Template

Evaluate before creating beads. Determines if spike is required.

```markdown
# Risk Assessment: [Feature Name]

## Risk Factors

### 1. Complexity
- **Assessment**: [LOW/MEDIUM/HIGH]
- **Evidence**: [What makes it simple/moderate/complex?]
- **Mitigations**: [If HIGH, what reduces risk?]

### 2. File Count
- **Assessment**: [LOW (1-2) / MEDIUM (3-5) / HIGH (6+)]
- **Files Affected**:
  - `file1.cs` - [Reason for change]
  - `file2.cs` - [Reason for change]
  - [...]

### 3. Novelty (Pattern Familiarity)
- **Assessment**: [LOW/MEDIUM/HIGH]
- **Novel Patterns**: [List unfamiliar APIs, architectures, workflows]
- **Familiar Patterns**: [List established patterns being reused]

### 4. Cross-Assembly Impact
- **Assessment**: [LOW/MEDIUM/HIGH]
- **Affected Assemblies**:
  - `Assembly1.asmdef` - [Why affected]
  - `Assembly2.asmdef` - [Why affected]

### 5. External Dependencies
- **Assessment**: [LOW/MEDIUM/HIGH]
- **New Dependencies**: [Unity packages, Asset Store assets, libraries]
- **Integration Risk**: [How hard to integrate?]

### 6. Test Coverage
- **Assessment**: [LOW (no tests) / MEDIUM (partial) / HIGH (comprehensive)]
- **Existing Tests**: [What's already covered]
- **New Tests Needed**: [What needs test coverage]

## Overall Risk Level

**[LOW / MEDIUM / HIGH]**

## Decision

- **If LOW**: Proceed directly with task beads
- **If MEDIUM**: Proceed with caution, add extra verification beads
- **If HIGH**: **CREATE SPIKE BEAD** (30-minute time-box validation)

### Spike Requirements (if HIGH):
- **Spike Name**: `[spike-name]`
- **Questions to Answer**:
  1. [Critical unknown #1]
  2. [Critical unknown #2]
- **Success Criteria**: [What proves this is viable?]
- **Abort Criteria**: [What proves this is NOT viable?]
- **Deliverable**: `.spikes/[feature]/[spike-id]/FINDINGS.md`

## Approval

- **Reviewer**: [Orchestrator agent name]
- **Approved**: [Yes/No]
- **Date**: [YYYY-MM-DD]
```

---

## 3. Spike Bead Template

Use for HIGH-risk validation (30-minute time-box).

```markdown
# Spike: [Spike Name]

**Epic**: [bd-N]  
**Bead ID**: [bd-M] (spike)  
**Time-Box**: 30 minutes  
**Status**: [OPEN/CLOSED]

## Objective

Validate [specific unknown] to determine if we can proceed with [feature].

## Questions to Answer

1. **[Question 1]**: [What do we need to learn?]
2. **[Question 2]**: [What do we need to learn?]
3. **[Question 3]**: [What do we need to learn?]

## Success Criteria (Proceed)

- [ ] [Evidence that validates approach is viable]
- [ ] [Evidence that validates approach is viable]
- [ ] [Performance/quality threshold met]

## Abort Criteria (Do Not Proceed)

- [ ] [Blocker that prevents implementation]
- [ ] [Blocker that prevents implementation]
- [ ] [Unacceptable trade-off discovered]

## Investigation Steps

1. [Step to validate question 1]
2. [Step to validate question 2]
3. [Step to validate question 3]

## Findings

[To be filled during spike execution]

### What We Learned

[Summary of discoveries]

### Evidence

- **Code Sample**: [Reference to prototype file or snippet]
- **Performance Data**: [Benchmark results, profiler screenshots]
- **Documentation**: [Links to official docs, forum posts, GitHub issues]

### Recommendation

**[PROCEED / ABORT / MODIFY APPROACH]**

**Rationale**: [Why this decision?]

**If PROCEED**: Convert to feature bead(s): [List task beads to create]

**If ABORT**: Alternative approach: [What to do instead?]

## Output Location

`.spikes/[feature]/[spike-id]/FINDINGS.md`

## References

- [Unity documentation link]
- [GitHub issue link]
- [Forum discussion link]
```

---

## 4. Epic Bead Template

Top-level bead for tracking entire feature (has child task beads).

```markdown
# Epic: [Feature Name]

**Bead ID**: [bd-N]  
**Priority**: [0=spike, 1=critical, 2=high, 3=medium, 4=low]  
**Status**: [OPEN/CLOSED]  
**Created**: [YYYY-MM-DD]

## Description

[High-level feature description from user request]

## Acceptance Criteria

- [ ] [User-facing requirement 1]
- [ ] [User-facing requirement 2]
- [ ] [User-facing requirement 3]
- [ ] [All tests pass]
- [ ] [Documentation updated]

## Child Beads

### Spikes (if any)
- [bd-M] - [Spike name] - **Status**: [OPEN/CLOSED]

### Task Beads
- [bd-X] - [Task 1 name] - **Status**: [OPEN/CLOSED] - **Track**: [N]
- [bd-Y] - [Task 2 name] - **Status**: [OPEN/CLOSED] - **Track**: [N]
- [bd-Z] - [Task 3 name] - **Status**: [OPEN/CLOSED] - **Track**: [N]

## Agent Mail Thread

**Thread ID**: `[bd-N]`  
**Purpose**: Epic-level coordination, orchestrator ↔ workers communication

## Execution Plan

Generated by `bv --robot-plan [bd-N]`:

```
Track 1 (Worker1): [bd-X] → [bd-Y]
Track 2 (Worker2): [bd-Z]
```

## File Reservations

[List files reserved across all child beads to check for conflicts]

## Dependencies

- **Blocks**: [Other beads that wait for this epic]
- **Blocked By**: [Other beads that must complete first]

## Completion Checklist

- [ ] All child beads closed
- [ ] Integration tests pass
- [ ] No merge conflicts
- [ ] Documentation updated
- [ ] Orchestrator approval
```

---

## 5. Task Bead Template

Atomic unit of work (typically 1 file, 1 test, 1 component).

```markdown
# Task: [Task Name]

**Bead ID**: [bd-N]  
**Epic**: [bd-M]  
**Priority**: [1=critical, 2=high, 3=medium, 4=low]  
**Status**: [OPEN/CLOSED]  
**Track**: [N]  
**Worker**: [AgentName]

## Description

[Specific, atomic task description]

## Implementation

### Files to Modify
- `path/to/file1.cs` - [What changes]
- `path/to/file2.cs` - [What changes]

### Files to Create
- `path/to/newfile.cs` - [Purpose]

### Tests Required
- [ ] Edit Mode test: `Test[Feature][Scenario]`
- [ ] Play Mode test: `Test[Feature][Integration]`

## Acceptance Criteria

- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [No compiler errors]
- [ ] [Tests pass]

## Dependencies

- **Depends On**: [bd-X] (must complete before this)
- **Blocks**: [bd-Y] (waits for this to finish)

## Agent Mail Thread

**Thread ID**: `track:[AgentName]:[epic-bd-M]`  
**Purpose**: Worker self-messages (context preservation between beads)

## File Reservations

Reserved via `file_reservation_paths`:
- `path/to/file1.cs` (exclusive)
- `path/to/file2.cs` (exclusive)

**Release after**: Bead closed + completion message sent

## Execution Steps

1. Reserve files via Agent Mail `file_reservation_paths`
2. Implement changes in listed files
3. Write/update tests
4. Verify compilation and test pass
5. Self-message to worker thread (context for next bead)
6. Message orchestrator: `[bd-N] COMPLETE`
7. Close bead: `bd close [bd-N]`
8. Release file reservations

## Completion Message Template

**Subject**: `[bd-N] COMPLETE`  
**To**: [Orchestrator]  
**Thread**: `[epic-bd-M]`  
**Body**:
```
Completed [task name].

**Changes**:
- Modified `file1.cs`: [summary]
- Created `file2.cs`: [purpose]

**Tests**:
- ✅ `Test[Feature][Scenario]` passes
- ✅ `Test[Feature][Integration]` passes

**Next**: Ready for [bd-N+1] (if any in track)
```

## Notes

[Any gotchas, design decisions, or future improvements]
```

---

## 6. Worker Prompt Template

Use when spawning autonomous worker agents (Phase 3).

```markdown
You are **Worker [N]** for epic [bd-M]: [Feature Name].

## Your Track

Execute these beads in sequence:
- [bd-X] - [Task 1 name]
- [bd-Y] - [Task 2 name]
- [bd-Z] - [Task 3 name]

## Agent Mail Setup

**Epic Thread**: `[bd-M]` (for orchestrator coordination)  
**Worker Thread**: `track:Worker[N]:[bd-M]` (for your context preservation)

## Workflow (Per Bead)

1. **Reserve Files**:
   ```
   file_reservation_paths(
     paths: [list from bead],
     exclusive: true,
     ttl_seconds: 7200
   )
   ```

2. **Execute Bead**:
   - Read task bead details (`bd show [bd-X]`)
   - Implement changes (files listed in bead)
   - Write/update tests
   - Verify compilation and test pass

3. **Preserve Context** (self-message):
   ```
   send_message(
     to: ["Worker[N]"],
     thread_id: "track:Worker[N]:[bd-M]",
     subject: "[bd-X] Context for Next Bead",
     body: "[Summary of what you did, gotchas, state for next bead]"
   )
   ```

4. **Report Completion**:
   ```
   send_message(
     to: ["Orchestrator"],
     thread_id: "[bd-M]",
     subject: "[bd-X] COMPLETE",
     body: "[Changes, tests, next steps]"
   )
   ```

5. **Close Bead**:
   ```
   bd close [bd-X]
   ```

6. **Release Files**:
   ```
   release_file_reservations(paths: [list from bead])
   ```

7. **Check Inbox** (orchestrator might have sent updates):
   ```
   fetch_inbox(thread_id: "[bd-M]")
   ```

8. **Next Bead**: Repeat for [bd-Y], then [bd-Z]

## Blocked Protocol

If you cannot proceed (missing dependency, conflict, unclear requirement):

1. **Message Orchestrator**:
   ```
   send_message(
     to: ["Orchestrator"],
     thread_id: "[bd-M]",
     subject: "[bd-X] BLOCKED: [reason]",
     body: "[Detailed explanation, what's needed to unblock]"
   )
   ```

2. **Wait for Resolution**: Check inbox periodically

3. **Resume**: Once unblocked, orchestrator will message you

## Track Completion

After closing all beads in your track:

```
send_message(
  to: ["Orchestrator"],
  thread_id: "[bd-M]",
  subject: "[Track [N]] COMPLETE",
  body: "All beads in track [N] completed successfully. Ready for integration."
)
```

## Tools Available

- **bd CLI**: `bd show`, `bd close`, `bd update`, `bd ls`
- **Agent Mail**: `send_message`, `fetch_inbox`, `file_reservation_paths`, `release_file_reservations`
- **Unity skills**: `/unity-code`, `/unity-test`, `/unity-investigate`

## Notes

- **Always** self-message context before moving to next bead
- **Always** check epic thread for orchestrator updates before each bead
- **Never** modify files outside your file reservations
- **Never** close a bead before sending completion message
```

---

## 7. Message Templates

### 7.1. Bead Completion Message

```markdown
**Subject**: `[bd-N] COMPLETE`  
**To**: [Orchestrator]  
**Thread**: `[epic-bd-M]`

**Body**:
```
Completed [bead name].

**Changes**:
- Modified `file1.cs`: [summary of changes]
- Created `file2.cs`: [purpose and functionality]
- Updated prefab `prefab.prefab`: [modifications]

**Tests**:
- ✅ `Test[Feature][Scenario]` passes
- ✅ `Test[Feature][Integration]` passes

**Verification**:
- ✅ No compiler errors
- ✅ Play Mode tested manually
- ✅ Performance acceptable (profiler checked)

**Next**: Ready for [bd-N+1] (or track complete if last bead)
```
```

### 7.2. Blocked Message

```markdown
**Subject**: `[bd-N] BLOCKED: [reason]`  
**To**: [Orchestrator]  
**Thread**: `[epic-bd-M]`

**Body**:
```
Cannot proceed with [bead name].

**Blocker**:
[Detailed explanation of what's blocking progress]

**Impact**:
- Blocks: [bd-X], [bd-Y] (if any)
- Affects Track [N]

**Needed to Unblock**:
- [Specific requirement 1]
- [Specific requirement 2]

**Suggested Resolution**:
[Proposed fix or workaround]

**Status**: Awaiting orchestrator decision
```
```

### 7.3. Context Preservation (Self-Message)

```markdown
**Subject**: `[bd-N] Context for Next Bead`  
**To**: [Self - Worker Name]  
**Thread**: `track:[WorkerName]:[epic-bd-M]`

**Body**:
```
Completed [bd-N]. Context for [bd-N+1]:

**State**:
- [File1.cs]: Implemented [feature], exposed [API]
- [Component]: Added to [prefab], configured with [settings]

**Gotchas**:
- [Warning about X]
- [Be aware of Y]

**For Next Bead [bd-N+1]**:
- Will need to integrate with [API from bd-N]
- File reservation: [file.cs] (currently held, will release after bd-N+1)
- Test coverage: [what's covered, what's not]

**Design Decisions**:
- Chose [approach A] over [approach B] because [reason]
- Added [field/method] for [future extensibility]
```
```

### 7.4. Interface Change Broadcast

```markdown
**Subject**: `[Interface Change] [Component/API Name]`  
**To**: [All affected workers]  
**CC**: [Orchestrator]  
**Thread**: `[epic-bd-M]`

**Body**:
```
⚠️ **Breaking Change Alert**

**Component**: [ComponentName]  
**Changed By**: [bd-N]  
**Change Type**: [API signature, data structure, event name, etc.]

**What Changed**:
```csharp
// Before
public void OldMethod(int param);

// After
public void NewMethod(Item item); // Item is now ScriptableObject
```

**Affected Beads**:
- [bd-X] - [Worker1] - [Why affected]
- [bd-Y] - [Worker2] - [Why affected]

**Migration Guide**:
1. Replace `OldMethod` calls with `NewMethod`
2. Convert `int itemId` to `Item scriptableObject` via `ItemDatabase.GetItem(itemId)`
3. Update tests that mock the interface

**Example**:
```csharp
// Before
inventory.OldMethod(itemId);

// After
Item item = ItemDatabase.GetItem(itemId);
inventory.NewMethod(item);
```

**Timeline**:
- [bd-N] merged to main: [date]
- Affected workers: please acknowledge and update your beads

**Questions**: Reply to this thread
```
```

### 7.5. Track Completion

```markdown
**Subject**: `[Track [N]] COMPLETE`  
**To**: [Orchestrator]  
**Thread**: `[epic-bd-M]`

**Body**:
```
All beads in Track [N] completed successfully.

**Completed Beads**:
- ✅ [bd-X] - [Task 1 name]
- ✅ [bd-Y] - [Task 2 name]
- ✅ [bd-Z] - [Task 3 name]

**Integration Status**:
- ✅ All tests pass
- ✅ No merge conflicts with main
- ✅ File reservations released

**Ready For**:
- Integration with other tracks (if any pending)
- Final verification and epic closure

**Notes**:
[Any gotchas for integration, future improvements, or follow-up work]
```
```

### 7.6. Spike Findings

```markdown
**Subject**: `[Spike bd-N] FINDINGS: [PROCEED/ABORT]`  
**To**: [Orchestrator]  
**Thread**: `[epic-bd-M]`

**Body**:
```
Completed spike: [spike name]

**Recommendation**: **[PROCEED / ABORT / MODIFY APPROACH]**

**Questions Answered**:
1. [Question 1]: [Answer with evidence]
2. [Question 2]: [Answer with evidence]
3. [Question 3]: [Answer with evidence]

**Evidence**:
- Prototype code: `.spikes/[feature]/[spike-id]/prototype.cs`
- Performance: [benchmark results]
- Documentation: [links to Unity docs, forum posts]

**If PROCEED**:
Create these feature beads:
- [bd-X] - [Task derived from spike]
- [bd-Y] - [Task derived from spike]

**If ABORT**:
Reason: [Why approach is not viable]
Alternative: [Suggested different approach]

**Findings Document**: `.spikes/[feature]/[spike-id]/FINDINGS.md`
```
```

### 7.7. Hotfix Bead (Orchestrator → Worker)

```markdown
**Subject**: `[HOTFIX] [bd-N] Unblocks [bd-X]`  
**To**: [Blocked Worker]  
**Thread**: `[epic-bd-M]`

**Body**:
```
Created hotfix bead [bd-N] to unblock your work on [bd-X].

**Issue**: [What was blocking the worker]

**Solution**: [bd-N] implements [fix description]

**Status**: [bd-N] is **CLOSED** and merged to main

**Action Required**:
1. Pull latest from main
2. Resume work on [bd-X]
3. [Any additional steps to integrate the fix]

**Changes**:
- [File1.cs]: [What changed]
- [File2.cs]: [What changed]

You can now proceed with [bd-X].
```
```

---

## 8. Integration Checklist

Use before closing epic (Phase 5).

```markdown
# Integration Checklist: [Epic bd-M]

## Bead Completion

- [ ] All child beads closed (`bd ls --open` returns none for epic)
- [ ] All workers reported track completion
- [ ] All file reservations released

## Code Quality

- [ ] No compiler errors
- [ ] No warnings in console (or documented exceptions)
- [ ] Code follows project conventions (`.opencode/rules/unity-csharp-conventions.md`)
- [ ] Comments and XML docs added for public APIs

## Testing

- [ ] All Edit Mode tests pass
- [ ] All Play Mode tests pass
- [ ] Manual testing completed (list scenarios tested)
- [ ] Performance profiling completed (no regressions)

## Integration

- [ ] Merged all tracks to main (or feature branch)
- [ ] No merge conflicts
- [ ] Git history clean (atomic commits per bead)
- [ ] Branch up-to-date with main

## Documentation

- [ ] README updated (if public API changed)
- [ ] Inline comments added (for complex logic)
- [ ] Agent Mail thread archived (findings, decisions)
- [ ] Knowledge base updated (if new patterns introduced)

## Verification

- [ ] Feature matches acceptance criteria (from epic bead)
- [ ] No breaking changes (or documented with migration guide)
- [ ] Assets validated (prefabs, materials, scenes)
- [ ] Build succeeds (if changes affect build pipeline)

## Sign-Off

- **Orchestrator**: [Name] - [Date]
- **Verification**: [Name] - [Date]
- **Approval**: [Name] - [Date]

## Post-Completion

- [ ] Close epic bead: `bd close [bd-M]`
- [ ] Message epic thread with completion summary
- [ ] Archive spike findings (if any) to `.spikes/[feature]/`
- [ ] Update project roadmap (if applicable)
```

---

## Quick Reference

### Bead Creation
```bash
# Spike bead
bd add "Spike: [name]" --epic [bd-M] --priority 0

# Task bead
bd add "[task name]" --epic [bd-M] --priority [1-4]
```

### Agent Mail Threads
```
Epic thread:   [bd-M]
Track thread:  track:[AgentName]:[bd-M]
```

### File Reservation
```javascript
// Reserve
file_reservation_paths(
  paths: ["path/to/file.cs"],
  exclusive: true,
  ttl_seconds: 7200
)

// Release
release_file_reservations(
  paths: ["path/to/file.cs"]
)
```

### Message Subjects
```
[bd-N] COMPLETE           - bead finished
[bd-N] BLOCKED: reason    - cannot proceed
[bd-N] Context for Next   - self-message (worker thread)
[Track N] COMPLETE        - all track beads done
[Interface Change] name   - breaking API change
[Spike bd-N] FINDINGS     - spike results
[HOTFIX] bd-N             - unblocking bead
```

---

**Templates Version**: 1.0  
**Last Updated**: [YYYY-MM-DD]

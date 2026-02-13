# Prompt Refinement Reference

Detailed patterns for the Prompt Refinement Workflow. Load this when analyzing user requests.

## Clarity Checklist

Score each dimension 1-3 (1=missing, 2=vague, 3=clear). Total < 12 triggers clarifying questions.

| Dimension | 1 (Missing) | 2 (Vague) | 3 (Clear) |
|---|---|---|---|
| **Goal** | No stated objective | "Fix the UI" | "Fix the lobby screen's player list not updating when new players join" |
| **Scope** | Unbound | "Change some stuff" | "Modify PlayerListController.cs and LobbyScreen.uxml" |
| **Constraints** | None stated | "Keep it clean" | "Must support Unity 6, follow existing MVC pattern, no new packages" |
| **Success criteria** | No way to verify | "It should work" | "Player list refreshes within 500ms of player join event; unit test passes" |
| **Context** | No references | "Look at the code" | "Uses DataManager pattern from Assets/Scripts/Managers/, binds to LobbyScreen.uxml" |

**Scoring guide:**
- 13-15: Clear enough — skip to refined prompt preview
- 9-12: Somewhat ambiguous — ask 2-3 targeted questions
- 5-8: Very unclear — ask 4-5 clarifying questions

---

## Ambiguity Patterns

Common issues in user requests that trigger clarifying questions:

### Pattern 1: Scope Ambiguity
**Signal**: Request could mean many things
- "Improve the UI" — which screen? which aspect? visual? functional?
- "Add player features" — what features? which player system?
- "Fix the bugs" — which bugs? where?

### Pattern 2: Missing Context
**Signal**: Can't determine where to start without more info
- "Add a settings screen" — what settings? design spec? existing patterns?
- "Implement matchmaking" — what backend? protocol? existing infra?

### Pattern 3: Conflicting Intent
**Signal**: Request implies multiple contradictory actions
- "Refactor and add new features" — refactor first? or interleave?
- "Optimize and redesign" — performance or architecture focus?

### Pattern 4: Unspecified Technology
**Signal**: Multiple valid approaches exist
- "Build a UI" — uGUI or UI Toolkit? Canvas or UXML?
- "Add networking" — Netcode? Mirror? custom?
- "Create animations" — Animator? DOTween? UI Toolkit transitions?

### Pattern 5: Scale Uncertainty
**Signal**: Can't estimate effort
- "Build the game" — what scope? MVP? full feature?
- "Create the data layer" — how many entities? local or server?

---

## Question Templates

### Goal Clarification
```
What specific outcome do you want? For example:
- A working feature that [does X]
- A code change that fixes [specific bug]
- A plan/design document for [system]
- A refactoring that achieves [architectural goal]
```

### Scope Clarification
```
Which files/systems should this touch?
- Specific scripts (e.g., "PlayerManager.cs")
- A subsystem (e.g., "the inventory system")
- A screen/UI (e.g., "the shop screen")
- Multiple systems (please list them)
```

### Constraint Clarification
```
Are there constraints I should know about?
- Must match existing patterns (which ones?)
- Performance budgets (FPS, memory, load time?)
- Platform targets (mobile, WebGL, desktop?)
- Dependencies to avoid or prefer
```

### Success Criteria Clarification
```
How will you verify this is done correctly?
- Specific behavior ("clicking X should do Y")
- Test that passes (unit test, play mode test?)
- Visual result (matches mockup? screenshot?)
- Performance metric (target FPS, load time?)
```

### Approach Clarification
```
Do you have a preference for the approach?
- Follow an existing pattern in the codebase
- Use a specific Unity feature/API
- Implement from scratch vs extend existing
- Priority: speed, quality, or maintainability
```

---

## Refined Prompt Template

Use this structure when presenting the refined prompt to the user before delegation:

```markdown
## Refined Prompt Preview

**Goal**: [One clear sentence describing the objective]

**Scope**: [Specific files, systems, or areas to modify]

**Approach**: [How the task will be accomplished]

**Selected Skill(s)**: [Skill names with rationale]
- Primary: `{primary-skill}` — [why this skill]
- Additional: `{additional-skill}` — [why needed]

**Expected Outcome**:
- [Deliverable 1]
- [Deliverable 2]
- Success: [How to verify completion]

**Constraints**:
- [Constraint 1]
- [Constraint 2]
- Safety: No git push, no AI metadata, no destructive actions without confirmation

---
Ready to delegate? (yes / no / edit)
```

---

## Before/After Examples

### Example 1: Vague Implementation Request

**Before** (user's raw request):
> "Add health regen to the player"

**Clarity Score**: Goal=2, Scope=1, Constraints=1, Success=1, Context=1 → Total=6 (very unclear)

**Clarifying Questions**:
1. Should health regenerate over time, on item use, or both?
2. Is there an existing PlayerHealth component to extend, or create new?
3. Should regen be configurable (rate, delay after damage, max cap)?
4. Any UI updates needed (health bar animation)?

**After** (refined prompt):
> **Goal**: Add passive health regeneration to the player character that starts after 3 seconds of not taking damage.
> **Scope**: Extend existing `PlayerHealth.cs` in `Assets/Scripts/Player/`. Update `PlayerHUD.uxml` health bar to show regen indicator.
> **Skill**: `unity/unity-code` + `unity/unity-test`
> **Expected Outcome**: PlayerHealth gains configurable regen (rate, delay, cap). HUD shows regen state. Edit mode tests cover regen logic.

### Example 2: Ambiguous UI Request

**Before**:
> "Make the lobby screen better"

**Clarity Score**: Goal=1, Scope=2, Constraints=1, Success=1, Context=1 → Total=6

**Clarifying Questions**:
1. "Better" in what way — visual design, performance, functionality, or UX flow?
2. Is there a design mockup or reference for the desired look?
3. Which parts of the lobby screen need improvement (player list, chat, matchmaking)?
4. Are you using UI Toolkit or uGUI for this screen?

**After**:
> **Goal**: Redesign the lobby screen player list to show player avatars, rank badges, and ready status with smooth animations.
> **Scope**: `LobbyScreen.uxml`, `LobbyScreen.uss`, `LobbyScreenController.cs`
> **Skill**: `unity/ui-toolkit/ui-toolkit-master` + `unity/ui-toolkit/ui-toolkit-patterns`
> **Expected Outcome**: Player list items show avatar, rank, ready status. List updates reactively. Enter/exit animations. Matches existing dark theme.

### Example 3: Clear Request (No Questions Needed)

**Before**:
> "Fix the NullReferenceException in InventoryManager.cs line 142 where it tries to access _playerData.Inventory before PlayerData is initialized"

**Clarity Score**: Goal=3, Scope=3, Constraints=2, Success=3, Context=3 → Total=14

**Action**: Skip questions, go directly to refined prompt preview.

**Refined prompt**:
> **Goal**: Fix NRE in InventoryManager.cs:142 — null-check `_playerData.Inventory` access.
> **Scope**: `InventoryManager.cs`, line 142 area.
> **Skill**: `unity/unity-fix-errors`
> **Expected Outcome**: NRE resolved. Null guard added. lsp_diagnostics clean. Existing tests pass.

---

## Skill Selection Heuristics

When the intent maps to multiple valid skills, prefer:

1. **Most specific skill first** — `unity/unity-fix-errors` over `unity/unity-code` for compilation errors
2. **Add complementary skills** — `unity/unity-test` alongside `unity/unity-code` for implementation tasks
3. **UI Toolkit depth** — start with `ui-toolkit-master`, add sub-skills based on specific needs (databinding, theming, responsive)
4. **Investigation before implementation** — suggest `explore` subagent first if the codebase is unfamiliar, then Sisyphus for implementation
5. **Max 4 skills per delegation** — more than 4 dilutes focus; split into sequential delegations instead

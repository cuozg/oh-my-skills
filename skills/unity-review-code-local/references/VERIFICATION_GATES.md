# Verification Gates

Evidence before claims. Investigate before commenting.

## Evidence Requirements by Severity

| Severity | Required Before Commenting | NOT Sufficient |
|:---------|:--------------------------|:---------------|
| 🔴 Critical | Caller count + affected files + reproduction scenario | "Looks wrong", "might crash" |
| 🟡 Major | Trigger conditions + what state leads to the bug | "Could be a problem" |
| 🔵 Minor | Brief explanation of why current code is suboptimal | "I prefer it differently" |

## Investigation Protocol

```
BEFORE adding any // REVIEW: comment:

1. IDENTIFY: What evidence proves this is a real issue?
2. SEARCH: grep/LSP for callers, subscribers, state mutations
3. TRACE: Follow the data flow — can this state actually occur?
4. VERIFY: Does evidence confirm the issue is real, not theoretical?
   - If NO: Don't comment. Move on.
   - If YES: Write comment with evidence inline.
```

## Investigation Commands

```bash
# Count callers of a method
grep -rn "MethodName\s*(" Assets/Scripts/ --include="*.cs" | wc -l

# Find all state mutations
grep -rn "_fieldName\s*=" Assets/Scripts/ --include="*.cs"

# Find event subscribers
grep -rn "EventName\s*[+-]=" Assets/Scripts/ --include="*.cs"

# Check if null guard exists anywhere in call chain
grep -rn "MethodName" Assets/Scripts/ --include="*.cs" | grep -E "null|==\s*null|\?\."
```

## Cross-File Verification

| What to Verify | How | Why |
|:---------------|:----|:----|
| All callers handle new exception | grep for method name + check try/catch | API contract changed |
| Serialized field rename handled | grep for FormerlySerializedAs | Prefab data loss |
| Event subscribers updated | grep for event += and -= | Missing notification |
| Interface implementation complete | LSP find implementations | Abstract contract |
| Enum switch exhaustive | grep for switch + enum type | Missing case |

## False Positive Detection

- Pattern exists but wrapped in `#if UNITY_EDITOR` -> not a runtime issue, downgrade
- Pattern exists but class has `[ExecuteInEditMode]` -> may be intentional
- GetComponent in method called from Awake/Start only -> not a hot path issue
- Allocation in method behind feature flag / `#if DEBUG` -> not shipped
- Null reference pattern but field has `[RequireComponent]` on the class -> guaranteed present

## Red Flags — Don't Comment

- Pattern is theoretical only — no real caller triggers it
- Issue exists but is already guarded elsewhere in the call chain
- "Best practice" violation with zero practical impact in this codebase
- Style preference disguised as logic issue

## When to Upgrade Severity

| Situation | Upgrade to |
|:----------|:-----------|
| Bug affects serialized data (saves, configs, network) | 🔴 — data corruption |
| Bug only triggers in editor, not runtime | Downgrade to 🔵 |
| Bug affects 10+ callers | 🔴 — wide blast radius |
| Bug requires specific rare state to trigger | Keep at 🟡, note rarity |

If a pattern would be 🔴 but the project has an established convention/wrapper that handles it (e.g., a SafeGetComponent wrapper, event bus with auto-cleanup), downgrade to 🔵 and note the convention.

# Verification Gates

No completion claims without fresh verification evidence. Evidence before claims, always.

## The Iron Law

```
NO STATUS CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this review, you cannot claim it passes.

## Gate Protocol

```
BEFORE claiming any status:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Verification Requirements

| Claim | Required Evidence | NOT Sufficient |
|:------|:------------------|:---------------|
| "Tests pass" | Test output: 0 failures | Previous run, "should pass" |
| "Build succeeds" | Build command: exit 0 | Linter passing, "looks good" |
| "No compile errors" | Compiler output: 0 errors | "Code looks correct" |
| "Bug fixed" | Test original symptom: passes | "Code changed, assumed fixed" |
| "No regressions" | Full test suite: all green | Spot check of changed files |
| "Requirements met" | Line-by-line checklist verified | "Tests passing" |

## Pre-Commit Verification Checklist

Run these in order before declaring "ready to commit":

### 1. Compile Check
```bash
# Unity project — check for compile errors
# If Unity is open, check console. Otherwise:
dotnet build <project>.csproj 2>&1 | tail -20
```
Evidence: exit code 0, zero errors.

### 2. Test Suite (if exists)
```bash
# Run Unity tests via command line
unity -runTests -testPlatform EditMode -projectPath . -testResults /tmp/test-results.xml
# Or via dotnet
dotnet test
```
Evidence: test output shows 0 failures.

### 3. Diff Sanity Check
```bash
git diff --stat          # verify only intended files changed
git diff --cached --stat # verify staging area matches intent
```
Evidence: no unexpected files, no debug artifacts (`.log`, `.tmp`, `*.bak`).

### 4. Asset Integrity (if prefabs/assets changed)
```bash
# Check for broken references
grep -rn "m_Script: {fileID: 0}" $(git diff --name-only | grep -E '\.(prefab|unity)$')
# Check for missing shaders
grep -rn "m_Shader: {fileID: 0}" $(git diff --name-only | grep -E '\.(mat|asset)$')
```
Evidence: zero matches on broken patterns.

## Red Flags — STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Done!", "Fixed!", "Ready!")
- About to commit without running checks
- Trusting agent reports without independent verification
- Relying on partial verification
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|:-------|:--------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Code looks correct" | Visual inspection ≠ execution |

## Evidence Reporting Format

When reporting verification results in the review:

```markdown
### Verification
- **Compile**: ✅ exit 0 (0 errors, 0 warnings)
- **Tests**: ✅ 42/42 passed (EditMode)
- **Diff check**: ✅ 3 files changed, all intended
- **Asset integrity**: ✅ no broken refs found
```

Or if issues found:

```markdown
### Verification
- **Compile**: ❌ 2 errors in PlayerController.cs (see Critical findings)
- **Tests**: ⚠️ 40/42 passed, 2 failures (see Major findings)
- **Diff check**: ⚠️ unexpected file: debug.log (remove before commit)
```

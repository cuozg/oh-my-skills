# Debug Report: [Error Name/Type]

## 1. Incident Summary
- **Timestamp**: [Current Time]
- **Severity**: [Critical/Major/Minor]
- **Target Script**: `[FilePath.cs]`
- **Error Message**: `[Exact Error Message]`

## 2. Console Intel
### Stack Trace
```text
[Paste Stack Trace Here]
```

### Frequency
- [ ] Single Occurrence
- [ ] Reproducible on [Action]
- [ ] Constant (Blocking)

## 3. Analysis & Root Cause
- **Suspected Logic**: [Explanation of failing code]
- **Dependencies**: [Objects or components involved]
- **Hypothesis**: Why is this happening? (e.g., Null reference, Race condition, Missing component).

## 4. Proposed Fixes
### Primary Solution
```csharp
// Proposed code fix
```

### Alternatives/Workarounds
- [ ] [Workaround 1]

## 5. Verification Steps
1. [ ] Apply fix to [Script]
2. [ ] Trigger [Reproduction Steps]
3. [ ] Verify console is clear using `read_console`

## 6. Prevention Suggestions
- [ ] Add null guards to [Class]
- [ ] Improve event unsubscription logic
- [ ] Optimize [Method] for better performance

# Response Template

Every response uses this exact tree structure. No alternative formats. No prose before or after.

```
🔴 {Issue Title}
│
│ {1-2 sentences: what is wrong, where, what the user observes. Cite File.cs:L##.}
│
├── impact
│   ├── {AffectedSystem} — {how it is affected}
│   ├── {AffectedSystem} — {how it is affected}
│   └── severity: CRITICAL | HIGH | MEDIUM | LOW — {1 sentence justification}
│
├── root cause
│   │ {2-4 sentences: WHY it happens — not surface symptoms.
│   │  Trace to origin. Every claim cites File.cs:L##.}
│   │
│   ├── flow
│   │   ├── 1. Class.Method (File.cs:L##) — {what happens}
│   │   ├── 2. Class.Method (File.cs:L##) — {what happens}
│   │   └── 3. Class.Method (File.cs:L##) — {failure point}
│   │
│   └── repro
│       ├── 1. {concrete step}
│       ├── 2. {concrete step}
│       └── 3. observe: {symptom}
│
├── solutions
│   ├── ✅ {Title} [RECOMMENDED]
│   │   ├── approach: {1-2 sentences}
│   │   ├── where: File.cs:L## — {method/area}
│   │   ├── trade-off: {pros and cons}
│   │   └── effort: SMALL | MEDIUM | LARGE
│   │
│   ├── {Title}
│   │   ├── approach: {1-2 sentences}
│   │   ├── where: File.cs:L##
│   │   ├── trade-off: {pros and cons}
│   │   └── effort: SMALL | MEDIUM | LARGE
│   │
│   └── workaround: {temporary bypass, or "none — root cause must be fixed"}
│
├── verify
│   ├── 1. {apply solution}
│   ├── 2. {trigger the scenario}
│   └── 3. {confirm expected behavior}
│
└── prevent
    ├── {actionable practice}
    └── {actionable practice}
```

## Rules

- **Minimum 2 solutions**, maximum 4. Mark exactly one `✅ [RECOMMENDED]`.
- **Cite `File.cs:L##`** for every claim in root cause and solution `where`.
- **Execution flow**: 2-8 steps from trigger to failure.
- **Repro steps**: concrete, not vague. Minimum 2 steps.
- **Verify**: minimum 2 steps confirming the fix works.
- **Prevent**: 1-3 actionable practices, not generic advice.
- **Solutions describe approach and location** — no code. That is `unity-debug-fix`'s job.
- **No narration** before or after the tree. Just the tree.

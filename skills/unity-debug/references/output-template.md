# Unity Debug Output Template

Use this template for all debug reports. Keep it compact and evidence-first.

```markdown
# 🐞 Debug Report: <issue title>

## 🚦 Severity

- 🔴 **Critical:** blocks play/build, data loss, crash, or severe regression
- 🟠 **High:** major feature broken, frequent failure, no safe workaround
- 🟡 **Medium:** partial breakage, limited frequency, workaround exists
- 🟢 **Low:** minor issue, polish, rare edge case

Selected severity: <🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low>

## 🔍 Explain

- **Current:** <what happens now>
- **Expected:** <what should happen>
- **Signal:** <key error, log, visual symptom, or failing state>

## 🎯 Impact

- **Affected:** <player, designer, build, scene, prefab, system>
- **Frequency:** <always / often / rare / condition-specific>
- **Risk:** <crash / broken flow / data issue / UX confusion / tech debt>

## 🧠 Root Cause

- **Cause:** <proven cause>
- **Proof:** `<file/path:line>` <specific evidence>
- **Why now:** <triggering condition or recent change, if known>

## 🌳 Flow

```text
Flow
├─ Input / trigger
│  └─ <event, user action, scene load, API callback>
├─ Data / state path
│  ├─ <source value or object>
│  ├─ <transformation or state change>
│  └─ <unexpected value or missing state>
├─ Logic path
│  ├─ <entry method>
│  ├─ <branch / condition>
│  └─ <wrong branch, skipped call, or invalid assumption>
└─ Failure point 🔴
   └─ `<file/path:line>` <exact failing behavior>
```

## 🧪 Reproduce

```text
Reproduce
├─ Setup
│  ├─ <Unity version / scene / prefab / data condition>
│  └─ <required editor or runtime state>
├─ Steps
│  ├─ 1. <first action>
│  ├─ 2. <second action>
│  └─ 3. <trigger failure>
├─ Expected 🟢
│  └─ <expected result>
└─ Actual 🔴
   └─ <actual result, log, or broken state>
```

## 🛠️ Solutions

```text
Solutions
├─ Option 1 — 🟢 Minimal fix
│  ├─ approach: <smallest safe code/config change>
│  ├─ where to fix: <file/path or system area>
│  ├─ scope: <touched files/systems>
│  ├─ verify: <test/editor check proving fix>
│  └─ trade-off: <risk, effort, downside>
├─ Option 2 — 🟡 Safer structural fix
│  ├─ approach: <alternative with better robustness>
│  ├─ where to fix: <file/path or system area>
│  ├─ scope: <touched files/systems>
│  ├─ verify: <test/editor check proving fix>
│  └─ trade-off: <risk, effort, downside>
└─ Option 3 — 🟠 Broader fix, only if justified
   ├─ approach: <system-level correction>
   ├─ where to fix: <file/path or system area>
   ├─ scope: <touched files/systems>
   ├─ verify: <test/editor check proving fix>
   └─ trade-off: <risk, effort, downside>
```

Recommended: <Option 1/2/3> because <short reason>.

## ✅ Verify

- 🧪 **Automated:** <unit/Edit Mode/Play Mode test or compile check>
- 🎮 **Unity Editor:** <scene, prefab, Play Mode, inspector, console check>
- 🔁 **Regression:** <nearby behavior that must still work>

## 🛡️ Prevent

- <guardrail, test, assertion, validation, logging, or process change>
```

Rules:
- Use icons to mark issue type, severity, evidence, fix, and verification.
- Use colored severity icons consistently: 🔴 critical/failure, 🟠 high-risk, 🟡 caution, 🟢 good/pass, 🔵 evidence/info.
- Start with the focus strip so the user can identify the issue immediately.
- Keep each section compact: 1 to 3 bullets unless evidence requires more.
- Use tree format for `Flow`, `Reproduce`, and `Solutions`.
- Include 2 to 3 solution options.
- Each solution must include `approach`, `where to fix`, `scope`, `verify`, and `trade-off`.
- Report only after the root cause is proven with cited evidence.

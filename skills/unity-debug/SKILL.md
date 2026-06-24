---
name: unity-debug
description: Diagnose Unity bugs from compile errors to stack traces, runtime failures, and tricky logic issues; gather reproduction details, trace the code path, prove the root cause with evidence, and report options without changing code unless asked.
metadata:
  author: kuozg
  version: "3.0"
---

# unity-debug

Use this skill for Unity debugging, diagnosis, and root-cause analysis.

Keep it compact and structured. Focus on evidence and actionable solutions. Avoid unnecessary prose.

*** MANDATORY: Use `references/output-template.md` for debug reports. Follow the structure and icon guidelines strictly. ***

## Workflow

### 1. Capture the issue.
   - Issue title or symptom
   - Current behavior vs expected behavior
   - Key signal: compile error, stack trace, log, visual symptom, or failing state
   - Affected scene, prefab, system, build target, or user path
   - Scope — single script, system interaction, or timing?
   - Check git log -5 for recent changes.
   - Reproduction steps and frequency
### 2. If required debug inputs are missing, ask only for the missing evidence. Do not assume.
### 3. Understand the codebase.
   - Spawn an explorer subagent to read related code when tracing needs more than 3 searches
   - Spawn another explorer only if docs, references, or package behavior are needed
### 4. Investigate the flow.
   - Trace input/trigger, data/state path, logic path, and failure point
   - Read only the code needed to prove the cause
   - Cite file paths and line numbers for every key claim
### 5. Prove the root cause.
   - Identify the cause, proof, and why-now trigger when known
   - Assign severity using `references/output-template.md`
   - Report uncertainty explicitly if proof is incomplete
### 6. Propose 2 to 3 solutions.
   - Each solution must include approach, where to fix, scope, verify, and trade-off
   - Prefer minimal fix first, then structural alternatives only when useful
   - Recommend one option with a short reason
### 7. Report the result using `references/output-template.md`.
   - Include Severity, Explain, Impact, Root Cause, Flow, Reproduce, Solutions, Verify, and Prevent sections
   - Use tree format for Flow, Reproduce, and Solutions
   - Keep each section compact: 1 to 3 bullets unless evidence requires more
   - Do not report a final root cause until it is proven with cited evidence

## Investigation Rules

- Never apply a fix unless the user asks for it.
- Never guess the root cause.
- If the root cause is not proven after 2 to 3 tries, stop and report what you found.
- Keep evidence concrete: file paths, lines, logs, stack traces, or repro steps.
- Prefer minimal, targeted reads over broad exploration.
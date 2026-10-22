---
name: unity-debug
description: Diagnose Unity bugs from compile errors to stack traces, runtime failures, and tricky logic issues; reproduce with unity-validate, trace the code path, prove the root cause with evidence, report options, and verify any applied fix with unity-validate.
metadata:
  author: kuozg
  version: "3.2"
---

# unity-debug

Use this skill for Unity debugging, diagnosis, and root-cause analysis.

Keep it compact and structured. Focus on evidence and actionable solutions. Avoid unnecessary prose.

*** MANDATORY: Use `references/output-template.md` for debug reports. Follow the structure and icon guidelines strictly. ***

*** MANDATORY: Every bug goes through skill `unity-validate` twice: **reproduce** before tracing (step 1), and **verify fix** after any fix (step 8). The `Docs/Validations/<bug>.md` report is the evidence for both. ***

## Workflow

### 1. Capture the issue.
   - Issue title or symptom
   - Current behavior vs expected behavior
   - Key signal: compile error, stack trace, log, visual symptom, or failing state
   - Affected scene, prefab, system, build target, or user path
   - Scope — single script, system interaction, or timing?
   - Check `git log -5` for recent changes.
   - Pull live evidence via `../unity-standards/references/other/unity-cli-routing.md`: Unity version, console errors/stack traces (`unity command` console/log route, else `grep` on `<project>/Logs/Editor.log`), and Safe Mode (`unity pipeline list --format json`) for "Editor won't connect / compile" symptoms.
   - Reproduction steps and frequency
   - Reproduce before tracing: dispatch a fresh subagent with skill `unity-validate` (bug: reproduce), compile errors included. It writes `Docs/Validations/<bug>.md`; link that file in the Reproduce section. `🔴 Reproduced` gives the evidence and the method; on `⚪ Not reproduced`, stop and ask the user for more detail.
   - **Done when:** the validation report exists with verdict `🔴 Reproduced`. Tracing starts only after this gate.
### 2. If required debug inputs are missing, ask only for the missing evidence. Do not assume.
### 3. Understand the codebase.
   - Spawn an `Explore` subagent to read related code when tracing needs more than 3 searches
   - Spawn another `Explore` subagent only if docs, references, or package behavior are needed
### 4. Investigate the flow.
   - Trace input/trigger, data/state path, logic path, and failure point
   - Read only the code needed to prove the cause
   - Cite file paths and line numbers for every key claim
   - When a live Editor is reachable, confirm runtime state with read-only probes (`get_scene_hierarchy`, `find_gameobjects`, small read-only `eval`) instead of inferring it from YAML
   - Need runtime values? Hand off to `unity-log` for targeted `[DBG]` snippets
### 5. Prove the root cause.
   - Identify the cause, proof, and why-now trigger when known
   - Assign severity using `references/output-template.md`
   - Report uncertainty explicitly if proof is incomplete
### 6. Propose 2 to 3 solutions.
   - Each solution must include approach, where to fix, scope, verify, and trade-off
   - Verify = after a fix is applied, dispatch `unity-validate` (bug: verify fix) on the same `Docs/Validations/<bug>.md`. It reruns the same method → `🟢 Fixed`
   - Prefer minimal fix first, then structural alternatives only when useful
   - Recommend one option with a short reason
### 7. Report the result using `references/output-template.md`.
   - Include Severity, Explain, Impact, Root Cause, Flow, Reproduce, Solutions, Verify, and Prevent sections
   - Use tree format for Flow, Reproduce, and Solutions
   - Keep each section compact: 1 to 3 bullets unless evidence requires more
   - Do not report a final root cause until it is proven with cited evidence
### 8. Verify the fix (whenever a fix is applied).
   - Applies when the user asks you to fix, or tells you they applied a fix.
   - After the fix compiles, dispatch a fresh subagent with skill `unity-validate` (bug: verify fix) on the same `Docs/Validations/<bug>.md`. It reruns the recorded repro method plus regression cases.
   - `🟢 Fixed` → report the fix done, with the verdict and report path in the Verify section.
   - `❌ Still reproduces` → return to step 4 with the new evidence; the fix is not done.
   - **Done when:** the validation report shows `🟢 Fixed`. Claim a fix only on that verdict.

## Investigation Rules

- Never apply a fix unless the user asks for it.
- Never guess the root cause.
- If the root cause is not proven after 2 to 3 tries, stop and report what you found.
- Keep evidence concrete: file paths, lines, logs, stack traces, or repro steps.
- Prefer minimal, targeted reads over broad exploration.
- Read-only Editor probes are evidence gathering, not fixes; mutate scenes/assets only when asked to fix.

## References

Read from `../unity-standards/references/debug/` as the symptom requires:
- `diagnosis-workflow.md` — triage order and hypothesis loop
- `compile-verification.md` — compile error formats, CS codes, Safe Mode
- `common-unity-errors.md` — known Unity 6 error patterns
- `deep-investigation-checklist.md` — multi-system or timing bugs
- `ecs-burst-debugging.md` — Entities/Jobs/Burst failures

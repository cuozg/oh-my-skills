# Unity Technical Solution Template

Use this structure for Unity technical approach documents. Keep the writing practical, evidence-backed, and decision-ready.

```markdown
# Technical Solution: <feature / problem / goal>

## 1. Shared Understanding

- **Goal:** <what the user wants to achieve>
- **Problem / Opportunity:** <why this work matters>
- **In Scope:** <systems, platforms, features, content, workflows included>
- **Out of Scope:** <explicit exclusions>
- **Success Criteria:** <observable acceptance criteria>
- **Assumptions:** <assumptions that must be true>

## 2. Evidence Reviewed

- **User inputs:** <docs, specs, images, logs, notes reviewed>
- **Codebase evidence:** `<file:line>` — <what this proves>
- **Unity / package evidence:** <official docs, package docs, best practice, version constraints>
- **Existing patterns:** <project conventions to follow>

## 3. Clarifying Decisions

| Decision | Recommended Answer | Alternatives | Why It Matters |
|---|---|---|---|
| <question> | <preferred answer> | <other answers> | <impact on design> |

## 4. Solution Options

### Option A — 80/20 Minimal Path

- **Approach:** <smallest shippable technical path>
- **Best for:** <when to choose it>
- **Tradeoffs:** <limitations and risks>
- **Estimated effort:** <XS/S/M/L/XL or concrete range>

### Option B — Recommended Path

- **Approach:** <preferred architecture / workflow>
- **Best for:** <why this fits the goal>
- **Tradeoffs:** <costs, risks, complexity>
- **Estimated effort:** <XS/S/M/L/XL or concrete range>

### Option C — Strategic / Scalable Path

- **Approach:** <larger investment, if justified>
- **Best for:** <future scale or high-risk contexts>
- **Tradeoffs:** <why not choose this by default>
- **Estimated effort:** <XS/S/M/L/XL or concrete range>

## 5. Preferred Approach

- **Recommendation:** <Option A/B/C>
- **Why:** <technical reasoning and user-value reasoning>
- **Why not the others:** <short comparison>
- **80/20 call:** <what to do first if speed matters>

## 6. Technical Design

- **Architecture:** <major components and responsibilities>
- **Runtime flow:** <initialization, update loop, events, data flow>
- **Editor / content workflow:** <designer or tool workflow, if relevant>
- **Data model:** <ScriptableObjects, prefabs, serialized data, save data, remote config, etc.>
- **Integration points:** <scene, prefab, package, SDK, platform, build pipeline>
- **Performance constraints:** <CPU, GC, memory, rendering, loading, WebGL/mobile limits>
- **Security / safety constraints:** <untrusted data, permissions, privacy, destructive editor actions>

## 7. Implementation Plan

1. <step> — touches `<file/system>` — verify with <test/check>
2. <step> — touches `<file/system>` — verify with <test/check>
3. <step> — touches `<file/system>` — verify with <test/check>

## 8. Verification Plan

- **Unit tests:** <EditMode / PlayMode tests>
- **Integration tests:** <scene, prefab, package, service checks>
- **Manual QA:** <Unity Editor or build steps>
- **Regression risks:** <what could break and how to catch it>

## 9. Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|
| <risk> | <impact> | <low/med/high> | <mitigation> |

## 10. Open Questions

- <question with recommended answer and alternatives>
```

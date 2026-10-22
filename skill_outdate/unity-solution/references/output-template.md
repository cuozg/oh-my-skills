# Unity Solution Output Template

Two sections — use the one that matches the detected mode.

---

## Mode A — Design Solution (user provided goal only)

```markdown
# Solution: <feature / problem / goal>

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

## 9. Risks & Concerns

| Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|
| <risk> | <impact> | <low/med/high> | <mitigation> |

## 10. Open Questions

- <question with recommended answer and alternatives>
```

---

## Mode B — Evaluate Solution (user provided goal + approach)

```markdown
# Solution Review: <feature / problem / goal>

## 1. Verdict

> ✅ Approve  /  🟡 Approve with conditions  /  🔴 Reject

**One-line summary:** <single-sentence verdict>

**Top blocker (if any):** <the single most important issue, or "none">

## 2. Solution as Proposed

- **Goal:** <user's stated goal, paraphrased>
- **Proposed approach:** <user's proposed solution, paraphrased in your own words>
- **Components:** <the parts named by the user>
- **Data flow:** <how data moves through the proposed system>
- **Lifecycle:** <initialization / update / teardown as proposed>
- **Integration points:** <files, packages, scenes, prefabs, SDKs the user names>

## 3. Strengths

- <thing the proposed solution gets right, with evidence>
- <another strength>

## 4. Findings by Dimension

Group findings by the dimension. Within each dimension, sort by severity (🔴 → 🟠 → 🟡 → 🔵).

### 4.1 Correctness

- 🟠 <finding> — evidence: `<file:line>` or <Unity doc / package doc / spec section>
- 🔵 <finding> — evidence: ...

### 4.2 Unity Fit

- ...

### 4.3 Performance

- ...

### 4.4 Lifecycle & Safety

- ...

### 4.5 Architecture

- ...

### 4.6 Risk & Migration

- ...

### 4.7 Standards Compliance

- Reference `unity-standards` for normative checks.
- ...

## 5. Unknowns vs Risks vs Blocks

| Type | Item | Action |
|---|---|---|
| Unknown | <needs investigation> | <who / how to verify> |
| Risk | <could become a problem> | <mitigation> |
| Block | <must change before implementation> | <required change> |

## 6. Proposed Improvements

For each 🟠 or 🔴 finding:

- **Current:** <what the user proposed>
- **Proposed:** <concrete alternative>
- **Why:** <reasoning with evidence>

## 7. Revised Recommendation (if not Approve)

- **If 🟡 Approve with conditions:** list the conditions that must be addressed before / during
  implementation.
- **If 🔴 Reject:** summarize the rework needed and the smallest viable next step.

## 8. Open Questions for the User

- <question that affects the verdict, with recommended answer>
```

---

## Usage Notes

- In Mode A, the document **designs** a solution. Implementation comes later, only on request.
- In Mode B, the document **evaluates** a solution. Lead with the verdict; do not bury it.
- Both modes use the same Evidence Reviewed / Clarifying Decisions rigor — evaluation without
  evidence is opinion, not review.
```
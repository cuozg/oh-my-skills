---
name: unity-costing
description: >
  Create tshirt costing, detail costing, highlevel costing, feature costing, task breakdown, estimate, effort sizing, or a detailed
  Unity delivery plan before implementation. Use for small-to-XL Unity work when a costed task tree is the deliverable;
  investigate the codebase first and fire subagents when scope touches multiple systems or evidence is needed.
metadata:
  author: kuozg
  version: "4.0"
---
# unity-costing

Produce a self-contained HTML costing report for a Unity feature/refactor. Answer "what will this cost?" — not "please implement this."
Supports: tshirt costing, detail costing, and highlevel costing.

**Pre-requisite:** Read `references/output-template.html`. Replace all `[PLACEHOLDER]` tokens exactly. Use predefined CSS badge classes. Maintain Vercel dark theme.

## Workflow

### 1. Clarify Requirements
Understand clearly the requirement. Do not assume. Ask user if: target platform, boundaries, quality bar, unknown SDKs, or estimate unit are unclear.

### 2. Investigate Context
Understand the code base and document context.
- Spawn `explore` or `librarian` subagents to gather evidence on:
  - Entry points, public APIs, module boundaries.
  - Cross-system dependencies (calls, shared state, events).
  - Existing patterns, test coverage, and performance-critical paths.
Record `file:line` evidence. Collect all results before scoping.

### 3. Analyze Scope & Sizing
- **Size Scale:** `XS` (1-2h, 1 file), `S` (2-4h, 1-3 files), `M` (4-16h, 3-10 files), `L` (16-40h, 10-25 files), `XL` (40+h, 25+ files).
- **Modifiers:** Bump +1 size if crossing assemblies, requiring data migration, or touching Editor+Runtime.
- **Confidence:** High (knowns), Med (some unknowns), Low (ambiguous territory).
- **BLOCKING:** If scope is ambiguous or confidence is Low, print a "🔍 SCOPE DETECTION" summary and stop for user confirmation before planning.

### 4. Architect & Technical Approach
- Spawn a subagent to define the architecture and technical approach (Current vs Proposed).
- Ensure numbered steps with `<code>` references are formulated.

### 5. Create Epics
- Group work into logical Epics: Foundation, Runtime Logic, UI/Scene, Data/Persistence, Assets, Tests/Release.

### 6. Create Tasks
- **Granularity:** 1-4h per task. Split >4h, merge <30m. One clear deliverable per task.
- **Format:** Subject starts with imperative verb. Description must have `{What}\n{Why}\n{How}\n→ skill:{name}`.
- **Dependencies:** Minimize chains. Use `blockedBy=[ID]` only for true data dependencies.
- **Tasks Data:** T-N ID, epic, title, 2-5 action steps, type, cost, affected files.
- **Types/Costs:** `Logic/UI/Data/API/Asset/Test/Config`. `S/M/L/XL/Spike`. Use predefined template badges.

### 7. Review Costing & Risks
- **Risk Levels:** `Low` (Accept), `Medium` (Monitor), `High` (Mitigate), `Critical` (Block/Spike).
- **Categories:** Technical, Integration, Performance, Data Migration, UX.
- **Mitigation:** Use spikes, feature flags, or rollback plans for High/Critical risks.
- Detail risks with severity (`badge-sev-high`), impact, and mitigations. Ensure backward compatibility is analyzed.

### 8. Generate Plan
Create directory: `mkdir -p Docs/Plans`
Generate `Docs/Plans/{Name}.html` using the template from `references/output-template.html`.
Report to user: Output location, total effort range, confidence level, top 2-3 risks, critical path.
**BLOCKING:** After generating the plan, print "❓ Next steps? 1. Create tasks 2. Adjust scope" and wait. **Do not execute or auto-create tasks.**

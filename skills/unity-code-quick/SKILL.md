---
name: unity-code-quick
description: "Fast Unity C# code generation. Receives a code request, generates production-ready C# following unity-code-shared, verifies with diagnostics. Other skills delegate code generation tasks here. Use when: (1) Generating a new MonoBehaviour, ScriptableObject, or plain C# class, (2) Implementing a method, interface, or data model, (3) Writing boilerplate code (events, state, services), (4) Quick code changes delegated from planning/debug/refactor skills, (5) Adding a feature to an existing script. Triggers: 'write code', 'generate class', 'create script', 'implement method', 'add feature', 'quick code', 'code this'."
---

# unity-code-quick — Fast Unity C# Code Generation

Generate production-ready Unity C# code fast. No lengthy investigation — receive request, match codebase conventions, write code, verify.

**Input**: Code request with context (what to create, where it goes, dependencies)
**Output**: C# code following `unity-code-shared`, zero compile errors

## References

| File | Purpose |
|------|---------|
| [workflow.md](references/workflow.md) | Orient → Generate → Verify steps, pattern table, quick rules, anti-patterns |
| [unity-code-shared](../unity-code-shared/SKILL.md) | Coding standards and quality gates (loaded during generation) |

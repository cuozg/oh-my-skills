---
name: unity-investigate-quick
description: "Quick investigation of Unity projects. Answers questions about how systems work with a short focused summary and 1-3 detailed explanations. No report document — direct conversational answers. Use when: (1) Quick question about how a feature works, (2) Understanding a class or method's purpose, (3) Tracing a call chain or data flow, (4) Finding where something is defined or used, (5) Understanding system dependencies, (6) Answering 'what does X do' or 'how does X work'. Triggers: 'how does X work', 'what does X do', 'explain this code', 'what calls this', 'investigate', 'where is X defined', 'how is X used', 'what triggers X', 'trace the flow', 'analyze this system'."
---
# Unity Quick Investigator

Answer the question. Nothing else.

## Output Format

Use the Vercel-themed tree template from `references/output-template.md` for every response. Tree connectors (`├──`, `└──`) for flow. Inline code (`cyan`) for all code identifiers, file refs, and values. **Bold** for labels. Emoji indicators for risk. No prose, no preamble — just the formatted tree.

## Workflow

Follow the 3-step workflow: Parse → Find → Reply.

## Reference Files
- [output-template.md](references/output-template.md) — Vercel-themed tree output format
- workflow.md — 3-step quick investigation workflow

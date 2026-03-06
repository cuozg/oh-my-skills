---
trigger: always_on
glob: Agent Behavior Rules
description: Core rules for AI agents working on oh-my-unity skill development
---

# oh-my-unity — Agent Rules

This project creates and maintains AI skills for Unity developers.
All work here is **skill authoring** — not game code.

## Skill Structure (mandatory)

```
skill-name/
├── SKILL.md          ← required, < 100 lines
├── scripts/          ← deterministic code, must have tests
├── references/       ← on-demand docs, < 100 lines each
└── assets/           ← templates/images, never loaded into context
```

## Hard Rules

```
├── SKILL.md
│   ├─ MUST be < 100 lines
│   ├─ YAML frontmatter: name (required), description (required)
│   ├─ Description: specific about WHAT it does + WHEN to use
│   ├─ Writing style: imperative/infinitive (verb-first, no "you")
│   ├─ Reference bundled resources — don't inline their content
│   └─ No duplication with reference files
│
├── References
│   ├─ Each file < 100 lines — split if larger
│   ├─ Practical instructions, not documentation
│   ├─ Can cross-reference other refs/scripts
│   ├─ Sacrifice grammar for concision
│   └─ ALWAYS check unity-standards first — if a ref fits there, add it
│       there instead of the skill folder (unity-standards is the hub)
│
├── Scripts
│   ├─ Prefer Python/Node over Bash (cross-platform)
│   ├─ MUST have tests — run until green
│   ├─ Include requirements.txt for Python
│   ├─ .env priority: process.env > skill/.env > skills/.env > .claude/.env
│   └─ No line limit, but must compile and run cleanly
│
└── Skills are INSTRUCTIONS, not documentation
    ├─ Teach HOW to perform tasks, not WHAT a tool is
    └─ Combine related topics (e.g., cloudflare-* → devops)
```
## Progressive Disclosure (core principle)

```
Level 1: Metadata (name + description)     ← always in context (~100 words)
Level 2: SKILL.md body                      ← loaded on skill trigger (<5k words)
Level 3: Bundled resources (refs/scripts)    ← loaded on-demand (unlimited)
```
Token budget drives everything. Keep SKILL.md lean → push details to references.

## Skill Creation Workflow

```
1. Understand    → gather concrete usage examples from user
2. Plan          → identify reusable scripts/refs/assets
3. Initialize    → run scripts/init_skill.py <name> --path <dir>
4. Edit          → write SKILL.md + resources
5. Validate      → run scripts/quick_validate.py or package_skill.py
6. Iterate       → use on real tasks → refine
```
## Validation Checklist (before done)

```
├── [ ] SKILL.md < 100 lines
├── [ ] All reference files < 100 lines
├── [ ] Scripts have tests and tests pass
├── [ ] Description covers what + when + triggers
├── [ ] No TODO/TBD left in SKILL.md
├── [ ] skill-validator passes
├── [ ] skill-deps passes (no broken refs)
└── [ ] No content duplicated between SKILL.md and references
```

## What NOT to Do

```
├── Write long prose in SKILL.md (keep it terse)
├── Inline reference content into SKILL.md
├── Skip tests for scripts
├── Use bash when Python/Node works
├── Leave example/placeholder files from init
├── Create overlapping skills (combine related topics)
├── Write "you should" — use imperative form
└── Automatically commit or push without explicit user request
```
## Project Context

```
├── skills/              ← all skills live here
├── tools/               ← MCP tools and analyzers
├── commands/            ← slash commands
└── agents/              ← agent persona configs
```

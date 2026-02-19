---
name: skill-creator
description: "Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends the agent's capabilities with specialized knowledge, workflows, or tool integrations."
---

# Skill Creator

## Input
Skill concept with concrete usage examples. Optional: existing skill folder, reference materials, scripts, assets.

## Output
Validated skill folder containing `SKILL.md` + optional `scripts/`, `references/`, `assets/`.
Optionally package into `.skill` zip via `package_skill.py` (only when user requests packaging).

## Skill Anatomy

```
skill-name/
├── SKILL.md              # Required: YAML frontmatter (name, description) + markdown body
├── scripts/              # Executable code for deterministic/repeated tasks
├── references/           # Docs loaded into context as needed
└── assets/               # Files used in output (templates, images, fonts)
```

**Frontmatter**: `name` + `description` only. Description is the primary trigger — include what the skill does AND when to use it.
**Body**: Loaded only after skill triggers. No "When to Use" sections here.
**Excluded files**: README.md, CHANGELOG.md, INSTALLATION_GUIDE.md — no auxiliary docs.

## Core Principles

1. **Concise** — Context window is shared. Only add what the agent doesn't know. Examples > explanations.
2. **Freedom matches fragility** — Fragile tasks → specific scripts. Flexible tasks → text guidance.
3. **Progressive disclosure** — Metadata always loaded (~100 words). SKILL.md on trigger (<5k words). References on demand.

### Resource Guidelines

| Resource | When to Use | Key Rule |
|:---|:---|:---|
| `scripts/` | Same code rewritten repeatedly; deterministic reliability | Test before packaging |
| `references/` | Domain knowledge needed while working | No duplication with SKILL.md; for large files (>10k words) add grep patterns |
| `assets/` | Templates, images, boilerplate for output | Not loaded into context |

### Progressive Disclosure Patterns

Keep SKILL.md under 500 lines. Reference files one level deep. For files >100 lines, add TOC.

- **Guide + references**: SKILL.md has quick start, links to detail files
- **Domain organization**: One reference file per domain/variant, load only what's needed
- **Conditional details**: Link to advanced content, load on demand

## Available MCP Tools

Use these native tools instead of calling scripts manually:

| Tool | Purpose |
|:---|:---|
| `skill-scaffold` | Create pre-populated skill directory (type-aware: unity/bash/git/other). **Preferred for new skills.** |
| `skill-scaffold-generator` | Generate domain-aware templates with skill type detection |
| `skill-validator` | Deep structural validation (frontmatter, body quality, references, naming). Supports `--fix` |
| `skill-deps` | Analyze dependencies and cross-skill references |
| `skill-finder` | Find best matching skill for a task description |

## Creating a New Skill

1. **Understand** — Gather concrete usage examples; ask targeted questions
2. **Plan** — Per example, identify reusable scripts, references, assets
3. **Initialize** — Use `skill-scaffold` MCP tool (preferred) or fallback `init_skill.py`:
   ```bash
   # Fallback only:
   python <skill-creator-dir>/scripts/init_skill.py <name> --path <dir>
   ```
4. **Edit** — Implement resources, write SKILL.md (imperative form)
   - Design patterns: load `references/workflows.md` and `references/output-patterns.md` via `read_skill_file`
   - Start with resources → update SKILL.md → test scripts → delete unused example files
5. **Validate** — Use `skill-validator` MCP tool to check structure
6. **Package** (only if requested) — Run `package_skill.py <folder> [output-dir]`
7. **Iterate** — Use on real tasks → notice gaps → update

## Updating an Existing Skill

1. **Load** — `use_skill` to read current SKILL.md into context
2. **Read resources** — `read_skill_file` for scripts, references, assets that need changes
3. **Edit** — Modify files directly at the skill's directory path
4. **Validate** — Use `skill-validator` MCP tool
5. **Package** (only if requested) — Run `package_skill.py`

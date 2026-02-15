---
name: skill-creator
description: "Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations."
---

# Skill Creator

## Input
Skill concept with concrete usage examples. Optional: existing skill folder, reference materials, scripts, assets.

## Output
Validated `.skill` package via `package_skill.py`. Contains `SKILL.md` + bundled `scripts/`, `references/`, `assets/`.

## Output Requirement (MANDATORY)
Run: `.opencode/skills/other/skill-creator/scripts/package_skill.py <path/to/skill-folder>`

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

1. **Concise** — Context window is shared. Only add what Claude doesn't know. Examples > explanations.
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

## Creation Process

1. **Understand** — Gather concrete usage examples; ask targeted questions
2. **Plan** — Per example, identify reusable scripts, references, assets
3. **Initialize** — Prefer `skill-scaffold` tool, fallback `init_skill.py`:
   ```bash
   python .opencode/tools/skill-scaffold.py <name> --type <unity|bash|git|other> --path <dir>
   # Fallback: .opencode/skills/other/skill-creator/scripts/init_skill.py <name> --path <dir>
   ```
4. **Edit** — Implement resources, write SKILL.md (imperative form)
   - Design patterns: [workflows.md](.opencode/skills/other/skill-creator/references/workflows.md), [output-patterns.md](.opencode/skills/other/skill-creator/references/output-patterns.md)
   - Start with resources → update SKILL.md → test scripts → delete unused example files
5. **Package**:
   ```bash
   python .opencode/tools/skill-validator.py <folder> [--fix] [--json]
   python .opencode/tools/skill-deps.py <folder> --skills-root .opencode/skills [--json]
   .opencode/skills/other/skill-creator/scripts/package_skill.py <folder> [output-dir]
   ```
   Validates frontmatter, structure, description quality. Creates `.skill` zip on success.
6. **Iterate** — Use on real tasks → notice gaps → update → re-package

---
name: omo-sisyphus
description: "Transparent pass-through proxy to Sisyphus. Use when: (1) You have pre-crafted prompts that need ZERO modification, (2) Testing specific prompt formulations, (3) Complex instructions with specific formatting, (4) Debugging exact Sisyphus responses, (5) Maximum control over what Sisyphus receives. Passes user input character-for-character to @sisyphus via delegate_task."
---

# Sisyphus Proxy

**Role**: Transparent pass-through proxy to Sisyphus  
**Tools**: delegate_task ONLY  
**Mode**: ZERO reasoning - just routing

---

## Purpose

This skill is a **pure proxy** that passes user prompts to Sisyphus **EXACTLY as-is** without any:
- ❌ Prompt optimization
- ❌ Context addition
- ❌ Interpretation or analysis
- ❌ Rewording or paraphrasing

---

## How It Works

```
User Message → omo-sisyphus → @sisyphus
      ↓              ↓              ↓
  "Build X"    No changes       "Build X"
```

Literally copy user input character-for-character to Sisyphus.

---

## Workflow

1. **Receive** - User provides prompt
2. **Delegate** - `@sisyphus <skill-name> <exact user prompt>`
3. **Return** - Pass Sisyphus response back to user

**DO NOT**:
- Add context or instructions
- Optimize or enhance the prompt
- Interpret what the user meant
- Add skill names or routing logic

---

## Session Continuity

Automatically maintain session continuity:

```
Message 1: "unity-review-pr https://github.com/xxx"
           → Delegate to @sisyphus
           → @sisyphus unity-review-pr https://github.com/xxx
           → Sisyphus returns result

Message 1: "Build auth system"
           → Delegate to @sisyphus
           → Sisyphus returns result

Message 2: "Add OAuth support"  
           → Delegate to @sisyphus (same session)
           → Sisyphus has FULL CONTEXT from Message 1
           → Continues seamlessly
```

---

## When to Use This Skill

✅ **Pre-crafted Prompts** - You've carefully crafted your prompt  
✅ **Testing Prompts** - Testing specific prompt formulations  
✅ **Complex Instructions** - Specific formatting that must be preserved  
✅ **Debugging** - See exactly how Sisyphus responds to exact input  
✅ **Maximum Control** - Full control over what Sisyphus receives

---

## When NOT to Use This Skill

❌ **Vague Requests** - Prompt would benefit from engineering  
❌ **New Users** - Other agents help optimize requests  
❌ **Need Skill Routing** - Use direct skill invocation instead

---

## Example Flow

```
User: Create a REST API for user management

omo-sisyphus: @sisyphus Create a REST API for user management
              ↑ EXACT copy, no modifications

Sisyphus: [Creates the API]

User: Add pagination to the list endpoint

omo-sisyphus: @sisyphus Add pagination to the list endpoint
              ↑ Same session, Sisyphus has full context

Sisyphus: [Adds pagination with context from previous turn]
```

---

## Technical Notes

- **Temperature: 0** - Deterministic routing behavior
- **Minimal Tools** - Only delegate_task to prevent side effects
- **Auto Session** - Automatically maintains session continuity
- **Zero Modification** - If prompt appears modified, it's a bug

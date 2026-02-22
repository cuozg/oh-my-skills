---
trigger: always_on

glob: Agent Behavior Rules

description: Core behavioral guidelines for AI agents in Unity projects.
---

##Core Values

1.**Safety First**: No destructive actions without explicit confirmation

2.**Proactive**: Always suggest next steps after completing tasks

3.**Unity Best Practices**: Follow Prefab workflows, ScriptableObjects, Component patterns

4.**Code Standards**: ALWAYS load `unity-code-standards` skill when writing, reviewing, or refactoring any C# code in Unity projects — this is MANDATORY and non-negotiable

5.**Forbidden Files**: NEVER read, open, or access `.env` or `.gitignore` files under any circumstances — this applies to ALL agents without exception

6.**No Git Commits or Pushes**: NEVER commit or push anything to GitHub/git repositories — no `git commit`, `git push`, `gh pr create`, or any equivalent operation — under any circumstances, even if explicitly asked

##Communication

-**Explain "Why"**: Especially for architectural decisions

-**Rich Formatting**: Use markdown, code snippets, clear structure

-**Question**: All task, subtask must ask as a Question, with suggestion options.

##Interaction Pattern

1.**Discover**: Explore project state before proposing changes

2.**Plan**: Break large tasks into verifiable steps

3.**Execute**: Provide point-by-point progress

4.**Collaborate**: Reference specialized skills when needed

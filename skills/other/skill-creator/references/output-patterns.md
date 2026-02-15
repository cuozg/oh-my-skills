# Output Patterns

## Template Pattern

Match strictness to needs:
- **Strict**: `ALWAYS use this exact template structure:` + template
- **Flexible**: `Sensible default format, use your best judgment:` + template + `Adjust as needed.`

## Examples Pattern

Provide input/output pairs when output quality depends on style:

```markdown
## Commit message format
**Example:** Input: Added user auth with JWT → Output: `feat(auth): implement JWT-based authentication`
Follow: type(scope): brief description, then detailed explanation.
```

Examples convey desired style better than descriptions alone.

# Bash Optimize — Workflow

## 1. Analyze Current Script
Understand purpose, functions, dependencies, complex/repeated patterns.

## 2. Apply Optimizations
Load [patterns.md](patterns.md) for specific optimization patterns:
- Performance — replace external commands with built-ins, avoid subshells, efficient loops
- Clarity — extract functions, descriptive names, simplify conditionals
- Modern bash — `[[ ]]`, `$(command)`, arrays
- Error handling — strict mode, traps, cleanup
- Documentation — script header with name, description, usage

## 3. Report Findings
Categorize changes by: Performance | Clarity | Safety | Style

## Optimization Checklist

| Category | Check |
|----------|-------|
| Performance | Replace external commands with built-ins, avoid subshells, efficient loops |
| Clarity | Extract functions, descriptive names, simplify conditionals |
| Safety | Strict mode, error handling |
| Style | Consistent indentation, comments for complex logic |

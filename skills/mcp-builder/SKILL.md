---
name: mcp-builder
description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
---
# MCP Server Development Guide

Create MCP servers enabling LLMs to accomplish real-world tasks through well-designed tools.

## Stack

- **Language**: TypeScript (preferred) or Python
- **Transport**: Streamable HTTP (remote/stateless) · stdio (local)
- **Validation**: Zod (TS) or Pydantic (Python)

## Workflow

### Phase 1 — Research & Plan

1. Study the MCP spec: start at `https://modelcontextprotocol.io/sitemap.xml`, fetch pages with `.md` suffix
2. Load framework docs:
   - TS SDK: `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
   - Python SDK: `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
3. Read `./reference/mcp_best_practices.md` — naming, response format, pagination, security
4. Review target service API: endpoints, auth, data models

### Phase 2 — Implement

1. Set up project — see `./reference/node_mcp_server.md` (TS) or `./reference/python_mcp_server.md` (Python)
2. Build shared utilities: API client + auth, error handling, response formatting, pagination
3. For each tool:
   - Input schema with Zod/Pydantic constraints and field descriptions
   - Output schema (`outputSchema` + `structuredContent` for TS SDK)
   - Concise description covering what it does, params, return type
   - Annotations: `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`
   - Async/await, pagination support, actionable error messages

### Phase 3 — Review & Test

1. Code quality: no duplication, consistent error handling, full types, clear descriptions
2. Build: `npm run build` (TS) or `python -m py_compile` (Python)
3. Test with MCP Inspector: `npx @modelcontextprotocol/inspector`

### Phase 4 — Evaluations

Load `./reference/evaluation.md` for full guidelines. Create 10 Q&A pairs:
- Tool inspection → content exploration (read-only) → generate questions → verify answers
- Each question: independent, read-only, complex (multi-tool), realistic, verifiable, stable

Output format:
```xml
<evaluation>
  <qa_pair><question>...</question><answer>...</answer></qa_pair>
</evaluation>
```

## Key Design Principles

- **Naming**: consistent prefix + action-oriented (`github_create_issue`, `github_list_repos`)
- **Coverage**: prioritize comprehensive API coverage over workflow shortcuts
- **Errors**: always actionable — tell the agent what to do next
- **Context**: return focused, relevant data; support filtering and pagination

## References

- `./reference/mcp_best_practices.md` — universal guidelines (load first)
- `./reference/node_mcp_server.md` — TypeScript patterns, examples, quality checklist
- `./reference/python_mcp_server.md` — Python/FastMCP patterns, examples, quality checklist
- `./reference/evaluation.md` — evaluation creation, XML format, running scripts

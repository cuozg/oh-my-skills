## Tool Selection

| Need              | Tool                          |
| :---------------- | :---------------------------- |
| Read target code  | `read`                        |
| Find definition   | `lsp_goto_definition`         |
| Who calls it      | `lsp_find_references`         |
| Find symbols      | `lsp_symbols` (workspace)     |
| Pattern search    | `grep` / `ast_grep_search`    |
| Blast radius      | `impact-analyzer`             |
| Broad sweep       | `glob`                        |
| Check diagnostics | `lsp_diagnostics`             |
| Delegate fix      | `task` (category + skills)    |

Chain tools to build evidence. Stop once root cause is clear.

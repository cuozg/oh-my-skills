import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
  description:
    "Analyze blast radius of a C# class or file. Traces all references (singleton access, inheritance, type usage) across Assets/Scripts/ and reports risk level. Use before modifying shared code to understand impact.",
  args: {
    target: tool.schema
      .string()
      .describe(
        "C# file path (relative to project root) or class name to analyze"
      ),
    depth: tool.schema
      .number()
      .optional()
      .describe(
        "Reference depth: 1 = direct only, 2 = direct + transitive (default: 1)"
      ),
    scope: tool.schema
      .string()
      .optional()
      .describe(
        "Subdirectory to scope search (relative to Assets/Scripts/). Defaults to all scripts."
      ),
  },
  async execute(args, context) {
    const scriptsDir = path.join(context.directory, "Assets/Scripts")
    const script = path.join(
      context.worktree,
      ".opencode/tools/impact-analyzer.py"
    )
    const cmdArgs = [script, args.target, scriptsDir]
    if (args.depth) {
      cmdArgs.push("--depth", String(args.depth))
    }
    if (args.scope) {
      cmdArgs.push("--scope", args.scope)
    }
    const result = await Bun.$`python3 ${cmdArgs}`.text()
    return result.trim()
  },
})

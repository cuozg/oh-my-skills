import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
  description:
    "Analyze Unity Editor console log output. Parse raw log text, classify errors/warnings/info, group duplicates, extract stack traces, and suggest likely fixes. Pipe Unity console output into this tool for structured analysis.",
  args: {
    logs: tool.schema
      .string()
      .describe(
        "Raw Unity console log text (paste from get_unity_logs output or console)"
      ),
    severity: tool.schema
      .enum(["all", "errors", "warnings"])
      .optional()
      .describe("Filter by severity level (default: all)"),
  },
  async execute(args, context) {
    const script = path.join(
      context.worktree,
      ".opencode/tools/unity-log-analyzer.py"
    )
    const severity = args.severity ?? "all"
    // Write logs to a temp file to avoid shell escaping issues
    const tmpFile = path.join(context.directory, ".opencode/tools/.tmp_logs.txt")
    await Bun.write(tmpFile, args.logs)
    try {
      const result =
        await Bun.$`python3 ${script} ${tmpFile} ${severity}`.text()
      return result.trim()
    } finally {
      // Clean up
      try {
        await Bun.$`rm -f ${tmpFile}`
      } catch {}
    }
  },
})

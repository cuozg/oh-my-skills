import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
  description:
    "Analyze skill dependencies and integration points. Builds a dependency graph showing script imports, cross-skill references, file references, and missing dependencies. Use before packaging to catch broken references or after editing to verify integrity.",
  args: {
    skill_path: tool.schema
      .string()
      .describe("Path to the skill directory to analyze (e.g., '.opencode/skills/unity/unity-code')"),
    skills_root: tool.schema
      .string()
      .optional()
      .describe("Root skills directory for cross-skill validation (e.g., '.opencode/skills')"),
    json: tool.schema
      .boolean()
      .optional()
      .describe("Output results as JSON instead of human-readable text"),
  },
  async execute(args, context) {
    const script = path.join(
      context.worktree,
      ".opencode/tools/skill-deps.py"
    )
    const skillDir = path.isAbsolute(args.skill_path)
      ? args.skill_path
      : path.join(context.worktree, args.skill_path)

    const flags: string[] = [skillDir]
    if (args.skills_root) {
      const root = path.isAbsolute(args.skills_root)
        ? args.skills_root
        : path.join(context.worktree, args.skills_root)
      flags.push("--skills-root", root)
    }
    if (args.json) flags.push("--json")

    try {
      const result =
        await Bun.$`python3 ${script} ${flags}`.text()
      return result.trim()
    } catch (e: any) {
      if (e?.stdout) return e.stdout.toString().trim()
      if (e?.stderr) return `Error: ${e.stderr.toString().trim()}`
      return `Error: ${e?.message ?? String(e)}`
    }
  },
})

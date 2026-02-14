import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
  description:
    "Generate domain-aware skill scaffolds. Creates tailored SKILL.md templates based on skill type (workflow, tool, reference, integration) with pre-populated sections and resource directories. Use when creating a new skill to get a better starting point than the generic init_skill.py template.",
  args: {
    skill_name: tool.schema
      .string()
      .describe("Hyphen-case skill name (e.g., 'pdf-editor', 'deploy-checker')"),
    type: tool.schema
      .string()
      .optional()
      .describe(
        "Scaffold type: 'workflow' (multi-step processes), 'tool' (utilities), 'reference' (knowledge/guidelines), 'integration' (external APIs). Defaults to 'tool'."
      ),
    output_path: tool.schema
      .string()
      .optional()
      .describe("Directory to create the skill in. Defaults to '.opencode/skills/other'"),
    list: tool.schema
      .boolean()
      .optional()
      .describe("List available scaffold types with their sections"),
  },
  async execute(args, context) {
    const script = path.join(
      context.worktree,
      ".opencode/tools/skill-scaffold-generator.py"
    )

    if (args.list) {
      try {
        const result = await Bun.$`python3 ${script} --list`.text()
        return result.trim()
      } catch (e: any) {
        if (e?.stdout) return e.stdout.toString().trim()
        if (e?.stderr) return `Error: ${e.stderr.toString().trim()}`
        return `Error: ${e?.message ?? String(e)}`
      }
    }

    const outputDir = args.output_path
      ? path.isAbsolute(args.output_path)
        ? args.output_path
        : path.join(context.worktree, args.output_path)
      : path.join(context.worktree, ".opencode/skills/other")

    const skillType = args.type || "tool"

    try {
      const result =
        await Bun.$`python3 ${script} ${args.skill_name} --type ${skillType} --path ${outputDir}`.text()
      return result.trim()
    } catch (e: any) {
      if (e?.stdout) return e.stdout.toString().trim()
      if (e?.stderr) return `Error: ${e.stderr.toString().trim()}`
      return `Error: ${e?.message ?? String(e)}`
    }
  },
})

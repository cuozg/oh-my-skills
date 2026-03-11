---
name: "imagegen"
description: >
  Use this skill when the user asks to generate or edit images — concept art, product shots, covers,
  icons, or batch variants. Covers generation from text prompts, editing existing images (inpainting,
  masking, style transfer), background removal or replacement, and transparent backgrounds. Use it even
  when the user says "make me a picture" or "create an icon" without mentioning the API. Runs the bundled
  CLI (scripts/image_gen.py) and requires OPENAI_API_KEY.
---

# Image Generation Skill

Generates or edits images for the current project using OpenAI's Image API. Defaults to `gpt-image-1.5` and the bundled CLI (`scripts/image_gen.py`) for deterministic, reproducible runs.

## When to use
- Generate a new image (concept art, product shot, cover, website hero)
- Edit an existing image (inpainting, masked edits, background replacement, object removal, style transfer, transparent background)
- Batch runs (many prompts or variants across prompts)

## Decision tree (generate vs edit vs batch)
- If the user provides an input image (or says "edit/retouch/inpaint/mask/translate/change only X") → **edit**
- Else if the user needs many different prompts/assets → **generate-batch**
- Else → **generate**

## Workflow
1. Decide intent: generate vs edit vs batch (decision tree above).
2. Collect inputs up front: prompt(s), exact text (verbatim), constraints/avoid list, and any input image(s)/mask(s).
3. If batch: write temporary JSONL under `tmp/imagegen/` (one job per line), run once, then delete it.
4. Augment prompt into a structured spec (see `references/prompt-augmentation.md`) without inventing new creative requirements.
5. Run bundled CLI: `python $IMAGE_GEN <command> <args>` (see `references/cli.md` for recipes).
6. For complex edits/generations, inspect outputs and validate: subject, style, composition, text accuracy, and invariants/avoid items.
7. Iterate: make a single targeted change (prompt or mask), re-run, re-check.
8. Save/return final outputs and note the final prompt + flags used.

## Temp and output conventions
- Use `tmp/imagegen/` for intermediate files (JSONL batches); delete when done.
- Write final artifacts under `output/imagegen/` when working in this repo.
- Use `--out` or `--out-dir` to control output paths; keep filenames stable and descriptive.

## Dependencies
Python packages (prefer `uv`):
```
uv pip install openai pillow
```
Or with pip:
```
python3 -m pip install openai pillow
```

## Environment
- **`OPENAI_API_KEY`** required for live API calls (no API key = dry-run only).
- If missing: user creates key at https://platform.openai.com/api-keys and sets it locally.
- Never ask user to paste the key; ask them to set it as an environment variable and confirm when ready.

## Defaults & rules
- Model: `gpt-image-1.5` (unless user explicitly asks for `gpt-image-1-mini` or cheaper alternative).
- Assume generate unless user explicitly says "edit".
- Use OpenAI Python SDK (`openai` package) for all API calls; never raw HTTP.
- Prefer bundled CLI (`scripts/image_gen.py`) over writing one-off scripts.
- Never modify `scripts/image_gen.py`; ask user if something is missing.
- If result isn't clearly relevant or doesn't satisfy constraints, iterate with small targeted prompt changes; only ask a question if a missing detail blocks success.

## Reference map
- **`references/prompt-augmentation.md`**: Use-case taxonomy + spec template + augmentation rules.
- **`references/prompting.md`**: Prompting principles (structure, constraints, iteration patterns, use-case tips).
- **`references/cli.md`**: How to run image generation/edits/batches via CLI (commands, flags, recipes).
- **`references/image-api.md`**: API parameter quick reference (sizes, quality, background, edit-only fields).
- **`references/sample-prompts-generate.md`**: Copy/paste prompts for generation workflows.
- **`references/sample-prompts-edit.md`**: Copy/paste prompts for edit workflows.
- **`references/sample-prompts-website.md`**: Website asset recipes (hero, cards, backgrounds, etc.).
- **`references/sample-prompts-game.md`**: Game asset recipes (concept art, items, environments, etc.).
- **`references/sample-prompts-asset-types.md`**: Asset-type templates (wireframes, logos, mockups, etc.).
- **`references/codex-network.md`**: Environment/sandbox/network-approval troubleshooting.

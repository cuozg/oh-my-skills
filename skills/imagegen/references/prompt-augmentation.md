# Prompt augmentation

Reformat user prompts into a structured, production-oriented spec. Only make implicit details explicit; do not invent new requirements.

## Use-case taxonomy (exact slugs)

Generate:
- `photorealistic-natural` — candid/editorial lifestyle scenes with real texture and natural lighting.
- `product-mockup` — product/packaging shots, catalog imagery, merch concepts.
- `ui-mockup` — app/web interface mockups that look shippable.
- `infographic-diagram` — diagrams/infographics with structured layout and text.
- `logo-brand` — logo/mark exploration, vector-friendly.
- `illustration-story` — comics, children's book art, narrative scenes.
- `stylized-concept` — style-driven concept art, 3D/stylized renders.
- `historical-scene` — period-accurate/world-knowledge scenes.

Edit:
- `text-localization` — translate/replace in-image text, preserve layout.
- `identity-preserve` — try-on, person-in-scene; lock face/body/pose.
- `precise-object-edit` — remove/replace a specific element (incl. interior swaps).
- `lighting-weather` — time-of-day/season/atmosphere changes only.
- `background-extraction` — transparent background / clean cutout.
- `style-transfer` — apply reference style while changing subject/scene.
- `compositing` — multi-image insert/merge with matched lighting/perspective.
- `sketch-to-render` — drawing/line art to photoreal render.

## Augmentation vs invention

- Implicit constraints OK: "a hero image for a landing page" → add "generous negative space on the right for headline text".
- Do not introduce new creative elements the user didn't ask for (mascot, brand names, changed subject).

## Spec template (include only relevant lines)

```
Use case: <taxonomy slug>
Asset type: <where the asset will be used>
Primary request: <user's main prompt>
Scene/background: <environment>
Subject: <main subject>
Style/medium: <photo/illustration/3D/etc>
Composition/framing: <wide/close/top-down; placement>
Lighting/mood: <lighting + mood>
Color palette: <palette notes>
Materials/textures: <surface details>
Quality: <low/medium/high/auto>
Input fidelity (edits): <low/high>
Text (verbatim): "<exact text>"
Constraints: <must keep/must avoid>
Avoid: <negative constraints>
```

## Augmentation rules

- Keep it short; add only details the user already implied or provided elsewhere.
- Classify into a taxonomy slug above; use the slug to find matching examples.
- If user gives a broad request, propose tasteful context-appropriate assets and map each to a slug.
- For edits, explicitly list invariants ("change only X; keep Y unchanged").
- If any critical detail is missing and blocks success, ask; otherwise proceed.

## Quick examples

### Generation (hero image)
```
Use case: stylized-concept
Asset type: landing page hero
Primary request: a minimal hero image of a ceramic coffee mug
Style/medium: clean product photography
Composition/framing: centered product, generous negative space on the right
Lighting/mood: soft studio lighting
Constraints: no logos, no text, no watermark
```

### Edit (invariants)
```
Use case: precise-object-edit
Asset type: product photo background replacement
Primary request: replace the background with a warm sunset gradient
Constraints: change only the background; keep the product and its edges unchanged; no text; no watermark
```

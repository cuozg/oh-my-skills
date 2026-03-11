# Sample prompts — Edit

Recipes only. Keep user-provided requirements; do not invent new creative elements.
Principles: `references/prompting.md` · Taxonomy + template: `references/prompt-augmentation.md`

## Per-slug examples

### text-localization
```
Use case: text-localization
Input images: Image 1: original infographic
Primary request: translate all in-image text to Spanish
Constraints: change only the text; preserve layout, typography, spacing, and hierarchy; no extra words; do not alter logos or imagery
```

### identity-preserve
```
Use case: identity-preserve
Input images: Image 1: person photo; Image 2..N: clothing items
Primary request: replace only the clothing with the provided garments
Constraints: preserve face, body shape, pose, hair, expression, and identity; match lighting and shadows; keep background unchanged; no accessories or text
Input fidelity (edits): high
```

### precise-object-edit
```
Use case: precise-object-edit
Input images: Image 1: room photo
Primary request: replace ONLY the white chairs with wooden chairs
Constraints: preserve camera angle, room lighting, floor shadows, and surrounding objects; keep all other aspects unchanged
```

### lighting-weather
```
Use case: lighting-weather
Input images: Image 1: original photo
Primary request: make it look like a winter evening with gentle snowfall
Constraints: preserve subject identity, geometry, camera angle, and composition; change only lighting, atmosphere, and weather
Quality: high
```

### background-extraction
```
Use case: background-extraction
Input images: Image 1: product photo
Primary request: extract the product on a transparent background
Output: transparent background (RGBA PNG)
Constraints: crisp silhouette, no halos/fringing; preserve label text exactly; no restyling
```

### style-transfer
```
Use case: style-transfer
Input images: Image 1: style reference
Primary request: apply Image 1's visual style to a man riding a motorcycle on a white background
Constraints: preserve palette, texture, and brushwork; no extra elements; plain white background
```

### compositing
```
Use case: compositing
Input images: Image 1: base scene; Image 2: subject to insert
Primary request: place the subject from Image 2 next to the person in Image 1
Constraints: match lighting, perspective, and scale; keep background and framing unchanged; no extra elements
Input fidelity (edits): high
```

### sketch-to-render
```
Use case: sketch-to-render
Input images: Image 1: drawing
Primary request: turn the drawing into a photorealistic image
Constraints: preserve layout, proportions, and perspective; choose realistic materials and lighting; do not add new elements or text
Quality: high
```

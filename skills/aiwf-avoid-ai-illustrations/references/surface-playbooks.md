# Surface Playbooks

Use the smallest route that can produce a correct final asset.

## Freeform Illustration Or Mood Image

Use normal image generation when exact text, data, anatomy, or instructional logic is not central.

Do:

- specify composition, focal point, medium, lighting, and subject count
- keep negative prompts targeted to likely defects
- generate multiple candidates and select by concept first, then polish locally

Avoid:

- asking the model to invent readable labels, charts, or brand marks
- stacking many style adjectives that conflict
- accepting random extra objects as harmless when they change the meaning

## Photoreal Person, Face, Or Hands

Use references, pose control, masks, or inpainting when hands, face identity, product handling, or anatomy must be credible.

Prompt guidance:

- "natural, subtle skin texture" for realistic skin without overdone pores
- "healthy clear skin, no acne, no cyst-like marks, no rash-like marks" when clean complexion matters
- "two visible hands, five fingers on each visible hand, natural relaxed pose" only when hands are visible and important
- describe exact hand-object interaction rather than only "holding"

Review:

- crop hands and face at 100% and 200%
- count visible fingers and check wrist/finger orientation
- check teeth, pupils, ears, hairline, jewelry, clothing seams, and contact shadows
- reject waxy, plastic, overly glossy, or pore-cluster artifacts when the user asked for clean realism

## Logo, Icon, Or Signage

Use generated images for concept exploration, not final production typography.

Route:

1. Generate rough visual directions without relying on exact text.
2. Select a mark, silhouette, or composition.
3. Redraw in vector form or build with design/code tools.
4. Add real text with a real font.
5. Check small-size legibility and accidental brand similarity.

Do not ship bitmap logo text unless it has been manually checked and is editable or reproducible.

## Diagram Or Flowchart

Route:

1. Write the nodes, edges, groups, and labels as text first.
2. Render with Mermaid, Graphviz, SVG, draw.io, Figma, or code.
3. Use generated imagery only for background texture, icons, or optional decorative polish.
4. Validate arrow direction, grouping, labels, and missing components.

If the user asks for a "diagram image", still prefer a structured source artifact plus exported image.

## Chart Or Quantitative Infographic

Route:

1. Identify the dataset, metric definitions, units, and intended comparison.
2. Render with Python, Vega-Lite, Observable, Plotly, matplotlib, or a spreadsheet/chart tool.
3. Use generated imagery only for decorative framing or non-data illustration.
4. Verify title, labels, axis scale, legend, values, and units.

Never infer numbers from an AI-rendered chart image. If the source data is missing, say the chart is illustrative only.

## Product, Mechanical, Or Technical Image

Use references or structured modeling when geometry matters.

Check:

- part count and placement
- functional plausibility
- cables, ports, screws, fasteners, shadows, and scale
- whether any decorative flourish changes the implied mechanism

For mechanical diagrams, use CAD, SVG, or vector annotations before raster polish.

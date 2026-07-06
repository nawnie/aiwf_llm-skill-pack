# Generated Image Failure Modes

Use this reference to name the failure class before deciding how to fix it.

## Composition And Prompt Faithfulness

Watch for missing prompt-critical objects, wrong object counts, swapped attributes, broken spatial relationships, and contradictory scenes. These are common enough that prompt faithfulness must be checked separately from aesthetics.

Common checks:

- every requested subject appears
- counts are correct
- color, shape, texture, clothing, and material attributes belong to the right object
- left/right, above/below, inside/outside, holding/wearing, and near/far relationships are correct
- the scene does not add distracting unrequested objects

## People, Anatomy, And Photorealism

Inspect people at full size and zoomed in. Strong portrait style can hide defects at a glance.

Common failures:

- extra, missing, fused, or malformed fingers
- implausible finger bends, hand-object grasps, wrists, elbows, shoulders, knees, and feet
- distorted teeth, pupils, eyes, ears, hairlines, and facial symmetry
- waxy, plastic, overly glossy, or over-sharpened skin
- pimple, cyst, scar, pore-cluster, or rash-like artifacts when prompts overemphasize skin micro-detail
- impossible shadows, reflections, perspective, or contact points
- accessories that melt into skin, hair, or clothing

Prompt hygiene:

- Use "natural, subtle skin texture" before "visible pores" when clean realism is desired.
- Add "clear healthy skin, no acne, no cysts, no rash-like marks" only when the user asks for that kind of clean portrait.
- For hands, reduce ambiguity: specify pose, visible hand count, finger visibility, and object interaction; use pose/control references when available.

## Logos, Icons, Signage, And Visual Text

Text and marks must be exact for professional output. Treat generated bitmap typography as a concept draft unless it has been checked and redrawn.

Common failures:

- misspelled or warped letters
- brand names with missing, duplicated, or pseudo-letters
- uneven baselines, random glyphs, or melted text
- fake trademarks or accidental lookalikes
- icons with inconsistent geometry, broken symmetry, or unclear silhouettes
- illegible small text after downscaling

Final assets should use editable vectors, real fonts, traced geometry, or explicit text layers.

## Diagrams

Diagrams are semantic artifacts. A pretty raster is not enough when the diagram teaches, documents, or routes a process.

Common failures:

- arrows point the wrong way
- labels are misspelled or attached to the wrong node
- grouping, hierarchy, and sequence are unclear
- repeated boxes have inconsistent shape, spacing, or naming
- technical diagrams omit necessary components
- the diagram cannot be edited without redrawing

Use structured formats first: Mermaid, Graphviz, SVG, draw.io, Figma, or code-generated layout.

## Charts And Data Visualizations

Charts must be faithful to data, not just plausible.

Common failures:

- wrong values, wrong categories, or invented numbers
- misleading axes, missing units, uneven scales, or truncated baselines
- labels that do not match the data
- decorative marks that imply unsupported precision or comparison
- color legends that do not map to the plotted series
- unreadable text after export

Render charts from data with a charting library, then polish style if needed.

## Evidence Map

The local research receipt for this skill is:

`research runs/20260706-081802-avoid-ai-illustration-skill/`

Key source-backed categories:

- compositional failures: T2I-CompBench and Attend-and-Excite
- visual text and design image risks: AnyText and DesignDiffusion
- human artifacts, hands, and photoreal artifacts: HADM, realistic-hand generation, CHI photorealism taxonomy
- diagrams: text-to-diagram generation benchmark
- charts: chart QA and visualization generation literature

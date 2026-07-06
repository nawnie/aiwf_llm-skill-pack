# Final Image Review Checklist

Use this before accepting generated image work as final.

## Universal Checks

- Prompt-critical subjects are present.
- Counts, attributes, and spatial relationships match the request.
- No extra object changes the meaning.
- Lighting, shadows, reflections, and perspective are plausible.
- Edges, seams, and small details hold up at final display size.
- The output still looks good after downscaling or export compression.

## People

- Hands have plausible finger counts, bends, joints, nails, and contact points.
- Faces have coherent eyes, pupils, teeth, ears, hairlines, and skin texture.
- Body proportions, clothing seams, jewelry, and object interactions make sense.
- Skin detail is natural for the request and does not create unwanted blemish-like artifacts.

## Text And Logos

- Every letter is readable and intentionally spelled.
- Real brand names are not accidentally imitated.
- Typography is editable or rendered from real text for final output.
- Small-size icon or logo use remains legible.

## Diagrams

- Nodes, labels, arrows, order, and grouping are correct.
- The diagram source is editable.
- Decorative elements do not obscure the logic.
- Exported image matches the structured source.

## Charts

- Values match source data.
- Axis scales, units, title, legend, and labels are correct.
- Visual encodings match the metric definitions.
- The chart does not imply unsupported precision, causality, or comparison.

## Verdict Format

Use this compact report:

```text
Verdict: pass | revise | reject
Surface: <image|portrait|logo|diagram|chart|mixed>
Blocking issues:
- ...
Fix route:
- regenerate | inpaint | redraw vector | rerender chart | revise prompt | request data/source asset
Final QA gates:
- ...
```

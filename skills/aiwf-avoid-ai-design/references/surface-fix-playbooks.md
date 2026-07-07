# Surface Fix Playbooks

Use the section that matches the artifact. Keep edits as small as the surface allows.

## Gradio Local AI Apps

Goal: a practical control surface that feels local, capable, and understandable.

Inspect first:

- `aiwf/web/app.py`
- `aiwf/web/tabs/`
- custom CSS or theme setup
- callback wiring around primary actions
- labels, helper text, status/error messages

Fix pattern:

1. Put required inputs, model/engine choice, and Generate/Run in the main flow.
2. Keep per-run controls near the action: seed, duration, fps, size, batch count, safety/model warnings.
3. Move rarely changed settings into a clear advanced section.
4. Give status, errors, logs, and output previews different visual roles.
5. Replace teal wash with a neutral base and one accent.
6. Keep Markdown helper text short. Long explanations belong in docs, not inside the app.
7. Verify with a Gradio smoke or screenshot when possible. Avoid model generation unless the user asked for it.

Good Gradio direction choices:

- `technical-workbench`: compact controls, neutral gray base, one accent, clear log/output split.
- `studio-console`: stronger visual hierarchy, output-first, restrained accent, visible model readiness.
- `operator-panel`: dense settings, exact labels, status colors with meaning.

## PDF Reports And Documents

Goal: a report or document that reads like a human laid it out for the audience.

Inspect first:

- source format: Markdown, HTML, LaTeX, DOCX, ReportLab, React PDF, template engine
- page size and margins
- heading hierarchy
- tables, figures, captions, source notes
- cover and footer/header rules

Fix pattern:

1. Decide whether the document is a report, handout, memo, guide, or marketing asset.
2. Build the page grid before decorating: margins, running header/footer, page numbers, body width.
3. Set type roles: title, section, body, label, caption, table cell, footnote.
4. Remove gradient covers, teal sidebars, and abstract icon cards unless they carry real brand meaning.
5. Make tables readable: units, alignment, row grouping, totals, footnotes, and consistent rules.
6. Use callouts sparingly. If every paragraph is in a card, no paragraph is emphasized.
7. Render pages and inspect page 1 plus any table-heavy or figure-heavy pages.

Good document direction choices:

- `engineering-memo`: tight hierarchy, small accent, clear tables, no decoration.
- `field-report`: strong section labels, source notes, compact charts, practical captions.
- `executive-brief`: restrained cover, high-contrast summary, clean tables, obvious next actions.

## React, Tailwind, Shadcn, And Web Pages

Goal: a web surface with a specific purpose, not the median SaaS page.

Before editing, read `modern-web-appeal.md` and choose which human signal is missing: hierarchy, credibility, product evidence, accessibility, responsiveness, performance, visible state, or audience fit.

Inspect first:

- `package.json`, framework, route files
- app/page components
- Tailwind config and CSS variables
- component primitives and imported icon sets
- responsive behavior and screenshots

Fix pattern:

1. Identify whether the user asked for a tool, dashboard, app, game, website, or marketing page.
2. For tools/apps, put the real work surface first. Do not make a landing page unless asked.
3. Replace default theme tokens before touching dozens of components.
4. Remove repeated card shells. Use layout, type, and density to create hierarchy.
5. Pick imagery or screenshots that show the real product or state.
6. Check contrast, focus-visible states, target affordance, text scaling, and mobile reflow.
7. Build stable dimensions for buttons, boards, controls, counters, tiles, and charts.
8. Keep media, fonts, motion, and third-party scripts light enough that the page still feels fast.
9. Verify with desktop and mobile screenshots. Check text fit, overlap, image loading, layout shift, and state changes.

Good web direction choices:

- `utilitarian-product`: neutral base, dense hierarchy, low decoration, fast scanning.
- `technical-industrial`: grid, mono labels, precise status colors, little motion.
- `product-showcase`: real product imagery, one accent, no generic hero-card formula.

## Dashboards

Goal: repeated-use clarity.

Fix pattern:

1. Name the decisions users make from the dashboard.
2. Put the highest-priority metric or state in the first scan path.
3. Use color semantically: good, warning, error, selected, active, disabled.
4. Avoid decorative chart colors. Series colors must carry grouping meaning.
5. Make empty, loading, stale, and error states visible.
6. Keep filters close to the data they affect.
7. If the dashboard has a public or executive-facing surface, apply `modern-web-appeal.md` for credibility, source notes, readable hierarchy, and performance.

## Second-Pass Audit

Ask these after editing:

- Did teal or another accent take over again?
- Did the surface become a different default, such as beige minimal, dark slate cards, or purple gradients?
- Can a user find the main action without reading helper text?
- Do tables, forms, and controls have state?
- Does the layout still work on mobile and desktop?
- If this is a PDF, does it still print clearly in grayscale?

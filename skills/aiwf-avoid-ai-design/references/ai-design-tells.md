# AI Design Tells

Use this catalog as a signal checklist. A single item is rarely enough. A cluster is the problem.

## How To Judge

- `code-certain`: The source contains a default class, theme, font, icon, or component pattern.
- `visual-certain`: A screenshot, PDF render, or browser view shows the tell.
- `inferred`: The source suggests the tell, but the artifact was not rendered.

Do not call something AI-designed just because it uses a common pattern. Flag it when the pattern is unchosen and repeated.

## Universal P0 Signals

- Teal everywhere: primary buttons, links, tabs, focus rings, icons, headings, graph accents, callouts, and PDF sidebars all use the same teal family.
- Purple/indigo/blue gradient as the main design idea.
- Gradient text on headings.
- Soft glow blobs, bokeh blobs, or blurred gradient orbs used as decoration.
- One template repeated across the artifact: centered hero, three cards, CTA strip, four-column footer.
- Default component library theme with no visible product-specific decisions.
- Every card has the same radius, shadow, border, padding, icon square, and hover.
- Placeholder media where the real product, chart, screenshot, or document evidence should be.

## Color

P0:

- Teal-as-default, especially `#14b8a6`, `#0d9488`, `#0f766e`, Tailwind `teal-*`, or CSS variables mapped everywhere.
- Indigo/violet/blue gradient backgrounds or CTA clusters.
- Several accent colors used at equal visual weight, with no dominant color.

P1:

- Default Tailwind blue, shadcn zinc/slate, Bootstrap primary blue, MUI blue, or Gradio default accent shipped unchanged.
- Status colors used decoratively instead of semantically.
- Low-contrast dark mode with gray text on near-black cards.

Fix:

- Choose one dominant neutral or brand color, one accent, and status colors that mean something.
- Use teal only when it has a role. One accent is fine. Teal on every affordance is not.
- Replace glow and gradient decoration with structure, contrast, or real media.

## Typography

P0:

- Inter, Roboto, Arial, Geist, or system font everywhere with no pairing, scale, or document hierarchy.
- PDF reports that use the same weight and size logic for cover, headings, captions, callouts, and tables.

P1:

- All-caps eyebrow labels in every section.
- One decorative italic word in an otherwise generic headline.
- Monospace used as "technical flavor" without a table, code, terminal, or data reason.

Fix:

- Pick type for the surface. Reports need readable body text and disciplined headings. Dashboards need compact, high-legibility labels. Marketing pages may use a stronger display face.
- Set a real scale: title, section, subsection, body, label, caption, table.

## Layout

P0:

- Centered everything: title, subtitle, cards, controls, chart, and CTA.
- Three identical cards as the main explanation.
- PDF cover or web hero that looks more important than the actual content.
- Gradio layouts where tabs, accordions, and examples stack without a task flow.

P1:

- `container mx-auto px-4` or one max width used everywhere.
- Four-column footer with fake or empty link groups.
- Generic stat strip with placeholder proof.
- Bento grid used because it looks current, not because content hierarchy needs it.

Fix:

- Choose the grid for the job. Operational tools need control clusters and output areas. Reports need page rhythm. Web pages need the actual product or offer visible fast.
- Vary section width and density by role.

## Components And States

P0:

- Untouched Gradio theme or shadcn theme used as the final design.
- `rounded-2xl shadow-lg` on every surface.
- Same icon-in-rounded-square pattern repeated across every feature or setting.

P1:

- Missing hover, active, disabled, loading, error, empty, and focus-visible states.
- Colored left-border cards used as the main hierarchy tool.
- Pill badges with vague labels such as "New", "AI-powered", or "Beta" when the label adds no useful information.

Fix:

- Use radius, shadow, border, and color to show hierarchy and state.
- Build the boring states. A real app has failures, disabled controls, empty outputs, and progress.

## Gradio-Specific Tells

P0:

- Default Gradio theme with a teal or blue accent pasted over everything.
- Generate/Run is visually buried while optional controls dominate.
- Too many controls visible at once with no task grouping.
- Accordions hide settings the user changes every run.

P1:

- Long Markdown headers inside the app explaining how to use the UI.
- Output gallery, logs, seed, model status, and errors all share the same visual weight.
- Examples are decorative instead of helping users start a real run.

Fix:

- Put the primary action and required inputs in the main flow.
- Group optional controls by frequency of use.
- Make status, errors, and outputs visually distinct.
- Keep copy short and concrete. Use the AIWF prose scan from `aiwf-avoid-ai-pushes` for long helper text.

## PDF And Document Tells

P0:

- Generic AI report cover: huge title, teal sidebar, gradient band, abstract icon, and no useful metadata.
- Every page uses the same card background, shadow, and accent.
- Tables are screenshots or decorative blocks instead of readable data.
- No page numbers, source notes, captions, or print-safe contrast.

P1:

- Too many heading levels for the amount of content.
- Bullets are used where prose, a table, or a figure would read better.
- Callouts are overused and all styled the same.
- Margins are too narrow, too wide, or inconsistent across pages.

Fix:

- Build a page grid: margins, header/footer, body measure, table rules, captions, source notes.
- Use color sparingly. In print, contrast and hierarchy matter more than brand wash.
- Make tables legible first: alignment, units, row grouping, totals, and footnotes.

## React And Web Tells

P0:

- Generic landing page when the user asked for an app or tool.
- Decorative cards nested in page sections without real interaction.
- Hero section hides the actual product, state, gameplay, person, or place.
- The page reads as one hue family.

P1:

- Untouched shadcn `components.json`, default radius, default Button/Card/Badge.
- Lucide `Sparkles`, `Zap`, `Rocket`, `ArrowRight`, `CheckCircle2` used in the same roles as every AI-built page.
- Layout shifts because buttons, labels, tiles, or counters have no stable dimensions.

Fix:

- Render desktop and mobile. Check overlap, text fit, blank canvases, image loading, and state changes.
- Use icons only where they clarify controls.
- For tools and dashboards, put the work surface first, not a marketing hero.

## What Not To Over-Flag

- Teal can be a valid brand or status color when it is restrained.
- Centered layouts can be intentional for luxury, editorial, or simple documents.
- A minimal interface can be excellent if hierarchy, spacing, states, and contrast are deliberate.
- Component libraries are fine. Shipping their defaults as the design is the tell.

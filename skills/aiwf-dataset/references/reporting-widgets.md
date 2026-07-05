# Reporting Widgets

Use this reference when the user asks for a dataset QA dashboard, intake report, cleanup report, or visual handoff.

## Data Analytics rules

- Use `dataAnalyticsWidgets` for hosted reports or dashboards.
- Call `validate_artifact` with the complete manifest and bounded snapshot before rendering.
- Call `render_artifact` only after validation passes.
- Keep snapshots bounded: at most 50 datasets, 2,000 rows per dataset, 3 MB total payload, and 200k inline source characters.
- Use `snapshot.datasets` as an object keyed by dataset ID, with each value as an array of row objects.
- Do not send secrets, credentials, direct personal contact details, hidden reasoning, or sensitive raw text to widgets.

## Useful dashboard blocks

Build dataset QA dashboards around:

- source counts by status,
- accepted/quarantined/rejected trend,
- license distribution,
- source type distribution,
- JSONL parse failures,
- duplicate ID counts,
- synthetic vs source-backed counts,
- caption status counts,
- media duration histograms,
- stale source counts by `review_after`.

## Report minimum

A report artifact should include:

- a first markdown block whose body starts with `# <report title>`,
- at least one chart,
- one table with default sort,
- source notes explaining the inspected root and validation command,
- a short markdown block for unresolved judgment calls.

## When not to render

Do not render a widget when:

- the user only needs a command-line validation result,
- the source rows include sensitive data that cannot be sampled safely,
- the root is missing and there is no dataset snapshot,
- validation errors have not been fixed.

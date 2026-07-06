# AIWF Receipt Schema

Use `receipt-schema.v1.json` when a skill produces durable proof for training, evals, serving, GPU diagnostics, security checks, pipeline audits, or debug passes.

Required fields:

- `schema`: `aiwf.receipt.v1`
- `receipt_id`: stable local identifier
- `created_at`: ISO-8601 timestamp
- `skill`: skill that produced the receipt
- `task`: short description of what was checked
- `status`: `passed`, `failed`, `partial`, `skipped`, or `blocked`
- `evidence`: one or more concrete evidence strings

Recommended fields:

- `scope`: files, endpoints, models, datasets, or runtime surfaces covered
- `commands`: command strings and pass/fail/not-run status
- `artifacts`: output files, logs, screenshots, or generated reports
- `risks`: residual risks or explicit skipped checks

Receipts should not contain secrets, private tokens, signed URLs, raw personal data, or large logs. Store paths or summaries instead.

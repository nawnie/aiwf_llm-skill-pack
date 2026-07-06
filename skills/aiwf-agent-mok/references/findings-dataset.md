# Findings Dataset Protocol

Use this protocol whenever Agent MoK searches, researches, browses, reads files for learning, receives user-uploaded material, interrogates a model, or otherwise finds reusable data.

## Root Selection

Choose the findings root in this order:

1. Use the user-provided findings directory when the user explicitly supplies one.
2. Otherwise create or use `moks findings` under the current working directory.
3. If that path is not writable, or the user declines choosing another directory, create or use `moks findings` under the root skill/plugin folder when writable.
4. If no candidate is writable, report the blocker and provide the dataset records in the response or a downloadable artifact when the host supports it.

Do not silently skip findings capture. Report the selected root and run folder path.

## Per-Usage Run Folder

Each usage creates a new subfolder:

```text
moks findings/
  YYYYMMDD-HHMMSS-short-task-slug/
    manifest.json
    atlas_cards.jsonl
    training_data.jsonl
    sources.jsonl
    README.md
    raw/
```

Use local time for the timestamp. Keep the slug short and filesystem-safe. If the folder already exists, add a numeric suffix.

## Required Files

### `manifest.json`

Record:

- `schema_version`: `moks-findings-v1`
- `created_at`
- `request`
- `run_id`
- `findings_root`
- `source_classes`
- `tools_used`
- `license_policy`
- `privacy_policy`
- `training_readiness`
- `validation_status`
- counts for cards, sources, and training records

### `atlas_cards.jsonl`

Write one JSON object per card:

```json
{
  "id": "card-001",
  "lane": "external_research",
  "type": "fact",
  "claim": "Short claim or finding.",
  "evidence": [{"source_id": "src-001", "locator": "URL, file path, or tool result id"}],
  "source_class": "official",
  "verification_state": "verified",
  "failure_mode": "How this could be wrong.",
  "success_check": "How the card was checked.",
  "tags": ["routing", "evidence"]
}
```

### `training_data.jsonl`

Use chat-style SFT records unless another schema is explicitly needed:

```json
{
  "id": "train-001",
  "messages": [
    {"role": "system", "content": "Use evidence-aware reasoning and label uncertainty."},
    {"role": "user", "content": "Task or question derived from the finding."},
    {"role": "assistant", "content": "Training target grounded in verified findings."}
  ],
  "metadata": {
    "source_ids": ["src-001"],
    "card_ids": ["card-001"],
    "source_class": "official",
    "license_status": "reference-only",
    "training_readiness": "usable_with_citation",
    "uncertainty": "low"
  }
}
```

Prefer multiple small records over one large record. Include negative or contrast records only when they teach a clear rejected behavior and are labeled as such.

### `sources.jsonl`

Write one JSON object per source:

```json
{
  "id": "src-001",
  "title": "Source title",
  "url_or_path": "https://example.com/doc",
  "source_class": "official",
  "retrieved_at": "2026-06-17T12:00:00-04:00",
  "owner_or_publisher": "Publisher",
  "license": "unknown",
  "allowed_use": "citation_and_summary",
  "notes": "Do not train on long verbatim text without license review."
}
```

## Training Safety

`training_data.jsonl` should contain training-ready structure, not indiscriminate copies of found material.

Rules:

- Do not store secrets, API keys, credentials, raw environment dumps, or unnecessary personal data.
- Do not store long copyrighted passages from web pages, books, papers, articles, or docs unless license review permits it.
- Store facts, summaries, source metadata, citations, short compliant excerpts, and derived training targets.
- Mark generated, stale, conflicting, unverified, or license-unclear data so it is not treated as canonical ground truth.
- Keep user-provided private material out of `raw/` unless the user clearly wants it saved there.

## Validation

Before finalizing a run:

- Confirm all JSONL files parse.
- Confirm every training record has at least one `source_id` or an explicit `generated`/`user_provided` label.
- Confirm every source has `source_class`, `url_or_path`, and `allowed_use`.
- Confirm no obvious secrets or unnecessary personal data were written.
- Report the run folder path and remaining readiness caveats.

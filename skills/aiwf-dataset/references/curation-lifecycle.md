# Curation Lifecycle

Use this reference for dataset duration, freshness, cleanup cadence, and retention decisions.

## Duration dimensions

Track more than one duration:

- Source age: time from `published_at` to `accessed_at`.
- Review age: time since the last validation pass.
- Dataset window: `dataset_window_start` and `dataset_window_end` for time-bounded corpora.
- Media duration: `duration_seconds` for video and audio.
- Retention window: how long raw intake, rejected sources, and intermediate artifacts should be kept.
- Training exposure: how long a record remains eligible before revalidation.

## Default cadence

- Daily: ingest new research, check source reachability, classify statuses, and render a small intake summary when requested.
- Weekly: rerun deduplication candidates, license audits, and stale-source checks.
- Monthly: revalidate accepted sources with unstable claims, refresh dataset cards, and archive stale rejected intake.
- Before training: run strict manifest/JSONL validation, dedup checks, license checks, and synthetic-label separation.

## Cleanup policy

Do not destroy source material during cleanup. Prefer:

- `quarantine/` reports,
- new manifest versions,
- `rejected_sources.jsonl`,
- `cleanup_plan.md`,
- additive normalized output folders,
- moved copies only when the user explicitly approves the move.

If the user asks to clean current datasets, inspect first, write a plan with exact paths, and apply only additive or reversible changes unless they explicitly approve deletion.

## Freshness gates

Use `review_after` for accepted sources that can drift:

- Software docs, model cards, benchmarks, and package APIs: 7 to 30 days.
- Legal/license pages: 7 days before training or publication.
- Stable papers and archived datasets: 180 to 365 days.
- Local synthetic guardrail rows: revalidate when policy or target behavior changes.

## Media duration gates

Use dataset-specific gates and record rejected clips:

- Image: no duration, but record capture timestamp if available.
- Short video clips: prefer 2 to 20 seconds for captioning and action labels unless the target model needs longer context.
- Long video sources: segment into scenes, store parent video ID, start/end timestamps, and transcript alignment.
- Audio clips: prefer 1 to 30 seconds for ASR/caption tasks unless long-form transcription is the target.

Always record `duration_seconds`, `start_seconds`, `end_seconds`, and `parent_asset_id` for clipped media.

## Training readiness gates

Block training exports when:

- accepted source count is zero for source-backed datasets,
- license is missing or incompatible,
- JSONL is not parseable,
- IDs are missing or duplicated,
- synthetic rows are not labeled,
- model-generated captions are mixed with verified captions,
- PII/NSFW review is missing for user-facing or scraped material.

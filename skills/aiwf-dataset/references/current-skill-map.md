# Current Skill Map

Use this map to compose existing skills instead of duplicating their instructions.

## Core companions

- `nemo-curator`: Use for GPU-scale curation, fuzzy/exact/semantic deduplication, quality filters, PII redaction, NSFW filtering, and text/image/video/audio corpus cleanup. Verify installed package APIs before running code because NeMo Curator versions move.
- `avoid-ai-writing`: Use in detect mode for original research prose, source descriptions, generated summaries, and public-facing dataset notes. Treat results as signal only. Do not use it as an authorship verdict.
- `dataAnalyticsWidgets`: Use for dataset QA reports and dashboards when the user should inspect charts or tables. Always call `validate_artifact` before `render_artifact`.

## Useful local companions

- `ray-data`: Use for large ETL, batch inference, and streaming reads across Parquet, CSV, JSON, images, audio, or video when NeMo-specific curation is not required.
- `sentence-transformers`: Use for embeddings, semantic clustering, and semantic duplicate candidates.
- `faiss`: Use for fast local vector search over embedding sets when metadata filtering is not the main requirement.
- `clip`: Use for image-text matching, image similarity, visual search, and caption consistency checks.
- `whisper`: Use for audio or video speech transcription before caption QA or transcript dataset creation.
- `segment-anything-model`: Use for masks, object crops, segmentation-derived labels, or annotation bootstrapping.

## Selection rule

Start with the cheapest reliable tool. Use local parsers and the bundled validator for receipt checks, then escalate to embeddings, Ray, or NeMo Curator when the dataset size, modality, or duplicate risk justifies it.

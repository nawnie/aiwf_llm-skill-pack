# Research Validation

Use this reference for daily automated research intake, source vetting, and provenance cleanup.

## Intake fields

Capture these fields before accepting a source:

- `source_id`
- `title`
- `url`
- `publisher_or_owner`
- `author_or_org`
- `published_at`
- `accessed_at`
- `source_type`
- `license`
- `license_url`
- `claim_summary`
- `evidence_used`
- `hash_or_revision`
- `validation_status`
- `validation_notes`

## Source tiers

- `primary`: Original paper, official documentation, official dataset card, repository owned by the project, standards body, government source, or direct artifact.
- `strong_secondary`: Reputable reporting or analysis that links back to primary material.
- `weak_secondary`: Blog, forum, social post, model answer, scraped summary, or unsourced aggregator.
- `synthetic`: AI-generated text, AI-assisted summary, generated caption, generated QA pair, or generated guardrail scenario.
- `unknown`: No stable provenance, missing authorship, broken source chain, or unclear license.

Prefer `primary`. Use `strong_secondary` only when the primary source is unavailable or when it adds interpretation that is separately useful. Quarantine `weak_secondary`, `synthetic`, and `unknown` unless the dataset explicitly needs that class.

## Original research rule

Original research that grounds factual dataset rows should not be AI-written. If a source reads as model-generated, has AI citation leaks, has placeholder text, or cannot be traced to a human/organization/source artifact, quarantine it until a primary source is found.

AI-generated material is acceptable for:

- synthetic guardrail examples,
- adversarial prompt/response pairs,
- generated captions pending verification,
- formatting drafts that are backed by accepted primary sources.

Label those rows as synthetic and keep their provenance separate from factual research sources.

## Validation pass

For each candidate source:

1. Open the source or official metadata.
2. Confirm author/organization, date, license, and access path.
3. Identify the exact claims or examples being used.
4. Check whether the source supports those claims without speculation.
5. Check for AI-writing tells with `avoid-ai-writing` when source quality is uncertain.
6. Reject detector-only conclusions. Use the writing check to trigger manual review, not to prove authorship.
7. Record status as `accepted`, `rejected`, `quarantined`, or `needs_review`.

## Red flags

- AI citation tokens such as `contentReference`, `oaicite`, `citeturn`, or `grok_card`.
- AI-tool URL tracking such as `utm_source=chatgpt.com`, `utm_source=claude.ai`, or `utm_source=perplexity.ai`.
- Placeholders such as `[INSERT SOURCE]`, `[Your Name]`, `2025-XX-XX`, or TODO comments in published prose.
- Vague attributions like "studies show" without named studies.
- License missing, contradictory, or incompatible with the intended dataset use.
- Claims that depend on "latest", "current", or "state of the art" without a checked date.

## Daily sorting statuses

- `new`: captured but not read.
- `screened`: accessible and roughly relevant.
- `accepted`: validated source, license recorded, claims mapped.
- `quarantined`: maybe useful, but provenance or license is not ready.
- `rejected`: not usable for this dataset.
- `curated`: accepted and transformed into dataset records.
- `reported`: included in the daily dashboard or summary.

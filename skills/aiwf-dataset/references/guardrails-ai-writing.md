# Guardrails and AI Writing

Use this reference when a dataset contains original research, generated summaries, guardrail examples, or synthetic adversarial rows.

## Boundary

Original research used as factual grounding should not be AI-written unless the dataset is explicitly studying AI-written artifacts. Guardrail training data can be AI-written when it is intentionally synthetic, labeled, and separated from factual source material.

## Acceptable AI-written data

AI-written material is allowed for:

- refusal examples,
- jailbreak attempts,
- unsafe prompt variants,
- safe-completion exemplars,
- style-transfer negatives,
- generated captions pending verification,
- synthetic noisy examples for detector or policy training.

Each row must include:

- `synthetic: true`
- `ai_generated: true`
- `generator`
- `generation_date`
- `prompt_hash` or prompt reference
- `review_status`
- `intended_use`

## Not acceptable as original research

Do not use AI-written material as the factual source when it:

- summarizes a paper without a checked citation,
- invents or omits source details,
- contains AI citation leaks,
- contains placeholders,
- claims current facts without a checked date,
- has no named publisher, author, repository, dataset card, or artifact.

Find the primary source instead, or quarantine the item.

## Using avoid-ai-writing

Use `avoid-ai-writing` in detect mode for:

- source descriptions that feel generic,
- generated research briefs before they become public notes,
- dataset cards,
- `AUDIT.md` files,
- source summaries that will be reused by other agents.

Apply the result as a review signal. Do not write "AI-authored" as a conclusion based only on style. Write "needs provenance review" or "quarantined pending primary source" unless there is direct evidence.

## Split hygiene

Keep factual and synthetic records separable by field and by export:

- factual source-backed rows,
- generated guardrail rows,
- generated captions pending verification,
- verified captions,
- rejected or adversarial examples.

Before training, report counts for each class and confirm the intended model behavior matches the mixture.

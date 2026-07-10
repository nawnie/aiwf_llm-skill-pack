# Research Loop

Use this reference for the actual research run.

## Phase 1: Scope

Write the request in operational terms:

- decision or question
- target domain lanes
- time sensitivity
- acceptable source classes
- excluded source classes
- expected output format

## Phase 2: Source Plan

Create `source_plan.json` before searching.

Required fields:

- `request`
- `domains`
- `target_sources`
- `excluded_sources`
- `query_templates`
- `reddit_allowed`
- `weighting_policy`
- `acceptance_gates`

Use `scripts/source_target_router.py` for a first draft, then adjust manually.

## Phase 3: Search

Search in this order:

1. Tier 0: local repo, user artifacts, receipts.
2. Tier 1: primary research, official docs, official repos, standards, government or lab reports.
3. Tier 2: scholarly discovery indexes and repositories.
4. Tier 3: implementation reality and platform metadata.
5. Tier 4: community/practitioner context, only when needed.

Record each search query in `queries.jsonl`.

## Phase 4: Source Register

Each `sources.jsonl` record should include:

```json
{
  "id": "src-001",
  "title": "Source title",
  "url_or_path": "https://example.com",
  "source_class": "tier1_primary",
  "publisher": "Publisher or owner",
  "retrieved_at": "2026-07-01T12:00:00-04:00",
  "license": "unknown",
  "allowed_use": "citation_and_summary",
  "evidence_weight": 90,
  "weight_reason": "Official paper page directly supports the mechanism claim."
}
```

## Phase 5: Claim Ledger

Each `claims.jsonl` record should include:

```json
{
  "id": "claim-001",
  "claim": "Short checkable claim.",
  "claim_type": "scientific_mechanism",
  "source_ids": ["src-001"],
  "evidence_weight": 90,
  "weight_reason": "Direct Tier 1 source.",
  "verification_state": "verified",
  "contradiction_ids": [],
  "date_sensitive": true,
  "used_in_final": true
}
```

Claim types:

- `scientific_mechanism`
- `engineering_mechanism`
- `implementation_feasibility`
- `api_runtime_behavior`
- `model_resource_availability`
- `educational_background`
- `practitioner_context`
- `open_question`

## Phase 6: Contradictions

Use `contradictions.jsonl` when sources disagree.

Record:

- conflicting claim IDs
- source IDs
- resolution rule
- chosen claim, if any
- remaining uncertainty

Do not hide contradictions by averaging claims.

## Phase 7: Synthesis

Write `research_brief.md` with:

- direct answer
- source map
- key findings with weights
- contradictions
- rejected low-quality sources
- unknowns and open questions
- practical next steps
- source list

## Phase 8: Validation

Run:

```powershell
python <this-skill>\scripts\validate_research_receipt.py "<run_dir>"
```

If validation fails, fix the receipt before using the findings as final.

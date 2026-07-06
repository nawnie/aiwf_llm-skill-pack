# Atlas Cartographer Continuity Reference

Use this reference when changing the local continuity card schema, storage
layout, lane taxonomy, or import/export workflow.

## Purpose

The continuity store is a local, searchable bridge across Codex context
compaction, deleted chats, and handoffs. It is not a replacement for the
workspace, git history, test receipts, or the canonical ATLAS research archive.

## Card Shape

Required fields:

- `card_id`: UTC timestamp, lane, slug, and short content hash.
- `created_at_utc`: ISO 8601 UTC timestamp.
- `project`: short project or workspace name.
- `lane`: stable routing lane.
- `title`: short human title.
- `summary`: compact restart summary.
- `details`: optional longer local handoff note.
- `source_pointers`: paths, URLs, command receipts, artifact IDs, or files to
  inspect before trusting the card.
- `tags`: simple searchable labels.
- `must_retrieve`: exact files, cards, artifacts, or commands that should be
  retrieved on resume.
- `decisions`: durable decisions made during the task.
- `verification`: tests, smoke checks, parsers, or manual checks run.
- `unresolved`: next actions, risks, blockers, or stale facts.
- `confidence`: numeric confidence from 0.0 to 1.0.
- `risk_level`: `low`, `medium`, or `high`.
- `current_verification_required`: true when the card describes volatile state.

Optional fields can be added only when they improve retrieval or provenance.
Avoid schema churn for stylistic preferences.

## Lane Taxonomy

Use stable snake_case lanes. Prefer these lanes before inventing new ones:

- `atlas_archive`
- `aiwf_studio`
- `mok`
- `rv1`
- `retrain`
- `codex_tooling`
- `local_ai_runtime`
- `dataset_library`
- `windows_host`
- `general_continuity`

Create a new lane only when the existing lane would hide the card during a
future search.

## What To Store

Store:

- exact repo roots and moved-path corrections
- files changed or intentionally left untouched
- durable decisions and tradeoffs
- validation commands and results
- receipt/artifact paths
- unresolved next actions
- source pointers for claims
- stale-fact warnings

Do not store:

- secrets, API keys, credentials, cookies, tokens, or private contacts
- hidden reasoning or chain-of-thought
- large raw datasets or full copied source files
- live runtime facts without a revalidation warning
- speculative claims without a source pointer

## Search Before Acting

For a continuation request, search before broad repo exploration:

```powershell
python C:\Users\Shawn\.codex\skills\aiwf-atlas-cartographer\scripts\search_continuity_cards.py --query "<task words>" --limit 8
```

If a card points to live-state evidence, verify the live state before making a
current claim. Memory can preserve where to look; it does not make volatile facts
current.

## Importing From Project Cartographers

The training-lab cartographer at
`C:\Users\Shawn\Desktop\sort desktop\AI_Projects\ai project workspace\atlas-lora-adapter\lora_training_lab\scripts\atlas_cartographer.py`
is for manifest-to-card ingestion and adapter/retrieval experiments. Read it
before adapting it. Do not copy its generated benchmark/private-source cards into
the continuity store unless the user asks for that import.

The MoK cartographer at
`C:\Users\Shawn\Desktop\MoK-Project\src\mok\companion\cartographer.py`
is a lightweight file/window-title classifier. Treat it as a design reference
for lane assignment, not as the canonical continuity store.

## Validation

After changing scripts or schema:

1. Run the skill validator.
2. Run a sample write into a temp data root.
3. Run a sample search against that temp data root.
4. Parse every JSONL line touched by the change.
5. Check that no test card leaked secrets or irrelevant bulk content.

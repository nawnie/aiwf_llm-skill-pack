---
name: aiwf-deep-research
description: AIWF deep research workflow for source-backed, weighted, multi-domain investigation. Use when Codex must research, verify, or build a mental model across arXiv, Hugging Face, GitHub, Civitai, Reddit with limits, open-source libraries, college/graduate/postgraduate sources, quantum physics, robotics, mechanical engineering, AI papers, model resources, or emergent science. Triggers for deep research, source weighting, source plans, claim ledgers, citations, evidence grading, literature review, technical due diligence, research receipts, and avoiding low-quality tutorials or cookbook search drift.
---

# AIWF Deep Research

## Overview

Use this skill to run research as an evidence pipeline, not a search session. Build a source plan first, weight every source by what it can actually prove, keep a claim ledger, and validate the receipt before using findings in an answer, plan, code change, or training data.

## Runtime Defaults

Default to the highest available reasoning for every non-trivial deep-research run.

When the host supports `/goal`, create or continue a goal for the active research run. Use no fixed token ceiling, the largest available context limit, and unlimited or expanded tool-call limits where those controls exist. If the host requires finite settings, choose the highest available values. If the host does not expose those controls, proceed with the same intent and do not block the research workflow.

Apply expanded budgets to active research work: source planning, source retrieval, evidence review, claim ledgers, contradictions, synthesis, and validation. Do not spend expanded budget on broad chat-history review. Use standard context length to decide how much past chat is relevant, then rely on the user's current request, local receipts, and source-backed research artifacts.

Use `AIWF_DEEP_RESEARCH_EXTRA_URLS` for required seed URLs that must appear in the source plan. The value is comma-separated. `scripts/init_research_run.py` also accepts repeated `--extra-url` flags and writes all required seed URLs to `source_plan.json`.

## Routing

Use this skill before `aiwf-agent-mok` when the primary work is external research or source selection. Add `aiwf-agent-mok` when the research must also update `plan.md`, create findings datasets, or verify a multi-step project route.

Use other AIWF skills after this one when research becomes implementation:

- Model loading, precision, quantization, LoRA compatibility: `aiwf-model-loader`.
- Pipeline/runtime readiness and model-source mismatch: `aiwf-ai-pipelines`.
- Training, LoRA, QLoRA, checkpoints, export: `aiwf-local-ai-training`.
- Evals, benchmark receipts, promotion gates: `aiwf-ai-evals`.
- Serving and endpoint checks: `aiwf-inference-serving`.
- Repo edits after research: `aiwf-ai-coding-guardrails`.

## Required Workflow

1. Restate the research question and intended decision.
2. Read `references/source-policy.md` for every run.
3. Read `references/domain-targets.md` before choosing sources.
4. Read `references/research-loop.md` before writing the final synthesis or receipt.
5. Read `references/reddit-policy.md` before using Reddit or community sources.
6. Create a research run folder with `scripts/init_research_run.py`.
7. Generate or write a source plan before searching.
8. Search in this order: local/user evidence, primary sources, scholarly discovery indexes, implementation sources, community sources.
9. Put important claims into `claims.jsonl` with `source_ids`, `evidence_weight`, and `weight_reason`.
10. Preserve contradictions instead of averaging them away.
11. Validate the run with `scripts/validate_research_receipt.py`.
12. Use only validated or clearly labeled uncertain findings in the final answer.

## Source Rules

Do not treat sources as interchangeable.

- Papers, standards, official docs, official repos, and local receipts carry different claims.
- Civitai is valid for model/resource metadata and ecosystem signals, not scientific proof.
- Reddit is lead generation and practitioner context, not final evidence.
- Open-source library docs prove API/runtime behavior, not scientific validity unless backed by primary research.
- College and graduate materials are useful, but course notes, theses, dissertations, and student projects need explicit academic-level labels and weights.
- Store citations, source metadata, summaries, and short permitted excerpts. Do not store long copyrighted source text.

## Helper Scripts

Create a run:

```powershell
python .\skills\aiwf-deep-research\scripts\init_research_run.py --title "wan attention research" --request "Compare WAN attention runtimes for AIWF Studio."
python .\skills\aiwf-deep-research\scripts\init_research_run.py --title "wan attention research" --request "Compare WAN attention runtimes for AIWF Studio." --extra-url "https://arxiv.org/abs/2405.00000"
```

Route a prompt to source targets:

```powershell
python .\skills\aiwf-deep-research\scripts\source_target_router.py --prompt "Research Civitai LoRA metadata and verify against Hugging Face and GitHub."
```

Validate a run:

```powershell
python .\skills\aiwf-deep-research\scripts\validate_research_receipt.py "research runs\20260701-120000-wan-attention-research"
```

## Output Contract

Every non-trivial run should leave:

- `request.md`
- `source_plan.json`
- `queries.jsonl`
- `sources.jsonl`
- `claims.jsonl`
- `source_weights.jsonl`
- `contradictions.jsonl`
- `research_brief.md`
- `validation.json`

The final user answer should summarize findings, cite source URLs, state evidence strength, list contradictions or gaps, and identify what should be checked next.

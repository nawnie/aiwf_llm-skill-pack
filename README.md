# AIWF LLM Skill Pack

AIWF LLM Skill Pack is a skills-only Codex plugin for local open-source AI development. It helps agents route AIWF work across model loading, dataset curation, source-backed research, ComfyUI workflow conversion, QLoRA planning, evals, inference serving, GPU diagnostics, repository guardrails, and public-release hygiene.

This repository vendors Shawn-owned `aiwf-` skills only. It does not bundle outside skill folders, external licenses, external branding, MCP servers, or apps. Public prose, design, and push hygiene are handled by AIWF-owned skills and scans in this pack.

## What It Is

AIWF stands for AI Without Fear: a local-first, open-source AI workflow brand focused on practical consumer AI tools that can be inspected, tested, and run without hiding the hard parts. This pack gives Codex a routing layer and specialized skills for AIWF-style work: build locally, cite sources, validate claims, respect hardware limits, and keep public copy honest.

Use this pack when you want a Codex plugin for:

- local AI app development on Windows or consumer GPUs
- model loading, quantization, LoRA, QLoRA, and inference planning
- ComfyUI workflow JSON to Python pipeline analysis
- dataset provenance, research receipts, and source-weighted claims
- AIWF Studio docs, beta copy, launch hygiene, and Torchie voice
- repo-safe coding, security checks, GPU diagnostics, and eval gates

## Layout

```text
Agent Skills/
  .codex-plugin/
    plugin.json
  AGENTS.md
  HANDOFF.md
  PROJECT_SKILLS.md
  README.md
  LICENSE
  install.ps1
  manifest.json
  skillfindings.md
  docs/
    github-skill-inventory.md
    projectskill-list.use-cases.json
    receipt-schema.md
    receipt-schema.v1.json
    seo-aeo.md
    skill-authoring-policy.md
  skills/
    aiwf-orchestration/
    aiwf-orchestrator/
    aiwf-deep-research/
    aiwf-dataset/
    aiwf-comfy-workflow-pipeline/
    aiwf-avoid-ai-design/
    aiwf-avoid-ai-illustrations/
    aiwf-avoid-ai-pushes/
    aiwf-torchie/
    aiwf-ai-coding-guardrails/
    aiwf-repo-sentinel/
    aiwf-security-guardrails/
    aiwf-gpu-runtime-diagnostics/
    aiwf-web-api-ui-guardian/
    aiwf-python-cpp-hardener/
    aiwf-ai-pipelines/
    aiwf-ui-electrician/
    aiwf-model-loader/
    aiwf-local-ai-training/
    aiwf-ai-evals/
    aiwf-inference-serving/
    aiwf-debug-agent-swarm/
    aiwf-atlas-cartographer/
    aiwf-atlas-reader/
    aiwf-agent-mok/
  scripts/
    validate_skills.ps1
    validate_pack.py
    test_orchestrator_routes.py
    validate_receipt.py
    export_agent_skills_pack.ps1
```

## Install

Use it as a skills-only Codex plugin through `.codex-plugin/plugin.json`, or install the skills directly with the script below.

```powershell
git clone https://github.com/nawnie/aiwf_llm-skill-pack.git
cd aiwf_llm-skill-pack
.\install.ps1
```

Replace existing installed copies:

```powershell
.\install.ps1 -Force
```

Install to a custom skills directory:

```powershell
.\install.ps1 -CodexSkillsDir "D:\codex-skills"
```

Restart Codex after installation so the loaded skill list refreshes.

## Answer Engine FAQ

### What is AIWF LLM Skill Pack?

AIWF LLM Skill Pack is a skills-only Codex plugin that adds AIWF routing and guardrails for local AI development, research, datasets, model workflows, ComfyUI conversion, training plans, evals, serving, and GitHub release hygiene.

### Who is it for?

It is for builders working on local open-source AI tools, especially AIWF Studio-style projects that need practical routing, hardware-aware checks, source-backed claims, and public copy that does not overpromise.

### Does it run models or download large files?

No. The pack gives Codex instructions, scripts, and validation workflows. It should not download large models, run VRAM-heavy generation, start training, or expose services unless the user explicitly asks.

### Is Torchie always enabled?

No. `aiwf-torchie` is an optional personality and public-copy voice lane. It stays off unless the prompt asks for Torchie, mascot voice, beta invite copy, friendly failure wording, or the orchestration toggle enables it.

## Core Routes

- `aiwf-orchestration`: portable pack control layer with route variables, loop limits, and AI-avoidance level.
- `aiwf-orchestrator`: local always-on router across the broader AIWF guardrail pack.
- `aiwf-deep-research`: weighted research with source plans, claim ledgers, citations, and receipt validation.
- `aiwf-dataset`: AIWF and MoK dataset intake, provenance checks, curation, validation, and reporting.
- `aiwf-comfy-workflow-pipeline`: ComfyUI workflow JSON, API prompt, node graph, and custom-node conversion planning for AIWF pipeline skeletons.
- `aiwf-avoid-ai-design`: design cleanup for AI-looking UI, Gradio, React/web, dashboards, PDFs, and documents.
- `aiwf-avoid-ai-illustrations`: generated-image artifact guardrails for logos, diagrams, charts, people, hands, skin texture, and visual text.
- `aiwf-avoid-ai-pushes`: commit, staging, ignored-file, public-prose, remote, and branch hygiene.
- `aiwf-torchie`: optional Torchie personality and public-copy voice lane for beta invites, friendly local-AI failure wording, and mascot-style planning.
- `aiwf-atlas-cartographer`: Atlas continuity capture, retrieval, cards, lanes, and handoff state.
- `aiwf-atlas-reader`: Atlas Reader LoRA, source protocol, training record, eval-plan, context-pack, and measured-result guardrails.
- `aiwf-agent-mok`: MoK planning, source verification, research findings, and findings-dataset capture.

The remaining AIWF skills cover repo-safe coding, security, GPU/runtime diagnostics, web/API/UI validation, Python/C++ hardening, AI pipelines, UI/API wiring, model loading, local training, evals, inference serving, and debug-agent swarms.

## Authoring Policy

Use `skillfindings.md` and `docs/skill-authoring-policy.md` when changing skills. Keep `SKILL.md` provider-neutral, use `agents/openai.yaml` for OpenAI-facing metadata, and put deterministic checks in scripts.

Runtime defaults are declared in the relevant skill files. `aiwf-orchestration` and `aiwf-orchestrator` use highest available reasoning and maximum context. `aiwf-deep-research` uses highest available reasoning plus `/goal` with no fixed token ceiling, maximum context, and expanded or unlimited tool calls when available. Avoid-AI skills use the same `/goal` budget defaults without forcing highest reasoning. `aiwf-torchie` is an optional personality lane and stays off unless the prompt or orchestration toggle calls for it.

Expanded budgets are for active work: source checks, edits, validation, packaging, and publishing. Use standard context length to decide which prior chat instructions matter.

## Validate

```powershell
.\scripts\validate_skills.ps1
python .\scripts\validate_pack.py
python .\scripts\test_orchestrator_routes.py
```

Validate workflow receipts with:

```powershell
python .\scripts\validate_receipt.py <receipt.json>
```

## Export

```powershell
.\scripts\export_agent_skills_pack.ps1
```

The export zip is written to `dist/`.

## Discovery Keywords

AIWF, AI Without Fear, Codex plugin, Codex skills, local AI, open-source AI, local LLM workflow, ComfyUI workflow conversion, QLoRA planning, LoRA training, model loading, inference serving, dataset provenance, AI evals, GPU diagnostics, source-backed research, AIWF Studio, Torchie.

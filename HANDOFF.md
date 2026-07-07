# Agent Skills Handoff

Created: 2026-06-30
Updated: 2026-07-06

## What This Is

This is a Desktop project for Shawn's custom Codex skills and skill-pack work.

Project path:

```text
C:\Users\Shawn\Desktop\AI_Projects\Agent Skills
```

`AI_Projects` was moved from:

```text
C:\Users\Shawn\Desktop\sort desktop\AI_Projects
```

to:

```text
C:\Users\Shawn\Desktop\AI_Projects
```

## Current Skill Set

Shawn-owned AIWF skills were renamed from the original global copies into canonical `aiwf-` skill names:

- `aiwf-ai-pipelines` from `ai-pipelines`
- `aiwf-ui-electrician` from `ui-electrician`
- `aiwf-model-loader` from `model-loader`
- `aiwf-debug-agent-swarm` from `debug-agent-swarm`
- `aiwf-atlas-cartographer` from `atlas-cartographer`
- `aiwf-agent-mok` from `agent-mok`

New AIWF skills added in this workspace:

- `aiwf-orchestrator`, always-on prompt routing for non-trivial local AI work
- `aiwf-orchestration`, portable pack control layer with route variables, AI-avoidance level, loop limits, and provider-adapter policy
- `aiwf-deep-research`, weighted source-backed deep research with source plans, claim ledgers, citations, source weights, Civitai/resource handling, open-source library checks, academic-source weighting, and Reddit limits
- `aiwf-dataset`, AIWF and MoK dataset intake, provenance checks, curation, validation, reporting, and synthetic guardrail boundaries
- `aiwf-comfy-workflow-pipeline`, ComfyUI workflow JSON, API prompt, node graph, custom-node mapping, and Python pipeline skeleton planning
- `aiwf-avoid-ai-design`, design cleanup for AI-looking UI, Gradio, React/web, dashboards, PDFs, and document layouts
- `aiwf-avoid-ai-illustrations`, generated-image artifact guardrails for logos, diagrams, charts, visual text, photoreal people, hands, anatomy, skin texture, and final image QA
- `aiwf-avoid-ai-pushes`, commit, staging, ignored-file, public-prose, remote, and branch hygiene
- `aiwf-torchie`, optional Torchie personality and public-copy voice lane for AIWF beta copy, friendly local-AI failure wording, and mascot-style planning
- `aiwf-ai-coding-guardrails`, repo-safe coding guardrails for AI-generated edits and existing-repository code work
- `aiwf-repo-sentinel`, repository preflight, package-manager, shell, test-integrity, and diff-discipline guardrails
- `aiwf-security-guardrails`, auth, CORS, secrets, injection, unsafe serialization, dependency supply-chain, and model-source trust guardrails
- `aiwf-gpu-runtime-diagnostics`, CUDA, ROCm, NVIDIA driver, PyTorch, TensorRT, VRAM, DLL/PATH, and GPU smoke diagnostics
- `aiwf-web-api-ui-guardian`, FastAPI, Gradio, React, TypeScript, JavaScript, HTML, CSS, API-contract, and UI validation guardrails
- `aiwf-python-cpp-hardener`, Python, C++, CMake, async, serialization, typing, toolchain, and memory-safety guardrails
- `aiwf-local-ai-training`, local LoRA, QLoRA, fine-tune, dataset, checkpoint, export, and validation planning
- `aiwf-ai-evals`, eval suites, smoke receipts, before/after comparisons, and acceptance gates
- `aiwf-inference-serving`, local serving with vLLM, llama.cpp, Ollama, OpenAI-compatible APIs, telemetry, queueing, and latency checks
- `aiwf-atlas-reader`, imported from Shawn's `nawnie/atlas-lora-adapter` Atlas protocol plugin and renamed under the AIWF pack policy

Pack boundary:

- The repository now vendors Shawn-owned `aiwf-` skills only. Do not copy outside skill folders, outside license files, or external branding into this workspace.

## Current Intent

Use this folder as the clean project workspace for:

- AIWF branded skill-pack work.
- Exportable/shareable skill bundles.
- Iterating skills before syncing them back to global Codex installs.
- Keeping provider-neutral skill cores plus provider-specific adapters.
- Clean handoff between Codex sessions.

## Runtime Budget Defaults

- `aiwf-orchestration` and `aiwf-orchestrator` default to highest available reasoning and maximum available context.
- `aiwf-deep-research` defaults to highest available reasoning and `/goal` with no fixed token ceiling, maximum context, and expanded or unlimited tool calls when available.
- Avoid-AI skills default to `/goal` with no fixed token ceiling, maximum context, and expanded or unlimited tool calls when available, without forcing highest reasoning unless the task warrants it.
- `aiwf-torchie` is a personality lane and should stay off unless the prompt or orchestration toggle calls for it.
- Expanded budgets apply to active work, not broad chat review. Use standard context length to decide which prior chat should be included.

## First Commands

Validate local skill copies:

```powershell
cd "C:\Users\Shawn\Desktop\AI_Projects\Agent Skills"
.\scripts\validate_skills.ps1
python .\scripts\test_orchestrator_routes.py
```

Export a shareable zip:

```powershell
.\scripts\export_agent_skills_pack.ps1
```

## Next Useful Step

Decide whether this project becomes the source of truth for Shawn's custom skills. If yes, future changes should happen here first, then sync into `C:\Users\Shawn\.codex\skills` only after validation.

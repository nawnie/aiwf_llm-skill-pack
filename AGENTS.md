# Agent Skills Project Instructions

## Scope

This project is the shareable workspace for Shawn's AIWF and agent workflow Codex skills.

Work inside this folder unless Shawn explicitly asks to sync changes back into global Codex skills.

## Rules

- Shawn-owned AIWF skills use canonical folder names and `SKILL.md` frontmatter names prefixed with `aiwf-`.
- Shawn-owned AIWF skills use `aiwf_` display names in `agents/openai.yaml`.
- This repository vendors Shawn-owned `aiwf-` skills only. Do not add outside skill folders, outside license files, or external branding.
- Prefer editing the project-local copies first, then sync or export deliberately.
- Do not include generated zip files, caches, debug passes, or temporary work in source control.
- Validate changed skills with `scripts/validate_skills.ps1`.
- Validate orchestrator route behavior with `scripts/test_orchestrator_routes.py` after route changes.
- Validate durable workflow receipts with `scripts/validate_receipt.py` when receipt files are produced.
- Export shareable packages with `scripts/export_agent_skills_pack.ps1`.

## Runtime Budget Defaults

- `aiwf-orchestrator` should use the highest available reasoning and maximum available context length.
- `aiwf-deep-research` should use the highest available reasoning and, when available, `/goal` with no fixed token ceiling, maximum context, and unlimited or expanded tool-call limits.
- Avoid-AI skills should use `/goal` with no fixed token ceiling, maximum context, and unlimited or expanded tool-call limits when available, but should not force highest reasoning unless the task warrants it.
- Expanded budgets apply to active working phases, not to reviewing old chat. Use standard context length to decide how much prior conversation is relevant.

## Included AIWF Skill Lanes

- `aiwf-orchestrator`: always-on prompt routing across the pack.
- `aiwf-orchestration`: portable pack control layer with route variables, AI-avoidance level, loop limits, and provider-adapter policy.
- `aiwf-deep-research`: weighted source-backed deep research across papers, model resources, open-source libraries, academic sources, Reddit with limits, quantum physics, robotics, and mechanical engineering.
- `aiwf-dataset`: AIWF and MoK dataset intake, provenance checks, curation, validation, reporting, and synthetic guardrail boundaries.
- `aiwf-comfy-workflow-pipeline`: ComfyUI workflow JSON, API prompts, node graph inspection, custom-node mapping, and Python pipeline skeleton planning.
- `aiwf-avoid-ai-design`: design cleanup for AI-looking UI, Gradio, React/web, dashboards, PDFs, and document layouts.
- `aiwf-avoid-ai-illustrations`: generated-image artifact guardrails for logos, diagrams, charts, visual text, photoreal people, hands, anatomy, skin texture, and final image QA.
- `aiwf-avoid-ai-pushes`: commit, staging, ignored-file, public-prose, remote, and branch hygiene.
- `aiwf-torchie`: optional Torchie personality and public-copy voice lane that can be toggled on or off.
- `aiwf-ai-coding-guardrails`: repo-safe coding guardrails for AI-generated edits.
- `aiwf-repo-sentinel`: repository preflight, package-manager, shell, test-integrity, and diff-discipline guardrails.
- `aiwf-security-guardrails`: auth, CORS, secrets, injection, unsafe serialization, dependency supply-chain, and model-source trust guardrails.
- `aiwf-gpu-runtime-diagnostics`: CUDA, ROCm, NVIDIA driver, PyTorch, TensorRT, VRAM, DLL/PATH, and GPU smoke diagnostics.
- `aiwf-web-api-ui-guardian`: FastAPI, Gradio, React, TypeScript, JavaScript, HTML, CSS, API-contract, and UI validation guardrails.
- `aiwf-python-cpp-hardener`: Python, C++, CMake, async, serialization, typing, toolchain, and memory-safety guardrails.
- `aiwf-ai-pipelines`: backend pipeline and runtime audit.
- `aiwf-ui-electrician`: UI/API connector and debug-pass audit.
- `aiwf-model-loader`: precision, quantization, backend, and LoRA loader contracts.
- `aiwf-local-ai-training`: LoRA, QLoRA, fine-tune, dataset, checkpoint, export, and validation planning.
- `aiwf-ai-evals`: eval suites, smoke receipts, before/after comparisons, and promotion gates.
- `aiwf-inference-serving`: vLLM, llama.cpp, Ollama, OpenAI-compatible APIs, telemetry, queueing, and latency checks.
- `aiwf-debug-agent-swarm`: read-only subagent debug-pass coordination.
- `aiwf-atlas-cartographer`: Atlas continuity capture and retrieval.
- `aiwf-atlas-reader`: Atlas Reader LoRA, source protocol, training record, eval-plan, context-pack, and measured-result guardrails.
- `aiwf-agent-mok`: MoK structured planning, research verification, and findings.

## Pack Boundary

No outside skills are bundled. Use installed external helpers only as working tools when Shawn asks for them or when local routing has already loaded them; do not copy their files into this repository.

## Handoff

Read `HANDOFF.md` before starting a new session here.

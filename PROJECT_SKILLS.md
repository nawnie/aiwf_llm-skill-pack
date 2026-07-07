# Project Skills

Standing rule: on every non-trivial task in this project, evaluate implicit skill triggers before acting. Prefer the smallest useful skill set, read selected `SKILL.md` files completely, then proceed with narrow edits and verification.

## Project Signals

- This is Shawn's project-local workspace for AIWF and agent workflow Codex skills.
- Work normally stays inside this folder. Syncing to `C:\Users\Shawn\.codex\skills` is deliberate, not automatic.
- Source skills live under `skills/`; package scripts live under `scripts/`; generated zips belong in `dist/` and are ignored.
- Validate changed skills with `scripts/validate_skills.ps1`.
- Validate orchestrator route behavior with `scripts/test_orchestrator_routes.py`.
- Validate durable workflow receipts with `scripts/validate_receipt.py`.
- Export shareable bundles with `scripts/export_agent_skills_pack.ps1`.
- This repository vendors Shawn-owned `aiwf-` skills only. Do not add outside skill folders, outside license files, or external branding.

## Default Route

Use `projectskill-list` first for project skill routing and map maintenance. For AIWF or local AI skill-pack work, route through `aiwf-orchestrator`, then choose the smallest downstream set.

## Skill Routes

| Use case | Skills |
| --- | --- |
| Add, rename, validate, package, or document skills | `projectskill-list`, `skill-creator`, `aiwf-orchestration`, `aiwf-orchestrator` |
| Deep research, source weighting, literature review, source plans, claim ledgers, citations, arXiv/Hugging Face/GitHub/Civitai/Reddit, open-source libraries, academic sources, quantum, robotics, or mechanical engineering | `aiwf-deep-research`, `aiwf-agent-mok` |
| Dataset intake, source provenance, curation, validation, reporting, multimodal caption QA, or synthetic guardrail dataset boundaries | `aiwf-dataset`, `aiwf-agent-mok` |
| ComfyUI workflow JSON, API prompts, node graph inspection, custom-node mapping, or Python pipeline skeleton conversion | `aiwf-comfy-workflow-pipeline`, `aiwf-ai-pipelines`, `aiwf-model-loader` |
| AI-looking UI, default Gradio/shadcn styling, teal-heavy design, generated-looking dashboards, PDFs, document layouts, or web surfaces | `aiwf-avoid-ai-design`, `aiwf-web-api-ui-guardian` |
| Generated images, AI illustrations, logos, diagrams, charts, visual text, photoreal people, hands, anatomy, skin texture, or final image QA | `aiwf-avoid-ai-illustrations`, `aiwf-deep-research` |
| Torchie, mascot voice, beta invite copy, friendly local-AI failure wording, or AIWF public copy in the Torchie voice | `aiwf-torchie`, `aiwf-avoid-ai-pushes` |
| Existing-repo coding or generated-code cleanup | `aiwf-ai-coding-guardrails`, `aiwf-repo-sentinel` |
| Security, auth, secrets, unsafe inputs, dependency supply chain, or model-source trust | `aiwf-security-guardrails` |
| CUDA, ROCm, NVIDIA driver, PyTorch GPU, TensorRT, VRAM, DLL/PATH, or GPU smoke failures | `aiwf-gpu-runtime-diagnostics` |
| Python, C++, or CMake hardening | `aiwf-python-cpp-hardener` |
| FastAPI, Gradio, React, TypeScript, JavaScript, HTML, or CSS work | `aiwf-web-api-ui-guardian`, `aiwf-ui-electrician` |
| AIWF backend pipeline or runtime audit | `aiwf-ai-pipelines` |
| Model loading, precision, quantization, LoRA compatibility, or backend selection | `aiwf-model-loader` |
| LoRA, QLoRA, fine-tune, dataset, checkpoint, export, or validation planning | `aiwf-local-ai-training`, `aiwf-ai-evals` |
| vLLM, llama.cpp, Ollama, OpenAI-compatible APIs, telemetry, queueing, or latency checks | `aiwf-inference-serving` |
| Eval suites, smoke receipts, before/after comparisons, or promotion gates | `aiwf-ai-evals` |
| Broad debug crawls or explicit subagent swarms | `aiwf-debug-agent-swarm` |
| Atlas continuity, compaction handoff, local cards, or resume state | `aiwf-atlas-cartographer` |
| Atlas Reader LoRA repo, Atlas adapter, training records, eval plans, context-pack construction, Qwen LoRA failures, or measured-result claims | `aiwf-atlas-reader`, `aiwf-atlas-cartographer`, `aiwf-agent-mok` |
| MoK planning, verification, research findings, or findings datasets | `aiwf-agent-mok` |
| Public docs, release text, commit scope, ignored files, staging, or GitHub push hygiene | `aiwf-avoid-ai-pushes` |

## Guardrails

- Do not download large models, run VRAM-heavy generation, start training, or expose public services unless Shawn explicitly asks.
- Prefer editing project-local copies first; sync/export deliberately after validation.
- Keep the pack Shawn-owned only; external helpers may guide work but should not be vendored.
- Do not include generated zips, caches, debug passes, or temporary work in source control.
- If global skills are changed, restart Codex so the loaded skill list refreshes.
- Runtime budget defaults: `aiwf-orchestrator` uses highest available reasoning and maximum context; `aiwf-deep-research` uses highest available reasoning plus `/goal` with no fixed token ceiling, maximum context, and expanded or unlimited tool calls when available; avoid-AI skills use the same `/goal` budget defaults without forcing highest reasoning.
- `aiwf-torchie` is an optional personality lane. Keep it off unless Shawn asks for Torchie-style output or turns the personality toggle on.
- Expanded budgets are for active work, not broad chat review. Use standard context length to choose relevant prior chat.

## Verification

Use these checks after relevant changes:

```powershell
.\scripts\validate_skills.ps1
python .\scripts\test_orchestrator_routes.py
.\scripts\export_agent_skills_pack.ps1
```

Run export only when a shareable bundle is actually wanted.

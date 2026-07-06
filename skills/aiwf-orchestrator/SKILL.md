---
name: aiwf-orchestrator
description: Always-on AIWF skill routing orchestrator. Use at the start of non-trivial local AI, AIWF, model loading, training, evaluation, inference serving, GPU runtime diagnostics, security guardrails, repository coding, generated-code guardrail, UI/API, debugging, research, documentation, or skill-pack work to infer the right downstream skill route from the user's prompt, even when the user does not explicitly name a skill.
---

# AIWF orchestrator

Use this skill as the first routing layer for AIWF, local AI, and AIWF-owned repository coding work. It decides which pack skill should handle the request, then hands off to the smallest useful set.

## Always-on behavior

When this skill is loaded, do not solve the task by itself unless the user only asks which skill applies. Pick downstream skills, announce the route briefly, then read those skills before acting.

## Runtime Defaults

Use the highest available reasoning and maximum available context length whenever this orchestrator is the active routing skill.

Keep routing cheap in what it loads. Expanded context, unlimited budgets, and expanded tool-call usage apply to the active working phase after the route is chosen, not to reviewing old chat. Use standard context length to decide how much prior conversation is relevant; include the current request, current project instructions, active handoff/plan, and recent receipts, but do not mine unrelated chat history unless Shawn asks.

## Workflow

1. Check whether the user explicitly named a skill. Use that skill unless it conflicts with the task.
2. If no skill is named, infer intent from the prompt using `references/routing-map.md`.
3. For ambiguous prompts, choose the skill that owns the first irreversible or expensive decision.
4. Use the smallest useful set. Add another skill only when the task crosses a real boundary.
5. Announce:

```text
Route: aiwf-orchestrator -> <skills>; reason: <short reason>
```

6. Read every selected downstream `SKILL.md` before editing files, running services, starting training, or publishing output.
7. Respect gates:
   - no large downloads unless asked
   - no training unless asked
   - no public network exposure unless asked
   - no GPU-heavy generation unless asked
   - no destructive git or filesystem operations unless asked
   - no major dependency upgrades, package-manager switches, broad rewrites, or weakened tests unless asked
   - no weakened security boundary unless asked

## Optional helper

Use the classifier when the prompt is broad or you want a quick route suggestion:

```powershell
python <this-skill>\scripts\route_prompt.py --prompt "train a qlora and test it"
```

The helper is advisory. The agent remains responsible for checking project instructions and current files.

## Common routes

- Training or fine-tuning: `aiwf-local-ai-training`, then `aiwf-ai-evals`.
- Model load, precision, quantization, LoRA compatibility: `aiwf-model-loader`.
- Serving, local endpoints, OpenAI-compatible API, queueing, telemetry: `aiwf-inference-serving`.
- Backend route readiness, smoke matrix, model-source mismatch: `aiwf-ai-pipelines`.
- UI/API state, progress, cancellation, client errors: `aiwf-ui-electrician`.
- Benchmarks, prompt suites, visual receipts, promotion gates: `aiwf-ai-evals`.
- Broad debug crawl or subagents: `aiwf-debug-agent-swarm`.
- Deep research, source weighting, literature review, source plans, claim ledgers: `aiwf-deep-research`, then `aiwf-agent-mok` when a durable plan or findings dataset is needed.
- Research planning, verification, findings datasets: `aiwf-agent-mok`.
- Continuity cards or handoff state: `aiwf-atlas-cartographer`.
- Atlas Reader LoRA repo, Atlas adapter, context-pack, eval plans, or measured-result claims: `aiwf-atlas-reader`.
- Dataset intake, source provenance, curation, reporting, or synthetic guardrail datasets: `aiwf-dataset`.
- AI-looking UI, Gradio, React/web, PDF, document, or dashboard design cleanup: `aiwf-avoid-ai-design`.
- Public docs, release text, commit scope, or push hygiene: `aiwf-avoid-ai-pushes`.
- Existing-repository coding, generated-code cleanup, or broad code review: `aiwf-ai-coding-guardrails`, then add focused guardrails as needed.
- Repo preflight, dirty tree, package manager, shell, test integrity, or diff scope: `aiwf-repo-sentinel`.
- Security, auth, CORS, secrets, injection, unsafe deserialization, dependency supply chain, model-source trust, or public exposure: `aiwf-security-guardrails`.
- CUDA, ROCm, NVIDIA driver, PyTorch GPU, TensorRT, xformers, flash-attn, bitsandbytes, VRAM, DLL/PATH, or GPU smoke failure: `aiwf-gpu-runtime-diagnostics`.
- FastAPI, Gradio, React, TypeScript, JavaScript, HTML, CSS, API contract, Vite, or UI validation: `aiwf-web-api-ui-guardian`.
- Python, C++, CMake, async, serialization, type shortcuts, toolchain, compiler, or memory-safety work: `aiwf-python-cpp-hardener`.
- Generated images, AI illustrations, logos, diagrams, charts, infographics, photoreal portraits, hands, fingers, skin texture, visual text, or final image QA: `aiwf-avoid-ai-illustrations`.

## Output

For routing-only requests, return the selected skill path and why. For implementation requests, keep the route line short and then continue with the selected skill workflow.

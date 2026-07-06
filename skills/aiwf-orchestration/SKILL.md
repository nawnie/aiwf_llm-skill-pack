---
name: aiwf-orchestration
description: AIWF always-on orchestration skill for local open-source AI work. Routes AIWF Studio, model, generation, training, research, dataset, design cleanup, writing guard, and GitHub hygiene tasks through a small set of configurable variables.
---

# AIWF Orchestration

## Orchestration Variables

Edit these values before changing the behavior of the pack. The variable block is the control surface for the skill set.

```yaml
AIWF_ORCHESTRATION_VERSION: 1
AIWF_MAX_AGENT_SPAWN: 3
AIWF_MAX_LOOPS_WITHOUT_PROGRESS: 2
AIWF_AI_AVOIDANCE_LEVEL: 1.0
AIWF_DEEP_RESEARCH_EXTRA_URLS: ""
AIWF_ALWAYS_ON_SKILLS:
  aiwf-orchestration: true
  aiwf-deep-research: false
  aiwf-dataset: false
  aiwf-avoid-ai-design: false
  aiwf-avoid-ai-pushes: false
```

Variable meanings:

- `AIWF_MAX_AGENT_SPAWN`: maximum helper agents or parallel research workers to spawn for one task. Use `0` for no spawned agents, `1` for a single helper, and `3` for the default bounded swarm.
- `AIWF_MAX_LOOPS_WITHOUT_PROGRESS`: stop after this many repeated loops with no new evidence, no passing check, no useful diff, or the same blocker.
- `AIWF_AI_AVOIDANCE_LEVEL`: shared strictness for AI-looking writing, UI design, and push hygiene.
- `AIWF_DEEP_RESEARCH_EXTRA_URLS`: optional comma-separated URLs that `aiwf-deep-research` must include in source planning.
- `AIWF_ALWAYS_ON_SKILLS`: toggles for skills that should be considered on every non-trivial task. `aiwf-orchestration` is always on and should not be disabled in this pack.

Strictness scale:

- `0.1`: effectively off. Only use AI-avoidance skills when the user explicitly asks.
- `1.0`: normal. Fix clear AI-looking prose, UI patterns, and risky push habits without over-editing.
- `2.0`: extreme. Treat borderline AI tells as failures. This is useful for stress testing but can make writing, UI, and workflow rules too strict for normal work.

## Core Rule

Use this skill first for AIWF skill-pack work and for local AI work that touches models, generation, training, datasets, research, UI, docs, repo edits, or GitHub publishing.

Start by reading the variable block. Then classify the task, choose only the needed downstream skills, and stop when progress stalls beyond `AIWF_MAX_LOOPS_WITHOUT_PROGRESS`.

## Runtime Defaults

Use the highest available reasoning and maximum available context length whenever this orchestration skill is active.

Expanded budgets and expanded tool-call usage apply to the working phase after routing: repo inspection, source checks, edits, validation, packaging, and publish steps. Do not spend expanded budget mining old chat. Use standard context length to decide which prior instructions matter, then focus on the current files, active git state, selected skills, and requested output.

When updating skills, keep the portable skill contract in `SKILL.md` and put provider-specific affordances in `agents/openai.yaml`, scripts, or direct references. Use `skillfindings.md` and `docs/skill-authoring-policy.md` as the project-local policy for universal agentic skills and provider adapters.

## Activation Callout

When this orchestration skill is used, state this before task work:

`Orchestration: aiwf-orchestration; downstream skills: <none|skill names>; avoidance-level: <value>; reason: <short reason>`

Use `<none>` when normal repo inspection is enough. If the selected downstream skills change, state the updated list before using them.

## Skill Selection

Use normal effort first for simple file edits, short explanations, path checks, or obvious fixes. Read [references/routing.md](references/routing.md) when the prompt references a harder AIWF pipeline, model, runtime, UI, training, validation, GitHub-writing, or product-research workflow.

Start with at most one downstream skill. Add another only when the task crosses a real boundary, such as deep research plus README writing, UI design cleanup plus React code, or GitHub publishing plus public prose.

Focused routing references:

- Image pipelines: [references/image-pipelines.md](references/image-pipelines.md)
- Video pipelines: [references/video-pipelines.md](references/video-pipelines.md)
- Models, checkpoints, and downloads: [references/model-assets-downloads.md](references/model-assets-downloads.md)
- Quantization and optimization: [references/quantization-optimization.md](references/quantization-optimization.md)
- UI routing: [references/ui-routing.md](references/ui-routing.md)
- Validation: [references/validation.md](references/validation.md)
- AI chat, training, and serving: [references/chat-training-serving.md](references/chat-training-serving.md)

Common downstream selections:

- Pipeline or local runtime work: `local-ai-dev`, `stable-diffusion-image-generation`
- Audio generation: `audiocraft-audio-generation`
- Speech or audio input: `whisper`
- Vision helpers for masks, captions, image-text search, or VLM chat: `segment-anything-model`, `clip`, `blip-2-vision-language`, `llava`
- Hugging Face model search, download, or catalog work: `hugging-face:hf-cli`
- Gradio wiring only: `hugging-face:huggingface-gradio`
- React frontend only: `build-web-apps:react-best-practices`
- AI-looking UI, Gradio, React, web, dashboard, PDF, or document layout cleanup: `aiwf-avoid-ai-design`
- Deep research, source weighting, literature review, source plans, claim ledgers, arXiv, Hugging Face, GitHub, Civitai, Reddit limits, open-source library checks, academic sources, quantum physics, robotics, or mechanical engineering: `aiwf-deep-research`
- Dataset intake, validation, curation, reporting, or synthetic guardrail datasets: `aiwf-dataset`
- GitHub-facing README, docs, commit messages, PR text, release notes, or non-ignored repo prose: `aiwf-avoid-ai-pushes`
- AIWF commit or push scope checks: `aiwf-avoid-ai-pushes`

## Always-On Toggles

Read `AIWF_ALWAYS_ON_SKILLS` before choosing skills.

- If a skill is `true`, consider it for every non-trivial task even when the user did not name it.
- If a skill is `false`, load it only when the prompt, file type, or repo operation matches its trigger.
- Do not disable `aiwf-orchestration`. It is the pack control layer.
- Keep the always-on list small. Too many always-on skills slow down work and increase rule conflicts.

## Deep Research URL Seeds

If `AIWF_DEEP_RESEARCH_EXTRA_URLS` is not empty, pass those URLs to `aiwf-deep-research` as required seed sources. Split on commas, trim spaces, and preserve each URL in the source plan.

Example:

```yaml
AIWF_DEEP_RESEARCH_EXTRA_URLS: "https://arxiv.org/abs/2405.00000, https://github.com/example/project"
```

## AI-Avoidance Level

Apply `AIWF_AI_AVOIDANCE_LEVEL` to:

- public prose scans in `aiwf-avoid-ai-pushes`.
- `aiwf-avoid-ai-design` for UI, PDF, dashboard, and document layout cleanup.
- `aiwf-avoid-ai-pushes` for public repo, commit, and push hygiene.

At `0.1`, only catch credibility failures and secrets-risk workflow errors. At `1.0`, use the normal skill rules. At `2.0`, treat every borderline AI-looking pattern as a fix candidate and be explicit that this can reduce usefulness.

## AIWF Validation Defaults

Prefer cheap receipts before heavy runs:

```powershell
venv\Scripts\python.exe scripts\smoke_models_and_pipelines.py
venv\Scripts\python.exe scripts\smoke_backend.py --video --list
venv\Scripts\python.exe -m pytest tests\individual_tests\test_pipeline_preflight.py tests\individual_tests\test_pipeline_registry.py -q
```

For video pipeline work, add focused Wan or LTX tests. For UI work, add the relevant Gradio or React tests. For chat or training work, validate the local API, worker, or training command in dry-run or probe mode when available.

## Scope Discipline

- Do not install or download large models unless the user explicitly asks.
- Do not consume VRAM for generation or training when metadata, preflight, list-mode, dry-run, or probe validation answers the request.
- Do not silently change existing engines when the user asks for one engine or pipeline.
- Surface missing local assets explicitly, including exact model path and expected format.
- If a changed file is not ignored by git, run the configured AI-avoidance prose check before finalizing.

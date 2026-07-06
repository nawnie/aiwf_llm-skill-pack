---
name: aiwf-ai-pipelines
description: AIWF pipeline backend audit skill. Use when reviewing local AI app pipeline wiring, engine/runtime selection, model card or arXiv alignment, GGUF or llama.cpp paths, lm-evaluation-harness readiness, Civitai fine-tune compatibility, UI/API connector bugs, generation route maturity, smoke receipts, model readiness matrices, and backend issue triage across image, video, audio, and LLM pipelines.
---

# AI Pipelines

Use this skill to audit a local AI application from backend to UI connector without spending GPU time by default. Start with local receipts, then compare runtime assumptions against primary model sources, then split independent lanes across subagents when useful.

## Operating Rules

- Prefer the project repo, local logs, readiness matrices, receipts, tests, and route definitions over README claims.
- Do not download large models, run training, or start VRAM-heavy generation unless the user explicitly asks.
- Treat model formats as first-class runtime contracts: Diffusers snapshot, single-file safetensors, GGUF, Nunchaku, ONNX, llama.cpp server, vLLM, or external API.
- Separate findings into `bug`, `missing wiring`, `asset/config issue`, `model-runtime mismatch`, `docs/status drift`, and `needs source research`.
- Verify source claims with primary sources: Hugging Face model cards/files, upstream GitHub, arXiv papers, Civitai model pages for fine-tunes, and local artifact receipts.
- When using subagents, use debug-pass reporting: subagents log issues to Markdown and the parent agent implements fixes.

## Workflow

1. Read project instructions (`AGENTS.md`, local skill maps, release plans if current).
2. Run the local crawler:

```powershell
python C:\Users\Shawn\.codex\skills\aiwf-ai-pipelines\scripts\audit_backend.py --root F:\AIWF_Studio --out F:\AIWF_Studio\.codex\aiwf-ai-pipelines\latest
```

3. Read the generated `audit.md` and `audit.json`.
4. If the user authorizes agents, create a debug pass folder and spawn explorer agents only after the local crawl identifies independent lanes. Good lanes are:
   - Image backend/runtime: Diffusers, Flux, Flux.2, Z-Image, Qwen, Sana image.
   - Video backend/runtime: Sana Video, Wan Diffusers/GGUF, LTX, RIFE/VSR post stages.
   - LLM/GGUF/runtime: llama.cpp, Ollama/vLLM paths, lm-evaluation-harness readiness.
   - UI/API connectors: FastAPI/React Pro, Gradio callbacks, client logs, runtime streams.
5. For each model family, compare local route assumptions to source truth:
   - Base model card and files on Hugging Face.
   - Upstream GitHub or arXiv for architecture/runtime constraints.
   - Civitai page for fine-tunes when a local checkpoint looks custom or non-standard.
6. Read any debug-pass reports, deduplicate findings, then convert confirmed issues into a short patch plan. Patch only clear, bounded bugs. Leave model asset/download gaps as explicit follow-up unless the user asks to download or test live generation.
7. Verify with targeted compile/tests/smokes, not full GPU generation by default.

## Source Research Rules

Read `references/model-source-checks.md` before making model-card, paper, Civitai, or quantization claims.

When using research:
- Cite exact source URLs in the final report.
- Distinguish confirmed source facts from local inference.
- For GGUF/llama.cpp paths, use `gguf-quantization` and `llama-cpp` guidance: Q4_K_M as the default balanced check, Q5_K_M/Q6_K/Q8_0 for quality, and imatrix for Q4 and below when quantizing.
- For LLM benchmark readiness, use `evaluating-llms-harness` guidance: do not run expensive benchmarks unless requested; audit whether model path, tokenizer, dtype, quantization, and server mode can be passed to `lm_eval`.

## Subagent Pattern

Use `aiwf-debug-agent-swarm` conventions when the user authorizes agents. Read `C:\Users\Shawn\.codex\skills\aiwf-ui-electrician\references\debug-pass-protocol.md` first so backend, frontend, and connector agents produce the same kind of artifact.

Subagents are read-only issue loggers by default:

- They write one Markdown report per lane into the selected debug pass folder.
- They describe issues, evidence, impact, affected files/routes, confidence, and research used.
- They do not write implementation recipes or broad fix plans.
- They may edit only for a simple syntax fix of three changed lines or fewer, and must record exact lines changed.
- They read only parent-provided context, `SUB_AGENTS.md` if present, or the `Known Issues` section of `AGENTS.md`.
- If no source research is used, confidence must be 90/100 or higher.

Recommended prompts:

```text
Use the AI pipeline audit skill at C:\Users\Shawn\.codex\skills\aiwf-ai-pipelines to inspect F:\AIWF_Studio. Focus only on <lane>. Write your report to <debug-pass>\<lane>.md using the debug-pass protocol. Report issues, evidence, impact, confidence, and source/model mismatches. Do not explain the fix. Do not edit files unless the entire repair is a syntax fix of three changed lines or fewer.
```

```text
Use the AI pipeline audit skill at C:\Users\Shawn\.codex\skills\aiwf-ai-pipelines to inspect <bounded issue> in F:\AIWF_Studio. Own only <lane>. Write findings to <debug-pass>\<lane>.md. The parent agent will implement the fix after reading reports.
```

## Output Format

Report:
- Local artifacts reviewed.
- Source URLs checked.
- Findings ranked by severity.
- Fixes made, with files changed.
- Commands run and results.
- Remaining model/runtime research gaps.

Keep the report explicit about whether a route is `smoked`, `registered`, `metadata-only`, `broken-runtime`, or `blocked-cleanly`.

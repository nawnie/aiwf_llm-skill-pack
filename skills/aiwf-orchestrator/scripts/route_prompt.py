from __future__ import annotations

import argparse
import json
import re


RULES: list[tuple[str, str, str]] = [
    (r"\b(code|coding|bug|fix|debug|refactor|review|generated code|ai[- ]?generated|patch|implementation)\b", "aiwf-ai-coding-guardrails", "repo-safe coding guardrails"),
    (r"\b(repo|repository|dirty tree|git status|package manager|lockfile|npm|pnpm|yarn|poetry|uv|powershell|shell|broad diff|weaken tests?|skip tests?|staging|commit|push|ignored files?)\b", "aiwf-repo-sentinel", "repository preflight or diff discipline"),
    (r"\b(security|auth|authorization|cors|csrf|secret|token|api key|injection|xss|ssrf|path traversal|unsafe deserialization|unsafe serialization|pickle|yaml\.load|shell=True|dependency supply|supply chain|public exposure|model source trust|vulnerabilit(y|ies))\b", "aiwf-security-guardrails", "security boundary or supply-chain guardrail"),
    (r"\b(cuda|rocm|nvidia|driver|gpu|vram|oom|out of memory|pytorch gpu|torch cuda|tensorrt|xformers|flash[-_ ]?attn|bitsandbytes|directml|dll|path issue|device visibility|gpu smoke)\b", "aiwf-gpu-runtime-diagnostics", "GPU runtime diagnostics"),
    (r"\b(fastapi|gradio|react|typescript|javascript|html|css|vite|openapi|frontend|backend|api contract|pydantic|ui validation|accessibility)\b", "aiwf-web-api-ui-guardian", "web API or UI guardrail"),
    (r"\b(python|pytest|ruff|pyright|mypy|async|serialization|pickle|yaml\.load|c\+\+|cmake|compiler|preset|memory safety|raii|cpp (file|code|source|project|extension))\b", "aiwf-python-cpp-hardener", "Python, C++, or CMake hardening"),
    (r"\b(image generation|generated images?|generate an image|generate a picture|ai art|ai illustration|ai-looking image|ai artifacts?|illustrations?|logos?|icons?|signage|visual text|typography|diagram|flowchart|architecture figure|chart|infographic|portrait|photoreal|photorealism|hands?|fingers?|anatomy|skin texture|pores?|pimples?|cysts?|blemish|misspelled text|bad hands?|extra fingers?|missing fingers?)\b", "aiwf-avoid-ai-illustrations", "generated-image artifact guardrail"),
    (r"\b(comfyui|comfy ui|workflow json|api prompt|node graph|custom nodes?|object_info|pipeline skeleton|workflow conversion)\b", "aiwf-comfy-workflow-pipeline", "ComfyUI workflow conversion"),
    (r"\b(deep research|literature review|source plan|source weighting|evidence weight|evidence_weight|claim ledger|weighted source|arxiv|openreview|reddit limits?|academic sources?|college|graduate|postgraduate|thesis|dissertation|quantum physics|robotics research|mechanical engineering research)\b|\b(research|verify|source-backed|source backed)\b.*\b(civitai|hugging face|github|arxiv|reddit|quantum|robotics|mechanical)\b|\b(civitai|hugging face|github|arxiv|reddit|quantum|robotics|mechanical)\b.*\b(research|verify|source-backed|source backed)\b", "aiwf-deep-research", "weighted source-backed deep research"),
    (r"\b(train|training|fine[- ]?tune|finetune|lora|qlora|checkpoint|resume|dataset split)\b", "aiwf-local-ai-training", "training or dataset readiness"),
    (r"\b(evals?|benchmarks?|lm[-_ ]?eval|prompt suites?|before.?after|regression|acceptance|promote|promotion|smoke receipts?)\b", "aiwf-ai-evals", "eval or promotion gate"),
    (r"\b(serve|serving|endpoint|api|vllm|llama\.cpp|ollama|openai-compatible|latency|queue|reload|unload)\b", "aiwf-inference-serving", "inference service or endpoint"),
    (r"\b(load|loader|dtype|precision|quant|quantize|quantization|gguf|safetensors|nunchaku|projector|vae|adapter compatibility)\b", "aiwf-model-loader", "model loader contract"),
    (r"\b(pipeline|route|backend|runtime wiring|smoke matrix|model source|civitai|hugging face)\b", "aiwf-ai-pipelines", "pipeline readiness or source mismatch"),
    (r"\b(ui|frontend|button|progress|cancel|cancellation|toast|poll|sse|websocket|payload|response shape|telemetry display)\b", "aiwf-ui-electrician", "UI/API connector"),
    (r"\b(subagent|swarm|parallel agents|debug pass|crawl|broad debug)\b", "aiwf-debug-agent-swarm", "parallel debug crawl"),
    (r"\b(research|verify|plan\.md|findings|mental model|source-backed|provenance)\b", "aiwf-agent-mok", "research or verification map"),
    (r"\b(handoff|continuity|cartographer|compact|resume later|cards)\b", "aiwf-atlas-cartographer", "continuity capture"),
    (r"\b(atlas reader|atlas lora|atlas adapter|context[- ]pack|qwen lora|lora-trained|training records?|evaluation plans?|measured logs?|no-wins)\b", "aiwf-atlas-reader", "Atlas Reader protocol guardrails"),
    (r"\b(dataset|datasets|curation|source registry|source provenance|dataset card|synthetic guardrail|captioning|receipt validation)\b", "aiwf-dataset", "dataset provenance or curation"),
    (r"\b(ai-looking design|ai design|teal everywhere|default gradio|default shadcn|de-slop ui|generated-looking|design cleanup|document layout|pdf report|dashboard design)\b", "aiwf-avoid-ai-design", "AI-looking design cleanup"),
    (r"\b(torchie|tiny robot|mascot voice|field[- ]?tech humor|beta invite|friendly failure|crash explanation|oom explanation|local-ai failure)\b", "aiwf-torchie", "Torchie personality or public-copy voice"),
    (r"\b(readme|docs|documentation|release notes|copy|ai writing|ai-isms|public text|commit|push|github-facing|staging|ignored files?)\b", "aiwf-avoid-ai-pushes", "public prose and push hygiene"),
]


def route(prompt: str) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    seen: set[str] = set()
    for pattern, skill, reason in RULES:
        if re.search(pattern, prompt, re.IGNORECASE) and skill not in seen:
            selected.append({"skill": skill, "reason": reason})
            seen.add(skill)
    if not selected:
        selected.append({"skill": "aiwf-agent-mok", "reason": "general non-trivial AIWF planning"})
    return selected


def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest AIWF skill routes from a prompt.")
    parser.add_argument("--prompt", required=True)
    args = parser.parse_args()
    print(json.dumps({"selected": route(args.prompt)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

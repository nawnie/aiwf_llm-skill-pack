from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass


MAX_SKILLS = 4
MAX_FOCUSED_SECURITY_SKILLS = 2
FOCUSED_SECURITY_SKILLS = {
    "aiwf-application-api-security",
    "aiwf-online-infrastructure-security",
    "aiwf-local-device-security",
    "aiwf-data-privacy-protection",
    "aiwf-software-ai-supply-chain-security",
    "aiwf-incident-response-recovery",
}


@dataclass(frozen=True)
class Rule:
    pattern: str
    skill: str
    reason: str
    priority: int


RULES = [
    Rule(r"\b(fix|debug|patch|refactor|implement|update|change|code review|review .*code|without breaking tests|repo|repository|dirty tree|package manager|lockfile|staging|commit|push)\b", "aiwf-repo-sentinel", "repository preflight and diff integrity", 5),
    Rule(r"\b(security|cybersecurity|privacy|auth|authorization|cors|csrf|secret|token|api key|injection|xss|ssrf|path traversal|unsafe (de)?serialization|pickle|yaml\.load|shell=true|supply chain|sbom|public exposure|hardening|incident response|malware|ransomware|data breach|vulnerabilit(?:y|ies))\b", "aiwf-security-guardrails", "security authorization, threat triage, and evidence", 10),
    Rule(r"\b(application security|api security|object[- ]level authorization|session security|cookie security|csrf|cors|xss|sql injection|command injection|ssrf|webhook signature|file upload security|archive extraction|unsafe (?:de)?serialization|prompt injection|llm tool security)\b", "aiwf-application-api-security", "application and API security", 11),
    Rule(r"\b(internet[- ]facing|online infrastructure|public exposure|publicly exposed|dns security|tls certificate|reverse proxy security|cloud iam|vps security|security group|exposed ports?|remote administration|service account|container hardening|network scan)\b", "aiwf-online-infrastructure-security", "online infrastructure security", 12),
    Rule(r"\b(local device security|workstation security|windows hardening|bitlocker|device encryption|secure boot|uac|application control|app control|memory integrity|defender|removable media security|usb security|local credential store)\b", "aiwf-local-device-security", "local device and data security", 13),
    Rule(r"\b(data privacy|privacy protection|personal data|customer data|employee data|pii|data inventory|data classification|data minimization|consent|retention policy|data deletion|privacy notice|soc 2 readiness|iso 27001 readiness|audit evidence)\b", "aiwf-data-privacy-protection", "data privacy and governance", 14),
    Rule(r"\b(software supply chain|ai supply chain|sbom|build provenance|artifact attestation|artifact signing|dependency provenance|package provenance|model provenance security|dataset provenance security|malicious dependency|ci/cd security|release signing)\b", "aiwf-software-ai-supply-chain-security", "software and AI artifact supply chain", 15),
    Rule(r"\b(security incident|incident response|compromised credential|credential leak|account takeover|malware|ransomware|data breach|security containment|forensic evidence|suspicious executable|restore after attack|breach notification)\b", "aiwf-incident-response-recovery", "security incident response and recovery", 16),
    Rule(r"\b(multi[- ]agent|shared agent workspace|agent workspace|codex and claude|claude and codex|codex.*grok|grok.*codex|writer lease|resource lease|rolling (?:chat )?context|last six exchanges|agent handoff)\b", "aiwf-multi-agent-workspace", "shared agent coordination", 18),
    Rule(r"\b(android|kotlin|jetpack compose|gradle\.kts|build\.gradle|room database|retrofit|okhttp|android app|apk|aab|adb|roborazzi|onnxruntime android)\b", "aiwf-android-kotlin-coding", "Android and Kotlin application work", 20),
    Rule(r"\b(c11|c17|c23|iso c|wg14|c source|c code|c header|c library|\.c file|\.h file)\b", "aiwf-c-coding", "C language and ABI work", 20),
    Rule(r"\b(c\+\+|cxx|iso c\+\+|c\+\+17|c\+\+20|c\+\+23|raii|templates?|pybind|native extension|cmake extension|cpp (?:file|code|source|project)|\.(?:cpp|cc|cxx) file)\b", "aiwf-cpp-coding", "C++ and native toolchain work", 20),
    Rule(r"\b(python\s*3\.10|python310|py\s+-3\.10|cp310|requires-python.*3\.10)\b", "aiwf-python310-coding", "Python 3.10 compatibility", 20),
    Rule(r"\b(python\s*3\.12|python312|py\s+-3\.12|cp312|requires-python.*3\.12|distutils removal)\b", "aiwf-python312-coding", "Python 3.12 compatibility", 20),
    Rule(r"\b(cuda|cudnn|nvidia sdk|sdk manager|nvcc|tensorrt|nsight|npp|cupti|nccl|compute capability|sm_[0-9]+)\b", "aiwf-nvidia-cuda-cudnn-sdk", "NVIDIA SDK or GPU code", 20),
    Rule(r"\b(fastapi|pydantic|starlette|uvicorn|openapi|asgi)\b", "aiwf-fastapi-coding", "FastAPI contract work", 20),
    Rule(r"\b(gradio blocks|gradio interface|mount_gradio_app|gradio queue|gradio events?|fix gradio|debug gradio)\b", "aiwf-gradio-coding", "Gradio callback or mount work", 20),
    Rule(r"\b(react|jsx|tsx|hooks?|useeffect|usestate|next\.js|nextjs)\b", "aiwf-react-coding", "React component behavior", 20),
    Rule(r"\b(vue(?:\.js)?|vitepress|composition api|\.vue file|vue reactivity)\b", "aiwf-vue-vitepress-coding", "Vue or VitePress work", 20),
    Rule(r"\b(typescript|tsconfig|tsc|typecheck|moduleresolution|\.ts file|\.tsx file)\b", "aiwf-typescript-coding", "TypeScript contracts", 21),
    Rule(r"\b(javascript|ecmascript|node\.?js|node script|esm|commonjs|cjs|\.js file|\.mjs|\.cjs)\b", "aiwf-javascript-coding", "JavaScript runtime behavior", 21),
    Rule(r"\b(css|stylesheet|cascade|specificity|media quer(?:y|ies)|container quer(?:y|ies)|flexbox|css grid|responsive layout)\b", "aiwf-css-coding", "CSS layout behavior", 21),
    Rule(r"\b(rag|retrieval[- ]augmented|embeddings?|chunking|semantic search|hybrid search|rerank(?:er|ing)?|retrieval eval|context pack|citation grounding)\b", "aiwf-rag-retrieval", "retrieval and grounding quality", 22),
    Rule(r"\b(sqlite|android room|room (?:database|schema|migration|dao|entity|app)|postgres|postgresql|pgvector|chroma(?:db)?|qdrant|milvus|vector store|database migration|schema migration|data integrity)\b", "aiwf-data-storage", "persistent data or vector storage", 23),
    Rule(r"\b(windows local|powershell|python venv|virtual environment|dll|path issue|docker desktop|wsl|port owner|process id|localhost boundary|local service)\b", "aiwf-windows-local-dev", "Windows local runtime", 24),
    Rule(r"\b(seo|technical seo|structured data|json-ld|canonical urls?|sitemaps?|robots meta|crawlability|indexability|search console|javascript seo|rendered metadata)\b", "aiwf-web-seo", "technical website discovery", 25),
    Rule(r"\b(answer[- ]engine optimization|generative[- ]engine optimization|aeo|geo optimization|ai[- ]search visibility|generative search|answer visibility|citation readiness|llms\.txt)\b", "aiwf-aeo-geo", "answer and generative search visibility", 26),
    Rule(r"\b(startup marketing|go[- ]to[- ]market|gtm strategy|ideal customer profile|\bicp\b|positioning statement|channel strategy|growth experiment|marketing funnel|conversion funnel|customer acquisition|activation metric|retention strategy)\b", "aiwf-startup-marketing-growth", "startup marketing and measurable growth", 27),
    Rule(r"\b(startup funding|fundraising|fundraise|runway|burn rate|unit economics|use of funds|investor diligence|angel investors?|venture capital|accelerator|sba (?:loan|funding)|federal grants?|regulation crowdfunding|reg cf|cap table)\b", "aiwf-startup-finance-funding", "startup finance and funding", 28),
    Rule(r"\b(meta business|facebook ads?|instagram business|whatsapp business|meta ads manager|business portfolio|meta pixel|conversions api|meta capi|meta lead forms?|meta account quality)\b", "aiwf-meta-business", "Meta business platform work", 29),
    Rule(r"\b(google ads|adwords|google ads api|google business profile|\bga4\b|google analytics 4|google tag manager|\bgtm container\b|merchant center|google conversion action)\b", "aiwf-google-ads-business", "Google business advertising and measurement", 29),
    Rule(r"\b(youtube|youtube data api|youtube analytics api|youtube partner program|\bypp\b|adsense|channel monetization|youtube channel)\b", "aiwf-youtube-adsense", "YouTube and AdSense operations", 29),
    Rule(r"\b(rnv1|robotics?|ros\s*2|ros2|robot (?:architecture|system|platform|prototype)|perception stack|path planning|robot control|control stack|mobile robot|manipulator)\b", "aiwf-robotics-systems", "robotics systems work", 30),
    Rule(r"\b(physics|simulation|sim[- ]?to[- ]?real|gazebo|mujoco|kinematics|dynamics|coordinate frames?|inertia|friction|contact model|timestep|rigid body)\b", "aiwf-physics-simulation", "physics or simulation", 31),
    Rule(r"\b(networking|iot|mqtt|websocket|rtsp|telemetry|lan|wi[- ]?fi|firewall|nat|vpn|heartbeat|reconnect|secure binding|device network)\b", "aiwf-networking-iot", "networking or IoT", 32),
    Rule(r"\b(embedded|edge ai|edge inference|microcontroller|mcu|rtos|freertos|zephyr|jetson|sbc|firmware|device tree|sensor bus|i2c|spi|uart|can bus|power budget|thermal)\b", "aiwf-embedded-edge-ai", "embedded or edge AI", 33),
    Rule(r"\b(service intake|services inquiry|website lead|customer lead|client brief|quote|scope a first pass|ai fit|workflow cleanup|employee ai training)\b", "aiwf-service-intake", "service lead scoping", 34),
    Rule(r"\b(field pilot|partner pilot|customer[- ]site|site constraints?|field test|operator handoff|rollback plan|go/no-go|hazards?|emergency stop|e[- ]?stop|pilot brief)\b", "aiwf-field-pilot-readiness", "field pilot readiness", 35),
    Rule(r"\b(cuda|rocm|gpu|driver|vram|oom|out of memory|torch cuda|tensorrt|xformers|flash[-_ ]?attn|bitsandbytes|directml|device visibility)\b.*\b(fail|error|broken|missing|install|runtime|diagnos|not found|mismatch)\b|\b(fail|error|broken|missing|install|runtime|diagnos|not found|mismatch)\b.*\b(cuda|rocm|gpu|driver|vram|tensorrt|directml)\b", "aiwf-gpu-runtime-diagnostics", "GPU runtime failure", 36),
    Rule(r"\b(deep research|literature review|source plan|source weighting|evidence weight|claim ledger|weighted source|arxiv|openreview|reddit limits?|academic sources?|thesis|dissertation)\b", "aiwf-deep-research", "source-backed deep research", 40),
    Rule(r"\b(train a model|training run|fine[- ]?tune|finetune|qlora|adapter training|checkpoint|resume training|dataset split)\b", "aiwf-local-ai-training", "model training", 41),
    Rule(r"\b(evals?|benchmarks?|lm[-_ ]?eval|prompt suites?|before.?after|promotion gate|acceptance threshold|regression suite)\b", "aiwf-ai-evals", "evaluation or promotion gate", 42),
    Rule(r"\b(vllm|llama\.cpp server|ollama|model server|inference server|openai-compatible|serve (?:a |the )?model|serving latency|model endpoint)\b", "aiwf-inference-serving", "model serving", 43),
    Rule(r"\b(model load|model loader|dtype|precision|quantize|quantization|gguf|safetensors|nunchaku|projector|vae|adapter compatibility)\b", "aiwf-model-loader", "model loader contract", 44),
    Rule(r"\b(workflow json|api prompt|node graph|pipeline skeleton|source-to-runtime|runtime wiring|pipeline plan|pipeline planning|pipeline route|smoke matrix|model source mismatch)\b", "aiwf-ai-pipelines", "AI pipeline wiring", 45),
    Rule(r"\b(progress stream|cancellation|response shape|payload mismatch|telemetry display|stale polling|sse|ui api|frontend backend|output link)\b", "aiwf-ui-electrician", "UI and API connector", 46),
    Rule(r"\b(subagent|swarm|parallel agents|debug pass|broad crawl)\b", "aiwf-debug-agent-swarm", "parallel debug crawl", 47),
    Rule(r"\b(plan\.md|findings dataset|atlas lanes?|verification map|durable plan)\b", "aiwf-agent-mok", "durable planning or findings", 48),
    Rule(r"\b(continuity|cartographer|compact chat|resume later|continuity cards?|handoff notes?|chat handoff)\b", "aiwf-atlas-cartographer", "continuity capture", 49),
    Rule(r"\b(atlas reader|atlas lora|atlas adapter|qwen lora|lora-trained|training records?|measured logs?|no-wins)\b", "aiwf-atlas-reader", "Atlas Reader protocol", 50),
    Rule(r"\b(dataset|datasets|curation|source registry|source provenance|dataset card|synthetic guardrail|captioning|dataset receipt)\b", "aiwf-dataset", "dataset provenance or curation", 51),
    Rule(r"\b(ai-looking design|ai design|teal everywhere|default gradio|default shadcn|de-slop ui|generated-looking|design cleanup|document layout|pdf report|dashboard design)\b", "aiwf-avoid-ai-design", "design cleanup", 52),
    Rule(r"\b(generate an image|generated images?|ai illustration|ai artifacts?|bad hands?|extra fingers?|missing fingers?|skin texture|misspelled logo|generated chart|generated diagram)\b", "aiwf-avoid-ai-illustrations", "generated-image quality", 53),
    Rule(r"\b(torchie|tiny robot|mascot voice|field[- ]?tech humor|beta invite|friendly failure)\b", "aiwf-torchie", "Torchie voice", 54),
    Rule(r"\b(commit|push|publish|release notes|github-facing|staging|public readme|public docs|ai writing audit)\b", "aiwf-avoid-ai-pushes", "release and push hygiene", 55),
]


def route(prompt: str) -> list[dict[str, str]]:
    matches: dict[str, tuple[int, str]] = {}
    for rule in RULES:
        if re.search(rule.pattern, prompt, re.IGNORECASE):
            current = matches.get(rule.skill)
            if current is None or rule.priority < current[0]:
                matches[rule.skill] = (rule.priority, rule.reason)

    backend = "aiwf-fastapi-coding" in matches or "aiwf-gradio-coding" in matches
    frontend = "aiwf-react-coding" in matches or "aiwf-vue-vitepress-coding" in matches
    if backend and frontend and re.search(r"\b(fix|debug|bug|contract|wiring|payload|response)\b", prompt, re.IGNORECASE):
        matches.setdefault("aiwf-ui-electrician", (22, "cross-layer UI and API connector"))

    if "aiwf-service-intake" in matches and "aiwf-embedded-edge-ai" in matches:
        hardware_signal = re.search(
            r"\b(mcu|microcontroller|rtos|jetson|firmware|sensor|actuator|edge inference|power budget|thermal|robot)\b",
            prompt,
            re.IGNORECASE,
        )
        if not hardware_signal:
            matches.pop("aiwf-embedded-edge-ai")

    if not matches:
        matches["aiwf-agent-mok"] = (99, "general non-trivial AIWF planning")

    ordered = sorted(matches.items(), key=lambda item: (item[1][0], item[0]))
    selected: list[tuple[str, tuple[int, str]]] = []
    focused_security_count = 0
    for item in ordered:
        skill = item[0]
        if skill in FOCUSED_SECURITY_SKILLS:
            if focused_security_count >= MAX_FOCUSED_SECURITY_SKILLS:
                continue
            focused_security_count += 1
        selected.append(item)
        if len(selected) == MAX_SKILLS:
            break
    return [{"skill": skill, "reason": reason} for skill, (_, reason) in selected]


def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest a bounded AIWF skill route.")
    parser.add_argument("--prompt", required=True)
    args = parser.parse_args()
    print(json.dumps({"selected": route(args.prompt), "max_skills": MAX_SKILLS}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

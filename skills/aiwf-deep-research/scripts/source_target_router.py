from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class SourceTarget:
    name: str
    source_class: str
    base_weight: int
    use_for: str
    notes: str


COMMON_EXCLUDED = [
    "generic top-10 blogs",
    "tutorial farms unless implementation examples are requested",
    "copied notebooks with unclear source",
    "LLM-generated summaries",
    "unlicensed source dumps",
    "random forks without paper, model card, package, or maintainer link",
]


TARGETS: dict[str, list[SourceTarget]] = {
    "core_ai_ml": [
        SourceTarget("arXiv", "tier1_primary", 90, "AI/ML papers and category search", "Use primary paper pages when possible."),
        SourceTarget("Hugging Face", "tier3_implementation", 65, "model cards, dataset cards, Spaces, paper linkage", "Record license, maintainer, intended use, and update date when available."),
        SourceTarget("GitHub/GitLab", "tier3_implementation", 70, "official repos, releases, issues, code", "Treat as official only when tied to authors, maintainers, packages, or papers."),
        SourceTarget("OpenReview", "tier1_primary", 88, "conference submissions, reviews, venue records", "Use public venue records when available."),
        SourceTarget("Semantic Scholar/OpenAlex/Crossref", "tier2_discovery", 70, "metadata and citation graph expansion", "Discovery only unless primary source unavailable."),
    ],
    "civitai": [
        SourceTarget("Civitai Developer Docs/API", "tier3_implementation", 75, "API fields and platform semantics", "Official platform documentation."),
        SourceTarget("Civitai model/resource pages", "tier3_implementation", 60, "resource availability, versions, creator notes, restrictions, examples", "Not scientific authority."),
        SourceTarget("Civitai comments/reviews", "tier4_practitioner", 25, "adoption and reproducibility leads", "Cross-check before use."),
    ],
    "open_source_libraries": [
        SourceTarget("Official library docs", "tier3_implementation", 80, "API/runtime behavior", "Best when paired with repo and release tag."),
        SourceTarget("Official source repo", "tier3_implementation", 80, "implementation status, releases, issues", "Check tags and changelog."),
        SourceTarget("Package registries", "tier3_implementation", 65, "versions, dependencies, licenses, distribution", "Use PyPI, conda-forge, npm, crates.io, Maven, NuGet, Docker Hub, ROS Index as relevant."),
        SourceTarget("NumFOCUS/project ecosystems", "tier2_discovery", 70, "scientific software discovery", "Follow through to official project docs."),
    ],
    "academic_sources": [
        SourceTarget("University/lab/faculty pages", "tier1_primary", 75, "lab context, project context, publication lists", "Weight higher when PI/lab-maintained and linked to artifacts."),
        SourceTarget("Graduate course notes", "tier2_academic", 65, "background, definitions, derivations", "Not current research consensus by default."),
        SourceTarget("Theses/dissertations", "tier2_academic", 70, "deep background and methods", "Mark peer-review status; verify important claims."),
        SourceTarget("OSF/Zenodo/Dataverse/CORE/OATD", "tier2_discovery", 70, "research artifacts, datasets, theses, open records", "Check record-specific license."),
        SourceTarget("Student project repos/pages", "tier4_practitioner", 40, "leads and examples", "Require lab/paper/advisor/release corroboration."),
    ],
    "quantum": [
        SourceTarget("arXiv quant-ph", "tier1_primary", 90, "quantum papers", "Add physics, cond-mat, math-ph when needed."),
        SourceTarget("APS/PRX Quantum/Physical Review", "tier1_primary", 92, "peer-reviewed quantum research", "Prefer official journal pages."),
        SourceTarget("Quantum Journal", "tier1_primary", 90, "quantum information research", "Check article license."),
        SourceTarget("Qiskit/Cirq/PennyLane/CUDA-Q/QuTiP docs", "tier3_implementation", 75, "framework API/runtime behavior", "Do not use docs as scientific proof alone."),
    ],
    "robotics": [
        SourceTarget("arXiv cs.RO", "tier1_primary", 90, "robotics papers", "Add cs.AI, cs.CV, eess.SY, cs.LG when needed."),
        SourceTarget("RSS proceedings", "tier1_primary", 90, "robotics conference papers", "Official proceedings."),
        SourceTarget("CoRL/OpenReview", "tier1_primary", 88, "robot learning papers and reviews", "Use public records."),
        SourceTarget("IEEE ICRA/IROS or IEEE Xplore metadata", "tier1_primary", 85, "robotics and automation papers", "Full text may require access."),
        SourceTarget("ROS/Open Robotics docs", "tier3_implementation", 75, "ROS implementation behavior", "API/runtime claims only."),
    ],
    "mechanical_engineering": [
        SourceTarget("ASME Digital Collection", "tier1_primary", 88, "mechanical engineering papers", "Use metadata/abstracts if full text unavailable."),
        SourceTarget("NIST publications", "tier1_primary", 90, "measurement, standards, engineering reports", "Government technical source."),
        SourceTarget("NASA NTRS", "tier1_primary", 85, "aerospace, controls, robotics, engineering reports", "Technical reports."),
        SourceTarget("DOE OSTI", "tier1_primary", 85, "DOE-funded science and engineering reports", "Technical reports and papers."),
        SourceTarget("Standards metadata", "tier1_primary", 80, "standard identification", "Do not quote paid standards text."),
    ],
    "reddit": [
        SourceTarget("Reddit", "tier4_practitioner", 20, "practitioner leads and failure modes", "Never sole source for final scientific claims."),
    ],
}


DOMAIN_PATTERNS: list[tuple[str, str]] = [
    (r"\b(civitai|lora|checkpoint|fine[- ]?tune|trigger words?|trainedwords?|stable diffusion|flux|sdxl)\b", "civitai"),
    (r"\b(arxiv|paper|model card|dataset card|hugging ?face|openreview|benchmark|ml|ai|llm|diffusion)\b", "core_ai_ml"),
    (r"\b(open[- ]source|library|libraries|package|pypi|conda|npm|crate|crates\.io|maven|nuget|docker|api docs|github|gitlab)\b", "open_source_libraries"),
    (r"\b(college|university|course|lecture|graduate|postgrad|postgraduate|phd|doctoral|master'?s|thesis|dissertation|student|lab)\b", "academic_sources"),
    (r"\b(quantum|qubit|qiskit|cirq|pennylane|quant-ph|hamiltonian)\b", "quantum"),
    (r"\b(robot|robotics|ros|manipulation|slam|locomotion|icra|iros|rss|corl)\b", "robotics"),
    (r"\b(mechanical|mechatronic|asme|sae|nist|nasa|osti|controls|finite element|cad|cam|cfd|materials)\b", "mechanical_engineering"),
    (r"\b(reddit|forum|practitioner|community|real users?|hardware report)\b", "reddit"),
]


def detect_domains(prompt: str) -> list[str]:
    selected: list[str] = []
    for pattern, domain in DOMAIN_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE) and domain not in selected:
            selected.append(domain)
    if not selected:
        selected = ["core_ai_ml", "open_source_libraries", "academic_sources"]
    return selected


def build_query_templates(prompt: str, domains: list[str]) -> list[str]:
    base = prompt.strip().strip(".")
    templates = [base]
    for domain in domains:
        if domain == "core_ai_ml":
            templates.extend([f"{base} arXiv", f"{base} OpenReview", f"{base} Hugging Face GitHub"])
        elif domain == "civitai":
            templates.extend([f"{base} Civitai model resource version", f"{base} Civitai Hugging Face GitHub"])
        elif domain == "open_source_libraries":
            templates.extend([f"{base} official docs GitHub release", f"{base} PyPI conda-forge package"])
        elif domain == "academic_sources":
            templates.extend([f"{base} university graduate course notes", f"{base} thesis dissertation OSF Zenodo"])
        elif domain == "quantum":
            templates.extend([f"{base} arXiv quant-ph", f"{base} PRX Quantum Quantum Journal"])
        elif domain == "robotics":
            templates.extend([f"{base} arXiv cs.RO RSS CoRL", f"{base} ICRA IROS ROS docs"])
        elif domain == "mechanical_engineering":
            templates.extend([f"{base} ASME NIST NASA NTRS DOE OSTI", f"{base} mechanical engineering official report"])
        elif domain == "reddit":
            templates.append(f"{base} Reddit reproducibility report")
    return list(dict.fromkeys(templates))


def route(prompt: str) -> dict:
    domains = detect_domains(prompt)
    targets = [asdict(target) for domain in domains for target in TARGETS[domain]]
    return {
        "request": prompt,
        "domains": domains,
        "target_sources": targets,
        "excluded_sources": COMMON_EXCLUDED,
        "query_templates": build_query_templates(prompt, domains),
        "reddit_allowed": "reddit" in domains,
        "weighting_policy": {
            "required_fields": ["evidence_weight", "weight_reason"],
            "scientific_or_engineering_threshold": 85,
            "implementation_threshold": 70,
            "model_resource_threshold": 60,
            "educational_background_threshold": 55,
            "practitioner_context_threshold": 25,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Route a research prompt to weighted source targets.")
    parser.add_argument("--prompt", required=True)
    args = parser.parse_args()
    print(json.dumps(route(args.prompt), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

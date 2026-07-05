# Source Policy

Use this reference for every `aiwf-deep-research` run.

## Evidence Tiers

### Tier 0: Local And User Evidence

Base weight: 95.

Use for current project state and user-specific claims:

- local repo files, tests, receipts, logs, configs, model manifests
- user-provided papers, notes, datasets, or constraints
- live command output from the current workspace

### Tier 1: Primary Research And Official Sources

Base weight: 90.

Use for scientific, engineering, method, algorithm, standard, or official capability claims:

- arXiv, peer-reviewed publisher pages, OpenReview venue records, official conference proceedings
- official documentation, official repositories, official model cards, official dataset cards
- standards bodies, government technical reports, university or research-lab publication pages

### Tier 2: Discovery And Academic Repositories

Base weight: 65 to 80.

Use to discover primary sources, citation trails, artifacts, theses, and related work:

- Crossref, OpenAlex, Semantic Scholar, Papers With Code
- CORE, OATD, EBSCO Open Dissertations
- university institutional repositories, OSF, Zenodo, Dataverse

Do not treat discovery metadata as canonical when the primary source is available.

Academic sub-weights:

- PhD dissertation: 70 to 80. Serious evidence, but not automatically peer-reviewed.
- Master's thesis: 60 to 75. Good methods/background source; verify important claims elsewhere.
- Official graduate course notes: 55 to 70. Good for foundations, definitions, derivations.
- Official undergraduate course notes: 45 to 60. Use for foundations only.
- University lab/project page: 60 to 85 depending on PI/lab maintenance and linked papers/data/code.
- Student project, personal academic page, or class GitHub repo: 30 to 55 unless tied to a paper, lab, advisor, or release.

### Tier 3: Implementation Reality

Base weight: 50 to 85.

Use for API behavior, code status, package status, implementation mismatch, reproducibility, and model/resource availability:

- GitHub/GitLab official repos, releases, tags, issue trackers, discussions, security advisories
- Hugging Face model cards, dataset cards, paper pages, Spaces, repository metadata
- Civitai model/resource/creator/version pages for availability, metadata, restrictions, examples, adoption, fine-tune compatibility
- official open-source library docs, package registries, changelogs, release notes, documentation sites

Open-source library sub-weights:

- Official docs plus official repository plus release tag: 80 to 90 for API/runtime behavior.
- Official docs or repository alone: 70 to 85 for API/runtime behavior.
- Package registry metadata from PyPI, conda-forge, npm, crates.io, Maven Central, NuGet, Docker Hub, or ROS Index: 55 to 75.
- Maintainer issue or discussion: 55 to 80 for current implementation reality, lower for unresolved reports.
- Third-party tutorial or copied code: 20 to 40 unless the user explicitly wants examples.

Library docs cannot prove scientific validity unless they cite and align with primary research.

### Tier 4: Practitioner And Community Context

Base weight: 10 to 35.

Use for leads, failure modes, hardware reports, adoption signals, and terminology discovery:

- Reddit, forums, community posts, user comments, Discord exports only when user-provided
- non-author blogs and writeups

Never use Tier 4 as the sole support for scientific, engineering, safety, or project-critical claims.

## Weight Model

Every important source gets:

- `evidence_weight`: integer 0 to 100
- `weight_reason`: one sentence explaining the score

Modifiers:

- Directness: +10 if the source directly proves the claim; -20 if adjacent.
- Authority: +10 for author, maintainer, standards body, official API, official docs; -15 for unaffiliated reposts.
- Freshness: +10 for current docs or recent fast-moving releases; -20 for stale or undated volatile claims.
- Reproducibility: +10 for inspectable code, data, benchmark scripts, or receipts; -10 without reproducible detail.
- Independence: +5 when corroborated independently; -10 when all evidence is same platform or author group.
- License/safety: -20 when artifact reuse rights are unclear.
- Academic level: +10 for graduate/postgraduate official institutional source; -20 for student projects not tied to lab, paper, release, or advisor.

Claim thresholds:

- Scientific or engineering mechanism: weight >= 85, normally Tier 1 or verified Tier 0.
- Implementation feasibility: weight >= 70, usually Tier 0 plus Tier 3.
- Open-source API/runtime behavior: weight >= 70, preferably docs plus repo/package metadata.
- Model/resource availability: weight >= 60, Civitai/Hugging Face/GitHub allowed if official enough and current.
- Educational/background claim: weight >= 55, with academic level labeled.
- Practitioner sentiment or pain point: weight >= 25, labeled as practitioner context.
- Final recommendation: at least two sources, or one direct Tier 0/Tier 1 source plus an explicit reason.

## Excluded By Default

- generic top-10 blogs
- tutorial/cookbook pages unless the user asks for examples
- copied notebooks with unclear source
- LLM-generated summaries
- unlicensed dumps of papers, books, comments, or images
- random forks with no paper, model card, package, or maintainer link

## Copyright And Training Safety

Store summaries, citations, metadata, and short permitted excerpts. Do not store long copyrighted source text. Do not train on Reddit comments, Civitai images/comments/descriptions, paid standards text, or course content unless a later license review allows it.

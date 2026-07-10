# AIWF Skill Pack Audit Findings

Updated: 2026-07-09

## Verdict

The pack is now a focused 43-skill Codex plugin with one implicit router, 42 explicit downstream skills, a four-skill route cap, and 17 self-contained Python helpers. The current inventory covers the shared stacks found in AIWF Studio, MoK, Ipaint-phone, Ai Embedded Systems projects, and Atlas work without requiring broad umbrella skills to load on every task.

## Gaps Filled

| Gap found in local projects | Skill added |
| --- | --- |
| Android/Kotlin, Gradle, Compose, Room, Retrofit, ONNX, and real-device behavior | `aiwf-android-kotlin-coding` |
| Chunking, embeddings, hybrid retrieval, reranking, grounding, and retrieval evaluation | `aiwf-rag-retrieval` |
| Relational/vector storage contracts, schemas, dimensions, metrics, migrations, and integrity | `aiwf-data-storage` |
| PowerShell, environments, paths, DLLs, ports, processes, Docker Desktop, WSL, and local services | `aiwf-windows-local-dev` |
| Vue 3 and VitePress code and documentation sites | `aiwf-vue-vitepress-coding` |
| Crawlability, canonicals, sitemaps, structured data, performance, and source-backed web claims | `aiwf-web-seo` |

The existing robotics, physics, networking/IoT, embedded edge AI, service intake, and field-pilot lanes remain distinct because they own materially different evidence and safety checks.

## Redundancy Removed

Four overlapping umbrella lanes were consolidated into focused owners. Repository-wide edit discipline is in `aiwf-repo-sentinel`; cross-layer UI/API behavior is in `aiwf-ui-electrician`; language/framework details stay in their specific skills; host-independent routing policy stays in `aiwf-orchestrator`.

`aiwf-agent-mok` was reduced from a mandatory four-pass process to proportional verify, plan, or findings modes. Findings datasets are now opt-in instead of being created during ordinary file reads.

All active `SKILL.md` files are 115 lines or fewer. This keeps trigger metadata and operating instructions compact while retaining detailed references and deterministic scripts where they add value.

## Incorrect Or Stale Guidance Corrected

- Python: Python 3.10 supports structural pattern matching and `X | Y`; `tomllib`, `Self`, `TaskGroup`, `ExceptionGroup`, and `except*` arrived in 3.11. Python 3.12 removed `distutils` and no longer installs `setuptools` as a core `venv` dependency.
- FastAPI: current FastAPI uses Pydantic v2; mixed v1/v2 guidance is migration-only. Application lifespan is the preferred startup/shutdown boundary for shared resources.
- TensorRT: serialized plans are normally version, platform, and device sensitive, but documented compatibility modes exist. Plans from untrusted sources are executable-risk artifacts and must not be deserialized casually.
- Model loading: no quantization level or component dtype is a universal default. Selection must follow runtime support, hardware, model architecture, quality requirements, and measured validation.
- ROS 2: generic robotics guidance no longer pins one distribution. The project must inspect its actual distribution and support state.
- CSS: the skill points to W3C current work instead of treating an old snapshot as permanently current.
- Android networking: a physical device does not reach the desktop through its own loopback address; use an explicit device/host route such as `adb reverse` when appropriate.
- Skill controls: route and loop values are instruction policy, not settings that alter the host model, context length, reasoning effort, or tool limits.
- Helper paths: skill-owned scripts are relative to the skill package, never hard-coded to a global install or another project.

## Primary Technical Anchors

- Python 3.10 and 3.12: https://docs.python.org/3.10/whatsnew/3.10.html and https://docs.python.org/3.12/whatsnew/3.12.html
- FastAPI migration and lifespan: https://fastapi.tiangolo.com/how-to/migrate-from-pydantic-v1-to-pydantic-v2/ and https://fastapi.tiangolo.com/advanced/events/
- TensorRT support and compatibility: https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html
- Android architecture and ADB: https://developer.android.com/topic/architecture and https://developer.android.com/tools/adb
- ROS 2 releases: https://docs.ros.org/en/rolling/Releases.html
- W3C CSS current work: https://www.w3.org/Style/CSS/current-work
- Google Search technical guidance: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
- Qdrant collection contracts: https://qdrant.tech/documentation/concepts/collections/
- pgvector: https://github.com/pgvector/pgvector

## Mechanical Guarantees

`scripts/validate_pack.py` now fails on:

- manifest/source inventory drift;
- missing or mismatched frontmatter and OpenAI metadata;
- more than one implicit skill;
- stale or missing router targets;
- missing referenced Python helpers or undocumented bundled helpers;
- retired/stale guidance in active skills and core docs;
- root-level ZIPs or generated Python caches;
- plugin version drift or non-skill capabilities.

`scripts/test_orchestrator_routes.py` uses exact expected routes, enforces the four-skill cap, rejects duplicates and unknown skills, and requires coverage for every downstream skill.

## Remaining Boundary

No static skill pack can make version-sensitive SDK or framework claims permanently current. Each focused skill therefore requires inspection of the repository's pinned versions and official current docs before changing compatibility-sensitive code.

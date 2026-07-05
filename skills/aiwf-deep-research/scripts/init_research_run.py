from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from source_target_router import route


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug[:64] or "deep-research-run"


def unique_run_dir(root: Path, title: str, created: datetime) -> Path:
    base = f"{created:%Y%m%d-%H%M%S}-{slugify(title)}"
    candidate = root / base
    index = 2
    while candidate.exists():
        candidate = root / f"{base}-{index}"
        index += 1
    return candidate


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_extra_urls(values: list[str]) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()
    for value in values:
        for raw_url in value.split(","):
            url = raw_url.strip()
            if not url or url in seen:
                continue
            urls.append(url)
            seen.add(url)
    return urls


def create_run(title: str, request: str, root: Path, extra_urls: list[str] | None = None) -> dict:
    created = datetime.now().astimezone()
    root = root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    run_dir = unique_run_dir(root, title, created)
    run_dir.mkdir(parents=True)

    source_plan = route(request)
    required_seed_urls = parse_extra_urls(extra_urls or [])
    source_plan.update(
        {
            "created_at": created.isoformat(),
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "run_dir": str(run_dir),
            "required_seed_urls": required_seed_urls,
            "acceptance_gates": [
                "source_plan_exists_before_search",
                "final_claims_have_source_ids",
                "final_claims_have_evidence_weight_and_weight_reason",
                "scientific_claims_use_tier1_or_verified_tier0_unless_labeled",
                "reddit_not_sole_source_for_final_claims",
                "civitai_used_as_platform_metadata_not_scientific_authority",
                "opensource_claims_distinguish_api_runtime_from_scientific_validity",
                "academic_sources_record_level_and_review_status",
                "contradictions_preserved",
            ],
        }
    )

    (run_dir / "request.md").write_text(f"# Request\n\n{request}\n", encoding="utf-8")
    write_json(run_dir / "source_plan.json", source_plan)
    for name in ["queries.jsonl", "sources.jsonl", "claims.jsonl", "source_weights.jsonl", "contradictions.jsonl"]:
        (run_dir / name).write_text("", encoding="utf-8")
    (run_dir / "research_brief.md").write_text(
        "# Research Brief\n\n"
        "## Direct Answer\n\n"
        "## Source Map\n\n"
        "## Key Findings\n\n"
        "## Contradictions\n\n"
        "## Rejected Sources\n\n"
        "## Open Questions\n\n"
        "## Next Steps\n",
        encoding="utf-8",
    )
    write_json(
        run_dir / "validation.json",
        {
            "status": "initialized",
            "created_at": created.isoformat(),
            "errors": [],
            "warnings": ["Run initialized. Add sources and claims, then validate again."],
        },
    )

    return {
        "run_dir": str(run_dir),
        "source_plan": str(run_dir / "source_plan.json"),
        "claims": str(run_dir / "claims.jsonl"),
        "sources": str(run_dir / "sources.jsonl"),
        "validation": str(run_dir / "validation.json"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an AIWF deep research run folder.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--request", required=True)
    parser.add_argument("--root", default="research runs")
    parser.add_argument(
        "--extra-urls",
        default=os.environ.get("AIWF_DEEP_RESEARCH_EXTRA_URLS", ""),
        help="Comma-separated URLs that must be included as seed sources.",
    )
    parser.add_argument(
        "--extra-url",
        action="append",
        default=[],
        help="A URL that must be included as a seed source. May be repeated.",
    )
    args = parser.parse_args()
    result = create_run(args.title, args.request, Path(args.root), [args.extra_urls, *args.extra_url])
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

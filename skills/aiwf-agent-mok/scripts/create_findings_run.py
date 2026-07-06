from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


SCHEMA_VERSION = "moks-findings-v1"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug[:48] or "aiwf-agent-mok-run"


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def can_write_directory(path: Path) -> bool:
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / ".mok_write_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return True
    except OSError:
        return False


def resolve_findings_root(requested_root: str | None, allow_skill_fallback: bool) -> Path:
    candidates: list[Path] = []
    if requested_root:
        candidates.append(Path(requested_root).expanduser())
    else:
        candidates.append(Path.cwd() / "moks findings")
    if allow_skill_fallback:
        candidates.append(skill_root() / "moks findings")

    for candidate in candidates:
        candidate = candidate.resolve()
        if can_write_directory(candidate):
            return candidate

    rendered = ", ".join(str(path) for path in candidates)
    raise PermissionError(f"no writable findings root found; tried: {rendered}")


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


def create_findings_run(
    *,
    title: str,
    request: str,
    root: str | None,
    allow_skill_fallback: bool,
) -> dict:
    created = datetime.now().astimezone()
    findings_root = resolve_findings_root(root, allow_skill_fallback)
    run_dir = unique_run_dir(findings_root, title, created)
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "raw").mkdir()

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_dir.name,
        "created_at": created.isoformat(),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "request": request,
        "title": title,
        "findings_root": str(findings_root),
        "run_dir": str(run_dir),
        "source_classes": [],
        "tools_used": [],
        "license_policy": "Store summaries, citations, source metadata, and short permitted excerpts unless license review allows more.",
        "privacy_policy": "Do not store secrets, credentials, raw environment dumps, or unnecessary personal data.",
        "training_readiness": "initialized",
        "validation_status": "pending",
        "counts": {
            "atlas_cards": 0,
            "sources": 0,
            "training_records": 0,
        },
    }
    write_json(run_dir / "manifest.json", manifest)
    (run_dir / "atlas_cards.jsonl").write_text("", encoding="utf-8")
    (run_dir / "training_data.jsonl").write_text("", encoding="utf-8")
    (run_dir / "sources.jsonl").write_text("", encoding="utf-8")
    (run_dir / "README.md").write_text(
        "# Agent MoK Findings Run\n\n"
        "This folder stores Atlas-style evidence cards, source metadata, and "
        "training JSONL derived from this Agent MoK usage.\n\n"
        "Review license, privacy, and verification fields before using the "
        "records for model training.\n",
        encoding="utf-8",
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "findings_root": str(findings_root),
        "run_dir": str(run_dir),
        "manifest": str(run_dir / "manifest.json"),
        "atlas_cards": str(run_dir / "atlas_cards.jsonl"),
        "training_data": str(run_dir / "training_data.jsonl"),
        "sources": str(run_dir / "sources.jsonl"),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create an Agent MoK findings dataset run folder.")
    parser.add_argument("--title", default="Agent MoK run", help="Short run title used in the folder name.")
    parser.add_argument("--request", default="", help="Original user request or run objective.")
    parser.add_argument("--root", help="Optional findings root. Defaults to ./moks findings.")
    parser.add_argument(
        "--no-skill-fallback",
        action="store_true",
        help="Disable fallback to the skill/plugin root when the primary root is unavailable.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = create_findings_run(
        title=args.title,
        request=args.request,
        root=args.root,
        allow_skill_fallback=not args.no_skill_fallback,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

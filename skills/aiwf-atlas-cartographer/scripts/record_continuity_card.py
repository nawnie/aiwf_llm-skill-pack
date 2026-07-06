#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def default_data_root() -> Path:
    explicit = os.environ.get("ATLAS_CARTOGRAPHER_HOME")
    if explicit:
        return Path(explicit)
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home) / "aiwf-atlas-cartographer"
    return Path.home() / ".codex" / "aiwf-atlas-cartographer"


def split_values(values: list[str] | None) -> list[str]:
    if not values:
        return []
    items: list[str] = []
    for value in values:
        for part in value.split(","):
            clean = part.strip()
            if clean:
                items.append(clean)
    return items


def slugify(value: str, *, fallback: str = "card", max_len: int = 48) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return (slug or fallback)[:max_len].strip("-") or fallback


def lane_name(value: str) -> str:
    lane = re.sub(r"[^a-z0-9_/-]+", "_", value.lower()).strip("_-/")
    lane = lane.replace("/", "_").replace("-", "_")
    return lane or "general_continuity"


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSONL at {path}:{line_no}: {exc}") from exc
    return rows


def write_manifest(data_root: Path) -> dict[str, Any]:
    cards_path = data_root / "cards.jsonl"
    cards = read_jsonl(cards_path)
    lane_counts: dict[str, int] = {}
    project_counts: dict[str, int] = {}
    for card in cards:
        lane = str(card.get("lane") or "general_continuity")
        project = str(card.get("project") or "unknown")
        lane_counts[lane] = lane_counts.get(lane, 0) + 1
        project_counts[project] = project_counts.get(project, 0) + 1
    manifest = {
        "schema": "atlas_cartographer_continuity_v1",
        "updated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "total_cards": len(cards),
        "lane_counts": dict(sorted(lane_counts.items())),
        "project_counts": dict(sorted(project_counts.items())),
        "cards_path": str(cards_path),
    }
    manifest_path = data_root / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Record a local Atlas-style continuity card.")
    parser.add_argument("--project", default="general", help="Project/workspace name.")
    parser.add_argument("--lane", default="general_continuity", help="Stable lane name.")
    parser.add_argument("--title", required=True, help="Short card title.")
    parser.add_argument("--summary", required=True, help="Compact restart summary.")
    parser.add_argument("--details", default="", help="Optional longer handoff note.")
    parser.add_argument("--details-file", help="Read additional details from a UTF-8 text file.")
    parser.add_argument("--source", action="append", help="Source pointer path, URL, artifact, or receipt.")
    parser.add_argument("--tag", action="append", help="Tag. May be repeated or comma-separated.")
    parser.add_argument("--must-retrieve", action="append", help="Required file/artifact to retrieve on resume.")
    parser.add_argument("--decision", action="append", help="Durable decision made.")
    parser.add_argument("--verification", action="append", help="Validation command or result.")
    parser.add_argument("--unresolved", action="append", help="Next action, blocker, risk, or stale fact.")
    parser.add_argument("--related-card", action="append", help="Related card_id.")
    parser.add_argument("--confidence", type=float, default=0.85, help="Confidence from 0.0 to 1.0.")
    parser.add_argument("--risk-level", choices=["low", "medium", "high"], default="medium")
    parser.add_argument("--current-verification-required", action="store_true")
    parser.add_argument("--data-root", type=Path, default=default_data_root())
    parser.add_argument("--print-card", action="store_true")
    args = parser.parse_args()

    details_parts = [args.details.strip()] if args.details.strip() else []
    if args.details_file:
        details_parts.append(Path(args.details_file).read_text(encoding="utf-8", errors="replace").strip())
    details = "\n\n".join(part for part in details_parts if part)

    lane = lane_name(args.lane)
    created_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    digest_source = json.dumps(
        {
            "project": args.project,
            "lane": lane,
            "title": args.title,
            "summary": args.summary,
            "details": details,
            "source": args.source or [],
        },
        sort_keys=True,
    )
    digest = hashlib.sha256(digest_source.encode("utf-8")).hexdigest()[:10]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    card_id = f"{timestamp}-{lane}-{slugify(args.title)}-{digest}"

    card = {
        "schema": "atlas_cartographer_continuity_v1",
        "card_id": card_id,
        "created_at_utc": created_at,
        "project": args.project,
        "lane": lane,
        "title": args.title,
        "summary": args.summary,
        "details": details,
        "source_pointers": split_values(args.source),
        "tags": split_values(args.tag),
        "must_retrieve": split_values(args.must_retrieve),
        "decisions": split_values(args.decision),
        "verification": split_values(args.verification),
        "unresolved": split_values(args.unresolved),
        "related_cards": split_values(args.related_card),
        "confidence": max(0.0, min(1.0, args.confidence)),
        "risk_level": args.risk_level,
        "current_verification_required": bool(args.current_verification_required),
    }

    data_root = args.data_root
    append_jsonl(data_root / "cards.jsonl", card)
    append_jsonl(data_root / "lanes" / f"{lane}.jsonl", card)
    (data_root / "latest-card.json").write_text(json.dumps(card, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    manifest = write_manifest(data_root)

    result = {
        "card_id": card_id,
        "data_root": str(data_root),
        "cards_path": str(data_root / "cards.jsonl"),
        "lane_path": str(data_root / "lanes" / f"{lane}.jsonl"),
        "total_cards": manifest["total_cards"],
    }
    print(json.dumps(card if args.print_card else result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
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


def tokens(query: str) -> list[str]:
    return [part for part in re.split(r"[^a-z0-9_./:-]+", query.lower()) if part]


def searchable_text(card: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in [
        "card_id",
        "project",
        "lane",
        "title",
        "summary",
        "details",
        "risk_level",
    ]:
        value = card.get(key)
        if value:
            parts.append(str(value))
    for key in ["source_pointers", "tags", "must_retrieve", "decisions", "verification", "unresolved"]:
        value = card.get(key)
        if isinstance(value, list):
            parts.extend(str(item) for item in value)
    return "\n".join(parts).lower()


def score(card: dict[str, Any], query_tokens: list[str]) -> int:
    if not query_tokens:
        return 1
    text = searchable_text(card)
    total = 0
    for token in query_tokens:
        if token in text:
            total += 3 if token in str(card.get("title", "")).lower() else 1
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description="Search local Atlas cartographer continuity cards.")
    parser.add_argument("--query", default="", help="Search text.")
    parser.add_argument("--project", help="Filter by project substring.")
    parser.add_argument("--lane", help="Filter by exact lane.")
    parser.add_argument("--tag", action="append", help="Required tag. May be repeated.")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--data-root", type=Path, default=default_data_root())
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--show-details", action="store_true")
    args = parser.parse_args()

    cards = read_jsonl(args.data_root / "cards.jsonl")
    query_tokens = tokens(args.query)
    required_tags = {tag.lower() for tag in (args.tag or [])}
    matches: list[tuple[int, dict[str, Any]]] = []

    for card in cards:
        if args.project and args.project.lower() not in str(card.get("project", "")).lower():
            continue
        if args.lane and args.lane != card.get("lane"):
            continue
        card_tags = {str(tag).lower() for tag in card.get("tags", [])}
        if required_tags and not required_tags.issubset(card_tags):
            continue
        card_score = score(card, query_tokens)
        if card_score <= 0:
            continue
        matches.append((card_score, card))

    matches.sort(key=lambda item: (item[0], str(item[1].get("created_at_utc", ""))), reverse=True)
    selected = [card for _, card in matches[: max(0, args.limit)]]

    if args.format == "json":
        print(json.dumps(selected, indent=2, ensure_ascii=False))
        return 0

    if not selected:
        print("No continuity cards found.")
        return 0

    for card in selected:
        print(f"{card.get('card_id')} [{card.get('lane')}] {card.get('title')}")
        print(f"  project: {card.get('project')}")
        print(f"  summary: {card.get('summary')}")
        if card.get("source_pointers"):
            print(f"  sources: {', '.join(card['source_pointers'])}")
        if card.get("verification"):
            print(f"  verification: {'; '.join(card['verification'])}")
        if card.get("unresolved"):
            print(f"  unresolved: {'; '.join(card['unresolved'])}")
        if args.show_details and card.get("details"):
            print(f"  details: {card.get('details')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

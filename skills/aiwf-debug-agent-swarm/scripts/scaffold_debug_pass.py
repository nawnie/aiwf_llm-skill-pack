#!/usr/bin/env python3
"""Create a local debug_pass folder and optional lane report templates."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import re


DEFAULT_LANES = (
    "api-contract",
    "progress-state",
    "errors-logs",
    "telemetry",
)


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip()).strip("-")
    return cleaned.lower() or "debug"


def parse_lanes(value: str | None) -> list[str]:
    if not value:
        return list(DEFAULT_LANES)
    lanes = [slugify(part) for part in value.split(",")]
    return [lane for lane in lanes if lane]


def report_template(lane: str) -> str:
    title = lane.replace("-", " ").title()
    return f"""# {title} Debug Report

- Agent:
- Scope: {lane}
- Status: partial
- Confidence:
- Research used: no
- Sources:
- Project notes read:
- Files/logs inspected:

## Issues

### medium: <title>
- Evidence:
- User-visible impact:
- Repro/trigger:
- Affected files/routes:
- Confidence:
- Needs parent research: yes
- Fix detail omitted: yes

## Syntax Fixes

- None
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Project root. Defaults to cwd.")
    parser.add_argument("--slug", default="debug", help="Pass name suffix.")
    parser.add_argument("--base", default=".codex/debug_pass", help="Debug pass base directory under root.")
    parser.add_argument("--lanes", help="Comma-separated lane names. Defaults to common UI/API lanes.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    pass_dir = root / args.base / f"{stamp}-{slugify(args.slug)}"
    pass_dir.mkdir(parents=True, exist_ok=False)

    lanes = parse_lanes(args.lanes)
    context = f"""# Debug Pass Context

- Root: {root}
- Created: {stamp}
- Slug: {slugify(args.slug)}
- Lanes: {", ".join(lanes)}

Subagents should use this folder for Markdown findings. They should read only parent-provided context, SUB_AGENTS.md if present, or the Known Issues section of AGENTS.md.
"""
    (pass_dir / "_context.md").write_text(context, encoding="utf-8")

    for lane in lanes:
        (pass_dir / f"{lane}.md").write_text(report_template(lane), encoding="utf-8")

    print(pass_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

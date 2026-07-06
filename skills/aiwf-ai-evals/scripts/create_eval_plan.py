from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def build_plan(args: argparse.Namespace) -> dict:
    return {
        "schema_version": "aiwf-eval-plan-v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "target": args.target,
        "modality": args.modality,
        "baseline": args.baseline or "",
        "candidate": args.candidate or args.target,
        "suite": args.suite or "",
        "runtime": {
            "backend": args.backend or "",
            "endpoint": args.endpoint or "",
            "model_path": "",
            "dtype": "",
            "quantization": "",
        },
        "acceptance": {
            "primary_metric": "",
            "threshold": "",
            "regression_budget": "",
            "manual_review_required": args.modality in {"image", "video"},
        },
        "receipts": {
            "root": args.receipts or "",
            "commands": [],
            "metrics": [],
            "artifacts": [],
            "logs": [],
        },
        "checks": {
            "readiness": "pending",
            "tiny_probe": "pending",
            "full_eval": "not_requested",
            "promotion": "pending",
        },
        "blockers": [],
        "notes": "",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an AIWF eval plan JSON skeleton.")
    parser.add_argument("--target", required=True, help="Model, route, adapter, or endpoint being evaluated.")
    parser.add_argument("--out", required=True, help="Output plan JSON path.")
    parser.add_argument("--modality", default="llm", choices=["llm", "image", "video", "ui-api", "serving", "multimodal", "other"])
    parser.add_argument("--baseline", default="", help="Baseline model, route, or receipt.")
    parser.add_argument("--candidate", default="", help="Candidate model, route, or receipt.")
    parser.add_argument("--suite", default="", help="Prompt suite, benchmark, smoke matrix, or eval name.")
    parser.add_argument("--backend", default="", help="Runtime backend.")
    parser.add_argument("--endpoint", default="", help="Endpoint URL if evaluating a service.")
    parser.add_argument("--receipts", default="", help="Receipt output root.")
    args = parser.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(build_plan(args), indent=2) + "\n", encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

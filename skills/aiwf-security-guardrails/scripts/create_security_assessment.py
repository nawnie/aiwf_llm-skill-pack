from __future__ import annotations

import argparse
import json
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def checked(value: str, label: str) -> str:
    text = value.strip()
    if not text or len(text) > 300:
        raise ValueError(f"{label} must contain 1-300 characters")
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an empty evidence-oriented security assessment.")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--scope", required=True)
    args = parser.parse_args()
    try:
        output = args.output.resolve()
        if output.exists():
            raise ValueError(f"refusing to overwrite existing file: {output}")
        payload = {
            "schema_version": 1,
            "assessment_id": f"SEC-{datetime.now(timezone.utc):%Y%m%d}-{secrets.token_hex(3)}",
            "title": checked(args.title, "title"),
            "owner": checked(args.owner, "owner"),
            "scope": checked(args.scope, "scope"),
            "created_at": utc_now(),
            "authorization": {"status": "unverified", "approved_targets": [], "prohibited_actions": []},
            "assets": [],
            "actors": [],
            "trust_boundaries": [],
            "data_flows": [],
            "threats": [],
            "findings": [],
            "audit_evidence": [],
            "validation": [],
            "residual_risk": [],
        }
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"assessment_id": payload["assessment_id"], "path": str(output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

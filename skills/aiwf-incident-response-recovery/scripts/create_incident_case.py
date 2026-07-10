from __future__ import annotations

import argparse
import hashlib
import json
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def safe_text(value: str, label: str) -> str:
    cleaned = value.strip()
    if not cleaned or len(cleaned) > 200:
        raise ValueError(f"{label} must contain 1-200 characters")
    return cleaned


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a local incident case without collecting evidence contents.")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--owner", required=True)
    args = parser.parse_args()
    try:
        title = safe_text(args.title, "title")
        owner = safe_text(args.owner, "owner")
        output = args.output.resolve()
        if output.exists() and any(output.iterdir()):
            raise ValueError(f"output directory is not empty: {output}")
        output.mkdir(parents=True, exist_ok=True)
        (output / "evidence").mkdir(exist_ok=True)
        (output / "notes").mkdir(exist_ok=True)
        now = utc_now()
        case_id = f"IR-{datetime.now(timezone.utc):%Y%m%d-%H%M%S}-{secrets.token_hex(3)}"
        case = {
            "schema_version": 1,
            "case_id": case_id,
            "title": title,
            "owner": owner,
            "status": "triage",
            "created_at": now,
            "authorized_scope": [],
            "affected_assets": [],
            "affected_data": [],
            "known_facts": [],
            "uncertainties": [],
            "approvals": [],
            "containment_options": [],
            "recovery_gates": [],
            "notifications": [],
        }
        timeline = {"schema_version": 1, "case_id": case_id, "timestamp": now, "event": "case_created", "actor": owner, "source": "create_incident_case.py"}
        case_text = json.dumps(case, indent=2) + "\n"
        (output / "incident.json").write_text(case_text, encoding="utf-8")
        (output / "timeline.jsonl").write_text(json.dumps(timeline) + "\n", encoding="utf-8")
        digest = hashlib.sha256(case_text.encode("utf-8")).hexdigest()
        (output / "CASE.md").write_text(
            f"# {case_id}\n\nTitle: {title}\n\nOwner: {owner}\n\nCreated UTC: {now}\n\nInitial incident.json SHA-256: `{digest}`\n\nDo not place credentials, private keys, or raw evidence contents in summary files. Record evidence paths and hashes, preserve originals, and obtain approval before containment or recovery mutations.\n",
            encoding="utf-8",
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"case_id": case_id, "path": str(output), "created_at": now}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

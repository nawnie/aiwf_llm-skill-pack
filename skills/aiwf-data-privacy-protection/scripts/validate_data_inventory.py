from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


TOP_LEVEL = ("schema_version", "inventory_id", "owner", "updated_at", "records")
RECORD_FIELDS = (
    "id",
    "name",
    "purpose",
    "subjects",
    "fields",
    "sensitivity",
    "source",
    "locations",
    "access_roles",
    "encryption",
    "retention",
    "deletion",
    "backup",
    "incident_owner",
)
FORBIDDEN_KEYS = {"raw_data", "sample_values", "password", "api_key", "access_token", "private_key"}
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\b(?:sk|rk|pk)-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
)


def nonempty(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value)
    if isinstance(value, dict):
        return bool(value)
    return value is not None


def validate(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["inventory must be a JSON object"]
    for field in TOP_LEVEL:
        if not nonempty(payload.get(field)):
            errors.append(f"missing or empty top-level field: {field}")
    if payload.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    updated_at = payload.get("updated_at")
    if isinstance(updated_at, str):
        try:
            datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
        except ValueError:
            errors.append("updated_at must be an ISO-8601 timestamp")

    records = payload.get("records")
    if not isinstance(records, list):
        return errors + ["records must be a list"]
    ids: set[str] = set()
    for index, record in enumerate(records):
        prefix = f"records[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be an object")
            continue
        lowered = {str(key).lower() for key in record}
        for key in sorted(lowered & FORBIDDEN_KEYS):
            errors.append(f"{prefix} contains forbidden raw-secret/data key: {key}")
        for field in RECORD_FIELDS:
            if not nonempty(record.get(field)):
                errors.append(f"{prefix} missing or empty field: {field}")
        record_id = record.get("id")
        if isinstance(record_id, str):
            if record_id in ids:
                errors.append(f"duplicate record id: {record_id}")
            ids.add(record_id)
        fields = record.get("fields")
        if fields is not None and not isinstance(fields, list):
            errors.append(f"{prefix}.fields must list field names, not raw data")

    serialized = json.dumps(payload)
    for pattern in SECRET_PATTERNS:
        if pattern.search(serialized):
            errors.append("inventory appears to contain a credential or private key value")
            break
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an AIWF data inventory without reading the underlying data.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors = validate(payload)
    result = {"valid": not errors, "record_count": len(payload.get("records", [])) if isinstance(payload, dict) else 0, "errors": errors}
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

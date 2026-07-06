from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED = ["schema", "receipt_id", "created_at", "skill", "task", "status", "evidence"]
STATUSES = {"passed", "failed", "partial", "skipped", "blocked"}
COMMAND_STATUSES = {"passed", "failed", "not_run"}


def fail(message: str) -> int:
    print(f"receipt validation failed: {message}", file=sys.stderr)
    return 1


def validate(payload: dict[str, Any]) -> int:
    for key in REQUIRED:
        if key not in payload:
            return fail(f"missing required field: {key}")
    if payload["schema"] != "aiwf.receipt.v1":
        return fail("schema must be aiwf.receipt.v1")
    if payload["status"] not in STATUSES:
        return fail(f"invalid status: {payload['status']}")
    if not isinstance(payload["evidence"], list) or not payload["evidence"]:
        return fail("evidence must be a non-empty list")
    if not str(payload["skill"]).startswith("aiwf-"):
        return fail("skill must start with aiwf-")
    commands = payload.get("commands", [])
    if commands:
        if not isinstance(commands, list):
            return fail("commands must be a list")
        for index, command in enumerate(commands):
            if not isinstance(command, dict):
                return fail(f"commands[{index}] must be an object")
            if "command" not in command or "status" not in command:
                return fail(f"commands[{index}] requires command and status")
            if command["status"] not in COMMAND_STATUSES:
                return fail(f"commands[{index}] invalid status: {command['status']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an AIWF workflow receipt.")
    parser.add_argument("receipt", help="Path to receipt JSON.")
    args = parser.parse_args()
    path = Path(args.receipt)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(str(exc))
    if not isinstance(payload, dict):
        return fail("receipt root must be an object")
    result = validate(payload)
    if result == 0:
        print(f"receipt valid: {path}")
    return result


if __name__ == "__main__":
    raise SystemExit(main())

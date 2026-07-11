from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TERMINAL_STATES = {
    "CLEAN",
    "ACCEPTABLE_WITH_MINOR",
    "STALLED",
    "ESCALATE",
    "BUDGET_EXHAUSTED",
    "BLOCKED",
    "ABORTED",
}
SEVERITIES = {"critical", "high", "medium", "low", "info"}
FINDING_STATES = {"open", "accepted", "fixed"}
BLOCKING_SEVERITIES = {"critical", "high", "medium"}


class ValidationError(ValueError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"expected a JSON object in {path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def inside(root: Path, candidate: Path) -> bool:
    return candidate == root or root in candidate.parents


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def surface_hash(root: Path, manifest: dict[str, Any]) -> str:
    paths = manifest.get("source_paths")
    if not isinstance(paths, list) or not paths or not all(isinstance(item, str) and item for item in paths):
        raise ValidationError("manifest source_paths must be a non-empty list of relative paths")

    files: dict[str, Path] = {}
    for relative in paths:
        candidate = (root / relative).resolve()
        if not inside(root, candidate):
            raise ValidationError(f"source path escapes project root: {relative}")
        if not candidate.exists():
            raise ValidationError(f"source path does not exist: {relative}")
        if candidate.is_symlink():
            raise ValidationError(f"source path must not be a symlink: {relative}")
        candidates = [candidate] if candidate.is_file() else [path for path in candidate.rglob("*") if path.is_file()]
        for path in candidates:
            resolved = path.resolve()
            if not inside(root, resolved) or path.is_symlink():
                raise ValidationError(f"source file escapes project root or is a symlink: {path}")
            files[resolved.relative_to(root).as_posix()] = resolved

    digest = hashlib.sha256()
    for relative, path in sorted(files.items()):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_hash(path).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def validate_manifest(manifest: dict[str, Any]) -> None:
    if manifest.get("schema_version") != 1:
        raise ValidationError("manifest schema_version must be 1")
    if not isinstance(manifest.get("target"), str) or not manifest["target"].strip():
        raise ValidationError("manifest target must be a non-empty string")
    gates = manifest.get("required_gates")
    flows = manifest.get("runtime_flows")
    if not isinstance(gates, list) or not gates:
        raise ValidationError("manifest required_gates must be a non-empty list")
    if not isinstance(flows, list):
        raise ValidationError("manifest runtime_flows must be a list")


def validate_report(report: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if report.get("schema_version") != 1:
        raise ValidationError("report schema_version must be 1")
    if not isinstance(report.get("lens"), str) or not report["lens"].strip():
        raise ValidationError("report lens must be a non-empty string")
    if not isinstance(report.get("progress"), bool):
        raise ValidationError("report progress must be true or false")

    gates = report.get("gates")
    if not isinstance(gates, list) or not gates:
        raise ValidationError("report gates must be a non-empty list")
    for gate in gates:
        if not isinstance(gate, dict) or not isinstance(gate.get("name"), str) or not gate["name"].strip():
            raise ValidationError("every gate needs a non-empty name")
        if not isinstance(gate.get("passed"), bool):
            raise ValidationError(f"gate {gate.get('name', '<unknown>')} needs a boolean passed value")
        if not isinstance(gate.get("evidence"), str) or not gate["evidence"].strip():
            raise ValidationError(f"gate {gate['name']} needs an evidence path or receipt")

    findings = report.get("findings", [])
    if not isinstance(findings, list):
        raise ValidationError("report findings must be a list")
    fingerprints: set[str] = set()
    for finding in findings:
        if not isinstance(finding, dict):
            raise ValidationError("every finding must be an object")
        fingerprint = finding.get("fingerprint")
        severity = finding.get("severity")
        status = finding.get("status")
        if not isinstance(fingerprint, str) or not fingerprint.strip():
            raise ValidationError("every finding needs a non-empty fingerprint")
        if fingerprint in fingerprints:
            raise ValidationError(f"duplicate finding fingerprint: {fingerprint}")
        fingerprints.add(fingerprint)
        if severity not in SEVERITIES:
            raise ValidationError(f"finding {fingerprint} has invalid severity: {severity}")
        if status not in FINDING_STATES:
            raise ValidationError(f"finding {fingerprint} has invalid status: {status}")
        if status == "accepted":
            if severity not in {"low", "info"}:
                raise ValidationError(f"only low or info findings may be accepted: {fingerprint}")
            if not isinstance(finding.get("reason"), str) or not finding["reason"].strip():
                raise ValidationError(f"accepted finding needs a reason: {fingerprint}")

    attempted = report.get("attempted_fixes", [])
    if not isinstance(attempted, list) or not all(isinstance(item, str) and item for item in attempted):
        raise ValidationError("report attempted_fixes must be a list of fingerprints")
    for flag in ("blocked", "aborted"):
        if flag in report and not isinstance(report[flag], bool):
            raise ValidationError(f"report {flag} must be true or false")
    return gates, findings


def summary(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "target": state["target"],
        "status": state["status"],
        "cycles": state["counters"]["cycles"],
        "clean_streak": state["counters"]["clean_streak"],
        "accepted_minor_streak": state["counters"]["accepted_minor_streak"],
        "no_progress_streak": state["counters"]["no_progress_streak"],
        "source_hash": state["baseline"]["source_hash"],
        "manifest_hash": state["baseline"]["manifest_hash"],
    }


def initialize(args: argparse.Namespace) -> dict[str, Any]:
    root = Path(args.root).resolve()
    manifest_path = Path(args.manifest).resolve()
    state_path = Path(args.state).resolve()
    if not root.is_dir():
        raise ValidationError(f"project root is not a directory: {root}")
    if not inside(root, manifest_path):
        raise ValidationError("manifest must be inside the project root")
    if state_path.exists() and not args.force:
        raise ValidationError(f"state already exists; use --force to replace it: {state_path}")

    manifest = read_json(manifest_path)
    validate_manifest(manifest)
    source = surface_hash(root, manifest)
    now = utc_now()
    state = {
        "schema_version": 1,
        "target": args.target or manifest["target"],
        "status": "IN_PROGRESS",
        "created_at": now,
        "updated_at": now,
        "root": str(root),
        "manifest_path": str(manifest_path),
        "policy": {
            "clean_streak": args.clean_streak,
            "accepted_minor_streak": args.accepted_minor_streak,
            "max_cycles": args.max_cycles,
            "max_no_progress": args.max_no_progress,
            "max_fix_attempts": args.max_fix_attempts,
        },
        "baseline": {
            "source_hash": source,
            "manifest_hash": file_hash(manifest_path),
        },
        "counters": {
            "cycles": 0,
            "clean_streak": 0,
            "accepted_minor_streak": 0,
            "no_progress_streak": 0,
        },
        "known_minor_fingerprints": [],
        "fix_attempts": {},
        "history": [],
    }
    write_json(state_path, state)
    return state


def record(args: argparse.Namespace) -> dict[str, Any]:
    state_path = Path(args.state).resolve()
    report = read_json(Path(args.report).resolve())
    state = read_json(state_path)
    if state.get("schema_version") != 1:
        raise ValidationError("state schema_version must be 1")
    if state.get("status") in TERMINAL_STATES:
        raise ValidationError(f"state is terminal ({state['status']}); initialize a new run")
    gates, findings = validate_report(report)

    root = Path(state["root"]).resolve()
    manifest_path = Path(state["manifest_path"]).resolve()
    manifest = read_json(manifest_path)
    validate_manifest(manifest)
    current_source = surface_hash(root, manifest)
    current_manifest = file_hash(manifest_path)
    surface_changed = (
        current_source != state["baseline"]["source_hash"]
        or current_manifest != state["baseline"]["manifest_hash"]
    )
    counters = state["counters"]
    if surface_changed:
        counters["clean_streak"] = 0
        counters["accepted_minor_streak"] = 0
        counters["no_progress_streak"] = 0
        state["known_minor_fingerprints"] = []
        state["baseline"] = {"source_hash": current_source, "manifest_hash": current_manifest}

    counters["cycles"] += 1
    unresolved = [finding for finding in findings if finding["status"] != "fixed"]
    blocking = [finding for finding in unresolved if finding["severity"] in BLOCKING_SEVERITIES]
    minor = [finding for finding in unresolved if finding["severity"] in {"low", "info"}]
    accepted_minor = all(finding["status"] == "accepted" for finding in minor)
    gates_passed = all(gate["passed"] for gate in gates)
    current_minor = {finding["fingerprint"] for finding in minor}
    known_minor = set(state["known_minor_fingerprints"])

    if gates_passed and not unresolved:
        counters["clean_streak"] += 1
        counters["accepted_minor_streak"] = 0
        state["known_minor_fingerprints"] = []
    elif gates_passed and not blocking and accepted_minor:
        counters["clean_streak"] = 0
        if counters["accepted_minor_streak"] == 0 or current_minor.issubset(known_minor):
            counters["accepted_minor_streak"] += 1
        else:
            counters["accepted_minor_streak"] = 1
        state["known_minor_fingerprints"] = sorted(current_minor)
    else:
        counters["clean_streak"] = 0
        counters["accepted_minor_streak"] = 0
        state["known_minor_fingerprints"] = sorted(current_minor)

    qualifying = gates_passed and not blocking and (not minor or accepted_minor)
    if report["progress"] or qualifying:
        counters["no_progress_streak"] = 0
    else:
        counters["no_progress_streak"] += 1

    attempts = state["fix_attempts"]
    for fingerprint in report.get("attempted_fixes", []):
        attempts[fingerprint] = int(attempts.get(fingerprint, 0)) + 1
    unresolved_fingerprints = {finding["fingerprint"] for finding in unresolved}
    repeated = sorted(
        fingerprint
        for fingerprint, count in attempts.items()
        if count >= state["policy"]["max_fix_attempts"] and fingerprint in unresolved_fingerprints
    )

    if report.get("aborted", False):
        status = "ABORTED"
    elif report.get("blocked", False):
        status = "BLOCKED"
    elif counters["clean_streak"] >= state["policy"]["clean_streak"]:
        status = "CLEAN"
    elif counters["accepted_minor_streak"] >= state["policy"]["accepted_minor_streak"]:
        status = "ACCEPTABLE_WITH_MINOR"
    elif repeated:
        status = "ESCALATE"
    elif counters["no_progress_streak"] >= state["policy"]["max_no_progress"]:
        status = "STALLED"
    elif counters["cycles"] >= state["policy"]["max_cycles"]:
        status = "BUDGET_EXHAUSTED"
    else:
        status = "IN_PROGRESS"

    state["status"] = status
    state["updated_at"] = utc_now()
    state["history"].append(
        {
            "cycle": counters["cycles"],
            "recorded_at": state["updated_at"],
            "lens": report["lens"],
            "surface_changed": surface_changed,
            "gates_passed": gates_passed,
            "blocking_fingerprints": sorted(finding["fingerprint"] for finding in blocking),
            "minor_fingerprints": sorted(current_minor),
            "repeated_fix_fingerprints": repeated,
            "progress": report["progress"],
            "status": status,
            "note": str(report.get("note", "")),
        }
    )
    write_json(state_path, state)
    return state


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("value must be at least 1")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Persist bounded QA convergence state.")
    commands = parser.add_subparsers(dest="command", required=True)

    init_parser = commands.add_parser("init", help="Create a new convergence state file.")
    init_parser.add_argument("--root", required=True)
    init_parser.add_argument("--manifest", required=True)
    init_parser.add_argument("--state", required=True)
    init_parser.add_argument("--target")
    init_parser.add_argument("--clean-streak", type=positive_int, default=2)
    init_parser.add_argument("--accepted-minor-streak", type=positive_int, default=3)
    init_parser.add_argument("--max-cycles", type=positive_int, default=8)
    init_parser.add_argument("--max-no-progress", type=positive_int, default=2)
    init_parser.add_argument("--max-fix-attempts", type=positive_int, default=3)
    init_parser.add_argument("--force", action="store_true")

    record_parser = commands.add_parser("record", help="Record one completed QA pass.")
    record_parser.add_argument("--state", required=True)
    record_parser.add_argument("--report", required=True)

    status_parser = commands.add_parser("status", help="Print the current state summary.")
    status_parser.add_argument("--state", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "init":
            state = initialize(args)
        elif args.command == "record":
            state = record(args)
        else:
            state = read_json(Path(args.state).resolve())
        print(json.dumps(summary(state), indent=2, sort_keys=True))
        return 0
    except (ValidationError, OSError, KeyError, TypeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
